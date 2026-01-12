# 🚀 Multi-API to PostgreSQL ETL Pipeline

A robust, modular ETL (Extract, Transform, Load) pipeline built with Python and PostgreSQL. This project orchestrates data collection from three distinct REST APIs, transforms dynamic JSON responses into a relational schema, and loads them into a production-ready database.

## 🏗️ Architecture & Engineering Decisions
This pipeline is designed with a focus on **modularity**, **idempotency**, and **reliability**:

* **Extraction**: Utilizes dedicated extractor classes to fetch data from the Advice Slip, ZenQuotes, and Dog CEO APIs.
* **Transformation**: Custom logic maps diverse API structures (e.g., converting list-based ZenQuotes responses) into a unified database format and uses URL parsing to determine dog breeds.
* **Loading**: Implements `UPSERT` logic (`ON CONFLICT DO NOTHING`) to ensure data remains clean even with duplicate API fetches.
* **Observability**: Integrated logging captures timestamps, execution status, and detailed error handling for API rate limits (HTTP 429) or network timeouts.



## 🛠️ Technical Stack
* **Language**: Python 3.12+
* **Database**: PostgreSQL 17
* **Libraries**: `requests`, `psycopg2-binary`, `python-dotenv`, `pytest`

## 🚀 Getting Started

### 1. Environment Setup
Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the root directory:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=etl_pipeline
DB_USER=postgres
DB_PASSWORD=your_password
```

### 2. Database Initialization
Initialize your PostgreSQL schema using the provided script:

```powershell
psql -h localhost -U postgres -d etl_pipeline -f sql/create_tables.sql
```

### 3. Execution
To run the full data ingestion pipeline, use:

```bash
python run_pipeline.py --batch-size 1 --log-level INFO
```

## 🧪 Quality Assurance
Verify the integrity of the components using the built-in test suite:

```bash
pytest tests/test_pipeline.py -v
```

The test suite includes verified unit tests for extractors and transformers, ensuring the data cleaning logic remains intact during refactors.

## 📊 Data Model & Logic
The pipeline manages a relational model across three core tables:

1. **Extraction**:
    * Fetches unique advice from the Advice Slip API.
    * Collects motivational quotes via ZenQuotes.
    * Retrieves random dog images from the Dog CEO API.
2. **Transformation**:
    * Normalizes JSON structures into tabular formats.
    * Parses breed names from image URLs using regex logic.
3. **Loading**:
    * **`advice_quotes`**: Stores unique pieces of advice with source IDs.
    * **`activities`**: Repurposed for ZenQuotes data (originally designed for Bored API).
    * **`dog_images`**: Stores image URLs and extracted breed names.



## 📈 Analytics & Monitoring
Use `sql/sample_queries.sql` to perform data quality checks:
* Identifying duplicate records.
* Monitoring collection rates per hour/day.
* Validating data integrity (Null checks and price ranges).
