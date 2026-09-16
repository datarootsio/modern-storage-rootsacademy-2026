# Exercise 2 — Fix yesterday's orders

**35 minutes** — 25 hands-on, 10 group debrief.

## The ask

Marc, who runs Ops, catches you before standup:

> Three orders from yesterday went out at the wrong price — someone keyed the amount in
> without the decimal point, so we've got a €23,000 order for a pair of boots. And there are
> two QA test rows in there from Friday's release.
>
> Finance exports at 18:00 and whatever's in the files at that point is what they'll book.
> Can you get them corrected before then?

## What you have

Yesterday's drop, already in your own storage container at `raw/orders/` — three Parquet
files, about 400 orders between them. The first cell of the notebook puts them there.

## Your job

1. Correct the three mispriced orders.
2. Remove the two test rows.
3. Be able to tell Marc, afterwards, exactly what you changed — he will ask.

Open `exercise.ipynb`. Point 3 is not an afterthought; treat it as part of the task.

Stuck? `solution/solution.ipynb` has the whole thing worked through.
