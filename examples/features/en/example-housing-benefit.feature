# language: en
# SPDX-License-Identifier: Community-Spec-1.0
# Example feature of the FPSOT decisions specification (DEC-080), under TST-020 to TST-036.
# The program, the act and every value are fictional. All data is synthetic (TST-050 to TST-056).
@example-housing-benefit
Feature: Eligibility for the example housing benefit
  Each scenario states the effective date, the facts, the result, the reason codes and the cited provision.

  Rule: The household income must not exceed the limit for the household size

    @example-housing-benefit-001
    Scenario: A household above the income limit is refused
      Given the rule set "example-housing-benefit" at version "1.2.0"
      And the effective date "2026-09-01"
      And a household of 3 persons with a household income of "53410.00" CAD
      When the decision service decides on the application
      Then the result kind is "decided" with the outcome "refused"
      And the principal reason is "household-income-above-limit" with the limit "52000.00" CAD
      And the reason cites section "4" of the act "E-1"

    @example-housing-benefit-002
    Scenario: A household at the income limit is granted
      Given the rule set "example-housing-benefit" at version "1.2.0"
      And the effective date "2026-09-01"
      And a household of 3 persons with a household income of "52000.00" CAD
      When the decision service decides on the application
      Then the result kind is "decided" with the outcome "granted"
      And the principal reason is "household-size" with the limit "52000.00" CAD
      And the reason cites section "4" of the act "E-1"

  Rule: A missing fact never leads to a refusal

    @example-housing-benefit-003
    Scenario: A household with no income data gets a request for information
      Given the rule set "example-housing-benefit" at version "1.2.0"
      And the effective date "2026-09-01"
      And a household of 3 persons with no household income on file
      When the decision service decides on the application
      Then the result kind is "insufficient-information" with the missing fact "household-income"
      And the reason cites section "4" of the act "E-1"
