This folder documents Spark-specific project behavior.

Workspace terminal settings for local Spark must remain in [.vscode/settings.json](../.vscode/settings.json).
VS Code does not apply a settings file stored under `spark/`, so moving that file here would stop the automatic `SPARK_HOME` override from taking effect.

With the current setup:

- The project venv uses `pyspark 4.1.1` and `delta-spark 4.3.1`.
- Workspace terminals clear inherited `SPARK_HOME`.
- Local Spark runs against the venv-managed PySpark runtime.

If you move the settings file into this folder without another mechanism to clear `SPARK_HOME`, Spark will likely fail again because the machine-level Spark 4.2.0 runtime will conflict with the venv packages.
