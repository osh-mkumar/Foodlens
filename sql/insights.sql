CREATE DATABASE foodlens;

CREATE TABLE restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    name TEXT,
    price FLOAT,
    city TEXT,
    region TEXT,
    timing TEXT,
    rating_type TEXT,
    rating FLOAT,
    votes FLOAT,
    url TEXT
);

CREATE TABLE cuisines (
    cuisine_id INTEGER PRIMARY KEY,
    cuisine_name TEXT
);

CREATE TABLE restaurant_cuisines (
    restaurant_id INTEGER,
    cuisine_id INTEGER
);

COPY restaurants
FROM 'D:/data-engineering-lab/datasets/processed/restaurants.csv'
DELIMITER ','
CSV HEADER;

COPY cuisines(cuisine_name, cuisine_id)
FROM 'D:/data-engineering-lab/datasets/processed/cuisines.csv'
DELIMITER ','
CSV HEADER;

COPY restaurant_cuisines
FROM 'D:/data-engineering-lab/datasets/processed/restaurant_cuisines.csv'
DELIMITER ','
CSV HEADER;

SELECT COUNT(*) FROM restaurants;
SELECT COUNT(*) FROM cuisines;
SELECT COUNT(*) FROM restaurant_cuisines;

/* Most Popular Cuisines in Mumbai*/

SELECT c.cuisine_name,
       ROUND(AVG(r.rating)::numeric, 2) AS avg_rating,
       COUNT(*) AS total_restaurants
FROM restaurants r
JOIN restaurant_cuisines rc ON r.restaurant_id = rc.restaurant_id
JOIN cuisines c ON rc.cuisine_id = c.cuisine_id
WHERE r.rating IS NOT NULL
GROUP BY c.cuisine_name
HAVING COUNT(*) >= 50
ORDER BY avg_rating DESC
LIMIT 10;

/* Highest Rated Cuisines (Min 50 Restaurants)*/
SELECT c.cuisine_name,
       ROUND(AVG(r.rating)::numeric, 2) AS avg_rating,
       COUNT(*) AS total_restaurants
FROM restaurants r
JOIN restaurant_cuisines rc ON r.restaurant_id = rc.restaurant_id
JOIN cuisines c ON rc.cuisine_id = c.cuisine_id
WHERE r.rating IS NOT NULL
GROUP BY c.cuisine_name
HAVING COUNT(*) >= 50
ORDER BY avg_rating DESC
LIMIT 10;