# Exercise 4 — The daily revenue pipeline

**75 minutes** — 60 hands-on, 15 group debrief. This is the long one.

## The ask

From Sofia, Head of Ops, after the quarterly review:

> Every morning we get an export of yesterday's orders, and every morning someone opens a
> spreadsheet and works out revenue by region by hand. I want that on a dashboard instead,
> refreshed daily, without anyone touching it.
>
> It has to be right. If the number on that dashboard is wrong, people will make decisions
> on it before anyone notices.

## What you have

Three days of exports have accumulated in your container under `raw/batches/`:
`day1/`, `day2/`, `day3/`. You will process them one at a time, in order, as if each one
landed the morning it arrived.

## Your job

Build the pipeline on day one. Then keep it running on day two and day three.

That's deliberately all the brief you get — like any pipeline, what it has to survive only
becomes clear once it's running. Work through `exercise.ipynb` top to bottom and **don't skip
ahead to a later day**: the point of each day is what it does to the pipeline you built on the
previous one.

Stuck? `solution/solution.ipynb` has the whole thing worked through.
