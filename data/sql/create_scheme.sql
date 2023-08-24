CREATE TABLE anime(
    mal_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    episodes INTEGER,
    type TEXT,
    source TEXT,
    season TEXT NOT NULL,
    year INTEGER NOT NULL,
    rating TEXT
);

CREATE TABLE genre(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE producer(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);