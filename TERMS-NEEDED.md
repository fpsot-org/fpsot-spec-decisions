# Terms needed

Entries in the format of `termbase/terms.yaml` of fpsot-spec-writing, for a pull request to the term base.
The pages of this specification write these terms in plain text for now, and will use the term attributes once the term base has them.
The French forms marked "to confirm" have no record in the Grand dictionnaire terminologique that the writer checked.

```yaml
  - id: dmn
    kind: abbreviation
    en: {short: "DMN", full: "Decision Model and Notation", definition: "A standard of the Object Management Group for decision models, decision tables and their expression language."}
    fr: {short: "DMN", full: "Decision Model and Notation", definition: "Norme de l’Object Management Group pour les modèles de décision, les tables de décision et leur langage d’expression."}
    source: {name: "Object Management Group, DMN 1.6 (proper name, kept in English)", url: "https://www.omg.org/spec/DMN/1.6/", checked: "2026-11-15"}
  - id: tck
    kind: abbreviation
    en: {short: "TCK", full: "Technology Compatibility Kit", definition: "A shared set of tests that checks whether an implementation follows a standard."}
    fr: {short: "TCK", full: "trousse de compatibilité technologique", definition: "Ensemble commun de tests qui vérifie si une mise en œuvre respecte une norme."}
    source: {name: "DMN TCK for the English form; French form to confirm (no GDT record found)", url: "https://dmn-tck.github.io/tck/", checked: "2026-11-15"}
  - id: oecd
    kind: abbreviation
    en: {short: "OECD", full: "Organisation for Economic Co-operation and Development", definition: "An intergovernmental organization that publishes policy studies and recommendations, such as those on rules as code."}
    fr: {short: "OCDE", full: "Organisation de coopération et de développement économiques", definition: "Organisation intergouvernementale qui publie des études et des recommandations sur les politiques publiques, comme celles sur les règles sous forme de code."}
    source: {name: "OECD (proper names in both languages)", url: "https://www.oecd.org/en/publications/cracking-the-code_3afe6ba5-en.html", checked: "2026-11-15"}
  - id: decision-type
    kind: term
    en: {full: "decision type", definition: "A kind of individual decision that a public body makes under one legal authority, such as eligibility for one benefit."}
    fr: {full: "type de décision", definition: "Catégorie de décisions individuelles qu’un organisme public prend en vertu d’un même pouvoir légal, comme l’admissibilité à une prestation."}
    source: {name: "FPSOT decisions specification, DEC-010; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: decision-record
    kind: term
    en: {full: "decision record", definition: "The append-only record of one result of a decision, made of codes, values and references, never of prose."}
    fr: {full: "enregistrement de décision", definition: "Enregistrement en ajout seul d’un résultat de décision, fait de codes, de valeurs et de références, jamais de texte rédigé."}
    source: {name: "FPSOT decisions specification, DEC-040; French form to confirm (GDT gives enregistrement for a data record)", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: rule-provider
    kind: term
    en: {full: "rule provider", definition: "Software that implements the rules of one decision type behind the decision contract."}
    fr: {full: "fournisseur de règles", definition: "Logiciel qui met en œuvre les règles d’un type de décision derrière le contrat de décision."}
    source: {name: "FPSOT decisions specification, DEC-002; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: decision-service
    kind: term
    en: {full: "decision service", definition: "Software that runs a rule provider, applies the controls of the profiles and keeps the decision records."}
    fr: {full: "service de décision", definition: "Logiciel qui exécute un fournisseur de règles, applique les contrôles des profils et tient les enregistrements de décision."}
    source: {name: "FPSOT decisions specification, DEC-002; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: deploying-body
    kind: term
    en: {full: "deploying body", definition: "The public body that answers for the decisions of a decision type."}
    fr: {full: "organisme responsable", definition: "Organisme public qui répond des décisions d’un type de décision."}
    source: {name: "FPSOT decisions specification, DEC-002; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: decision-contract
    kind: term
    en: {full: "decision contract", definition: "The interface between a decision service and the rules of one decision type: an input, an evaluation context and a result of one of four kinds."}
    fr: {full: "contrat de décision", definition: "Interface entre un service de décision et les règles d’un type de décision : une entrée, un contexte d’évaluation et un résultat d’un des quatre types."}
    source: {name: "FPSOT decisions specification, DEC-020; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: jurisdiction-profile
    kind: term
    en: {full: "jurisdiction profile", definition: "A released set of controls that the law of one jurisdiction asks for, such as notices and human review, by impact level."}
    fr: {full: "profil juridictionnel", definition: "Ensemble publié de contrôles qu’exige le droit d’une collectivité publique, comme les avis et la révision humaine, selon le niveau d’incidence."}
    source: {name: "FPSOT decisions specification, DEC-011; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: impact-level
    kind: term
    en: {full: "impact level", definition: "The grade of the impact of a decision type on people, from level 1 to level 4, which decides the controls that apply."}
    fr: {full: "niveau d’incidence", definition: "Degré de l’incidence d’un type de décision sur les personnes, du niveau 1 au niveau 4, qui détermine les contrôles applicables."}
    source: {name: "Treasury Board of Canada Secretariat, Algorithmic Impact Assessment tool (French page: niveau d’incidence), to confirm", url: "https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/algorithmic-impact-assessment.html", checked: "2026-11-15"}
  - id: algorithmic-impact-assessment
    kind: term
    en: {full: "Algorithmic Impact Assessment", definition: "The questionnaire of the Government of Canada that scores an automated decision system and gives its impact level."}
    fr: {full: "Évaluation de l’incidence algorithmique", definition: "Questionnaire du gouvernement du Canada qui note un système décisionnel automatisé et en donne le niveau d’incidence."}
    source: {name: "Treasury Board of Canada Secretariat, Algorithmic Impact Assessment tool, French version to confirm", url: "https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/algorithmic-impact-assessment.html", checked: "2026-11-15"}
  - id: fundamental-rights-impact-assessment
    kind: term
    en: {full: "fundamental rights impact assessment", definition: "An assessment, before first use, of the effects of a high-risk artificial intelligence system on the fundamental rights of the people it concerns."}
    fr: {full: "analyse d’impact sur les droits fondamentaux", definition: "Analyse, avant la première utilisation, des effets d’un système d’intelligence artificielle à haut risque sur les droits fondamentaux des personnes visées."}
    source: {name: "Regulation (EU) 2024/1689, article 27, French version to confirm", url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj", checked: "2026-11-15"}
  - id: result-kind
    kind: term
    en: {full: "result kind", definition: "One of the four kinds of result of the decision contract: decided, referred, insufficient information or not applicable."}
    fr: {full: "type de résultat", definition: "Un des quatre types de résultat du contrat de décision : décidé, renvoyé, renseignements insuffisants ou sans objet."}
    source: {name: "FPSOT decisions specification, DEC-024; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: effective-date
    kind: term
    en: {full: "effective date", definition: "The date whose law applies to a case, such as the date of an application."}
    fr: {full: "date d’effet", definition: "Date dont le droit s’applique à un dossier, comme la date d’une demande."}
    source: {name: "FPSOT decisions specification, DEC-022; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: record-time
    kind: term
    en: {full: "record time", definition: "The knowledge cutoff of a decision: only facts and rule versions recorded at or before it count."}
    fr: {full: "moment d’enregistrement", definition: "Limite de connaissance d’une décision : seuls comptent les faits et les versions de règles enregistrés à ce moment ou avant."}
    source: {name: "Martin Fowler, Bitemporal History, for the English form; French form to confirm", url: "https://martinfowler.com/articles/bitemporal-history.html", checked: "2026-11-15"}
  - id: rule-version
    kind: term
    en: {full: "rule version", definition: "One released version of the rules of a decision type, with its validity, its enactment time and its legal sources."}
    fr: {full: "version de règles", definition: "Version publiée des règles d’un type de décision, avec sa période de validité, son moment d’adoption et ses sources juridiques."}
    source: {name: "FPSOT decisions specification, DEC-030; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: dated-parameter
    kind: term
    en: {full: "dated parameter", definition: "An amount, a rate or a threshold whose value changes over time, kept in a data file with the period and the legal source of each value."}
    fr: {full: "paramètre daté", definition: "Montant, taux ou seuil dont la valeur change au fil du temps, conservé dans un fichier de données avec la période et la source juridique de chaque valeur."}
    source: {name: "OpenFisca, Legislation parameters, for the concept; French form to confirm", url: "https://openfisca.org/doc/coding-the-legislation/legislation_parameters.html", checked: "2026-11-15"}
  - id: cliff-edge
    kind: term
    en: {full: "cliff edge", definition: "A rule under which a small change in one fact removes a whole benefit."}
    fr: {full: "effet de seuil", definition: "Règle selon laquelle un faible changement d’un fait supprime toute une prestation."}
    source: {name: "FPSOT decisions specification, DEC-027; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: reason-code
    kind: term
    en: {full: "reason code", definition: "The code of a concept of a reason scheme that names one factor of a decision."}
    fr: {full: "code de motif", definition: "Code d’un concept d’un schéma de motifs qui nomme un facteur d’une décision."}
    source: {name: "FPSOT decisions specification, DEC-050; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: principal-reason
    kind: term
    en: {full: "principal reason", definition: "A reason that drove the result of a decision more than the others, of which a notice gives at most four."}
    fr: {full: "motif principal", definition: "Motif qui a pesé plus que les autres sur le résultat d’une décision, et dont un avis donne au plus quatre."}
    source: {name: "Consumer Financial Protection Bureau, Regulation B, for the English form; French form to confirm", url: "https://www.consumerfinance.gov/rules-policy/regulations/1002/9/", checked: "2026-11-15"}
  - id: counterfactual-value
    kind: term
    en: {full: "counterfactual value", definition: "The exact value of a factor at which a reason would stop applying, with the other facts unchanged."}
    fr: {full: "valeur contrefactuelle", definition: "Valeur exacte d’un facteur à laquelle un motif cesserait de s’appliquer, les autres faits restant les mêmes."}
    source: {name: "Wachter, Mittelstadt and Russell, Counterfactual Explanations without Opening the Black Box; French form to confirm", url: "https://arxiv.org/abs/1711.00399v2", checked: "2026-11-15"}
  - id: degree-of-automation
    kind: term
    en: {full: "degree of automation", definition: "How much a person took part in a decision, derived from its review steps: fully automated, confirmed by a person or decided by a person."}
    fr: {full: "degré d’automatisation", definition: "Mesure de la participation d’une personne à une décision, tirée de ses étapes de révision : entièrement automatisée, confirmée par une personne ou décidée par une personne."}
    source: {name: "FPSOT decisions specification, DEC-060; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: review-step
    kind: term
    en: {full: "review step", definition: "The record of one action of one person on a decision record that a service showed them."}
    fr: {full: "étape de révision", definition: "Enregistrement d’une action d’une personne sur un enregistrement de décision qu’un service lui a présenté."}
    source: {name: "FPSOT decisions specification, DEC-062; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: dual-review
    kind: term
    en: {full: "dual review", definition: "A control under which two different people must each complete a review step before a final decision."}
    fr: {full: "double révision", definition: "Contrôle selon lequel deux personnes différentes doivent chacune réaliser une étape de révision avant une décision finale."}
    source: {name: "FPSOT decisions specification, DEC-064; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: engagement-evidence
    kind: term
    en: {full: "engagement evidence", definition: "Facts that show how a reviewer engaged with a record, such as what they opened and for how long."}
    fr: {full: "preuves d’examen", definition: "Faits qui montrent comment une personne qui révise a examiné un enregistrement, comme ce qu’elle a ouvert et pendant combien de temps."}
    source: {name: "FPSOT decisions specification, DEC-065; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: frozen-corpus
    kind: term
    en: {full: "frozen corpus", definition: "A set of test cases with expected results that nobody changes once its rule version is in force."}
    fr: {full: "corpus figé", definition: "Ensemble de cas d’essai avec leurs résultats attendus que personne ne modifie une fois sa version de règles en vigueur."}
    source: {name: "FPSOT decisions specification, DEC-081; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-decisions", checked: "2026-11-15"}
  - id: rules-as-code
    kind: term
    en: {full: "rules as code", definition: "The practice of writing the rules of a law or a policy as code that a machine can run, next to the legal text."}
    fr: {full: "règles sous forme de code", definition: "Pratique qui consiste à rédiger les règles d’une loi ou d’une politique sous forme de code exécutable par une machine, à côté du texte juridique."}
    source: {name: "OECD, Cracking the Code (2020), for the English form; French form to confirm", url: "https://www.oecd.org/en/publications/cracking-the-code_3afe6ba5-en.html", checked: "2026-11-15"}
```
