The filenames ARE the timeline. Each instant is <timestamp>.<state>:

  20260311091500.commit     finished
  20260311093000.commit     finished
  20260311094500.inflight   started, not finished -- readers ignore it

A writer creates .requested, then .inflight, then .commit. A reader takes the
newest .commit and ignores anything still inflight, which is how it sees a
consistent snapshot without locking.
