"""Resolve Spark's Maven JARs at image build time, so nothing downloads mid-workshop.

Run once from the Dockerfile. It imports the same helper the notebooks use, so the
cache is warmed for exactly the coordinates get_spark() will later ask Ivy for --
delta-spark and hadoop-azure. Getting those from one place is what stops the image
and the notebooks disagreeing about versions.

This lives in a file rather than a `python -c "..."` inside the Dockerfile for a
specific reason: see the warning above the COPY line in the Dockerfile.
"""

import sys

sys.path.insert(0, "/tmp/shared")

import northtrail

northtrail.warm_cache()
