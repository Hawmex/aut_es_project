import os
import requests
import pandas as pd

from typing import Any, Dict
from dotenv import load_dotenv

from core.inference_engine import InferenceEngine
from core.utils import print_headline
from rulebase import rulebase
from utils import map_phrases

load_dotenv()

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.environ.get("TMDB_TOKEN")}",
}


def get_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list"
    response = requests.get(url, headers=HEADERS)

    return dict(
        map(
            lambda value: (value["name"], value["id"]),
            response.json()["genres"],
        )
    )


def get_keyword_id(keyword: str):
    url = "https://api.themoviedb.org/3/search/keyword"
    response = requests.get(url, {"query": keyword}, headers=HEADERS)
    results = response.json()["results"]

    if not results:
        return None

    return results[0]["id"]


def refine_query(query: Dict[str, Any]):
    query = query.copy()
    genres = get_genres()

    if "with_genres" in query:
        query["with_genres"] = map_phrases(
            query["with_genres"], lambda phrase: str(genres[phrase])
        )

    if "with_keywords" in query:
        query["with_keywords"] = map_phrases(
            query["with_keywords"], lambda phrase: str(get_keyword_id(phrase))
        )

    return query


def get_movies(query: Dict[str, Any]):
    url = "https://api.themoviedb.org/3/discover/movie"
    response = requests.get(url, query, headers=HEADERS)

    return response.json()["results"]


def main():
    engine = InferenceEngine(rulebase)
    query = engine.infer("backward")

    if query is None:
        return

    print_headline("Resulted Search Query")
    print(pd.DataFrame([query]).T)

    query = refine_query(query)

    print_headline("Refined Search Query")
    print(pd.DataFrame([query]).T)

    movies = get_movies(query)

    print_headline("Recommended Movies")

    print(
        pd.DataFrame(
            movies,
            columns=["title", "release_date", "vote_average", "vote_count"],
        ),
    )


if __name__ == "__main__":
    main()
