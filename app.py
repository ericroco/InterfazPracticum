from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

ratings_file = 'ratings.csv'

def calculate_average_ratings():

    ratings_df = pd.read_csv(ratings_file)
    
    average_ratings = ratings_df.groupby('movie_id')['rating_value'].mean().reset_index()
    
    movies_df = pd.read_csv('movies_clean_updated.csv')
    
    movies_df = movies_df.merge(average_ratings, how='left', left_on='id', right_on='movie_id')

    movies_df['ratings'] = movies_df['rating_value']
    
    movies_df = movies_df.drop(columns=['rating_value', 'movie_id_x', 'movie_id_y', 'movie_id'], errors='ignore')
    
    movies_df.to_csv('movies_clean_updated.csv', index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_rating', methods=['POST'])
def add_rating():
    movie_id = request.form['movie_id']
    user_id = request.form['user_id']
    rating_value = request.form['rating_value']
    
    new_rating = pd.DataFrame({
        'movie_id': [movie_id],
        'user_id': [user_id],
        'rating_value': [rating_value],
        'timestamp': [pd.Timestamp.now()]
    })
    
    try:
        ratings_df = pd.read_csv(ratings_file)
        ratings_df = pd.concat([ratings_df, new_rating], ignore_index=True)
    except FileNotFoundError:
        ratings_df = new_rating
    

    ratings_df.to_csv(ratings_file, index=False)
    

    calculate_average_ratings()

    return jsonify({'status': 'Rating agregado y base de datos actualizada correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
