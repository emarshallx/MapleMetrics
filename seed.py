import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "data" / "housing.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


# ---------------------------------------------------------
# MAKE SURE DATA DIRECTORY EXISTS
# ---------------------------------------------------------

DATABASE_PATH.parent.mkdir(exist_ok=True)


# ---------------------------------------------------------
# CONNECT TO SQLITE
# ---------------------------------------------------------

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

# Turn on foreign-key enforcement in SQLite
cursor.execute("PRAGMA foreign_keys = ON;")


# ---------------------------------------------------------
# CREATE DATABASE TABLES FROM schema.sql
# ---------------------------------------------------------

with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
    cursor.executescript(file.read())

connection.commit()

print("MapleMetrics database created successfully.")


# ---------------------------------------------------------
# VERIFY TABLES
# ---------------------------------------------------------

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
""")

print("\nTables created:")

for table in cursor.fetchall():
    print("-", table[0])


# ---------------------------------------------------------
# SEED CANADIAN REAL ESTATE MARKETS
# ---------------------------------------------------------

markets = [
    (1, "Toronto", "Ontario"),
    (2, "Vancouver", "British Columbia"),
    (3, "Calgary", "Alberta"),
    (4, "Montreal", "Quebec"),
    (5, "Ottawa", "Ontario")
]

cursor.executemany("""
INSERT OR IGNORE INTO markets (
    id,
    city,
    province
)
VALUES (?, ?, ?);
""", markets)

connection.commit()


# ---------------------------------------------------------
# VERIFY MARKETS
# ---------------------------------------------------------

cursor.execute("""
SELECT
    id,
    city,
    province
FROM markets
ORDER BY city;
""")

print("\nMarkets loaded:")

for row in cursor.fetchall():
    print(row)


# ---------------------------------------------------------
# SEED DEMONSTRATION MARKET STATISTICS
# ---------------------------------------------------------
#
# These values are demonstration data for development.
# Before publishing the project, we can replace these
# with properly sourced Canadian real-estate datasets.
#

market_stats = [
    (
        1,
        1,
        "2026-08",
        "Composite",
        993410,
        -4.5,
        6200
    ),
    (
        2,
        2,
        "2026-08",
        "Composite",
        1081900,
        -5.6,
        3100
    ),
    (
        3,
        3,
        "2026-08",
        "Composite",
        595000,
        1.8,
        2800
    ),
    (
        4,
        4,
        "2026-08",
        "Composite",
        625000,
        3.2,
        4100
    ),
    (
        5,
        5,
        "2026-08",
        "Composite",
        690000,
        0.9,
        1700
    )
]

cursor.executemany("""
INSERT OR IGNORE INTO market_stats (
    id,
    market_id,
    period,
    property_type,
    price,
    yoy_change,
    sales
)
VALUES (?, ?, ?, ?, ?, ?, ?);
""", market_stats)

connection.commit()


# ---------------------------------------------------------
# VERIFY MARKET STATISTICS USING A JOIN
# ---------------------------------------------------------

cursor.execute("""
SELECT
    markets.city,
    markets.province,
    market_stats.period,
    market_stats.property_type,
    market_stats.price,
    market_stats.yoy_change,
    market_stats.sales
FROM market_stats
JOIN markets
    ON market_stats.market_id = markets.id
ORDER BY market_stats.price DESC;
""")

print("\nMarket statistics loaded:")

for row in cursor.fetchall():
    print(row)


# ---------------------------------------------------------
# BASIC DATABASE SUMMARY
# ---------------------------------------------------------

cursor.execute("""
SELECT COUNT(*)
FROM markets;
""")

market_count = cursor.fetchone()[0]


cursor.execute("""
SELECT COUNT(*)
FROM market_stats;
""")

stats_count = cursor.fetchone()[0]


print("\nDatabase summary:")
print(f"- Markets: {market_count}")
print(f"- Market statistic records: {stats_count}")


# ---------------------------------------------------------
# CLOSE DATABASE CONNECTION
# ---------------------------------------------------------

connection.close()

print("\nMapleMetrics seed process completed successfully.")