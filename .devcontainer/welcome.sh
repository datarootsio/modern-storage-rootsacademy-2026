#!/usr/bin/env bash
# Printed every time a participant attaches. Their first job is the .env file.
echo ""
echo "  NorthTrail Lakehouse Workshop"
echo "  ---------------------------------------------------------------"
if [[ -f .env ]]; then
  echo "  .env found        -> $(grep -E '^CONTAINER=' .env || echo 'CONTAINER not set')"
  echo "  Next: run notebooks/00_sanity_check.ipynb"
else
  echo "  No .env yet."
  echo "  1. Save the .env file the facilitator sent you in this folder:"
  echo "       $(pwd)/.env"
  echo "  2. Run notebooks/00_sanity_check.ipynb"
fi
echo ""
