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

## Worked Example

A lesson's worked example, then its practice task. Each step says why.

```md
## Worked Example

Make every row in `order_items` point to an order that exists.

1. Name the referring column and the column it refers to: `order_items.order_id` refers to `orders.id`. Why: the constraint goes on the table that does the referring.
2. Check that `orders.id` is the primary key. Why: a foreign key can only refer to a primary key or a unique column.
3. Add the constraint: `ALTER TABLE order_items ADD FOREIGN KEY (order_id) REFERENCES orders (id);`. Why: from now on the database refuses an item whose order does not exist.
4. Check it: insert an item with `order_id = 999` when there is no order 999. The insert fails, so the constraint works.

## Practice

Make every row in `payments` point to an order that exists, and say how you would check it.

<details>
<summary>Answer</summary>

`ALTER TABLE payments ADD FOREIGN KEY (order_id) REFERENCES orders (id);` Then insert a payment for an order that does not exist; it should fail.

</details>
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

## Distinction Card

`WHERE` (lesson 2.1) and `HAVING` (lesson 3.2) are easy to confuse, so other lessons sit between them. The section that teaches `HAVING` gets one card that contrasts them:

```html
<details>
<summary>A report should list only customers with more than 3 orders. WHERE or HAVING, and why?</summary>

`HAVING`: the condition is on each group's count, and `WHERE` filters rows before they are grouped.

Source lessons: [[02 Filtering/01 Filtering Rows|Filtering Rows]], [[03 Grouping/02 Filtering Groups|Filtering Groups]]

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

## Growing Review Interval

Two clean reviews of one study set. Work out the previous interval before you overwrite the dates.

Before the first review:

```yaml
status: mastered
last_reviewed: 2026-03-01
next_review: 2026-03-15
review_count: 3
confidence: 5
```

On 2026-03-15 the learner answers every prompt quickly and correctly: confidence 5. The previous interval is 14 days, so the next one is the larger of 14 and 2 × 14, which is 28 days:

```yaml
status: mastered
last_reviewed: 2026-03-15
next_review: 2026-04-12
review_count: 4
confidence: 5
```

On 2026-04-12 every answer is correct, but two take a while: confidence 4. The previous interval is 28 days, so the next one is the larger of 7 and 2 × 28, which is 56 days:

```yaml
status: needs review
last_reviewed: 2026-04-12
next_review: 2026-06-07
review_count: 5
confidence: 4
```

If a later review scores 3 or lower, the set goes back to the base schedule: 3 days, or tomorrow.

## Prerequisite Check

On 2026-05-25 the next lesson is `03 Joins/01 Inner Join`. No lesson in `03 Joins` is studied yet, so it starts a new section. Its section index says "None yet." under Prerequisites, so both earlier sections count.

`01 Tables And Rows/flashcards/Flashcards.md`:

```yaml
status: needs review
next_review: 2026-05-20
confidence: 4
```

`02 Relational Modeling/quizes/Quiz.md`:

```yaml
status: needs review
next_review: 2026-05-30
confidence: 2
```

`02 Relational Modeling/exercises/Exercises.md` is `not started`, so it is skipped. The quiz is weak (confidence 2), and the flashcards are overdue. The tutor asks a few questions from the quiz, then from the flashcards, updates both sets, and then starts the lesson. The session close says: "Before Joins: reviewed the Relational Modeling quiz (confidence 2) and the overdue Tables And Rows flashcards."

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
