import pandas as pd
import numpy as np

# 1: Load the dataset
df = pd.read_csv('RawData/raw_titles.csv')

# 2: Drop unnecessary columns
df.drop(columns=['index', 'imdb_id'], inplace=True, errors='ignore')

# 3: Drop rows with nulls/missing or invalid values
df.dropna(subset=['title', 'imdb_score', 'imdb_votes'], inplace=True)
df = df[df['runtime'] > 0]

# 4: Fill missing values
df['seasons'] = df['seasons'].fillna(0)
df['age_certification'] = df['age_certification'].fillna('Others')
df['genres'] = df['genres'].replace('[]', 'N/A').fillna('N/A')
df['production_countries'] = df['production_countries'].replace('[]', 'N/A').fillna('N/A')

# 5: Normalize strings (capitalization & trim)
for col in ['type', 'title', 'genres']:
    df[col] = df[col].astype(str).str.title().str.strip()

# 6: Clean genre and country columns
def clean_bracketed_string(s):
    s = str(s)
    if s.startswith('[') and s.endswith(']'):
        s = s[1:-1]
    return s.replace("'", "").strip()

df['genre'] = df['genres'].apply(clean_bracketed_string)
df['country'] = df['production_countries'].apply(clean_bracketed_string)

# Replace known issue
df['country'] = df['country'].replace({'Lebanon': 'LB'})
df['genre'] = df['genre'].replace('/', 'N/A')
df['country'] = df['country'].replace('/', 'N/A')

# title fix
df['title'] = df['title'].replace('30 March', '30.March')
df['title'] = df['title'].str.lstrip('#')

# Drop old raw columns after extraction
df.drop(columns=['genres', 'production_countries'], inplace=True)

#  7: Export cleaned DataFrame
df.to_csv('titles_cleaned.csv', index=False)

print(" Data cleaned and saved: 'titles_cleaned.csv'")
