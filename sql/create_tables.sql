CREATE TABLE IF NOT EXISTS advice_quotes (
    id SERIAL PRIMARY KEY,
    advice_id INTEGER UNIQUE NOT NULL,
    advice_text TEXT NOT NULL,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS activities (
    id SERIAL PRIMARY KEY,
    activity_key TEXT UNIQUE NOT NULL,
    activity TEXT NOT NULL,
    type TEXT,
    participants INTEGER,
    price DECIMAL(3,2),
    accessibility DECIMAL(3,2),
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dog_images (
    id SERIAL PRIMARY KEY,
    breed TEXT,
    image_url TEXT UNIQUE NOT NULL,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);