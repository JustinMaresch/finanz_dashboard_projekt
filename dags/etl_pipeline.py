from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sqlalchemy
from sqlalchemy import text

DB_URL = "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"


def create_table():
    """Erstellt die Tabelle, falls sie noch nicht existiert."""
    engine = sqlalchemy.create_engine(DB_URL)
    ddl = """
    CREATE TABLE IF NOT EXISTS finanz_kpis (
        id SERIAL PRIMARY KEY,
        datum DATE UNIQUE,
        betrag NUMERIC,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))


def insert_testdata():
    """Leert die Tabelle und fügt Beispiel-Testdaten ein (idempotent)."""
    engine = sqlalchemy.create_engine(DB_URL)
    test_data = [
        {"datum": "2023-01-01", "betrag": 110.0},
        {"datum": "2023-01-02", "betrag": 220.0},
        {"datum": "2023-01-03", "betrag": 330.0},
    ]
    with engine.begin() as conn:
        # Tabelle leeren (ID Reset)
        conn.execute(text("TRUNCATE TABLE finanz_kpis RESTART IDENTITY;"))
        # Neue Daten einfügen
        for row in test_data:
            conn.execute(
                text("INSERT INTO finanz_kpis (datum, betrag) VALUES (:datum, :betrag)"),
                row,
            )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="etl_pipeline",
    default_args=default_args,
    description="ETL Pipeline für Finanz-KPIs",
    schedule_interval="@once",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["finanz"],
) as dag:

    t1 = PythonOperator(
        task_id="create_table",
        python_callable=create_table,
    )

    t2 = PythonOperator(
        task_id="insert_testdata",
        python_callable=insert_testdata,
    )

    t1 >> t2
