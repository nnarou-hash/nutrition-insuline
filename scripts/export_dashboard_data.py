"""Exécute les requêtes de dashboard/queries/ et écrit des CSV agrégés."""
from pathlib import Path

from google.cloud import bigquery

ROOT = Path(__file__).resolve().parent.parent
client = bigquery.Client(project="nutrition-homa-nn", location="EU")
out = ROOT / "dashboard" / "exports"
out.mkdir(parents=True, exist_ok=True)

for sql_file in sorted((ROOT / "dashboard" / "queries").glob("*.sql")):
    df = client.query(sql_file.read_text()).to_dataframe()
    if "participant_id" in df.columns or len(df) > 500:
        raise SystemExit(f"{sql_file.name} : résultat trop détaillé, il doit être agrégé")
    df.to_csv(out / f"{sql_file.stem}.csv", index=False)
    print(f"OK {sql_file.stem} : {len(df)} lignes")
