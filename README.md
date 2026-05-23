# names-details-project

A data engineering ETL pipeline that processes US baby name data from raw `.txt` files and loads them into a relational PostgreSQL database hosted on Supabase.

---

## Overview

This project reads yearly baby name files (e.g. `yob2014.txt`), cleans and transforms the data, and loads it into two relational tables — `names` and `details` — using a batch processing pipeline.

---

## Project Structure

```
names-details-project/
│
├── main.py                  # Pipeline entry point
├── database.py              # Supabase/Postgres connection
├── __init__.py
│
├── data/
│   └── raw/                 # Raw yob*.txt files go here
│
├── pipelines/
│   ├── __init__.py
│   ├── extract.py           # Reads and parses raw .txt files
│   ├── transform.py         # Cleans and shapes data
│   └── load.py              # Inserts data into Postgres
│
├── models/
│   └── schema.sql           # Database schema reference
│
├── utils/
│   ├── __init__.py
│   └── logger.py            # Centralized logging setup
│
├── testing/
│   ├── __init__.py
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
│
├── logs/                    # Pipeline run logs (auto-generated)
├── .env                     # Environment variables (not committed)
├── .gitignore
└── requirements.txt
```

---

## Database Schema

Two relational tables hosted on Supabase:

**`names`** — unique name and gender combinations

| Column | Type | Notes |
|---|---|---|
| name_id | UUID | Primary key, auto-generated |
| name | VARCHAR(100) | Capitalized |
| gender | CHAR(1) | `M` or `F` only |
| created_at | TIMESTAMPTZ | Set on insert |

**`details`** — yearly count per name

| Column | Type | Notes |
|---|---|---|
| detail_id | UUID | Primary key, auto-generated |
| name_id | UUID | Foreign key → `names.name_id` |
| year | SMALLINT | Extracted from filename |
| count | INT | Number of births |
| created_at | TIMESTAMPTZ | Set on insert |
| updated_at | TIMESTAMPTZ | Updated on conflict |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/hrrtjaymee/names-details-project.git
cd names-details-project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
DB_HOST=db.xxxxxxxxxxxx.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_PORT=5432
```

You can find these values in your Supabase project under **Settings → Database → Connection parameters**.

### 5. Add raw data files

Place your `yob*.txt` files in `data/raw/`:

```
data/
└── raw/
    ├── yob2010.txt
    ├── yob2011.txt
    └── ...
```

Each file should be comma-delimited with the format:
```
Emma,F,18000
Liam,M,17000
```

Files with or without headers are both supported.

---

## Running the Pipeline

```bash
python -m main
```

The pipeline will:
1. Connect to the Supabase database
2. Scan `data/raw/` for all `yob*.txt` files
3. Extract, clean, and transform each file in batches
4. Load names and details into the database
5. Log progress to the console and `logs/` folder

---

## Running Tests

```bash
python -m pytest testing/ -v
```

---

## Requirements

```
psycopg2-binary
python-dotenv
pandas
pytest
```

---

## Notes

- The `data/` and `logs/` folders are excluded from version control via `.gitignore`
- All credentials must be stored in `.env` — never commit this file
- Logs are saved per pipeline run with a timestamp in the filename
