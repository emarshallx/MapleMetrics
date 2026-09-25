CREATE TABLE IF NOT EXISTS "markets" (
    "id" INTEGER,
    "city" TEXT NOT NULL,
    "province" TEXT NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "market_stats" (
    "id" INTEGER,
    "market_id" INTEGER NOT NULL,
    "period" TEXT NOT NULL,
    "property_type" TEXT NOT NULL,
    "price" NUMERIC NOT NULL,
    "yoy_change" NUMERIC,
    "sales" INTEGER,
    PRIMARY KEY("id"),
    FOREIGN KEY("market_id") REFERENCES "markets"("id")
);