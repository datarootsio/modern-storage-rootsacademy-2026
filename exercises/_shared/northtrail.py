"""Shared setup for every Spark notebook in the workshop.

Imported as `from northtrail import get_spark, path`. The devcontainer puts this
folder on PYTHONPATH (see .devcontainer/devcontainer.json), so the import works
the same from an exercise notebook and from a solution notebook.

There is exactly one reason this file exists: the Spark session needs ~15 lines
of connection wiring that teach nothing about lakehouse architecture. Copying
those lines into nine notebooks would be nine places to get them wrong.
"""

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

# hadoop-azure gives Spark the abfss:// filesystem driver; PySpark does not
# bundle it. The version must match the Hadoop client jars PySpark ships with
# (4.0.1 -> 3.4.1). A mismatch fails at runtime with NoClassDefFoundError, not
# at install time, so keep this in step with the pin in .devcontainer/Dockerfile.
HADOOP_AZURE = "org.apache.hadoop:hadoop-azure:3.4.1"


def _config():
    """Read the participant's .env, searching upward from the notebook's folder."""
    dotenv = find_dotenv(usecwd=True)
    if dotenv:
        load_dotenv(dotenv)
    return (
        os.environ.get("STORAGE_ACCOUNT", "").strip(),
        os.environ.get("CONTAINER", "").strip(),
        os.environ.get("SAS_TOKEN", "").strip().lstrip("?"),
    )


def _local_lake():
    """Fallback used when no .env is present, so the notebooks stay runnable offline."""
    here = Path.cwd().resolve()
    root = next((p for p in [here, *here.parents] if (p / "exercises").is_dir()), here)
    lake = root / "_local_lake"
    lake.mkdir(exist_ok=True)
    return lake


def local_data(*parts):
    """Path to the data files shipped with the repo, from any notebook folder."""
    here = Path.cwd().resolve()
    root = next((p for p in [here, *here.parents] if (p / "data" / "output").is_dir()), None)
    if root is None:
        raise FileNotFoundError(
            "Could not find data/output. Run this notebook from inside the workshop repo."
        )
    return str(root.joinpath("data", "output", *parts))


def base_path():
    """Root of this participant's storage, e.g. abfss://participant-07@acct.dfs.core.windows.net"""
    account, container, _ = _config()
    if not account or not container:
        return f"file://{_local_lake()}"
    return f"abfss://{container}@{account}.dfs.core.windows.net"


def path(*parts):
    """Build a path inside the participant's container: path('bronze', 'orders')."""
    return "/".join([base_path(), *[str(p).strip("/") for p in parts]])


def get_spark(app_name="northtrail-workshop"):
    from delta import configure_spark_with_delta_pip
    from pyspark.sql import SparkSession

    account, _, sas = _config()

    if account and not sas:
        raise RuntimeError(
            "STORAGE_ACCOUNT is set but SAS_TOKEN is empty.\n"
            "Check the .env file in the repo root: it needs all three of\n"
            "STORAGE_ACCOUNT, CONTAINER and SAS_TOKEN. Compare it against\n"
            ".env.example, and ask your facilitator for a fresh one if the\n"
            "SAS_TOKEN line looks truncated."
        )

    builder = (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.jars.ivy", os.environ.get("SPARK_IVY_DIR", "/opt/ivy"))
        # Tiny data, so keep the shuffle tiny too -- 200 partitions on 400 rows
        # turns a two-second job into a twenty-second one.
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.ui.showConsoleProgress", "false")
    )

    if account and sas:
        # Hadoop 3.4+ takes a SAS token directly via fs.azure.sas.fixed.token.
        # Deliberately no fs.azure.sas.token.provider.type here: the class that
        # consumes the fixed token has no no-arg constructor, so naming it
        # explicitly fails with NoSuchMethodException.
        # The spark.hadoop. prefix is what forwards these into Hadoop's config.
        # Without it Spark prints "Ignoring non-Spark config property" warnings.
        prefix = f"spark.hadoop.fs.azure"
        host = f"{account}.dfs.core.windows.net"
        builder = builder.config(
            f"{prefix}.account.auth.type.{host}", "SAS"
        ).config(f"{prefix}.sas.fixed.token.{host}", sas)

    spark = configure_spark_with_delta_pip(
        builder, extra_packages=[HADOOP_AZURE]
    ).getOrCreate()

    if account and sas:
        # Also set it on the live session, not just the builder above. Builder
        # spark.hadoop.* properties are only read when the SparkContext is first
        # constructed, and getOrCreate() returns an existing session when the
        # kernel already has one -- so a participant who ran a cell before saving
        # their .env, then re-ran it without restarting the kernel, would get a
        # session with no SAS config at all. ABFS then falls back to shared-key
        # auth and fails with:
        #   Invalid configuration value detected for fs.azure.account.key
        # Setting the Hadoop conf here works whether the session is new or reused.
        hadoop_conf = spark._jsc.hadoopConfiguration()
        host = f"{account}.dfs.core.windows.net"
        hadoop_conf.set(f"fs.azure.account.auth.type.{host}", "SAS")
        hadoop_conf.set(f"fs.azure.sas.fixed.token.{host}", sas)

    spark.sparkContext.setLogLevel("ERROR")
    return spark


def where_am_i():
    """One-line summary printed at the top of each notebook, so mis-set .env files are obvious."""
    account, container, sas = _config()
    if not account:
        return f"No .env found -- using local storage at {_local_lake()}"
    return f"storage account {account}, container {container} (SAS {'set' if sas else 'MISSING'})"


def ls(spark, target):
    """List the files in a storage folder, newest name last.

    Peeking at the actual folder layout is a recurring move in exercises 2-4, and
    the alternative is four lines of py4j in a participant notebook.
    """
    jvm = spark._jvm
    hadoop_path = jvm.org.apache.hadoop.fs.Path(target)
    fs = hadoop_path.getFileSystem(spark._jsc.hadoopConfiguration())
    entries = []
    for status in fs.listStatus(hadoop_path):
        name = status.getPath().getName()
        entries.append(f"{name}/" if status.isDirectory() else f"{name}  ({status.getLen()} bytes)")
    return sorted(entries)


def remove(spark, *targets):
    """Delete storage paths, so an exercise can start from a known state.

    Re-running a notebook otherwise leaves the previous run's commit history in place,
    which makes version numbers meaningless. Only ever called on paths the exercise owns.
    """
    jvm = spark._jvm
    for target in targets:
        hadoop_path = jvm.org.apache.hadoop.fs.Path(target)
        fs = hadoop_path.getFileSystem(spark._jsc.hadoopConfiguration())
        if fs.exists(hadoop_path):
            fs.delete(hadoop_path, True)


def warm_cache():
    """Resolve the Spark jars at image build time so no download happens live.

    Called from the Dockerfile. Uses the same coordinates get_spark() uses, so
    the cache can never be warmed for the wrong versions.
    """
    spark = get_spark("warm-ivy-cache")
    print(f"resolved jars for Spark {spark.version}")
    spark.stop()
