#################### Imports and SetUp ####################
import requests
import json
import csv
import time

import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

YEAR = None

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

#################### Get All IDs of TMDB ####################
def __get_ids_on_page(movies):
    ids = []
    for movie in movies:
        ids.append(movie["id"])
    return ids

def get_ids_tmdb(year):
    url = "https://api.themoviedb.org/3/discover/movie"
    args= {"api_key": "cd3eec7022f7ec26a0edf1ea2073f10a", "primary_release_year": str(year), "page": "1"}

    response = requests.get(url, args)
    page = response.json()
    nb_pages = page["total_pages"]
    ids = __get_ids_on_page(page["results"])

    
    time.sleep(11)
    for i in range(1, nb_pages):
        if(i % 40 == 0):
            time.sleep(11)
        args["page"] = str(i + 1)
        response = requests.get(url, args)
        page = response.json()
        ids += __get_ids_on_page(page["results"])
    return ids

#################### Get All Movies on TMDB and OMDB ####################
def __is_movie_tmdb_valid(movie_tmdb):
    return movie_tmdb["release_date"] != "" and movie_tmdb["runtime"] != 0 and movie_tmdb["runtime"] != None and movie_tmdb["title"] != "" and movie_tmdb["budget"] != 0

def __is_movie_omdb_valid(movie_omdb):
    return movie_omdb.get("Response") == "True" and movie_omdb["Rated"] != "N/A" and movie_omdb["Metascore"] != "N/A" and movie_omdb["imdbRating"] != "N/A"

def get_movies(ids_tmdb):
    url_tmdb = "https://api.themoviedb.org/3/movie/"
    args_tmdb = {"api_key": "cd3eec7022f7ec26a0edf1ea2073f10a"}

    url_omdb = "http://www.omdbapi.com/"
    args_omdb = {"i": ""}

    movies = []

    for i in range(len(ids_tmdb)):
        eprint(i) #DEBUG
        if i % 40 == 0:
            time.sleep(10)
        response = requests.get(url_tmdb + str(ids_tmdb[i]), args_tmdb)
        if response.status_code == 404: continue
        movie_tmdb = response.json()
        if __is_movie_tmdb_valid(movie_tmdb):
            args_omdb["i"] = movie_tmdb["imdb_id"]
            time.sleep(0.05)
            response = requests.get(url_omdb, args_omdb)
            try:
                movie_omdb = response.json()
            except Exception as e:
                eprint(response) #DEBUG
                eprint(e) #DEBUG
            if __is_movie_omdb_valid(movie_omdb):
                movies.append({"budget": movie_tmdb["budget"], "release_date": movie_tmdb["release_date"], "runtime": movie_tmdb["runtime"], "title": movie_tmdb["title"], "rated": movie_omdb["Rated"], "genre": movie_omdb["Genre"], "director": movie_omdb["Director"], "awards": movie_omdb["Awards"], "metascore": movie_omdb["Metascore"], "imdb_rating": movie_omdb["imdbRating"]})
    return movies

#################### Print Movies in CSV ####################
def print_movies_csv(movies, fieldnames):
    outfile = open("data.csv", "w", encoding="utf8", newline="")

    writer = csv.DictWriter(outfile, fieldnames, delimiter=";")
    writer.writeheader()

    for film in movies:
        writer.writerow(film)

    outfile.close()

#################### Write JSON in Text File ####################
def save_file(file_name, obj):
    outfile = open(file_name, "w", encoding="utf8")
    json.dump(obj, outfile)
    outfile.close()

#################### Load JSON from Text File ####################
def load_file(file_name):
    infile = open(file_name, "r", encoding="utf8")
    obj = json.load(infile)
    infile.close()
    return obj