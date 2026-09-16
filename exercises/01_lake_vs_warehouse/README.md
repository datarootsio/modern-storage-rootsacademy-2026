# Exercise 1 — Last week's revenue

**25 minutes** — 15 hands-on, 10 group debrief.

## The ask

Priya, who runs Marketing, sent this on Monday morning:

> Can you get me total revenue from orders over €100, broken down by region, for last week?
> The board deck is Thursday.
>
> Also — heads up for next sprint — we want to look at what people clicked on before they
> bought. Nothing formal yet, just exploring.

## What you have

Two places the order data lives:

- **The daily file drop** — `data/output/ex1_raw/`. Whatever the upstream systems export,
  landed as-is. Orders as CSV, clickstream as JSON.
- **The BI team's `orders` table** — a single clean, typed table they load every night.
  It's what the existing dashboards run on.

## Your job

1. Answer Priya's first question. Get a revenue-by-region number you'd be willing to put
   in front of the board.
2. Then work out what it would take to answer her second one.

Open `exercise.ipynb` and work top to bottom. When you hit something that doesn't behave,
that's the exercise — slow down there rather than working around it.

Stuck? `solution/solution.ipynb` has the whole thing worked through.
