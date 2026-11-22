# Exercise 13 – Understanding Data Processing

## Structured vs unstructured data

| Type | What it looks like | Examples in this repo | How it is processed |
|---|---|---|---|
| **Structured** | Rows and columns with a fixed schema | `titanic.csv`, `sales.csv`, SQL tables | pandas / SQL directly |
| **Semi-structured** | Self-describing keys/tags; records can differ | JSON from an API, XML, MQTT JSON payloads | parse, then flatten (`pd.json_normalize`) |
| **Unstructured** | No predefined schema | `customer_reviews.txt`, images, audio, PDFs | NLP / computer vision / regex to pull out fields |

## The five stages of data processing

1. **Collection** – gather raw data from sources (files, APIs, sensors, databases). Quality here limits everything after it.
2. **Preparation (cleaning)** – remove duplicates, fix types, handle missing values and outliers, standardise formats.
3. **Input** – convert the prepared data into a machine-readable form and load it into the processing system (e.g. a DataFrame or a database), with validation.
4. **Processing** – transform, aggregate, join, run statistics or ML models to turn data into information.
5. **Output & interpretation / storage** – present the results (reports, charts, dashboards, files) and store them for later use and auditing.

`data_processing_basics.py` runs all five stages on `data/sales.csv` and writes `output/monthly_sales.csv`.
