import logging
import os

from peewee import *

db = SqliteDatabase('people.db')

host = os.getenv('HOST', '')
user = os.getenv('USER', '')
password = os.getenv('PASSWORD', '')
database = os.getenv('DATABASE', '')
port = os.getenv('PORT', '0')

if host is None or \
        user is None or \
        password is None or \
        database is None or \
        port is None:
    msg = "No database config"
    logging.error(msg)

# set logging level

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

mysql = pw.MySQLDatabase(
    database,
    user=user,
    password=password,
    host=host,
    port=int(port)
)


def get_mysql_db():
    return mysql


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.