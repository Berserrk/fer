# inspect_db.py
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

# 1) Make sure you have these installed in your env:
#    pip install duckdb pandas matplotlib

# 2) Connect to your DuckDB file
conn = duckdb.connect('articles_metadata.duckdb')

# 3) Load tables into pandas
df_articles     = conn.execute('SELECT * FROM articles').df()
df_entities     = conn.execute('SELECT * FROM entities').df()
df_descriptions = conn.execute('SELECT * FROM descriptions').df()

# 4) Quick peek
print("=== ARTICLES ===")
print(df_articles.head(), "\n")
print("=== ENTITIES ===")
print(df_entities.head(), "\n")
print("=== DESCRIPTIONS ===")
print(df_descriptions.head(), "\n")

# 5) Compute how many entities each article has
entity_counts = (
    df_entities
    .groupby('article_hash')
    .size()
    .reset_index(name='entity_count')
)
print("=== ENTITY COUNTS ===")
print(entity_counts.sort_values('entity_count', ascending=False).head(), "\n")

# 6) Bar‐plot: top 10 articles by entity count
top10 = entity_counts.nlargest(10, 'entity_count')
fig, ax = plt.subplots()
ax.bar(top10['article_hash'], top10['entity_count'])
ax.set_xlabel('Article Hash')
ax.set_ylabel('Number of Entities')
ax.set_title('Top 10 Articles by Entity Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()