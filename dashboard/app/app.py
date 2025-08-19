from flask import Flask, render_template
import pandas as pd
import sqlalchemy
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

DB_URL = "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"


@app.route("/")
def index():
    engine = sqlalchemy.create_engine(DB_URL)

    try:
        conn = engine.raw_connection()
        try:
            df = pd.read_sql("SELECT * FROM finanz_kpis ORDER BY datum", conn)
        finally:
            conn.close()
    except Exception as e:
        return f"<h1>Database Error</h1><p>{e}</p>"

    if df.empty:
        return "<h1>No Data</h1><p>The table 'finanz_kpis' exists but has no rows. Run your ETL DAG first.</p>"

    # Spaltennamen klein schreiben
    df.columns = df.columns.str.lower()

    # Datum ins richtige Format bringen
    if "datum" in df.columns:
        df["datum"] = pd.to_datetime(df["datum"]).dt.strftime("%d.%m.%Y")

    # Tabelle rendern
    table_html = df.to_html(classes="data")

    # Chart rendern
    if "datum" in df.columns and "betrag" in df.columns:
        fig = px.line(df, x="datum", y="betrag", title="Finanzentwicklung")
        chart_html = pio.to_html(fig, full_html=False)
    else:
        chart_html = "<p>No chart available (columns missing)</p>"

    return render_template("index.html", table=table_html, chart=chart_html)


@app.route("/testdb")
def testdb():
    try:
        engine = sqlalchemy.create_engine(DB_URL)
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT 1")).scalar()
        return f"✅ DB OK → {result}"
    except Exception as e:
        return f"❌ DB ERROR: {e}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
