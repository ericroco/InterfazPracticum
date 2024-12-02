import pandas as pd

df = pd.read_csv("DataBases/datos_limpios.csv")

df = df.dropna(subset=["title"])

for column in df.select_dtypes(include=['object']).columns:
    df[column] = df[column].str.replace(r'[^A-Za-z0-9 ]', '', regex=True)

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

for column in df.columns:
    null_count = df[column].isnull().sum()
    total_count = len(df)
    valid_data_count = total_count - null_count

    if df[column].dtype in ['float64', 'int64']:
        zero_count = (df[column] == 0).sum()
        non_zero_count = (df[column] > 0).sum()
        if zero_count > non_zero_count:
            df = df.drop(columns=[column])
            continue

    if df[column].dtype == 'bool':
        false_count = (df[column] == False).sum()
        true_count = (df[column] == True).sum()
        if false_count > true_count:
            df = df.drop(columns=[column])
            continue

    if null_count > valid_data_count:
        df = df.drop(columns=[column])
    else:
        df[column] = df[column].fillna("No Data")

df = df.drop_duplicates(subset="id")

df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x, axis=0)

df = df.fillna("No Data")

df.to_csv("DataBases/movies_clean2.csv", index=False)
