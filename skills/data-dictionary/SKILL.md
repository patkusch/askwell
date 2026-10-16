---
name: data-dictionary
description: Builds a business glossary and data dictionary that defines each term and data field, its format, source, owner and rules, so everyone uses words the same way. Use when asked for a glossary or data dictionary, when teams disagree about what a term means, or when data requirements are needed.
license: MIT
metadata:
  version: "1.0"
---

# Data dictionary and glossary

Half of "the report is wrong" is two people using one word differently.

## Glossary: business terms

For each term: **name**, a one-sentence **definition** a new starter would understand, **synonyms to avoid**, an **example**, a **non-example**, and an **owner** who settles disputes.

Test: does "active customer" mean bought in 12 months, has an open account, or logged in? Write the answer you chose and why.

## Data dictionary: fields

| Field | Business meaning | Type & format | Allowed values / range | Required? | Source system | Owner | Rules / notes |
|---|---|---|---|---|---|---|---|

Capture also:
- **Where it comes from** and how often it updates.
- **Quality rules**: not blank, unique, within a range, matches another field.
- **Sensitivity**: personal, financial or confidential, and who may see it.
- **Retention**: how long it is kept.
- **Calculated fields** with the exact formula.

## Steps

1. Pull the field list from forms, reports and the existing database.
2. Draft definitions from the people who use them, not from IT alone.
3. Find clashes: same name, different meaning; different name, same meaning.
4. Get owners to agree one definition; record retired terms.
5. Publish in one place and name who maintains it.

## Watch for

- Definitions that repeat the word ("Customer: a person who is a customer").
- Free-text fields that should be lists.
- Dates without a time zone; amounts without a currency.
