import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import inflect

# Function to get film data from TSV (tab-seperated values) dataset file
def get_data():
    # Read from file
    film_data = pd.read_csv("cleaned-movies-dataset.tsv", sep="\t")
    # Drop unneeded columns
    film_data = film_data.drop(columns=["runtimeMinutes", "director_name", "numVotes"])
    # select range due to computing limitations
    return film_data[30000:30010]

# #Function to calculate the cosine similarities by first creating a matrix of values for frequency of
# genres (bag of words) and then calcuating the cosine similarities between genres for each film
def calc_data(film_data):
    film_data = film_data.drop(columns = ["tconst"])
    p = inflect.engine()
    film_data["averageRating"] = film_data["averageRating"].apply(lambda x: p.number_to_words(int(x)))
    film_data["merged"] = film_data[film_data.columns[0:3]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
    film_data = film_data.drop(columns = ["genres", "averageRating", "primaryTitle"])

    merged = film_data["merged"]
    count = CountVectorizer()
    count_matrix = count.fit_transform(merged)
    print(count_matrix)
    sparse_matrix = count_matrix.toarray()
    print(sparse_matrix)
    calc_cosines = cosine_similarity(sparse_matrix, sparse_matrix)
    return calc_cosines

# Function that takes inputs and produces top 24 recommendations based on cosine similarity for that film
def rec_films(film_title, film_data, cosine_sims):
    # Get indices for films taking into consideration for range selected
    array_indices = pd.Series(film_data.index - 30000, index = film_data["primaryTitle"])
    # get index for chosen film
    array_index = array_indices[film_title]
    
    # get cosine similarities for chosen film
    similarities = list(enumerate(cosine_sims[array_index]))
    # sort from most similar to least
    similarities = sorted(similarities, key = lambda x: x[1], reverse = True)
    # get top 24 excluding first since most similar film will be itself
    top_24 = similarities[1:25]

    # get data that we want to return
    film_indices = [i[0] for i in top_24]
    film_id = film_data["tconst"].iloc[film_indices]
    film_title = film_data["primaryTitle"].iloc[film_indices]

    # store data we want to return in a dataframe
    rec_data = pd.DataFrame(columns = ["imdb_id", "title"])
    rec_data["imdb_id"] = film_id
    rec_data["title"] = film_title

    return rec_data


film_data = get_data()
cosine_sims = calc_data(film_data)

def get_recs(selected_title):
    recommendations = rec_films(selected_title, film_data, cosine_sims)
    return recommendations
print(cosine_sims)