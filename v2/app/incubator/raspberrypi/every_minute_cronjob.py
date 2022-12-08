#!/usr/env/bin python3

# Run me!

from typing import Tuple
from loguru import logger
import time

import adafruit_shtc3
import board
import cowsay
import sqlite3


cowsay.turtle("mmmmmm, plants")

logger.add("every_minute_cronjob.log", rotation="1 week")


@logger.catch
def get_sensor():
    i2c = board.I2C()
    return adafruit_shtc3.SHTC3(i2c)


@logger.catch
def get_db_conn_and_cursor() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect("lucas-test.db")
    return (conn, conn.cursor())


def setup_table(cursor: sqlite3.Cursor):
    # TODO: make time_sec default to now?
    return cursor.execute("""
    CREATE TABLE IF NOT EXISTS temp_humid_1m (
        time_sec INTEGER PRIMARY KEY,
        temp REAL NOT NULL,
        humidity REAL NOT NULL
    );
    """)


def get_latest_temp_from_db(cursor: sqlite3.Cursor) -> sqlite3.Cursor:
    return cursor.execute("""
    SELECT * FROM temp_humid_1m
    ORDER BY time_sec DESC
    LIMIT 1;
    """)


def record_temp_and_humidiy(conn: sqlite3.Connection, cursor: sqlite3.Cursor, sensor):
    temperature, relative_humidity = sensor.measurements
    logger.info("Got temp [{}] and humidity [{}]",
                temperature, relative_humidity)
    cursor.execute("""
    INSERT INTO temp_humid_1m (time_sec, temp, humidity)
    VALUES (?, ?, ?)
    """, (int(time.time()), temperature, relative_humidity))
    conn.commit()


@logger.catch
def main():
    conn, cursor = get_db_conn_and_cursor()
    setup_table(cursor)
    result = get_latest_temp_from_db(cursor).fetchone()
    if result is None:
        logger.warning("No data in DB!")
    else:
        logger.info("Last row in DB is [{}].", result)

    logger.info("Getting sensor")
    # TODO: catch and log debugging suggestions like sudo raspi-config and checking
    # sensor type
    sensor = get_sensor()
    record_temp_and_humidiy(conn, conn.cursor(), sensor)
    logger.info("Recorded temperature and humidity")


if __name__ == "__main__":
    main()
