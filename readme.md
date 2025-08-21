Finanz Dashboard Projekt

Ein Finanz-Dashboard mit ETL-Pipeline und Weboberfläche. Das Projekt verwendet Docker, um Daten aus CSV-Dateien zu laden, zu transformieren und in einer Datenbank bereitzustellen. Anschließend können die Daten über ein Dashboard visualisiert werden.

Projektstruktur

```plaintext
finanz_dashboard_projekt/
├── docker-compose.yml       # Docker Setup für Datenbank + Dashboard
├── init.sql                 # Initiales SQL-Skript für die Datenbank
├── dags/                    # ETL-Pipelines (z. B. mit Airflow)
│   ├── etl_pipeline.py
│   └── data/                # Beispieldaten für ETL
├── dashboard/               # Web-Dashboard
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── app.py
│       ├── static/
│       └── templates/
├── data/                    # Weitere Beispieldaten
└── .env                     # Umgebungsvariablen
```


Voraussetzungen

Docker
Docker Compose

Installation & Nutzung

.env Datei erstellen (siehe .env.example) mit den notwendigen Zugangsdaten.

Docker-Container starten:
docker-compose up --build

Airflow im Browser öffnen:
Localhost:8080

Dashboard im Browser öffnen:
Localhost:5000
