# SPDX-License-Identifier: Apache-2.0
"""Checks the example files of the FPSOT decisions specification.

Usage: python3 -I examples/check-examples.py [ROOT]

ROOT is the repository root, by default the parent of this folder. The check reads
model/decisions.yaml and its imports, profiles/, registry/events/ and examples/.
It needs the Python standard library and PyYAML only (examples/requirements.txt).

It runs two kinds of checks, and reports every failure with the rule it breaks.

- Schema checks: each file against its class of the LinkML model, through a small
  reader of the parts of LinkML that the model uses (required slots, ranges, types,
  patterns, enumerations, lists and closed classes). It is not a LinkML validator.
- Structural checks of the rules: revision links resolve, the resolver finds one rule
  version, thresholds come from the dated parameters, reason codes exist in the
  scheme, at most four principal reasons, a gated result has its review steps, the
  degree of automation matches them, no prose in records, no value of a fact in an
  event, notices meet the profiles, and the English and French features match.
"""
import glob
import json
import os
import re
import sys

import yaml

BUILTIN = {"string", "integer", "boolean", "uri", "date", "datetime", "double", "float"}
URI = re.compile(r"^https?://\S+$")
GENERIC = {"not-eligible", "ineligible", "does-not-meet-criteria", "criteria-not-met", "policy",
           "internal-policy", "internal-standard", "score-too-low", "insufficient-score",
           "failed-qualifying-score", "refused", "denied", "rejected"}
# Slots that may hold text that a person writes (DEC-054, DEC-062), and the values of facts.
TEXT_PATHS = (re.compile(r"\.justification$"), re.compile(r"\.otherText\.[a-z-]+$"),
              re.compile(r"^\$\.inputs\[\d+\]\.value(\.|\[|$)"))

failures = []


def fail(where, message, rule):
    failures.append(f"FAIL: {where}: {message} ({rule})")


def load(path):
    with open(path, encoding="utf-8") as f:
        if path.endswith((".yaml", ".yml")):
            return yaml.safe_load(f)
        return json.load(f)


class Model:
    """The parts of a LinkML schema that the check reads."""

    def __init__(self, path):
        self.types, self.classes, self.enums = {}, {}, {}
        self._read(path)

    def _read(self, path):
        schema = load(path)
        for imp in schema.get("imports") or []:
            if not imp.startswith("linkml:"):
                self._read(os.path.join(os.path.dirname(path), imp + ".yaml"))
        self.types.update(schema.get("types") or {})
        self.classes.update(schema.get("classes") or {})
        self.enums.update(schema.get("enums") or {})

    def base(self, rng):
        """The built-in type and the patterns of a type, through its typeof chain."""
        patterns = []
        while rng not in BUILTIN:
            t = self.types[rng]
            if t.get("pattern"):
                patterns.append(t["pattern"])
            rng = t["typeof"]
        return rng, patterns

    def identifier(self, cls):
        for name, slot in (self.classes[cls].get("attributes") or {}).items():
            if (slot or {}).get("identifier"):
                return name, slot
        return None, None

    def check(self, obj, cls, where, path="$"):
        spec = self.classes[cls]
        if spec.get("class_uri") == "linkml:Any":
            return
        if not isinstance(obj, dict):
            fail(where, f"{path} must be an object of class {cls}", "DEC-040")
            return
        attrs = spec.get("attributes") or {}
        for key in obj:
            if key not in attrs and not spec.get("extra_slots"):
                fail(where, f"{path}.{key} is not a slot of {cls}", "DEC-040")
        for name, slot in attrs.items():
            slot = slot or {}
            if name not in obj:
                if slot.get("required") or slot.get("identifier"):
                    fail(where, f"{path}.{name} is required in {cls}", "DEC-040")
                continue
            value = obj[name]
            if slot.get("multivalued"):
                if not isinstance(value, list) or not value:
                    fail(where, f"{path}.{name} must be a list with at least one item", "DEC-040")
                    continue
                for i, item in enumerate(value):
                    self.value(item, slot, where, f"{path}.{name}[{i}]")
            else:
                self.value(value, slot, where, f"{path}.{name}")

    def value(self, v, slot, where, path):
        rng = slot.get("range", "string")
        if rng in self.enums:
            if v not in (self.enums[rng].get("permissible_values") or {}):
                fail(where, f"{path} has {v!r}, which is not a value of {rng}", "DEC-040")
            return
        if rng in self.classes:
            ident, ident_slot = self.identifier(rng)
            if slot.get("inlined") or slot.get("inlined_as_list") or ident is None:
                self.check(v, rng, where, path)
            else:
                self.value(v, ident_slot, where, path)
            return
        base, patterns = self.base(rng)
        if slot.get("pattern"):
            patterns.append(slot["pattern"])
        ok = {"integer": isinstance(v, int) and not isinstance(v, bool),
              "boolean": isinstance(v, bool),
              "double": isinstance(v, (int, float)) and not isinstance(v, bool),
              "float": isinstance(v, (int, float)) and not isinstance(v, bool),
              "uri": isinstance(v, str) and bool(URI.match(v))}.get(base, isinstance(v, str))
        if not ok:
            fail(where, f"{path} has {v!r}, which is not a {rng}", "DEC-040")
            return
        for p in patterns:
            if isinstance(v, str) and not re.search(p, v):
                fail(where, f"{path} has {v!r}, which does not match the pattern of {rng}", "DEC-040")
        if "minimum_value" in slot and v < slot["minimum_value"]:
            fail(where, f"{path} is below {slot['minimum_value']}", "DEC-040")


def leaves(v, path="$"):
    """Yields (path, scalar) for every scalar inside a JSON value."""
    if isinstance(v, dict):
        for k, x in v.items():
            yield from leaves(x, f"{path}.{k}")
    elif isinstance(v, list):
        for i, x in enumerate(v):
            yield from leaves(x, f"{path}[{i}]")
    else:
        yield path, v


def json_schema(v, s, where, path="$"):
    """The parts of JSON Schema 2020-12 that the event schemas use."""
    t = s.get("type")
    kinds = {"object": dict, "array": list, "string": str, "boolean": bool}
    if t in kinds and (not isinstance(v, kinds[t]) or (t != "boolean" and isinstance(v, bool))):
        fail(where, f"{path} must be of type {t}", "API-103")
        return
    if "enum" in s and v not in s["enum"]:
        fail(where, f"{path} has {v!r}, which is not in the schema enumeration", "API-103")
    if isinstance(v, str):
        if "pattern" in s and not re.search(s["pattern"], v):
            fail(where, f"{path} has {v!r}, which does not match its schema pattern", "API-103")
        if len(v) < s.get("minLength", 0) or len(v) > s.get("maxLength", 1 << 30):
            fail(where, f"{path} has the wrong length", "API-103")
    if isinstance(v, list):
        if len(v) < s.get("minItems", 0):
            fail(where, f"{path} has too few items", "API-103")
        for i, x in enumerate(v):
            json_schema(x, s.get("items", {}), where, f"{path}[{i}]")
    if isinstance(v, dict):
        for k in s.get("required", []):
            if k not in v:
                fail(where, f"{path}.{k} is required by the event schema", "API-103")
        props = s.get("properties", {})
        for k, x in v.items():
            if k in props:
                json_schema(x, props[k], where, f"{path}.{k}")
            elif s.get("additionalProperties") is False:
                fail(where, f"{path}.{k} is not allowed by the event schema", "API-103")


def covers(validity, day):
    return validity["start"] <= day and ("end" not in validity or day < validity["end"])


def overlap(a, b):
    a_end, b_end = a.get("end", "9999-12-31"), b.get("end", "9999-12-31")
    return a["start"] < b_end and b["start"] < a_end


def scheme_codes(path):
    graph = load(path)["@graph"]
    scheme = next(n for n in graph if n.get("@type") == "skos:ConceptScheme")
    codes = {}
    for n in graph:
        if n.get("@type") != "skos:Concept":
            continue
        code = n.get("skos:notation")
        if n["@id"] != scheme["@id"] + "/concepts/" + str(code):
            fail(path, f"concept {n['@id']} is not the scheme URI, /concepts/ and its code", "VOC-003")
        langs = {x["@language"] for x in n.get("skos:prefLabel", [])}
        defs = {x["@language"] for x in n.get("skos:definition", [])}
        if not {"en", "fr"} <= langs or not {"en", "fr"} <= defs:
            fail(path, f"concept {code} needs a label and a definition in English and in French", "VOC-010, VOC-015")
        if code in GENERIC:
            fail(path, f"concept {code} is a generic reason, not a factor", "DEC-051")
        codes[code] = n
    versioned = scheme["@id"] + "/versions/" + scheme.get("owl:versionInfo", "")
    return versioned, codes


def gherkin(path):
    """Tags, scenarios and steps of a feature file, enough to compare two languages."""
    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]
    scenarios, tags, current = [], [], None
    for line in lines[1:]:
        s = line.strip()
        if s.startswith("@"):
            tags = s.split()
        elif re.match(r"^(Scenario|Scénario|Scenario Outline|Plan du scénario):", s):
            current = {"tags": tags, "steps": []}
            scenarios.append(current)
            tags = []
        elif current is not None and re.match(r"^(Given|When|Then|And|But|Étant donné|Quand|Alors|Et|Mais)\b", s):
            current["steps"].append(s)
    return lines[0], scenarios


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
    ex = os.path.join(root, "examples")
    model = Model(os.path.join(root, "model", "decisions.yaml"))

    def rel(p):
        return os.path.relpath(p, root)

    # Profiles (DEC-011, DEC-012).
    profiles = {}
    for p in sorted(glob.glob(os.path.join(root, "profiles", "*.yaml"))):
        doc = load(p)
        model.check(doc, "Profile", rel(p))
        if os.path.basename(p) != doc.get("code", "") + ".yaml":
            fail(rel(p), "the file name must be the code of the profile", "DEC-011")
        profiles[(doc.get("code"), doc.get("version"))] = doc
    if not any(code == "core" for code, _ in profiles):
        fail("profiles", "the core profile is missing", "DEC-011")

    def levels_of(refs, level, where):
        found = []
        for ref in refs:
            prof = profiles.get((ref.get("code"), ref.get("version")))
            if prof is None:
                fail(where, f"profile {ref.get('code')} {ref.get('version')} is not in profiles/", "DEC-012")
                continue
            lv = [x for x in prof["levels"] if x["level"] == level]
            if not lv:
                fail(where, f"profile {ref['code']} has no impact level {level}", "DEC-013")
            found += lv
        if not any(r.get("code") == "core" for r in refs):
            fail(where, "the profiles must include core", "DEC-011")
        return found

    # Decision type (DEC-010 to DEC-014).
    dt_path = os.path.join(ex, "decision-type.yaml")
    dtype = load(dt_path)
    model.check(dtype, "DecisionType", rel(dt_path))
    dt_levels = levels_of(dtype["profiles"], dtype["impactLevel"], rel(dt_path))
    kinds = {a["kind"] for a in dtype.get("impactAssessments") or []}
    for ref in dtype["profiles"]:
        for k in profiles.get((ref["code"], ref["version"]), {}).get("impactAssessmentKinds") or []:
            if k not in kinds:
                fail(rel(dt_path), f"profile {ref['code']} asks for an impact assessment of kind {k}", "DEC-014")
    if not dtype["publication"].get("sourceUri") and not dtype["publication"].get("exception"):
        fail(rel(dt_path), "publish the rule source or name the ground for an exception", "DEC-038")

    # Reason scheme (DEC-050, DEC-051).
    scheme_path = os.path.join(ex, "reason-codes.jsonld")
    scheme_uri, codes = scheme_codes(scheme_path)
    if dtype["reasonScheme"] != scheme_uri:
        fail(rel(dt_path), f"reasonScheme must be {scheme_uri}", "DEC-050")

    # Rule versions and parameters (DEC-030 to DEC-037).
    rv_path = os.path.join(ex, "rule-versions.yaml")
    versions = load(rv_path)
    for i, v in enumerate(versions):
        model.check(v, "RuleVersion", rel(rv_path), f"$[{i}]")
    for i, a in enumerate(versions):
        for b in versions[i + 1:]:
            if a["ruleSetCode"] == b["ruleSetCode"] and overlap(a["validity"], b["validity"]):
                fail(rel(rv_path), f"versions {a['version']} and {b['version']} cover the same dates", "DEC-035")
    params = {}
    for p in sorted(glob.glob(os.path.join(ex, "parameters", "*.yaml"))):
        doc = load(p)
        model.check(doc, "ParameterSet", rel(p))
        params[(doc["code"], doc["version"])] = doc
        for par in doc["parameters"]:
            vals = par["values"]
            for i, a in enumerate(vals):
                for b in vals[i + 1:]:
                    if overlap(a["validity"], b["validity"]):
                        fail(rel(p), f"two values of {par['code']} cover the same dates", "DEC-037")

    # Records, review steps and notices (DEC-040 to DEC-066).
    records, steps, notices = {}, {}, {}
    for pattern, cls, store in (("decision-record*.json", "DecisionRecord", records),
                                ("review-step*.json", "ReviewStep", steps),
                                ("notice*.json", "Notice", notices)):
        for p in sorted(glob.glob(os.path.join(ex, pattern))):
            doc = load(p)
            model.check(doc, cls, rel(p))
            if doc.get("id") in records or doc.get("id") in steps or doc.get("id") in notices:
                fail(rel(p), f"id {doc.get('id')} is used twice", "DEC-041")
            store[doc.get("id")] = (rel(p), doc)
            for path, v in leaves(doc):
                if isinstance(v, str) and re.search(r"\s", v) and not any(t.search(path) for t in TEXT_PATHS):
                    fail(rel(p), f"{path} holds prose; records hold codes and values only", "DEC-056")

    for rid, (where, r) in records.items():
        kind = r.get("resultKind")
        if kind == "decided" and (not r.get("outcome") or r.get("referralReason")):
            fail(where, "a decided result has an outcome and no referral reason", "DEC-024")
        if kind != "decided" and r.get("outcome"):
            fail(where, "only a decided result has an outcome", "DEC-024")
        if kind == "referred" and not r.get("referralReason"):
            fail(where, "a referred result needs a referral reason", "DEC-026")
        if kind == "insufficient-information" and not r.get("missingFacts"):
            fail(where, "an insufficient-information result lists the missing facts", "DEC-025")
        if r.get("decisionType") != dtype["code"] or r.get("decisionTypeVersion") != dtype["version"]:
            fail(where, "the decision type and its version must match decision-type.yaml", "DEC-010")
        if r.get("profiles") != dtype["profiles"] or r.get("impactLevel") != dtype["impactLevel"]:
            fail(where, "the profiles and the impact level must match the decision type", "DEC-011, DEC-013")
        levels = levels_of(r.get("profiles", []), r.get("impactLevel"), where)
        for inp in r.get("inputs", []):
            if ("value" in inp) == ("reference" in inp):
                fail(where, f"input {inp.get('name')} needs a value or a reference, not both", "DEC-042")
        # Resolver (DEC-035) and interpretation status (DEC-032).
        rs = r.get("ruleSet", {})
        known = [v for v in versions if v["ruleSetCode"] == rs.get("code") and v["enactedAt"] <= r["recordTime"]
                 and covers(v["validity"], r["effectiveDate"])]
        if len(known) != 1 or known[0]["version"] != rs.get("version"):
            fail(where, "the resolver must find exactly the rule version that the record names", "DEC-035")
        elif known[0]["interpretationStatus"] != "approved":
            fail(where, "a rule version in production needs the status approved", "DEC-032")
        # Thresholds come from the dated parameters (DEC-037).
        values = []
        for ref in r.get("parameterSets") or []:
            doc = params.get((ref["code"], ref["version"]))
            if doc is None:
                fail(where, f"parameter set {ref['code']} {ref['version']} is not in examples/parameters/", "DEC-037")
                continue
            for par in doc["parameters"]:
                values += [v["value"] for v in par["values"]
                           if covers(v["validity"], r["effectiveDate"]) and v["enactedAt"] <= r["recordTime"]]
        # Reasons (DEC-050 to DEC-055).
        if r.get("reasonScheme") != scheme_uri:
            fail(where, f"reasonScheme must be {scheme_uri}", "DEC-050")
        reasons = r.get("reasons") or []
        if sorted(x.get("rank") for x in reasons) != list(range(1, len(reasons) + 1)) or \
                [x.get("rank") for x in reasons] != sorted(x.get("rank") for x in reasons):
            fail(where, "reasons come in order of rank, from 1 with no gap", "DEC-052")
        principal = [x for x in reasons if x.get("principal")]
        if not principal and kind in ("decided", "referred"):
            fail(where, "a result needs at least one principal reason", "DEC-052")
        if len(principal) > 4 and not any(l.get("allReasons") for l in levels):
            fail(where, f"{len(principal)} principal reasons; give at most four", "DEC-053")
        for x in reasons:
            code = x.get("code")
            if code not in codes:
                fail(where, f"reason code {code} is not in the reason scheme", "DEC-050")
            if code in GENERIC:
                fail(where, f"reason code {code} is a generic reason", "DEC-051")
            if (code == "other") != ("otherText" in x):
                fail(where, "the code other, and only it, carries otherText in English and French", "DEC-054")
            if code == "other" and not r.get("reviewStepIds"):
                fail(where, "only a person may give the reason other", "DEC-054")
            if "thresholdValue" in x and x["thresholdValue"] not in values:
                fail(where, f"the threshold of {code} is not a parameter value for the effective date", "DEC-037")
            if ("counterfactualValue" in x) != ("counterfactualRelation" in x):
                fail(where, f"a counterfactual of {code} needs a relation and a value", "DEC-055")
        # Revisions (DEC-043).
        pred = r.get("predecessorId")
        if (pred is None) != (r.get("changeCause") is None):
            fail(where, "a revision has both predecessorId and changeCause", "DEC-043")
        chain, seen = [rid], {rid}
        while pred is not None:
            if pred in seen or pred not in records:
                fail(where, f"predecessor {pred} does not resolve to an earlier record", "DEC-043")
                break
            if records[pred][1]["createdAt"] >= records[chain[-1]][1]["createdAt"]:
                fail(where, f"predecessor {pred} is not older than the record that revises it", "DEC-043")
            chain.append(pred)
            seen.add(pred)
            pred = records[pred][1].get("predecessorId")
        # Review steps and degree of automation (DEC-060 to DEC-064).
        own = []
        for sid in r.get("reviewStepIds") or []:
            if sid not in steps:
                fail(where, f"review step {sid} does not resolve", "DEC-061")
                continue
            s = steps[sid][1]
            own.append(s)
            if s.get("decisionId") not in chain[1:]:
                fail(where, f"review step {sid} must be about a record that this one revises", "DEC-061")
            if s.get("completedAt", "") > r["createdAt"]:
                fail(where, f"review step {sid} ends after the record", "DEC-061")
        changed = any(s.get("action") != "confirmed" or not s.get("agreement") for s in own)
        degree = "fully-automated" if not own else ("human-decided" if changed else "human-confirmed")
        if r.get("automationDegree") != degree:
            fail(where, f"the degree of automation must be {degree}, from the review steps", "DEC-060")
        gated = dtype["humanReview"] or any(l.get("humanReview") for l in levels)
        if kind == "decided" and gated and not own:
            fail(where, f"impact level {r.get('impactLevel')} needs a review step before a decided result", "DEC-061")
        dual = dtype["dualReview"] or any(l.get("dualReview") for l in levels)
        if kind == "decided" and dual and len({s.get("actorId") for s in own}) < 2:
            fail(where, "dual review needs two review steps by distinct people", "DEC-064")

    for sid, (where, s) in steps.items():
        if s.get("decisionId") not in records:
            fail(where, f"decisionId {s.get('decisionId')} does not resolve", "DEC-062")
        if (s.get("action") == "changed" or s.get("agreement") is False) and not s.get("overrideReason"):
            fail(where, "a change or a disagreement needs an override reason", "DEC-062")
        if s.get("overrideReason") and s["overrideReason"] not in codes:
            fail(where, f"override reason {s['overrideReason']} is not in the reason scheme", "DEC-063")
        if s.get("startedAt", "") > s.get("completedAt", ""):
            fail(where, "a review step cannot end before it starts", "DEC-062")

    for nid, (where, n) in notices.items():
        if n.get("decisionId") not in records:
            fail(where, f"decisionId {n.get('decisionId')} does not resolve", "DEC-056")
            continue
        r = records[n["decisionId"]][1]
        for l in levels_of(r["profiles"], r["impactLevel"], where):
            need = l["automationNotice"] == "required" or (
                l["automationNotice"] == "required-when-fully-automated" and r["automationDegree"] == "fully-automated")
            if need and not n.get("automationNotice"):
                fail(where, "the profile asks the notice to state that automation took part", "DEC-057")
            if l["recourseNotice"] == "required" and not n.get("recourseChannels"):
                fail(where, "the profile asks the notice to give a recourse channel", "DEC-057")

    # Event schemas (API-103) and events (DEC-041, DEC-044, DEC-072).
    schemas = {}
    for p in sorted(glob.glob(os.path.join(root, "registry", "events", "*.schema.json"))):
        s = load(p)
        t = os.path.basename(p)[:-len(".schema.json")]
        if s.get("title") != t or not s.get("$id", "").endswith("/" + os.path.basename(p)):
            fail(rel(p), "the title and the $id must name the event type of the file", "API-103")
        if not re.match(r"^org\.fpsot\.decisions\.[a-z]+(-[a-z]+)*\.[a-z]+$", t):
            fail(rel(p), f"{t} is not of the form org.fpsot.decisions.<resource>.<event>", "NAM-050")
        if not set(s.get("required", [])) <= set(s.get("properties", {})):
            fail(rel(p), "each required field needs a property", "API-103")
        schemas[t] = s
    for p in sorted(glob.glob(os.path.join(ex, "decision-event*.json"))):
        e, where = load(p), rel(p)
        for attr, want in (("specversion", "1.0"), ("datacontenttype", "application/json")):
            if e.get(attr) != want:
                fail(where, f"{attr} must be {want}", "API-101")
        for attr in ("id", "source", "type", "time"):
            if not e.get(attr):
                fail(where, f"the attribute {attr} is required", "API-101")
        if e.get("type") not in schemas:
            fail(where, f"event type {e.get('type')} has no schema in registry/events/", "API-103")
            continue
        json_schema(e.get("data"), schemas[e["type"]], where, "$.data")
        data = e.get("data") or {}
        rid = data.get("decisionId")
        if e["type"].endswith(".decision.recorded"):
            if rid not in records or e.get("id") != rid:
                fail(where, "the event id must be the id of a decision record", "DEC-041")
                continue
            r = records[rid][1]
            want = {"resultKind": r.get("resultKind"), "outcome": r.get("outcome"),
                    "reasonCodes": [x["code"] for x in r.get("reasons", [])],
                    "automationDegree": r.get("automationDegree"), "ruleSetVersion": r["ruleSet"]["version"],
                    "predecessorId": r.get("predecessorId")}
            for k, v in want.items():
                if data.get(k) != v:
                    fail(where, f"data.{k} must match the decision record", "DEC-072")
            facts = {json.dumps(v, sort_keys=True) for i in r.get("inputs", [])
                     for v in [i.get("value")] + [x for _, x in leaves(i.get("value"))] if v is not None}
            for path, v in list(leaves(data)) + [(f"$.data.{k}", v) for k, v in data.items()]:
                if json.dumps(v, sort_keys=True) in facts:
                    fail(where, f"{path} holds the value of a fact: a personal value has no place in an event", "DEC-044")

    # Features (DEC-080).
    en_files = sorted(glob.glob(os.path.join(ex, "features", "en", "*.feature")))
    if not en_files:
        fail("examples/features", "no feature file", "DEC-080")
    for en in en_files:
        fr = en.replace(os.sep + "en" + os.sep, os.sep + "fr" + os.sep)
        if not os.path.exists(fr):
            fail(rel(en), "the French feature file is missing", "TST-030")
            continue
        (en_head, en_sc), (fr_head, fr_sc) = gherkin(en), gherkin(fr)
        if en_head != "# language: en" or fr_head != "# language: fr":
            fail(rel(en), "the first lines must be # language: en and # language: fr", "TST-031")
        if [s["tags"] for s in en_sc] != [s["tags"] for s in fr_sc] or \
                [len(s["steps"]) for s in en_sc] != [len(s["steps"]) for s in fr_sc]:
            fail(rel(en), "the English and French scenarios must have the same tags and steps", "TST-032")
        for lang, sc_list, path in (("en", en_sc, en), ("fr", fr_sc, fr)):
            for s in sc_list:
                text = "\n".join(s["steps"])
                tag = s["tags"][0] if s["tags"] else "(no tag)"
                if not s["tags"]:
                    fail(rel(path), "each scenario needs a tag", "TST-027")
                if not re.search(r'"\d{4}-\d{2}-\d{2}"', text):
                    fail(rel(path), f"scenario {tag} states no effective date", "DEC-080")
                if not re.search(r'(result kind is|type de résultat est) "[a-z-]+"', text):
                    fail(rel(path), f"scenario {tag} states no result", "DEC-080")
                if not re.search(r'(cites section|cite l’article) "', text):
                    fail(rel(path), f"scenario {tag} cites no provision", "DEC-080")
                for code in re.findall(r'(?:principal reason is|motif principal est) "([a-z0-9-]+)"', text):
                    if code not in codes:
                        fail(rel(path), f"scenario {tag} names reason code {code}, which is not in the scheme", "DEC-050")

    for f in failures:
        print(f)
    if failures:
        sys.exit(1)
    print(f"PASS: decision records {len(records)}, review steps {len(steps)}, notices {len(notices)}, "
          f"profiles {len(profiles)}, feature pairs {len(en_files)}")


if __name__ == "__main__":
    main()
