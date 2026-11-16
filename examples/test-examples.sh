#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Tests examples/check-examples.py: the repository passes, and each broken copy fails
# for the reason that its case names. Each case copies the files that the check reads,
# breaks one rule, and expects the check to report that rule.
set -uo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
check="$here/examples/check-examples.py"
fail=0
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

if ! python3 -I "$check" "$here"; then
  echo "FAIL: the repository itself does not pass"; fail=1
fi

# case_fails NAME EXPECTED-REGEX PYTHON: the script runs in a copy of the repository.
case_fails() {
  local name=$1 want=$2 script=$3 dir="$tmp/$1" out
  mkdir -p "$dir"
  cp -r "$here/model" "$here/profiles" "$here/registry" "$here/examples" "$dir/"
  (cd "$dir" && python3 -I -c "import json, yaml
def rj(p): return json.load(open(p, encoding='utf-8'))
def wj(p, d): json.dump(d, open(p, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
def ry(p): return yaml.safe_load(open(p, encoding='utf-8'))
def wy(p, d): yaml.safe_dump(d, open(p, 'w', encoding='utf-8'), allow_unicode=True, sort_keys=False)
R1, R2, S, N, E = 'examples/decision-record-1.json', 'examples/decision-record-2.json', 'examples/review-step.json', 'examples/notice.json', 'examples/decision-event.json'
$script") || { echo "FAIL: case $name: the setup script failed"; fail=1; return; }
  if out=$(python3 -I "$check" "$dir" 2>&1); then
    echo "FAIL: case $name passed but should fail"; fail=1
  elif ! grep -qE -- "$want" <<<"$out"; then
    echo "FAIL: case $name failed for another reason:"; echo "$out" | head -5; fail=1
  else
    echo "ok: case $name fails"
  fi
}

case_fails missing-rule-set 'ruleSet is required' \
  'd = rj(R1); del d["ruleSet"]; wj(R1, d)'
case_fails five-principal-reasons 'principal reasons; give at most four \(DEC-053\)' \
  'd = rj(R2); x = d["reasons"][0]; d["reasons"] = [dict(x, rank=i) for i in range(1, 6)]; wj(R2, d)'
case_fails unknown-reason-code 'not in the reason scheme \(DEC-050\)' \
  'd = rj(R2); d["reasons"][0]["code"] = "income-too-high"; wj(R2, d)'
case_fails generic-reason-code 'generic reason, not a factor \(DEC-051\)' \
  'd = rj("examples/reason-codes.jsonld"); c = dict(d["@graph"][1]); c["skos:notation"] = "not-eligible"; c["@id"] = d["@graph"][0]["@id"] + "/concepts/not-eligible"; d["@graph"].append(c); wj("examples/reason-codes.jsonld", d)'
case_fails other-without-text 'otherText in English and French \(DEC-054\)' \
  'd = rj(R2); d["reasons"][1]["code"] = "other"; wj(R2, d)'
case_fails unresolved-predecessor 'does not resolve to an earlier record \(DEC-043\)' \
  'd = rj(R2); d["predecessorId"] = "0199485a-0000-7000-8000-000000000000"; wj(R2, d)'
case_fails cause-without-predecessor 'both predecessorId and changeCause \(DEC-043\)' \
  'd = rj(R1); d["changeCause"] = "correction"; wj(R1, d)'
case_fails level-3-without-review 'needs a review step before a decided result \(DEC-061\)' \
  'd = rj(R2); del d["reviewStepIds"]; d["automationDegree"] = "fully-automated"; wj(R2, d)'
case_fails degree-not-from-steps 'degree of automation must be human-confirmed, from the review steps \(DEC-060\)' \
  'd = rj(R2); d["automationDegree"] = "fully-automated"; wj(R2, d)'
case_fails dual-review-one-person 'two review steps by distinct people \(DEC-064\)' \
  'd = ry("examples/decision-type.yaml"); d["dualReview"] = True; wy("examples/decision-type.yaml", d)'
case_fails override-without-reason 'needs an override reason \(DEC-062\)' \
  'd = rj(S); d["agreement"] = False; wj(S, d)'
case_fails prose-in-record 'holds prose; records hold codes and values only \(DEC-056\)' \
  'd = rj(R2); d["reasons"][0]["actualValue"] = "The income of the household is too high"; wj(R2, d)'
case_fails fact-value-in-event 'personal value has no place in an event \(DEC-044\)' \
  'd = rj(E); d["data"]["outcome"] = "53410.00"; wj(E, d)'
case_fails field-not-in-event-schema 'not allowed by the event schema \(API-103\)' \
  'd = rj(E); d["data"]["householdIncome"] = {"amount": "53410.00", "currency": "CAD"}; wj(E, d)'
case_fails event-id-not-record 'event id must be the id of a decision record \(DEC-041\)' \
  'd = rj(E); d["id"] = "01994d84-0000-7000-8000-000000000000"; wj(E, d)'
case_fails overlapping-rule-versions 'cover the same dates \(DEC-035\)' \
  'd = ry("examples/rule-versions.yaml"); d[0]["validity"]["end"] = "2026-10-01"; wy("examples/rule-versions.yaml", d)'
case_fails rule-version-not-approved 'needs the status approved \(DEC-032\)' \
  'd = ry("examples/rule-versions.yaml"); d[1]["interpretationStatus"] = "policy-reviewed"; wy("examples/rule-versions.yaml", d)'
case_fails threshold-not-a-parameter 'is not a parameter value for the effective date \(DEC-037\)' \
  'd = rj(R2); d["reasons"][0]["thresholdValue"] = {"amount": "50500.00", "currency": "CAD"}; wj(R2, d)'
case_fails notice-without-automation 'state that automation took part \(DEC-057\)' \
  'd = rj(N); d["automationNotice"] = False; wj(N, d)'
case_fails missing-impact-assessment 'asks for an impact assessment of kind \(?algorithmic-impact-assessment' \
  'd = ry("examples/decision-type.yaml"); del d["impactAssessments"]; wy("examples/decision-type.yaml", d)'
case_fails unknown-profile-version 'is not in profiles/ \(DEC-012\)' \
  'd = rj(R1); d["profiles"][1]["version"] = "9.0.0"; wj(R1, d)'
case_fails feature-parity 'same tags and steps \(TST-032\)' \
  'p = "examples/features/fr/example-housing-benefit.feature"; s = open(p, encoding="utf-8").read().replace("@example-housing-benefit-002", "@example-housing-benefit-009"); open(p, "w", encoding="utf-8").write(s)'
case_fails feature-without-date 'states no effective date \(DEC-080\)' \
  'p = "examples/features/en/example-housing-benefit.feature"; s = open(p, encoding="utf-8").read().replace("And the effective date \"2026-09-01\"", "And the effective date of the application", 1); open(p, "w", encoding="utf-8").write(s)'

[ $fail -eq 0 ] && echo "PASS: every case"
exit $fail
