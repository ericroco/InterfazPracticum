import pandas as pd
df = pd.read_csv("DataBases/movies_clean3.csv") 

genre_pairs = []

if 'genres' in df.columns:
    for genres in df['genres']:
        if pd.notna(genres):
            for genre in genres.split("id"):
                genre = genre.strip()
                if genre:
                    parts = genre.split("name")
                    if len(parts) == 2:
                        genre_id = parts[0].strip() 
                        genre_name = parts[1].strip()
                        genre_pairs.append((genre_id, genre_name))
    genre_df = pd.DataFrame(genre_pairs, columns=["genre_id", "genre_name"]).drop_duplicates()


    genre_df.to_csv("TablasAdicionales/genres_table.csv", index=False)
    df['genres'] = df['genres'].apply(lambda x: ",".join([g.split("name")[0].strip() for g in x.split("id") if "name" in g]) if pd.notna(x) else x)

company_pairs = []

if 'production_companies' in df.columns:
    for companies in df['production_companies']:
        if pd.notna(companies):
            parts = companies.split("name")
            for part in parts[1:]:
                part = part.strip()
                if "id" in part:
                    name_part, id_part = part.split("id", 1)
                    company_name = name_part.strip()
                    company_id = id_part.strip()
                    company_pairs.append((company_id, company_name))

    company_df = pd.DataFrame(company_pairs, columns=["company_id", "company_name"]).drop_duplicates()

    company_df.to_csv("TablasAdicionales/production_companies_table.csv", index=False)

    def extract_ids(companies):
        if pd.notna(companies):
            ids = []
            parts = companies.split("name")
            for part in parts[1:]:
                part = part.strip()
                if "id" in part:
                    id_part = part.split("id", 1)[1].strip()
                    ids.append(id_part)
            return ",".join(ids)
        return companies

    df['production_companies'] = df['production_companies'].apply(extract_ids)

country_pairs = []

if 'production_countries' in df.columns:
    for countries in df['production_countries']:
        if pd.notna(countries):
            for countries in countries.split("iso31661"):
                countries = countries.strip()
                if countries:
                    parts = countries.split("name")
                    if len(parts) == 2:
                        iso31661 = parts[0].strip() 
                        country_name = parts[1].strip()
                        country_pairs.append((iso31661, country_name))
    countries_df = pd.DataFrame(country_pairs, columns=["iso31661", "country_name"]).drop_duplicates()


    countries_df.to_csv("TablasAdicionales/countries_table.csv", index=False)
    df['production_countries'] = df['production_countries'].apply(lambda x: ",".join([g.split("name")[0].strip() for g in x.split("id") if "name" in g]) if pd.notna(x) else x)

import pandas as pd

languages_pairs = []

if 'spoken_languages' in df.columns:
    for languages in df['spoken_languages']:
        if pd.notna(languages):  
            parts = languages.split("iso6391")
            for part in parts[1:]:
                part = part.strip()
                if "name" in part:
                    iso_part, name_part = part.split("name", 1)
                    iso_code = iso_part.strip()
                    language_name = name_part.strip()
                    languages_pairs.append((iso_code, language_name))

    languages_df = pd.DataFrame(languages_pairs, columns=["iso6391", "language_name"]).drop_duplicates()

    languages_df.to_csv("TablasAdicionales/languages_table.csv", index=False)

    def extract_iso_codes(languages):
        if pd.notna(languages):
            iso_codes = []
            parts = languages.split("iso6391")
            for part in parts[1:]:
                part = part.strip()
                if "name" in part:
                    iso_code = part.split("name", 1)[0].strip()
                    iso_codes.append(iso_code)
            return ",".join(iso_codes)
        return languages

    df['spoken_languages'] = df['spoken_languages'].apply(extract_iso_codes)


keyWords_pairs = []

if 'keywords' in df.columns:
    for keywords in df['keywords']:
        if pd.notna(keywords):
            for keyword in keywords.split("id"):
                keyword = keyword.strip()
                if keyword:
                    parts = keyword.split("name")
                    if len(parts) == 2:
                        keyword_id = parts[0].strip() 
                        keyword_name = parts[1].strip()
                        keyWords_pairs.append((keyword_id, keyword_name))
    keywords_df = pd.DataFrame(keyWords_pairs, columns=["keyword_id", "keyword_name"]).drop_duplicates()


    keywords_df.to_csv("TablasAdicionales/keywords_table.csv", index=False)
    df['keywords'] = df['keywords'].apply(lambda x: ",".join([g.split("name")[0].strip() for g in x.split("id") if "name" in g]) if pd.notna(x) else x)

castInfo = []

if 'cast' in df.columns and 'id' in df.columns:
    for members, movie_id in zip(df['cast'], df['id']):
        if pd.notna(members):
            for member in members.split("castid"):
                member = member.strip()
                if member:
                    parts = member.split("character")
                    if len(parts) == 2:
                        member_id = parts[0].strip()
                        member_name_and_creditid = parts[1].strip()
                        if "creditid" in member_name_and_creditid:
                            name_parts = member_name_and_creditid.split("creditid")
                            member_name = name_parts[0].strip()
                            credit_id = name_parts[1].strip()
                        if 'gender' in credit_id:
                            parts2 = credit_id.split("gender")
                            credit_id = parts2[0].strip()
                            gender = parts2[1].strip()
                        if "id" in gender:
                            parts3 = gender.split("id")
                            gender = parts3[0].strip()
                            id = parts3[1].strip()
                        if 'name' in id:
                            parts4 = id.split('name')
                            id = parts4[0].strip()
                            name = parts4[1].strip()
                        if 'order' in name:
                            parts5 = name.split("order")
                            name = parts5[0].strip()
                            order = parts5[1].strip()
                        if 'profilepath' in order:
                            parts6 = order.split("profilepath")
                            order = parts6[0].strip()
                            profilepath = parts6[1].strip()
                        else:
                            profilepath = None
                        
                        castInfo.append((movie_id, member_id, member_name, credit_id, gender, id, name, order, profilepath))

members_df = pd.DataFrame(
    castInfo,
    columns=["movie_id", "cast_id", "character_name", "credit_id", "gender", "id", "name", "order", "profilepath"]
)

df['cast'] = df['id']

members_df.to_csv("TablasAdicionales/cast_Info.csv", index=False)

crewInfo = []

if 'crew' in df.columns and 'id' in df.columns:
    for roles, movie_id in zip(df['crew'], df['id']):
        if pd.notna(roles):
            for role in roles.split("creditid"):
                role = role.strip()
                if role:
                    parts = role.split("department")
                    if len(parts) == 2:
                        crewcastid = parts[0].strip()
                        remaining = parts[1].strip()
                        
                        if "gender" in remaining:
                            parts2 = remaining.split("gender")
                            department = parts2[0].strip()
                            remaining = parts2[1].strip()
                        
                        if "id" in remaining:
                            parts3 = remaining.split("id")
                            gender = parts3[0].strip()
                            remaining = parts3[1].strip()
                        
                        if "job" in remaining:
                            parts4 = remaining.split("job")
                            id = parts4[0].strip()
                            remaining = parts4[1].strip()
                        
                        if "name" in remaining:
                            parts5 = remaining.split("name")
                            job = parts5[0].strip()
                            remaining = parts5[1].strip()
                        
                        if "profilepath" in remaining:
                            parts6 = remaining.split("profilepath")
                            name = parts6[0].strip()
                            profilepath = parts6[1].strip()
                        else:
                            profilepath = None

                        crewInfo.append((movie_id, crewcastid, department, gender, id, job, name, profilepath))

crew_df = pd.DataFrame(
    crewInfo,
    columns=["movie_id", "castid", "department", "gender", "id", "job", "name", "profilepath"]
)

df['crew'] = df['id']

crew_df.to_csv("TablasAdicionales/crew_Info.csv", index=False)

ratingsInfo = []

if 'ratings' in df.columns and 'id' in df.columns:
    for ratings, movie_id in zip(df['ratings'], df['id']):
        if pd.notna(ratings):
            for rating in ratings.split("userId"):
                rating = rating.strip()
                if rating:
                    parts = rating.split("rating")
                    if len(parts) == 2:
                        userId = parts[0].strip()
                        rating_value = parts[1].strip()
                    if 'timestamp' in rating_value:
                        parts2 = rating_value.split("timestamp")
                        rating_value = parts2[0].strip()
                        timestamp = parts2[1].strip()
                        ratingsInfo.append((movie_id, userId, rating_value, timestamp))

ratings_df = pd.DataFrame(ratingsInfo, columns=["movie_id", "user_id", "rating_value", "timestamp"])

ratings_df.to_csv("TablasAdicionales/ratings.csv", index=False)

ratings_df['rating_value'] = pd.to_numeric(ratings_df['rating_value'], errors='coerce')

average_ratings = ratings_df.groupby('movie_id')['rating_value'].mean().reset_index()

average_ratings.rename(columns={'movie_id': 'id'}, inplace=True)

df = df.merge(average_ratings, how='left', on='id')

df['ratings'] = df['rating_value']

df.drop(columns=['rating_value'], inplace=True)

df.to_csv("DataBases/movies_clean_updatedV2.csv", index=False)