from core.rulebase import *


rulebase = Rulebase(
    "rulebase.txt",
    # MOOD + GENRE COMBINATIONS
    # 1 - Happy + Comedy: Focus on feel-good comedies
    Rule(
        LogicalAnd(
            Evaluation("user_mood", "==", "Happy"),
            Evaluation("favorite_genre", "==", "Comedy"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Comedy"),
            Assignment("with_keywords", "feel-good|buddy comedy"),
            Assignment("vote_average.gte", "6.5"),
        ),
    ),
    # 2 - Happy + Lighthearted vibe: Popular family-friendly content
    Rule(
        LogicalAnd(
            Evaluation("user_mood", "==", "Happy"),
            Evaluation("movie_vibe", "==", "Lighthearted"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Comedy|Family|Romance"),
            Assignment("vote_average.gte", "6.0"),
            Assignment("sort_by", "popularity.desc"),
        ),
    ),
    # 3 - Sad + Drama: Emotional, cathartic dramas
    Rule(
        LogicalAnd(
            Evaluation("user_mood", "==", "Sad"),
            Evaluation("favorite_genre", "==", "Drama"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Drama"),
            Assignment("with_keywords", "tearjerker|emotional|loss"),
            Assignment("vote_average.gte", "7.0"),
        ),
    ),
    # 4 - Sad + Cathartic vibe: High-quality emotional content
    Rule(
        LogicalAnd(
            Evaluation("user_mood", "==", "Sad"),
            Evaluation("movie_vibe", "==", "Cathartic"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Drama"),
            Assignment("vote_average.gte", "7.5"),
            Assignment("sort_by", "vote_average.desc"),
        ),
    ),
    # 5 - Adventurous + Action: Popular action adventures
    Rule(
        LogicalAnd(
            Evaluation("user_mood", "==", "Adventurous"),
            Evaluation("favorite_genre", "==", "Action"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Action|Adventure"),
            Assignment("vote_average.gte", "6.5"),
            Assignment("sort_by", "popularity.desc"),
        ),
    ),
    # 6 - Adventurous + Epic Journey: Quest-based adventures
    Rule(
        LogicalAnd(
            Evaluation("user_mood", "==", "Adventurous"),
            Evaluation("movie_vibe", "==", "Epic Journey"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Adventure|Fantasy"),
            Assignment("with_keywords", "quest|journey|epic"),
            Assignment("vote_average.gte", "7.0"),
        ),
    ),
    # 7 - Horror mood + Horror genre: Quality horror films
    Rule(
        LogicalAnd(
            Evaluation("user_mood", "==", "In the mood for a scare"),
            Evaluation("favorite_genre", "==", "Horror"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Horror"),
            Assignment("vote_average.gte", "6.5"),
            Assignment("sort_by", "vote_average.desc"),
        ),
    ),
    # 8 - Intellectual mood: Sci-fi or documentaries
    Rule(
        LogicalAnd(
            Evaluation("user_mood", "==", "Intellectual"),
            LogicalOr(
                Evaluation("favorite_genre", "==", "Science Fiction"),
                Evaluation("favorite_genre", "==", "Documentary"),
            ),
        ),
        LogicalOr(
            LogicalAnd(
                Assignment("with_genres", "Science Fiction"),
                Assignment("vote_average.gte", "7.0"),
                Assignment("sort_by", "vote_average.desc"),
            ),
            LogicalAnd(
                Assignment("with_genres", "Documentary"),
                Assignment("vote_average.gte", "7.5"),
                Assignment("sort_by", "vote_average.desc"),
            ),
        ),
    ),
    # GENRE + VIBE COMBINATIONS
    # 9 - Sci-fi + Dystopian: Dark future themes
    Rule(
        LogicalAnd(
            Evaluation("favorite_genre", "==", "Science Fiction"),
            Evaluation("movie_vibe", "==", "Dystopian"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Science Fiction"),
            Assignment("with_keywords", "dystopian|dystopia|dark future"),
            Assignment("vote_average.gte", "6.5"),
        ),
    ),
    # 10 - Action + Heist: Crime action films
    Rule(
        LogicalAnd(
            Evaluation("favorite_genre", "==", "Action"),
            Evaluation("movie_vibe", "==", "Heist"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Action|Crime"),
            Assignment("with_keywords", "heist|robbery|bank robbery"),
            Assignment("vote_average.gte", "6.5"),
        ),
    ),
    # ERA-BASED RULES
    # 11 - Golden Age (1940s-1960s): Classic cinema
    Rule(
        Evaluation("movie_era", "==", "Golden Age"),
        LogicalAnd(
            Assignment("primary_release_date.gte", "1940-01-01"),
            Assignment("primary_release_date.lte", "1969-12-31"),
            Assignment("vote_average.gte", "7.0"),
            Assignment("sort_by", "vote_average.desc"),
        ),
    ),
    # 12 - 1970s: Full decade coverage
    Rule(
        Evaluation("movie_era", "==", "70s"),
        LogicalAnd(
            Assignment("primary_release_date.gte", "1970-01-01"),
            Assignment("primary_release_date.lte", "1979-12-31"),
            Assignment("vote_average.gte", "6.5"),
            Assignment("sort_by", "vote_average.desc"),
        ),
    ),
    # 13 - 1980s: Popular 80s films
    Rule(
        Evaluation("movie_era", "==", "80s"),
        LogicalAnd(
            Assignment("primary_release_date.gte", "1980-01-01"),
            Assignment("primary_release_date.lte", "1989-12-31"),
            Assignment("vote_average.gte", "6.0"),
            Assignment("sort_by", "popularity.desc"),
        ),
    ),
    # 14 - 1990s: Full decade coverage
    Rule(
        Evaluation("movie_era", "==", "90s"),
        LogicalAnd(
            Assignment("primary_release_date.gte", "1990-01-01"),
            Assignment("primary_release_date.lte", "1999-12-31"),
            Assignment("vote_average.gte", "6.0"),
            Assignment("sort_by", "popularity.desc"),
        ),
    ),
    # 15 - 2000s: Action and thrillers from the decade
    Rule(
        Evaluation("movie_era", "==", "2000s"),
        LogicalAnd(
            Assignment("primary_release_date.gte", "2000-01-01"),
            Assignment("primary_release_date.lte", "2009-12-31"),
            Assignment("vote_average.gte", "6.0"),
            Assignment("sort_by", "popularity.desc"),
        ),
    ),
    # DURATION-BASED RULES
    # 16 - Short films: Under 90 minutes
    Rule(
        Evaluation("movie_duration", "==", "Short"),
        LogicalAnd(
            Assignment("with_runtime.lte", "90"),
            Assignment("vote_average.gte", "6.0"),
            Assignment("sort_by", "vote_average.desc"),
        ),
    ),
    # 17 - Standard length: 90-150 minutes
    Rule(
        Evaluation("movie_duration", "==", "Standard"),
        LogicalAnd(
            Assignment("with_runtime.gte", "90"),
            Assignment("with_runtime.lte", "150"),
            Assignment("vote_average.gte", "6.0"),
        ),
    ),
    # 18 - Epic length: Over 150 minutes, focus on genres that benefit
    Rule(
        Evaluation("movie_duration", "==", "Epic"),
        LogicalAnd(
            Assignment("with_runtime.gte", "150"),
            Assignment("with_genres", "Drama|History|War|Adventure"),
            Assignment("vote_average.gte", "7.0"),
            Assignment("sort_by", "vote_average.desc"),
        ),
    ),
    # RATING-BASED RULES
    # 19 - Family friendly content
    Rule(
        Evaluation("movie_rating", "==", "Family Friendly"),
        LogicalAnd(
            Assignment("certification_country", "US"),
            LogicalOr(
                Assignment("certification", "G"),
                Assignment("certification", "PG"),
            ),
            Assignment("vote_average.gte", "6.0"),
        ),
    ),
    # 20 - Teen appropriate content
    Rule(
        Evaluation("movie_rating", "==", "Teen"),
        LogicalAnd(
            Assignment("certification_country", "US"),
            Assignment("certification", "PG-13"),
            Assignment("vote_average.gte", "6.0"),
        ),
    ),
    # 21 - Mature content
    Rule(
        Evaluation("movie_rating", "==", "Mature"),
        LogicalAnd(
            Assignment("certification_country", "US"),
            Assignment("certification", "R"),
            Assignment("vote_average.gte", "6.5"),
            Assignment("include_adult", "true"),
        ),
    ),
    # COMPLEX COMBINATION RULES
    # 22 - Adventure + Long duration: Epic adventures
    Rule(
        LogicalAnd(
            LogicalOr(
                Evaluation("favorite_genre", "==", "Adventure"),
                Evaluation("movie_vibe", "==", "Epic Journey"),
            ),
            Evaluation("movie_duration", "==", "Epic"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Adventure|Fantasy"),
            Assignment("with_runtime.gte", "150"),
            Assignment("vote_average.gte", "7.0"),
            Assignment("sort_by", "vote_average.desc"),
        ),
    ),
    # 23 - Horror + Mature rating: Adult horror films
    Rule(
        LogicalAnd(
            LogicalOr(
                Evaluation("favorite_genre", "==", "Horror"),
                Evaluation("movie_vibe", "==", "Supernatural"),
            ),
            Evaluation("movie_rating", "==", "Mature"),
        ),
        LogicalAnd(
            Assignment("with_genres", "Horror"),
            Assignment("certification_country", "US"),
            Assignment("certification", "R"),
            Assignment("vote_average.gte", "6.5"),
        ),
    ),
    # 24 - Thought-provoking sci-fi or drama
    Rule(
        LogicalAnd(
            Evaluation("user_mood", "==", "Thought Provoking"),
            LogicalOr(
                Evaluation("favorite_genre", "==", "Science Fiction"),
                Evaluation("favorite_genre", "==", "Drama"),
            ),
        ),
        LogicalOr(
            LogicalAnd(
                Assignment("with_genres", "Science Fiction"),
                Assignment("vote_average.gte", "7.5"),
                Assignment("sort_by", "vote_average.desc"),
            ),
            LogicalAnd(
                Assignment("with_genres", "Drama"),
                Assignment(
                    "with_keywords",
                    "philosophical|existential|thought-provoking",
                ),
                Assignment("vote_average.gte", "7.5"),
            ),
        ),
    ),
    # 25 - True stories from 2000s
    Rule(
        LogicalAnd(
            Evaluation("movie_vibe", "==", "Based on a true story"),
            Evaluation("movie_era", "==", "2000s"),
        ),
        LogicalAnd(
            Assignment("with_keywords", "based on a true story|biographical"),
            Assignment("primary_release_date.gte", "2000-01-01"),
            Assignment("primary_release_date.lte", "2009-12-31"),
            Assignment("vote_average.gte", "6.5"),
        ),
    ),
    # 26 - Animation + Anime: Japanese animated films
    Rule(
        LogicalAnd(
            Evaluation("favorite_genre", "==", "Animation"),
            Evaluation("movie_vibe", "==", "Anime"),
        ),
        LogicalOr(
            LogicalAnd(
                Assignment("with_genres", "Animation"),
                Assignment("with_origin_country", "JP"),
                Assignment("vote_average.gte", "7.0"),
            ),
            LogicalAnd(
                Assignment("with_genres", "Animation"),
                Assignment("with_keywords", "anime|manga"),
                Assignment("vote_average.gte", "7.0"),
            ),
        ),
    ),
    # 27 - Mind-bending thrillers/sci-fi
    Rule(
        LogicalAnd(
            Evaluation("movie_vibe", "==", "Mind Bending"),
            LogicalOr(
                Evaluation("favorite_genre", "==", "Thriller"),
                Evaluation("favorite_genre", "==", "Science Fiction"),
            ),
        ),
        LogicalOr(
            LogicalAnd(
                Assignment("with_genres", "Thriller|Science Fiction"),
                Assignment(
                    "with_keywords", "psychological|mind-bending|reality"
                ),
                Assignment("vote_average.gte", "7.0"),
            ),
            LogicalAnd(
                Assignment("with_genres", "Mystery|Thriller"),
                Assignment("vote_average.gte", "7.5"),
                Assignment("sort_by", "vote_average.desc"),
            ),
        ),
    ),
    # 28 - Modern classics in drama/crime
    Rule(
        LogicalAnd(
            Evaluation("movie_era", "==", "Modern Classic"),
            LogicalOr(
                Evaluation("favorite_genre", "==", "Drama"),
                Evaluation("favorite_genre", "==", "Crime"),
            ),
        ),
        LogicalAnd(
            Assignment("primary_release_date.gte", "2000-01-01"),
            Assignment("primary_release_date.lte", "2015-12-31"),
            Assignment("with_genres", "Drama|Crime"),
            Assignment("vote_average.gte", "8.0"),
            Assignment("sort_by", "vote_average.desc"),
        ),
    ),
)
