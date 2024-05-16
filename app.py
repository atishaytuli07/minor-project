from flask import Flask, request, jsonify, render_template
import random
import math
from flask import  request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

movie_data = {
    'action': [
        {'name': 'The Dark Knight', 'rating': 9.0},
        {'name': 'Inception', 'rating': 8.8},
        {'name': 'Mad Max: Fury Road', 'rating': 8.1},
        {'name': 'John Wick', 'rating': 7.4},
        {'name': 'Avengers: Infinity War', 'rating': 8.4},
        {'name': 'Mission: Impossible - Fallout', 'rating': 7.7},
        {'name': 'Gladiator', 'rating': 8.5},
        {'name': 'The Matrix', 'rating': 8.7},
        {'name': 'Die Hard', 'rating': 8.2},
        {'name': 'Extraction 2', 'rating': 9.2},
        {'name': 'Animal', 'rating': 8.5},
        {'name': 'Leo (Hindi)', 'rating': 8.7},
        {'name': 'Jawan', 'rating': 6.2},
        {'name': 'Salaar', 'rating': 7.9},
        {'name': 'Mission Majnu', 'rating': 9.0},
        {'name': 'Kill Bill: Vol. 1', 'rating': 8.1}
    ],
    'romantic': [
        {'name': 'The Notebook', 'rating': 7.8},
        {'name': 'Pride & Prejudice', 'rating': 7.8},
        {'name': 'La La Land', 'rating': 8.0},
        {'name': 'Titanic', 'rating': 7.8},
        {'name': 'Before Sunrise', 'rating': 8.1},
        {'name': '500 Days of Summer', 'rating': 7.7},
        {'name': 'Eternal Sunshine of the Spotless Mind', 'rating': 8.3},
        {'name': 'A Walk to Remember', 'rating': 7.4},
        {'name': 'The Fault in Our Stars', 'rating': 7.7},
        {'name': 'Hi Papa', 'rating': 8.2},
        {'name': '365 Days', 'rating': 9.2},
        {'name': 'Lust Stories 2', 'rating': 8.5},
        {'name': 'Anyone About You', 'rating': 8.7},
        {'name': 'Tu Jhooti Mai Makkar', 'rating': 6.2},
        {'name': 'Kushi', 'rating': 7.9},
        {'name': 'Mission Majnu', 'rating': 9.0},
        {'name': 'Casablanca', 'rating': 8.5}
    ],
    'horror': [
        {'name': 'The Shining', 'rating': 8.4},
        {'name': 'Hereditary', 'rating': 7.3},
        {'name': 'Get Out', 'rating': 7.7},
        {'name': 'A Quiet Place', 'rating': 7.5},
        {'name': 'The Conjuring', 'rating': 7.5},
        {'name': 'Paranormal Activity', 'rating': 6.3},
        {'name': 'Psycho', 'rating': 8.5},
        {'name': 'Insidious', 'rating': 6.8},
        {'name': 'It', 'rating': 7.3},
        {'name': 'Shaitaan', 'rating': 8.2},
        {'name': 'Bulbbul', 'rating': 9.2},
        {'name': 'Veronica', 'rating': 8.5},
        {'name': 'Ghost Stories', 'rating': 8.7},
        {'name': 'Sabrina', 'rating': 6.2},
        {'name': 'Stree', 'rating': 7.9},
        {'name': 'Chandramukhi 2', 'rating': 9.0},
        {'name': 'The Exorcist', 'rating': 8.0}
    ],
    'thriller': [
        {'name': "Bodkin (Season 1)", 'rating': 'NA'}, 
        {'name': "The Chestnut Man (Season 2)", 'rating': 'NA'},
        {'name': "Behind Her Eyes (Season 2)", 'rating': 'NA'},
        {'name': "You (Season 4)", 'rating': 8.0},
        {'name': "Mindhunter (Season 3)", 'rating': 'NA'},
        {'name': "The Body (Season 1)", 'rating': 7.5},
        {'name': "The Stranger (Season 2)", 'rating': 6.7},
        {'name': "Clickbait (Miniseries)", 'rating': 7.1},
        {'name': "The Innocent (Season 2)", 'rating': 'NA'},
        {'name': "The OA (Season 3)", 'rating': 'NA'},
        {'name': "Black Mirror (Season 6)", 'rating': 'NA'},
        {'name': "The Society (Season 2)", 'rating': 'NA'},
        {'name': "Locke & Key (Season 3)", 'rating': 'NA'},
        {'name': "The Haunting of Hill House (Season 2)", 'rating': 'NA'},
        {'name': "Ratched (Season 2)", 'rating': 'NA'},
    ],
    'new': [
        {'name': "Carol & the End of the World (Season 1)", 'rating': 8.2},
        {'name': "Dead Boy Detectives (Season 1)", 'rating': 8.8},
        {'name': "Boy Swallows Universe (Season 1)", 'rating': 7.4},
        {'name': "Ripley (Season 1)", 'rating': 'NA'},
        {'name': "The Lincoln Lawyer (Season 1)", 'rating': 7.2},
        {'name': "The Circle (Season 5)", 'rating': 7.8},
        {'name': "Selling Sunset (Season 6)", 'rating': 'NA'},
        {'name': "Too Hot to Handle (Season 4)", 'rating': 'NA'},
        {'name': "Love is Blind (Season 4)", 'rating': 'NA'},
        {'name': "The Ultimatum (Season 2)", 'rating': 'NA'},
        {'name': "Never Have I Ever (Season 4)", 'rating': 'NA'},
        {'name': "Outer Banks (Season 3)", 'rating': 'NA'},
        {'name': "The Umbrella Academy (Season 4)", 'rating': 'NA'},
        {'name': "Stranger Things (Season 5)", 'rating': 'NA'},
        {'name': "The Witcher (Season 4)", 'rating': 'NA'},
    ],
    'trending': [
        {'name': "Heeramandi (Season 1)", 'rating': 'NA'},
        {'name': "Demon Slayer: Kimetsu no Yaiba (Season 3)", 'rating': 9.2},
        {'name': "The Great Indian Kapil Show (Season 4)", 'rating': 8.1},
        {'name': "Khakee: The Bihar Chapter (Season 1)", 'rating': 8.5},
        {'name': "Queen of Tears (Season 1)", 'rating': 'NA'},
        {'name': "Bridgerton (Season 3)", 'rating': 7.9},
        {'name': "The Crown (Season 6)", 'rating': 'NA'},
        {'name': "The Sandman (Season 1)", 'rating': 'NA'},
        {'name': "Cobra Kai (Season 6)", 'rating': 8.3},
        {'name': "The Good Place (Season 4)", 'rating': 8.1},
        {'name': "Dead to Me (Season 4)", 'rating': 'NA'},
        {'name': "Emily in Paris (Season 4)", 'rating': 'NA'},
        {'name': "The Witcher: Blood Origin (Season 1)", 'rating': 'NA'}
    ],
    'comedy': [
        {'name': "Hacks (Season 3)", 'rating': 8.2},
        {'name': "Dead to Me (Season 4)", 'rating': 'NA'}, 
        {'name': "Never Have I Ever (Season 4)", 'rating': 'NA'}, 
        {'name': "Russian Doll (Season 3)", 'rating': 'NA'},
        {'name': "Space Force (Season 3)", 'rating': 'NA'},
        {'name': "Master of None (Season 4)", 'rating': 'NA'},
        {'name': "The Good Place (Season 4)", 'rating': 8.1},
        {'name': "Kim's Convenience (Season 6)", 'rating': 8.6},
        {'name': "The Mindy Project (Season 7)", 'rating': 8.1},
        {'name': "Brooklyn Nine-Nine (Season 8)", 'rating': 8.4},
        {'name': "Schitt's Creek (Season 7)", 'rating': 8.3},
        {'name': "The Office (US) (Season 10)", 'rating': 8.9},
        {'name': "Parks and Recreation (Season 8)", 'rating': 8.6},
        {'name': "Community (Season 7)", 'rating': 8.5},
        {'name': "The IT Crowd (Season 5)", 'rating': 8.4},
    ],
    'kids': [
         {'name': "The Magic School Bus Rides Again (Season 3)", 'rating': 8.1},
         {'name': "Carmen Sandiego (Season 5)", 'rating': 8.4},
         {'name': "The Dragon Prince (Season 5)", 'rating': 8.8},
         {'name': "The Boss Baby: Back in the Business (Season 5)", 'rating': 7.8},
         {'name': "Trollhunters: Tales of Arcadia (Season 3)", 'rating': 8.2},
         {'name': "Alexa & Katie (Season 4)", 'rating': 7.9},
         {'name': "Waffles + Mochi (Season 3)", 'rating': 8.4},
         {'name': "Headspace Guide to Sleep (Season 1)", 'rating': 8.7},
         {'name': "Ada Twist, Scientist (Season 3)", 'rating': 8.2},
         {'name': "Dinotrux (Season 7)", 'rating': 7.5},
         {'name': "The Last Kids on Earth (Season 4)", 'rating': 7.9},
         {'name': "She-Ra and the Princesses of Power (Season 5)", 'rating': 8.7},
         {'name': "Green Eggs and Ham (Season 2)", 'rating': 7.8},
         {'name': "The Mitchells vs. the Machines (Movie)", 'rating': 8.3},
         {'name': "Vivo (Movie)", 'rating': 8.1},
    ],
    'fiction': [
         {'name': "The Witcher (Season 4)", 'rating': 'NA'},  
         {'name': "Stranger Things (Season 5)", 'rating': 'NA'},  
         {'name': "The Umbrella Academy (Season 4)", 'rating': 'NA'}, 
         {'name': "Locke & Key (Season 3)", 'rating': 'NA'},  
         {'name': "The Haunting of Hill House (Season 2)", 'rating': 'NA'},  
         {'name': "The OA (Season 3)", 'rating': 'NA'},  
         {'name': "Shadow and Bone (Season 3)", 'rating': 'NA'},
         {'name': "The Sandman (Season 1)", 'rating': 'NA'},  
         {'name': "The Lincoln Lawyer (Season 1)", 'rating': 7.2}, 
         {'name': "The Society (Season 2)", 'rating': 'NA'}, 
         {'name': "The Crown (Season 6)", 'rating': 'NA'}, 
         {'name': "Bridgerton (Season 3)", 'rating': 7.9},  
         {'name': "The Witcher: Blood Origin (Season 1)", 'rating': 'NA'}, 
         {'name': "Never Have I Ever (Season 4)", 'rating': 'NA'},
         {'name': "Outer Banks (Season 3)", 'rating': 'NA'},
    ],
    'indian': [
        {'name': "Heeramandi (Season 1)", 'rating': 'NA'},  
        {'name': "Khakee: The Bihar Chapter (Season 1)", 'rating': 8.5}, 
        {'name': "Sacred Games (Season 3)", 'rating': 'NA'},
        {'name': "The Family Man (Season 3)", 'rating': 'NA'},
        {'name': "Delhi Crime (Season 3)", 'rating': 'NA'},
        {'name': "Aranyak (Season 2)", 'rating': 'NA'},
        {'name': "She (Season 3)", 'rating': 'NA'},
        {'name': "Criminal Justice (Season 4)", 'rating': 'NA'},
        {'name': "Jamtara - The Great Indian Scam (Season 3)", 'rating': 'NA'},
        {'name': "Misfits (Season 2)", 'rating': 'NA'},
        {'name': "Yeh Ballet (Movie)", 'rating': 8.0},  
        {'name': "Bulbbul (Movie)", 'rating': 9.2}, 
        {'name': "Stree (Movie)", 'rating': 7.9}, 
        {'name': "Sherni (Movie)", 'rating': 'NA'},  
        {'name': "AK vs AK (Movie)", 'rating': 7.6},  
    ],
    'mystery': [
        {'name': "Bodkin (Season 1)", 'rating': 'NA'}, 
        {'name': "The Chestnut Man (Season 2)", 'rating': 'NA'}, 
        {'name': "Behind Her Eyes (Season 2)", 'rating': 'NA'}, 
        {'name': "Clickbait (Miniseries)", 'rating': 7.1}, 
        {'name': "The Innocent (Season 2)", 'rating': 'NA'}, 
        {'name': "Unsolved Mysteries (Volume 3)", 'rating': 7.8},
        {'name': "Murder, Mystery & Mayhem (Season 3)", 'rating': 'NA'},
        {'name': "The Keepers (Season 2)", 'rating': 8.6},  
        {'name': "Making a Murderer (Season 3)", 'rating': 8.4},
        {'name': "The Disappearance of Madeleine McCann (Season 2)", 'rating': 7.8}, 
        {'name': "The Sons of Sam: A Descent into Madness (Miniseries)", 'rating': 8.2},
        {'name': "Night Stalker: The Hunt for a Serial Killer (Miniseries)", 'rating': 8.4}, 
        {'name': "Unsolved Murders (Season 3)", 'rating': 'NA'},
        {'name': "The Imposter (Movie)", 'rating': 8.6}, 
    ],
    'documentary': [
        {"name": "Our Planet (Season 3)", 'rating': 9.1},
        {"name": "Night on Earth (Season 3)", 'rating': 8.8},
        {"name": "Planet Earth (Season 3)", 'rating': 9.5},
        {"name": "Street Food (Volume 4)", 'rating': 8.8},
        {"name": "Formula 1: Drive to Survive (Season 5)", 'rating': 8.3},
        {"name": "The Social Dilemma (Movie)", 'rating': 8.0},
        {"name": "Icarus (Movie)", 'rating': 8.0}, 
        {"name": "My Octopus Teacher (Movie)", 'rating': 9.0}, 
        {"name": "American Murder: The Family Next Door (Miniseries)", 'rating': 8.1},
        {"name": "The Tinder Swindler (Movie)", 'rating': 8.4}, 
        {"name": "Don't Look Up (Movie)", 'rating': 7.3}, 
        {"name": "Seaspiracy (Movie)", 'rating': 8.3},
        {"name": "The Act of Killing (Movie)", 'rating': 8.3},
        {"name": "Amanda Knox (Movie)", 'rating': 7.8},
        {"name": "Winter on Fire: Ukraine's Fight for Freedom (Movie)", 'rating': 8.8},
]


}


@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/page2.html")
def page():
    return render_template("page2.html")

@app.route("/gpt.html")
def gpt():
    return render_template("gpt.html")


@app.route("/suggest_movies", methods=["POST"])
def suggest_movies():
    data = request.json
    genre = data["genre"].lower()
    print("Received genre:", genre)
    if genre in movie_data:
        movies = random.sample(movie_data[genre], k=min(10, len(movie_data[genre])))
        return jsonify({"movies": movies})
    else:
        return jsonify({"error": "Genre not found"})


def prepare_data(x):
        return str.lower(x.replace(" ", ""))

def create_soup(x):
    return x['Genre'] + ' ' + x['Tags'] + ' ' +x['Actors']+' '+ x['ViewerRating']

def get_recommendations(title, cosine_sim):
    global result
    title=title.replace(' ','').lower()
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:51]
    movie_indices = [i[0] for i in sim_scores]
    result =  netflix_data.iloc[movie_indices]
    result.reset_index(inplace = True)
    return result

netflix_data = pd.read_csv('NetflixDataset.csv',encoding='latin-1', index_col = 'Title')
netflix_data.index = netflix_data.index.str.title()
netflix_data = netflix_data[~netflix_data.index.duplicated()]
netflix_data.rename(columns={'View Rating':'ViewerRating'}, inplace=True)
Language = netflix_data.Languages.str.get_dummies(',')
Lang = Language.columns.str.strip().values.tolist()
Lang = set(Lang)
Titles = set(netflix_data.index.to_list())

netflix_data['Genre'] = netflix_data['Genre'].astype('str')
netflix_data['Tags'] = netflix_data['Tags'].astype('str')
netflix_data['IMDb Score'] = netflix_data['IMDb Score'].apply(lambda x: 6.6 if math.isnan(x) else x)
netflix_data['Actors'] = netflix_data['Actors'].astype('str')
netflix_data['ViewerRating'] = netflix_data['ViewerRating'].astype('str')
new_features = ['Genre', 'Tags', 'Actors', 'ViewerRating']
selected_data = netflix_data[new_features]
for new_feature in new_features:
    selected_data.loc[:, new_feature] = selected_data.loc[:, new_feature].apply(prepare_data)
selected_data.index = selected_data.index.str.lower()
selected_data.index = selected_data.index.str.replace(" ",'')
selected_data['soup'] = selected_data.apply(create_soup, axis = 1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(selected_data['soup'])
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
selected_data.reset_index(inplace = True)
indices = pd.Series(selected_data.index, index=selected_data['Title'])
result = 0
df = pd.DataFrame()


@app.route('/indexa.html')
def indexa():
    return render_template('indexa.html', languages = Lang, titles = Titles) 

@app.route('/about',methods=['POST'])
def getvalue():
    global df
    movienames = request.form.getlist('titles')
    languages = request.form.getlist('languages')
    for moviename in movienames:
        get_recommendations(moviename,cosine_sim2)
        for language in languages:
            df = pd.concat([result[result['Languages'].str.count(language) > 0], df], ignore_index=True)
    df.drop_duplicates(keep = 'first', inplace = True)
    df.sort_values(by = 'IMDb Score', ascending = False, inplace = True)
    images = df['Image'].tolist()
    titles = df['Title'].tolist()
    return render_template('result.html',  titles =  titles, images = images)

@app.route('/moviepage/<name>')
def movie_details(name):
    global df
    details_list = df[df['Title'] == name].to_numpy().tolist()
    return render_template('moviepage.html', details = details_list[0])


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
