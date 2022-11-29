import logging
import os

import pymysql.cursors

host = os.getenv('WATCHDOG_DATABASE_HOST', 'dev.townhall.place')
user = os.getenv('WATCHDOG_DATABASE_USER', 'admin')
password = os.getenv('WATCHDOG_DATABASE_PASSWORD', '3d8JCwN@h48x')
database = os.getenv('WATCHDOG_DATABASE_NAME', 'watchdog')
port = os.getenv('WATCHDOG_DATABASE_PORT', '3306')

if host is None or \
        user is None or \
        password is None or \
        database is None or \
        port is None:
    msg = "No database config"
    logging.error(msg)


def open_connection():
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=int(port),
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )


def fetchone(sql):
    logging.info(sql)
    connection = open_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()
    except pymysql.Error as e:
        logging.error(e)

    connection.close()


def fetchall(sql):
    logging.info(sql)
    connection = open_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except pymysql.Error as e:
        logging.error(e)

    connection.close()


def insert(sql):
    logging.info(sql)
    connection = open_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
    except pymysql.Error as e:
        logging.error(e)

    connection.close()


def update(list):
    logging.info(list)
    sql = f'UPDATE log_tb SET type = %s WHERE uuid = %s'
    connection = open_connection()

    try:
        with connection.cursor() as cursor:
            cursor.executemany(sql,list)
    except pymysql.Error as e:
        logging.error(e)

    connection.close()


class Log:
    timestamp: int
    remote_addr: str
    path: str
    status: str
    protocol: str
    method: str
    user_agent: str
