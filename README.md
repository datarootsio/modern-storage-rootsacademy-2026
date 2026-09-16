# NorthTrail Lakehouse Workshop

A hands-on, 4-hour workshop on modern data storage architectures, for data engineers who know
Python and SQL but haven't worked with lakes, warehouses or lakehouses.

Everything runs on one continuous story: **NorthTrail**, a small outdoor-gear shop whose daily order
and clickstream exports you're responsible for. Five exercises, each one another day in the life of
that pipeline. You hit every problem before anyone names the concept that solves it.

| | Exercise | Time |
|---|---|---|
| 1 | Last week's revenue — lake vs warehouse | 25 min |
| 2 | Fix yesterday's orders — file format, table format, catalog | 35 min |
| 3 | How locked in are we? — open table formats | 15 min |
| 4 | The daily revenue pipeline — Bronze/Silver/Gold, schema change, incident recovery | 75 min |
| 5 | Capstone — make the call and defend it | 30 min |

---

## Participants — start here

> **Do all of this the day before the workshop, not on the morning.** The container image is about
> 2 GB. Twenty people downloading that simultaneously on conference wifi is the most reliable way to
> lose the first half hour of a four-hour session.

### 1. Install the three prerequisites

| | What | Notes |
|---|---|---|
| 1 | [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Needs admin rights to install. **Windows:** accept the WSL 2 backend when prompted — that is the default and the one you want. **macOS:** pick the Apple Silicon or Intel build to match your Mac. **Linux:** Docker Engine is fine, Desktop isn't required. |
| 2 | [Visual Studio Code](https://code.visualstudio.com/) | |
| 3 | The **Dev Containers** extension | Install by ID — `ms-vscode-remote.remote-containers`. Searching the marketplace for "dev container" returns several similarly named extensions; this is the Microsoft one. |

Then **start Docker Desktop and leave it running.** On Windows and macOS it is not running just
because it is installed. Wait for its whale icon to stop animating before the next step.

### 2. Give Docker enough memory

Spark runs a Java virtual machine inside the container. With less than 4 GB available it fails in a
way that looks like a bug in the workshop (`Java gateway process exited before sending its port
number`), so set this now:

- **Docker Desktop (Windows/macOS):** Settings → Resources → Memory → at least **4 GB**. 8 GB if
  you have it to spare.
- **Linux:** nothing to do; containers use the host's memory directly.

### 3. Clone the repo and open it in VS Code

```bash
git clone <this-repo-url>
cd modern-architecture-course
code .
```

**Open the repository root** — the folder containing this `README.md`. Opening a subfolder (say,
`exercises/`) is the single most common way this goes wrong, because VS Code then can't see the
`.devcontainer/` folder.

### 4. Reopen in the container

VS Code should show a notification: **"Folder contains a Dev Container configuration file. Reopen
folder to develop in a container."** Click **Reopen in Container**.

If the notification doesn't appear, press `F1`, type `Reopen in Container`, and pick
**Dev Containers: Reopen in Container**.

> ⚠️ **If you instead get a list of configuration templates** — "Python 3", "Ubuntu", "Anaconda",
> and so on — **stop and close it.** That is the *Add Dev Container Configuration Files* picker, and
> it only appears when VS Code cannot find the config this repo already ships. Picking one would
> overwrite ours. Check that you opened the repository root, and that the Dev Containers extension
> is installed.
>
> This repo has exactly one configuration, `.devcontainer/devcontainer.json`, named
> **NorthTrail Lakehouse Workshop**. You never have to choose it — VS Code finds it.

The first build takes several minutes (it installs Java, Python packages and the Spark JARs). You
can watch progress via "Starting Dev Container (show log)". After this first time, it reopens in
seconds.

### 5. Check it worked

When the container is running, the **bottom-left corner of VS Code** reads
**"Dev Container: NorthTrail Lakehouse Workshop"**. If it doesn't, you are still on your own
machine and nothing below will work.

Open a terminal in VS Code (`` Ctrl+` ``) — it is now a shell *inside* the container — and run:

```bash
python -c "import pyspark; print('pyspark', pyspark.__version__)"
java -version
```

You want `pyspark 4.0.1` and a Java **17** version string. Both come from the container; neither
needs to be installed on your laptop.

### 6. Add your storage credentials

Save the `.env` file your facilitator sent you into the **root of this repo** — the folder
containing this README.

It must be named exactly `.env`, not `participant-07.env`. See [.env.example](.env.example) for the
shape. It is gitignored, so your token won't end up in a commit.

### 7. Run the connectivity check

Open [notebooks/00_sanity_check.ipynb](notebooks/00_sanity_check.ipynb) and run every cell top to
bottom. It writes a tiny table to your own storage container, reads it back, and prints ✅ or ❌.

If VS Code asks which kernel to use, choose the interpreter at **`/opt/venv/bin/python`**.

A ✅ means you are done setting up. Anything else — see the table below, then ask your facilitator.

### 8. Start Exercise 1

Read [Exercise 1's README](exercises/01_lake_vs_warehouse/), then work through its
`exercise.ipynb`.

---

### If something goes wrong

| What you see | What it means | Fix |
|---|---|---|
| A list of config templates ("Python 3", "Ubuntu"…) | VS Code can't find `.devcontainer/` | Close it. Open the repo **root**, and check the Dev Containers extension is installed |
| `Cannot connect to the Docker daemon` | Docker Desktop isn't running | Start it, wait for the whale icon to settle, then reopen |
| `Java gateway process exited before sending its port number` | Docker has too little memory | Docker Desktop → Settings → Resources → Memory → 4 GB+ |
| Build fails downloading packages | A corporate proxy or VPN is intercepting TLS | Try off the VPN if permitted; otherwise tell your facilitator before the session |
| `No FileSystem for scheme "abfss"` | VS Code opened the folder **outside** the container | Check the bottom-left corner. If it doesn't say "Dev Container", run **Reopen in Container** — the Java driver only exists inside |
| `ModuleNotFoundError: northtrail` | Same cause as above | Same fix |
| `No .env found` | The file isn't in the repo root, or isn't named exactly `.env` | Move/rename it next to this README |
| `Server failed to authenticate` | Your access token expired, or was truncated when copied | Ask your facilitator for a fresh `.env` |
| The first Spark cell takes ~20 seconds | Normal — that's the JVM starting | Nothing. It's quicker after the first time |

**Why a container rather than just installing things?** Spark doesn't run in Python — it runs in a
Java virtual machine that Python talks to. On Windows, Spark in local mode additionally needs
`winutils.exe` and `hadoop.dll` installed and `HADOOP_HOME` set before it will write anything, and
every `GROUP BY` in exercises 2–4 goes through a local directory. The container means nobody spends
the workshop installing a JDK.

Each exercise has a fully worked `solution/` beside it. Use it when you're stuck — but give the
problem a real go first, because the exercises are built around what you discover by getting stuck.

**When something fails, that's usually the exercise.** Slow down rather than working around it.

---

## What's in here

```
exercises/01…05/          one folder per exercise: README.md, exercise.ipynb, solution/
exercises/_shared/        northtrail.py — Spark session + path helpers, on PYTHONPATH
notebooks/                00_sanity_check.ipynb
data/output/              the NorthTrail dataset the exercises read
pyproject.toml, uv.lock   Python dependencies, locked
.devcontainer/            the image — Python, Java 17, Spark, Delta, DuckDB, Jupyter
```

**`data/output/` is committed on purpose.** The synthetic NorthTrail data is deterministic and
tiny (280 KB), so it ships with the repo and there is nothing to generate. Exercise 1 reads it
straight off disk; Exercise 2 copies it into your storage container.

## Versions

Python dependencies are declared in [pyproject.toml](pyproject.toml) and locked, whole tree
included, in [uv.lock](uv.lock). The image installs them with
[uv](https://docs.astral.sh/uv/) via `uv sync --frozen`, so a rebuild next year resolves to exactly
the same 109 packages that were tested.

The versions that matter, verified together against live ADLS Gen2:

| | |
|---|---|
| `pyspark` | 4.0.1 — bundles the Hadoop 3.4.1 client jars |
| `delta-spark` | 4.0.1 — the release paired with Spark 4.0 |
| `hadoop-azure` | 3.4.1 — the `abfss://` driver, which PySpark does not ship |
| Java | 17 — from apt in the image, not a Python package |

Note that only the first two are pip-installable. `hadoop-azure` is a Java library, resolved from
Maven into a pre-warmed cache at `/opt/ivy` when the image is built, which is why the first Spark
session works without touching the network.

These move as a set. **Spark 3.5 does not work here:** its Hadoop 3.3.4 predates the fixed-SAS
support that `abfss://` needs, and dropping a newer `hadoop-azure` into it fails mid-write.

Spark runs in local mode throughout — no cluster, no Databricks. The only cloud resource is one
Standard_LRS storage account.
