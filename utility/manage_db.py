from os import getenv
import click
import psycopg2
import psycopg2.errors
from psycopg2 import errorcodes

postgres_host = getenv("POSTGRES_HOST", default="db")
postgres_port = getenv("POSTGRES_PORT", default=5432)
postgres_user = getenv("POSTGRES_USER", default="postgres")
postgres_password = getenv("POSTGRES_PASSWORD", default="postgres")
postgres_database = getenv("POSTGRES_DATABASE", default="convergent")


@click.pass_context
def create(ctx):
    connection = psycopg2.connect(
        database="postgres",
        user=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=postgres_port,
    )
    cursor = connection.cursor()

    def try_create_user(username, password):
        try:
            cursor.execute(
                "CREATE USER {} WITH ENCRYPTED PASSWORD '{}';".format(
                    username, password
                )
            )
        except psycopg2.DatabaseError as e:
            if e.pgcode != errorcodes.DUPLICATE_OBJECT:
                raise
            print("User {} already exists.".format(username))
        else:
            print("Created user {}.".format(username))

    try_create_user(postgres_user, postgres_password)

    def try_create_db(name, owner):
        try:
            cursor.execute("CREATE DATABASE {} WITH OWNER = {};".format(name, owner))
        except psycopg2.DatabaseError as e:
            if e.pgcode != errorcodes.DUPLICATE_DATABASE:
                raise
            print("Database {} already exists.".format(name))
        else:
            print("Created database {}.".format(name))

    try_create_db(postgres_database, postgres_user)
    cursor.close()
    connection.close()
