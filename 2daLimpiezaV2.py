import pandas as pd

df = pd.read_csv("DataBases/datos_limpios.csv")

df = df.dropna(subset=["title"])

for column in df.select_dtypes(include=['object']).columns:
    df[column] = df[column].str.replace(r'[^A-Za-z0-9 ]', '', regex=True)

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

df = df.drop_duplicates(subset="id")

df = df.fillna("No Data")

df.to_csv("DataBases/movies_clean3.csv", index=False)