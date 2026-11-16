# language: fr
# SPDX-License-Identifier: Community-Spec-1.0
# Exemple de fonctionnalité de la spécification FPSOT sur les décisions (DEC-080), selon TST-020 à TST-036.
# Le programme, la loi et toutes les valeurs sont fictifs. Toutes les données sont synthétiques (TST-050 à TST-056).
@example-housing-benefit
Fonctionnalité: Admissibilité à l’allocation de logement d’exemple
  Chaque scénario énonce la date d’effet, les faits, le résultat, les codes de motif et la disposition citée.

  Règle: Le revenu du ménage ne doit pas dépasser la limite qui s’applique à la taille du ménage

    @example-housing-benefit-001
    Scénario: Un ménage au-dessus de la limite de revenu reçoit un refus
      Étant donné l’ensemble de règles "example-housing-benefit" à la version "1.2.0"
      Et la date d’effet "2026-09-01"
      Et un ménage de 3 personnes dont le revenu du ménage est de "53410.00" CAD
      Quand le service de décision statue sur la demande
      Alors le type de résultat est "decided" avec l’issue "refused"
      Et le motif principal est "household-income-above-limit" avec la limite "52000.00" CAD
      Et le motif cite l’article "4" de la loi "E-1"

    @example-housing-benefit-002
    Scénario: Un ménage à la limite de revenu reçoit l’allocation
      Étant donné l’ensemble de règles "example-housing-benefit" à la version "1.2.0"
      Et la date d’effet "2026-09-01"
      Et un ménage de 3 personnes dont le revenu du ménage est de "52000.00" CAD
      Quand le service de décision statue sur la demande
      Alors le type de résultat est "decided" avec l’issue "granted"
      Et le motif principal est "household-size" avec la limite "52000.00" CAD
      Et le motif cite l’article "4" de la loi "E-1"

  Règle: Un fait manquant ne mène jamais à un refus

    @example-housing-benefit-003
    Scénario: Un ménage sans données de revenu reçoit une demande de renseignements
      Étant donné l’ensemble de règles "example-housing-benefit" à la version "1.2.0"
      Et la date d’effet "2026-09-01"
      Et un ménage de 3 personnes sans revenu du ménage au dossier
      Quand le service de décision statue sur la demande
      Alors le type de résultat est "insufficient-information" avec le fait manquant "household-income"
      Et le motif cite l’article "4" de la loi "E-1"
