CREATE TABLE anime(
    mal_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    title_english TEXT,
    episodes INTEGER,
    type TEXT,
    source TEXT,
    season TEXT NOT NULL,
    year INTEGER NOT NULL,
    rating TEXT,
    synopsis TEXT
);

CREATE TABLE genre(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE producer(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE anime_genre(
    id INTEGER PRIMARY KEY,
    anime_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    FOREIGN KEY(anime_id) REFERENCES anime(mal_id),
    FOREIGN KEY(genre_id) REFERENCES genre(id)
);

CREATE TABLE anime_producer(
    id INTEGER PRIMARY KEY,
    anime_id INTEGER NOT NULL,
    producer_id INTEGER NOT NULL,
    FOREIGN KEY(anime_id) REFERENCES anime(mal_id),
    FOREIGN KEY(producer_id) REFERENCES producer(id)
);