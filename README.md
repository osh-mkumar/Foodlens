# 🍽️ FoodLens — Mumbai Food Intelligence

A small data engineering project where I took a messy Zomato dataset and turned it into something actually usable.

Live app: https://your-streamlit-link.streamlit.app



## Why I Built This

Most public datasets look clean until you try to use them.

This one wasn’t:

* Broken delimiters
* Quoted fields everywhere
* Multi-valued columns (cuisines)
* Missing ratings and prices

Instead of doing surface-level analysis, I wanted to treat it like real production data and build a proper pipeline.


## What This Project Does

* Cleans and standardizes raw restaurant data
* Normalizes it into a relational schema
* Preserves messy real-world edge cases (instead of dropping them)
* Exposes insights through an interactive dashboard



## Pipeline (How Data Flows)

Raw CSV
→ parsed with custom handling (bad rows, broken quotes)
→ cleaned with pandas
→ normalized into multiple tables
→ loaded into PostgreSQL
→ queried and visualized with Streamlit



## Data Model (Simplified)

* **restaurants** → core info (name, price, region, rating, votes)
* **cuisines** → unique cuisine types
* **restaurant_cuisines** → mapping table (because one restaurant can have many cuisines)

The key decision here was splitting cuisines properly instead of keeping them as a comma-separated column.



## Interesting Things I Noticed

* A large chunk of restaurants have no ratings at all — ignoring them would bias results
* Some places have high votes but low ratings (overhyped spots)
* Cuisine distribution is heavily skewed toward a few categories

---

## Features (Dashboard)

* Filter by rating, price, cuisine, and region
* Search for specific restaurants
* Explore top cuisines interactively
* Identify best value and overhyped places



## Tech Used

* Python (pandas)
* PostgreSQL
* SQL
* Streamlit
* Plotly



## Running It Locally

```bash
pip install -r requirements.txt
streamlit run app/foodlens_app.py
```



## What I’d Improve Next

* Replace CSV ingestion with API-based data
* Add scheduled pipeline (Airflow / cron)
* Move database to cloud (Neon/Supabase)
* Build a proper frontend (React instead of Streamlit)



## Final Thought

This project is less about “analyzing food data” and more about
handling messy data the way it actually shows up in real systems.



## Author

Osh Manoj Kumar
