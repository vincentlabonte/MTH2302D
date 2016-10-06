import scripts
import time

FIELD_NAMES = ["title", "release_date", "budget", "runtime", "rated", "genre", "director", "awards", "metascore", "imdb_rating"]

def save_ids_tmdb(year):
    ids_tmdb = scripts.get_ids_tmdb(year)
    scripts.save_file("./ids_tmdb/ids_tmdb_" + str(year) + ".json", ids_tmdb)

def save_movies_json(year):
    ids_tmdb = scripts.load_file("./ids_tmdb/ids_tmdb_" + str(year) + ".json")
    movies = scripts.get_movies(ids_tmdb)
    scripts.save_file("./movies/movies_" + str(year) + ".json", movies)

def save_movies_csv(start_year, end_year):
    movies = []
    for i in range(start_year, end_year + 1):
        movies += scripts.load_file("./movies/movies_" + str(i) + ".json")
    
    scripts.print_movies_csv(movies, FIELD_NAMES)

if __name__ == "__main__":
    start_time = time.time()

    start_year = 2000
    end_year = 2016
    #for year in range(start_year, end_year + 1):
        #scripts.eprint("---------- Début ids {0} ----------".format(year))
        #save_ids_tmdb(year)
        #scripts.eprint("---------- Fin ids {0} ----------".format(year))
        #scripts.eprint("---------- Début movies {0} ----------".format(year))
        #save_movies_json(year)
        #scripts.eprint("---------- Fin movies {0} ----------".format(year))
    scripts.eprint("---------- Début sauvegarde  ----------")
    save_movies_csv(start_year, end_year)
    scripts.eprint("---------- Fin sauvegarde  ----------")

    time_span = int(time.time() - start_time)
    print("DONE! {0}h {1}m {2}s".format(time_span // 3600, (time_span // 60) % 60, time_span % 60))