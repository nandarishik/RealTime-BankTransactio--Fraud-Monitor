
# Real-Time Fraud Detection Pipeline

## Project Overview

This is a complete, end-to-end data engineering project that simulates a real-time banking fraud detection system. The pipeline ingests a continuous stream of transaction data, processes it in real-time to detect potential fraud, stores the results, and displays them on a live-updating web dashboard.

---

## Architecture & Data Flow

The entire infrastructure is containerized using Docker, allowing for easy setup and teardown. The data flows through the following stages:

1.  **Kafka Producer (`kafka_producer.py`)** Streams transaction data as JSON messages into a Kafka topic.

2.  **Message Broker (Kafka)** A Kafka cluster (run via Docker) acts as a high-throughput, persistent message queue for the transaction stream.

3.  **Stream Processor (Spark)** A PySpark application (`spark_consumer.py`) connects to the Kafka stream in real-time. It parses the data, applies fraud detection logic (e.g., `amount > 9000`), and enriches the data.

4.  **Data Warehouse (PostgreSQL)** The processed and enriched data (including the `is_flagged` column) is written from Spark into a PostgreSQL database in real-time.

5.  **Visualization (Streamlit)** A Streamlit web application (`fraud_detection_app.py`) connects to PostgreSQL, queries the processed data, and displays real-time metrics and alerts on an auto-refreshing dashboard.

**Flow Diagram:** Kafka Producer -> Kafka (transactions topic) -> Spark Streaming -> PostgreSQL -> Streamlit Dashboard

---

## Technologies Used

-   **Infrastructure:** Docker, Docker Compose
-   **Data Ingestion:** Apache Kafka
-   **Stream Processing:** Apache Spark (PySpark)
-   **Data Storage:** PostgreSQL
-   **Visualization:** Streamlit
-   **Core Language:** Python

**Key Python Libraries:** `pandas`, `kafka-python`, `pyspark`, `psycopg2-binary`, `sqlalchemy`, `plotly`, `streamlit`

---

## Prerequisites

Before you begin, ensure you have the following installed:

-   Docker Desktop
-   Python 3.9+
-   A code editor (e.g., VS Code)

---

## Setup & Installation

1.  **Clone the Repository** Ensure all project files (docker-compose.yml, Python scripts, etc.) are in a single directory.

2.  **Navigate to Project Directory**
    ```bash
    cd "path/to/project/folder"
    ```
3.  **Create and Activate a Virtual Environment**
    ```bash
    # Create environment
    python -m venv venv

    # Activate environment
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
4.  **Install Python Dependencies**
    ```bash
    pip install pyspark kafka-python psycopg2-binary pandas streamlit plotly sqlalchemy
    ```
5.  **Configure Streamlit Connection**

    Create a folder named `.streamlit` and a `secrets.toml` file inside it:
    ```bash
    mkdir .streamlit
    # Windows
    type nul > .streamlit\secrets.toml
    # macOS/Linux
    touch .streamlit/secrets.toml
    ```
    Add your PostgreSQL connection details to `.streamlit/secrets.toml`:
    ```toml
    [connections.postgres]
    dialect = "postgresql"
    host = "localhost"
    port = 5432
    database = "fraud_detection"
    username = "user"
    password = "password"
    ```

---

## How to Run the Pipeline

You will need three separate terminals running simultaneously:

**Terminal 1: Start Infrastructure & Kafka Producer**
```bash
docker-compose up -d
python kafka_producer.py
````

Leave this terminal running.

**Terminal 2: Start the Spark Consumer**

```bash
docker-compose exec spark-master /opt/spark/bin/spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.2.23 \
/opt/spark/work/spark_consumer.py
```

This terminal will show Spark logs and batch writes.

**Terminal 3: Launch the Streamlit Dashboard**

```bash
streamlit run fraud_detection_app.py
```

Your browser will open automatically with the live dashboard updating every 5 seconds.

-----

## Stopping the Project

1.  Stop the producer, consumer, and dashboard in their respective terminals using **Ctrl + C**.
2.  Shut down all Docker containers:
    ```bash
    docker-compose down
    ```

-----

## Future Enhancements

  - **Complex Fraud Rules:** Implement stateful streaming logic in Spark to detect patterns like rapid transactions from different locations for the same user.
  - **Machine Learning Model:** Integrate predictive models (e.g., Isolation Forest) into Spark for advanced fraud detection.
  - **Alerting System:** Send alerts to a dedicated Kafka topic when fraud is detected.
  - **Cloud Deployment:** Deploy the Dockerized application on AWS, Azure, or GCP.

<!-- end list -->

```

Would you like me to help you add those **badges, screenshots, and a "Quick Start" section** now to make it more professional for recruiters?
```
