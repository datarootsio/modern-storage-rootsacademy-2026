# Exercise 5 — Capstone: make the call and defend it

**30 minutes** — 20 in small groups, 10 for pitches and open discussion.

Three companies have asked for an opinion. None of them is NorthTrail, and none of them has a
single right answer. Your job is to make a defensible recommendation and say what it costs.

Work in small groups. Fill in `worksheet.md`, then each group pitches one case in **2 minutes**.

---

## Case A — Ledgerline

A payments company. 40 OLTP Postgres databases, one per market, with change-data-capture
streaming out of all of them — roughly 8 million row changes a day, most of them updates to
rows that already exist rather than new rows.

Three teams consume it and none will move: the analysts use **Trino**, the fraud team runs
**Flink** for streaming features, and the data science team uses **Spark** on notebooks.
Today each team keeps its own copy of the data, and the three copies disagree often enough
that there is a recurring meeting about it.

Platform team: 6 engineers. Data volume: 40 TB and growing.

> **They asked:** "Can we get to one copy that all three engines read, without telling any team
> to change tools?"

---

## Case B — Northwind Supply

A 400-person industrial parts distributor. Everything already runs on **Databricks** — it was
chosen two years ago and nobody is revisiting it. BI dashboards for the sales team, plus two
ML models for demand forecasting.

Data volume is 900 GB and grows slowly. The platform "team" is **two engineers**, both of whom
also handle ingestion, on-call and stakeholder requests.

> **They asked:** "We keep reading that we should be using an open format so we're not locked
> in. Should we be worried, and should we switch?"

---

## Case C — Kitewatch

Real-time fleet monitoring for logistics operators. Every vehicle reports position and status
continuously, and dashboards must reflect reality within about a minute.

The workload is almost entirely **updates to existing records** — the current state of 50,000
vehicles, changing constantly. Around 4,000 record updates per second at peak, in tiny batches
arriving every few seconds. Queries are mostly "current state of this fleet", occasionally
"history of this vehicle for the last 30 days".

Platform team: 4 engineers, comfortable with Spark and Kafka.

> **They asked:** "Our nightly batch rewrite worked when we had 500 vehicles. It now takes six
> hours. What should this look like instead?"

---

## What to produce

For each case, in `worksheet.md`:

1. **Architecture** — warehouse, lake, or lakehouse.
2. **Table format** — if the architecture needs one.
3. **Three bullets of justification**, one each on:
   - **workload fit** — does the shape of their data and queries suit this?
   - **ecosystem** — do the engines and people they already have support it?
   - **interoperability** — what happens when something new needs to read this data?
4. **The first pain they'll hit** — name the specific thing from this morning's exercises that
   this company runs into first.

Point 4 is the one to spend time on. Anyone can pick a format from a comparison table.

Your facilitator has a model answer for each case and will share them after the pitches. Don't ask
for them early — they disagree with themselves in a couple of places on purpose, and the argument
you have in your group first is the point of the exercise.
