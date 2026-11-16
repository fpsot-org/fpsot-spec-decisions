# Instructions for agents

This repository holds the FPSOT decisions specification: decision types with jurisdiction profiles and impact levels, a decision contract with four result kinds, rule versions with effective dates and record times, dated parameters, the decision record and its revisions, reason codes and notices, human review steps and their gating, responses and events, and a conformance suite for rule providers. It standardizes the decision, not the engine.

- The normative text is in `spec/en/` and `spec/fr/`. Every rule has an ID such as `DEC-001`.
- Follow `skill/SKILL.md` when you write or review code that decides about a person, implements or overrides a rule provider, stores decision records, renders decision notices or records human review. The spec text wins on any difference.
- Every page exists in English and in French, with the same file name and the same IDs.
- Terms and abbreviations come from the term base of `fpsot-spec-writing`. Add a missing term there first; `TERMS-NEEDED.md` lists the ones this spec waits for.
- This is a layer 1 specification. It may refer to the layer 0 specifications, to data types, vocabularies, data models, api-restful, testing, security, observability, identity and log. It never refers to the registry, code or capability specifications, except by topic.
- Other specifications own business events and event identifiers (observability), actors and representation (identity), concept schemes (vocabularies), problem details and CloudEvents (api-restful), seals and the transparency log (log). Cite their rules; never redefine them.
- No rule may require a rules engine, a framework or a product. Engines and languages appear only on the informative page `maturity.adoc`. Provider discovery, defaults and override precedence belong to the future capability specification.
- `model/decisions.yaml` is the source of the record form. When you change it, update the examples and run `bash examples/test-examples.sh`.
- Examples hold synthetic data only: a fictional program, domains reserved for documentation, and no value of a fact in an event.
- Do not copy text from the Treasury Board, Québec or French law, the European Union, the OMG, the CFPB, OpenFisca or Catala. Summarize in your own words and cite the exact version.
- Do not state a legal point as a rule. Points that need a lawyer go in an informative note or in `questions-for-counsel.adoc`, and a text that nobody read at the source is marked "to be verified".
- Commits follow Conventional Commits and are signed. Pull requests are squash-merged.
