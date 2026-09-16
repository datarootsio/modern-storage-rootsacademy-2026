# NorthTrail Lakehouse Workshop devcontainer.
#
# Everything the four hours need is baked in. Nothing installs at workshop time:
# no pip, no apt, and -- the easy one to miss -- no Maven downloads either.
#
# Why a container at all, when uv could install the Python side natively: Spark
# runs in a JVM and, in local mode on native Windows, needs winutils.exe and
# hadoop.dll with HADOOP_HOME set before it will write anything through a local
# directory. Every GROUP BY in exercises 2-4 spills through spark.local.dir, so
# that is not avoidable. A container gives every laptop the same Linux underneath
# and the question never comes up.
#
# Pinned to bookworm on purpose: trixie ships only Java 21, and Spark 4.0 is
# pinned to Java 17 here. Do not bump this without bumping Spark too.
FROM python:3.11-slim-bookworm

# Spark needs a JVM. The rest is what the VS Code Dev Containers extension and a
# working shell expect from a slim base.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless \
        ca-certificates \
        git \
        less \
        procps \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s "$(dirname "$(dirname "$(readlink -f "$(which java)")")")" /usr/lib/jvm/current
ENV JAVA_HOME=/usr/lib/jvm/current

# A non-root user, which the Dev Containers extension expects.
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash vscode

# uv from PyPI rather than COPY --from=ghcr.io/astral-sh/uv. The ghcr copy is the
# documented pattern, but it makes the build depend on a second registry, and
# corporate proxies that allow PyPI often don't allow ghcr.io. One less thing to
# get whitelisted before a workshop.
RUN pip install --no-cache-dir uv==0.11.29

# Dependencies come from pyproject.toml + uv.lock, which pin the whole tree
# rather than just the top-level packages. --frozen fails the build if the lock
# is out of date with pyproject.toml, so the image can never drift from it.
#
# The environment lives at /opt/venv, deliberately outside the workspace: a
# .venv inside the project would be shadowed by the devcontainer's bind mount.
# --no-cache matters: without it uv's download cache (~1.4 GB of wheels) is
# baked into the layer alongside the environment it was used to build.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON=/usr/local/bin/python \
    UV_PYTHON_DOWNLOADS=never
WORKDIR /tmp/build
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-cache
ENV PATH=/opt/venv/bin:$PATH

# Pre-resolve the Spark JARs into a shared Ivy cache.
#
# Two of them are not optional:
#   delta-spark   -- the Delta reader/writer
#   hadoop-azure  -- the abfss:// filesystem driver. PySpark bundles Hadoop's
#                    client jars but NOT this one, so without it every
#                    abfss:// path fails with "No FileSystem for scheme".
# The exact coordinates come from exercises/_shared/northtrail.py, so the image
# and the notebooks can never disagree about which jars they expect. Resolving
# them here means the first Spark session of the session is a cache hit, and
# works even on a flaky conference network.
# ⚠️ Do not inline this as `python -c "... from northtrail import ..."`.
# The VS Code Dev Containers extension finds the base image by scanning this file
# line by line for /^\s*FROM\s+/ and taking the LAST match. A Python import
# written at the start of a continuation line matches, so it decided the base
# image was "northtrail" and failed with "pull access denied" before building
# anything. `docker build` was unaffected -- Docker's real parser knows that text
# belongs to the RUN -- so this only broke Reopen in Container. Keep Python that
# starts a line with `from` out of this file.
COPY exercises/_shared/northtrail.py /tmp/shared/northtrail.py
COPY .devcontainer/warm_jars.py /tmp/shared/warm_jars.py
ENV SPARK_IVY_DIR=/opt/ivy
RUN mkdir -p ${SPARK_IVY_DIR} \
    && python /tmp/shared/warm_jars.py \
    && chmod -R a+rwX ${SPARK_IVY_DIR}

# Quieter Spark logs. Participants should see their own output, not a screenful of
# INFO lines -- and a wall of red WARN text makes a real failure hard to spot.
RUN SPARK_CONF="$(python -c 'import pyspark,os;print(os.path.join(os.path.dirname(pyspark.__file__),"conf"))')" \
    && mkdir -p "$SPARK_CONF" \
    && printf '%s\n' \
    'rootLogger.level = error' \
    'rootLogger.appenderRef.stdout.ref = console' \
    'appender.console.type = Console' \
    'appender.console.name = console' \
    'appender.console.target = SYSTEM_ERR' \
    'appender.console.layout.type = PatternLayout' \
    'appender.console.layout.pattern = %d{HH:mm:ss} %p %c{1}: %m%n' \
    > "$SPARK_CONF/log4j2.properties"

WORKDIR /workspaces
ENV PYTHONUNBUFFERED=1
USER vscode
