# Three table formats, side by side

All three do the same job: keep metadata next to your data files so a folder behaves like a
table. They disagree about how to organise that metadata, and those disagreements are what
make one a better fit than another for a given workload.

## Where the metadata lives

| | Delta Lake | Apache Iceberg | Apache Hudi |
|---|---|---|---|
| Metadata folder | `_delta_log/` | `metadata/` | `.hoodie/` |
| One change is… | a numbered JSON file (`000...007.json`) | a new snapshot in `vN.metadata.json` + an Avro manifest list | a timestamped instant file (`20260311093000.commit`) |
| Metadata encoding | JSON, plus periodic Parquet checkpoints | JSON for the table, Avro for manifests | JSON |
| Finding current state | replay the JSON commits from the last checkpoint | read the latest `metadata.json`, follow it to the snapshot | take the newest `.commit` on the timeline |
| Readable by eye | yes | the table file, yes; manifests are binary Avro | yes |

## What each one optimises for

**Delta Lake** — the simplest model of the three: an ordered log of commits. Easy to reason
about and to inspect by hand. Originated at Databricks and is most mature there, though
engine support elsewhere has grown a lot.

**Iceberg** — designed so that no engine needs to list the storage folder to plan a query.
The manifest tree carries per-file statistics (min/max per column), so a query prunes files
before opening any of them. That indirection costs an extra metadata hop per read, and buys
the widest genuinely multi-engine support: Spark, Trino, Flink, DuckDB, Snowflake, BigQuery.

**Hudi** — built around updating records rather than appending files, which is why its
config names a `recordkey` and a `precombine` field. Its `MERGE_ON_READ` mode writes changes
to small delta logs and merges them at read time, then compacts in the background — which is
what makes frequent small upserts affordable instead of rewriting whole files each time.

## The part that matters more than the table above

Every one of these is a **specification** — a documented layout of files that any engine can
learn to read. None is a running service. That is the whole point of "open": your data stays
in Parquet files in your own storage, and the format only describes how to interpret the
folder around them.

So the real question when choosing is rarely "which spec is best". It is *which engines your
organisation actually runs, and which of these they read and write well today.*
