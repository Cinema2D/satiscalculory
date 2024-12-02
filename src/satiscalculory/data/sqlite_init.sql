CREATE TABLE items (
    name TEXT PRIMARY KEY,
    stack_size INTEGER,
    sink_points INTEGER
);

CREATE TABLE recipes (
    name TEXT PRIMARY KEY,
    ingredients TEXT,
    ingredient_rates REAL,
    facility TEXT,
    facility_rates REAL,
    products TEXT,
    product_rates REAL,
    item TEXT,

    FOREIGN KEY (item) REFERENCES items(name)
);
