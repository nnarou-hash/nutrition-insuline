"""Charge les fichiers NHANES (.xpt) bruts dans BigQuery (dataset nhanes_raw)."""
from pathlib import Path

import pandas as pd
from google.cloud import bigquery

PROJECT = "nutrition-homa-nn"
DATASET = "nhanes_raw"
LOCATION = "EU"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
FILES = ["DEMO_L", "BMX_L", "INS_L", "GLU_L", "PAQ_L", "FASTQX_L"]

client = bigquery.Client(project=PROJECT, location=LOCATION)

for name in FILES:
    df = pd.read_sas(RAW_DIR / f"{name}.xpt", format="xport", encoding="utf-8")
    df.columns = [c.lower() for c in df.columns]
    table_id = f"{PROJECT}.{DATASET}.{name.lower()}"
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
    )
    job.result()
    print(f"OK  {table_id} : {len(df)} lignes, {len(df.columns)} colonnes")
