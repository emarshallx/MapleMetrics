import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "housing.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def run_query(query, params=None):
    connection = get_connection()

    try:
        dataframe = pd.read_sql_query(
            query,
            connection,
            params=params or {}
        )
        return dataframe

    finally:
        connection.close()


def get_market_summary():
    query = """
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
    """

    return run_query(query)


def get_mortgage_schedule(
    principal,
    payment,
    annual_rate,
    months
):
    sql_path = BASE_DIR / "sql" / "mortgage_schedule.sql"

    with open(sql_path, "r", encoding="utf-8") as file:
        query = file.read()

    return run_query(
        query,
        {
            "principal": principal,
            "payment": payment,
            "rate": annual_rate,
            "months": months
        }
    )