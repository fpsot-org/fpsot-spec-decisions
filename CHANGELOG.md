# Changelog

All notable changes to this specification are listed here.
The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-11-15

### Added

- Scope, roles, the capability boundary, legal status and conformance DEC-001 to DEC-006: any technique is in scope; rule provider, decision service and deploying body; provider discovery, defaults and override precedence left to the future capability specification, with four outcomes that every provider meets; no claim of legal compliance; pinned versions; suites that check output only.
- Jurisdiction profiles DEC-010 to DEC-014: the description of a decision type; the `core`, `ca-federal`, `ca-qc`, `fr` and `eu-ai-high-risk` profiles as data files in `profiles/`, each released apart from the core; impact levels; no production without the impact assessments that a profile names.
- Decision contract DEC-020 to DEC-028: a language-neutral form and a plain Java binding with a sealed result; the effective date and the record time in the context; deterministic providers; the four result kinds `decided`, `referred`, `insufficient-information` and `not-applicable`; no adverse outcome from a missing fact; reachable discretion and hardship; cliff-edge flags; no undeclared risk scores.
- Rule versions DEC-030 to DEC-038: metadata with legal sources and interpretation status, named presumptions, every needed version in the artifact, a bitemporal resolver, retroactive changes as new linked decisions, dated parameter files, and publication of rules.
- Decision records DEC-040 to DEC-048: one record for each result in the form of `model/decisions.yaml`, aligned with PROV-O, with each field taken from the specification that owns it; one identifier across record, event and seal; input values kept; append-only revisions; three separate stores; sealing under the signed records specification; retention; replay as decided and as corrected; traces by reference.
- Reasons and notices DEC-050 to DEC-058: factor-named reason codes from a concept scheme, no generic reasons, ordered reasons with values and cited provisions, at most four principal reasons, `other` only from a person in both languages, exact counterfactual values, notices rendered at notice time and sealed, notice controls of the profiles, and a published general explanation.
- Human review DEC-060 to DEC-066: the degree of automation derived from review steps, gating by impact level, review steps as their own records with identity actors, override and stop functions, dual review, engagement evidence behind a privacy impact assessment, and override statistics without identities.
- Interfaces and events DEC-070 to DEC-073: results as successful responses, business events without personal values, three CloudEvents types with their schemas in `registry/events/`, and authorized, audited access to records.
- Testing and conformance DEC-080 to DEC-086: scenarios with dates and cited provisions, frozen corpora, property invariants, a data-driven decision conformance suite, replacement under TST-045, baseline and override comparison, and the declaration of a DMN provider.
- Informative pages on a five-level rules as code maturity scale, defined by FPSOT, with notes on engines to watch, and on questions for counsel.
- The LinkML model `model/decisions.yaml`, with a copy of the data types model.
- Examples for a fictional housing benefit: a decision type, a reason scheme, two rule versions, a parameter set, a referred record, a review step, the final record that revises it, a notice, an event and a feature in English and French, with a check script and its test, run by the `examples` job of the continuous integration.
- Comparison data with international and European Union rows, and rows for Canada, Québec and France.
- How-to guide that puts a decision type under the specification.

[Unreleased]: https://github.com/fpsot-org/fpsot-spec-decisions/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fpsot-org/fpsot-spec-decisions/releases/tag/v0.1.0
