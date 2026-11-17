---
name: fpsot-decisions
description: Decision rules for FPSOT software. Use when writing or reviewing code that makes or assists an individual administrative decision, implements or overrides a rule provider, resolves rule versions by effective date, stores decision records or review steps, gives reason codes or renders decision notices, gates results on human review, emits decision events, or tests rule providers.
---

# FPSOT decisions

Summary of the FPSOT decisions specification. It adds no rules of its own.
The spec text in `spec/` wins on any difference. Each line cites its requirement ID.
It standardizes the decision, not the engine: no rule requires a rules engine, a framework or a product.
The record form is `model/decisions.yaml`; the profiles are in `profiles/`; `examples/check-examples.py` checks the examples.

Each line keeps the strength of its rule: "must" and "must not" are MUST and MUST NOT, "should" and "should not" are SHOULD and SHOULD NOT, "may" is MAY.

Other specs own business events and event ids (OBS), actors and representation (IAM), concept schemes (VOC), problem details and CloudEvents (API), seals and the transparency log (LOG). Cite them; never redefine them.

## Scope and roles

- Applies to every decision type that software makes or assists about one party, whatever the technique (DEC-001).
- State your roles: rule provider, decision service, deploying body (DEC-002).
- Provider discovery, defaults and override precedence belong to the future capability spec; every provider implements the contract, passes the suite, gives the same result for the same input, context and rule version, and is fixed at build time, with no rule loaded at run time (DEC-003).
- A conformance claim never says that decisions meet a law (DEC-004). Follow the pinned versions (DEC-005); suites check output only, under TST-044 (DEC-006).

## Profiles

- Describe each decision type as a `DecisionType`: profiles with releases, impact level, legal authority, reason scheme, rule set, review settings; new release for each change (DEC-010).
- Always declare `core`, plus each of `ca-federal`, `ca-qc`, `fr`, `eu-ai-high-risk` whose law applies; apply every control of each; the stricter setting wins (DEC-011).
- Profiles have their own SemVer; never remove a result kind or relax a core MUST; removing or relaxing a control takes a new major; records name each profile release (DEC-012).
- One impact level, `level-1` to `level-4`; under `ca-federal` it is the published Algorithmic Impact Assessment level; the level, never the provider, decides the controls (DEC-013).
- Name each impact assessment the profiles ask for; no production while one is missing; review it when scope or rules change (DEC-014).

## Contract

- Each provider implements the contract; the language-neutral form is the model: `InputFact`, `EvaluationContext` and `DecisionResult`; the service builds a `DecisionRecord` from each `DecisionResult`; Java providers also implement the Java binding (DEC-020).
- Java binding: plain module, no framework annotation, no framework or engine dependency; record input; sealed result of records; no engine interface exposed (DEC-021).
- Context holds the effective date, the record time, the decision type and the profiles with releases; an optional language never changes the result (DEC-022).
- Compute only from input, context, rule version and parameters; no clock, random source, file, database or network; same input gives the same result and reasons (DEC-023).
- Exactly one of `decided`, `referred`, `insufficient-information`, `not-applicable`; a failure to compute is an error, never a result (DEC-024).
- A missing fact never leads to an adverse outcome: return `insufficient-information` or `referred`; no default value without a named presumption (DEC-025).
- Discretion and hardship return `referred` with a reason; never an adverse `decided` where the law leaves the case to a person (DEC-026).
- Results in proportion to the facts (should); set `cliffEdge` when one small change can remove the whole benefit (DEC-027).
- No risk or fraud score in entitlement rules unless declared with its provision; scores come from their own decision type (DEC-028).

## Rule versions

- Each version carries `RuleVersion` metadata: rule set, SemVer, validity interval, enactment time, legal sources, interpretation status, presumptions, `cliffEdge` (DEC-030).
- Legal sources are stable URIs down to the article; one per official language (should) (DEC-031).
- Status `draft`, `policy-reviewed` or `approved`; only `approved` runs in production (DEC-032).
- Presumptions and inferred facts are named, cited rules; records list each one applied (DEC-033).
- The artifact holds every version an open decision may need; removing one is a major version; state the review window per decision type (DEC-034).
- Resolver: at most one version, from those enacted at or before the record time, whose validity holds the effective date; no overlaps; none found gives `not-applicable`, the only record that may omit `ruleSet` (DEC-035).
- Retroactive change: a new version, new revised decisions with cause `retroactive-law`, never an overwrite; payments are their own events (DEC-036).
- Amounts and thresholds in `ParameterSet` files (should), each value with validity, enactment time and source, packaged at build, never read from a mutable store (DEC-037).
- FPSOT publishes its reference rules; adopters should publish theirs or name the legal ground (DEC-038).

## Records

- One `DecisionRecord` for each result of any kind, with fields taken from their owning specs (DEC-040).
- Record `id` = the business event's `org.fpsot.event.id` = the CloudEvents `id` = the seal manifest `id` (DEC-041).
- Keep input values or immutable references that live as long as the record, never a hash alone, with source, as-of date and collection method (DEC-042).
- Never change a record; corrections, reviews and reprocessing create a new full record with `predecessorId` and `changeCause`; a `decided` revision of a `referred` record names a review step; a revision of an `insufficient-information` record rests on new inputs or a review step, never on elapsed time alone (DEC-043).
- Three stores apart: full inputs in the access-controlled record; ids and codes only in business events; statistics with keyed pseudonyms under OBS-093 (DEC-044).
- Seal each record under the signed records spec in a series of at least `seal-log` (LOG-002); destroy the salt with the record (DEC-045).
- Retention rules name the schedule rule, legal hold and destruction events as OBS-102 to OBS-104 set; keep rule versions, parameters and scheme releases while a record uses them (DEC-046).
- Replay "as decided" gives the same result and reasons; "as corrected" gives a new revising record (DEC-047).
- A trace is optional, referenced by URI and digest, never inline, and kept as long as the record (DEC-048).

## Reasons and notices

- Reason codes are concepts of a scheme under the vocabularies spec; records name the scheme release; codes name factors (DEC-050).
- No verdict-only or generic codes such as `not-eligible` or `score-too-low` (DEC-051).
- Reasons ordered by rank, each with a principal flag and the cited provision; values and thresholds (should) (DEC-052).
- At most four principal reasons (should); every reason when a profile sets `allReasons` (DEC-053).
- `other` only from a person in a review step, with `otherText` in English and French (DEC-054).
- Exact counterfactual value and relation for each principal reason (should) (DEC-055).
- No prose in records; render notices at notice time from the record and a versioned template, in the person's language; keep a `Notice` record; seal the rendered notice (DEC-056).
- Meet each profile's `automationNotice` and `recourseNotice`; the notice record states both (DEC-057).
- Publish a plain-language explanation of each decision type in both languages (should) (DEC-058).

## Human review

- Derive `automationDegree` from the review steps: `fully-automated`, `human-confirmed`, `human-decided`; never from a setting (DEC-060).
- Where a profile level or the decision type asks for review: no final `decided` without a review step; until then `referred` with `human-review-required` and `recommendedOutcome`; the final record revises the referred one (DEC-061).
- Each `ReviewStep` is its own record: actor (IAM-091), represented party (IAM-064), authority, items shown, action, agreement, justification with language, times; the service never pre-fills the justification or offers a template for it; an override reason for a change or disagreement (DEC-062).
- Reviewers can set aside, change or reverse results; an authorized role can stop automation of a decision type; observations, reconsiderations and appeals lead to review steps (DEC-063).
- Dual review: two steps by different actors before a final `decided` (DEC-064).
- Engagement evidence (should), only once the privacy impact assessment covers it; never to rate one employee without that assessment and labor agreements (DEC-065).
- Count agreement, change and reversal rates and recourse outcomes per decision type and rule version from the attributes of the DEC-071 events, without identities (DEC-066).

## Interfaces and events

- Every result is a `2xx` response; problem details under API-030 only when no result can be produced (DEC-070).
- A business event under OBS-070 for each record, review step and notice, with lifecycle `complete`, an activity key and object references; the required `org.fpsot.decision.*` attributes, including `change_cause`, `review_step.action` and `review_step.agreement`, whenever the record has a value; no input value, amount or name (DEC-071).
- CloudEvents to other services: `org.fpsot.decisions.decision.recorded`, `org.fpsot.decisions.review-step.recorded`, `org.fpsot.decisions.notice.issued`; data per `registry/events/`; ids and codes only (DEC-072).
- Authorize every read of a record (IAM-050) and audit it (OBS-042); the person or a representative can obtain their own record (DEC-073).

## Testing

- Gherkin scenarios per rule version in English and French: effective date, inputs, result kind and outcome, reason codes, cited provision; a decision table may drive one Scenario Outline per table rule, each row one case of that rule (DEC-080).
- A frozen corpus per rule version once in production; a changed expected result needs a new version (DEC-081).
- Property tests (should): reasons present, at most one version per date, no adverse outcome on missing facts, determinism, intended monotonicity (DEC-082).
- FPSOT publishes a data-driven decision conformance suite with a Java runner; every provider passes it; results are never a certification (DEC-083).
- A replacing provider meets TST-045: passes the replaced provider's scenarios and corpus except listed, retested changes (DEC-084).
- Run baseline and override on the same corpus and publish the differences (should) (DEC-085).
- A DMN provider (may) states its DMN version, which must be 1.6 or a later version under DEC-005, and the compatibility kit commit and score; models fixed at build (DEC-086).
