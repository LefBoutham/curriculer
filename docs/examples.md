# Examples

These examples are short synthetic snippets. They are not a sample course and should not be expanded into one inside this repository.

## Lesson Fragment

```md
---
type: lesson
title: "Foreign Key Constraint"
section: "02 Relational Modeling"
source:
order: 2.3
study_status: not started
last_studied:
study_count: 0
prerequisites:
  - "[[01 Tables And Rows/01 Primary Keys|Primary Keys]]"
depends_on:
mastery_evidence:
---

## Core Idea

A foreign key records that values in one table must match existing values in another table.

## Practice

Explain what should happen when an order references a customer id that does not exist.
```

## Exercise Answer Block

```md
### 1. Apply the core idea

Write the constraint that makes `orders.customer_id` reference `customers.id`.

<details>
<summary>Answer</summary>

Use a foreign key from `orders(customer_id)` to `customers(id)`.

</details>
```

## Flashcard

```html
<details>
<summary>When should a course add a glossary term?</summary>

When the learner asks for it, when it becomes central across lessons, or when confusing it with a nearby term would cause real misunderstanding.

</details>
```

## Review Metadata Update

```yaml
status: needs review
last_reviewed: YYYY-MM-DD
next_review: YYYY-MM-DD
review_count: 2
confidence: 3
notes: "Confused foreign key validation with joins; retry constraint-writing exercise."
```

## Quiz Question Object

Keep the Markdown quiz note as the human-readable inventory, then mirror the question in the self-contained HTML quiz.

```js
{
  q: "What does a foreign key constraint protect against?",
  a: 1,
  choices: [
    "Duplicate column names",
    "References to missing parent rows",
    "Slow SELECT queries"
  ],
  rationale: "A foreign key enforces that referenced parent values exist."
}
```
