import click
import bcrypt
import uuid
import re
from os import getenv
import psycopg2
from psycopg2 import errorcodes

postgres_host = getenv("POSTGRES_HOST", default="db")
postgres_port = getenv("POSTGRES_PORT", default=5432)
postgres_user = getenv("POSTGRES_USER", default="postgres")
postgres_password = getenv("POSTGRES_PASSWORD", default="postgres")
postgres_database = getenv("POSTGRES_DATABASE", default="postgres")

username = getenv("USERNAME")
password = getenv("PASSWORD")


@click.command()
def create():
    print("Attempting to create db")
    connection = psycopg2.connect(
        database="postgres",
        user=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=postgres_port,
    )
    connection.set_session(autocommit=True)  # set autocommit to True
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
            cursor.execute("CREATE DATABASE {} WITH OWNER {};".format(name, owner))
        except psycopg2.DatabaseError as e:
            if e.pgcode != errorcodes.DUPLICATE_DATABASE:
                raise
            print("Database {} already exists.".format(name))
        else:
            print("Created database {}.".format(name))

    try_create_db(postgres_database, postgres_user)
    cursor.close()
    connection.close()


@click.command()
def add_user():
    print("Attempting to add user")

    connection = psycopg2.connect(
        database=postgres_database,
        user=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=postgres_port,
    )
    connection.set_session(autocommit=True)  # set autocommit to True
    cursor = connection.cursor()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    user = {
        "user_id": username,
        "partner_id": None,
        "password": hashed_password.decode("utf-8"),
    }
    try:
        cursor.execute(
            "INSERT INTO users (user_id, password, partner_id) VALUES (%(user_id)s, %(password)s, %(partner_id)s)",
            user,
        )
    except psycopg2.errors.UniqueViolation as e:
        print("Bootstrap user already exists")

    print(f"Successfully added user {username} to the users table.")

    cursor.close()
    connection.close()


@click.command()
def add_bible():
    conn = psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        user=postgres_user,
        password=postgres_password,
        database=postgres_database,
    )

    cursor = conn.cursor()

    # Check if bible table is empty
    cursor.execute("SELECT COUNT(*) FROM bible")
    num_rows = cursor.fetchone()[0]
    if num_rows > 0:
        print("bible table already has rows. Skipping insertion from file.")
        return

    # Insert data from file
    with open("utility/bible.sql", "r") as f:
        sql_commands = f.read()
        # Split SQL commands by semicolon, excluding those in quotes
        sql_commands = re.split(";(?=(?:[^']*'[^']*')*[^']*$)", sql_commands)
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)

    conn.commit()

    cursor.close()
    conn.close()


@click.group()
def cli():
    pass


if __name__ == "__main__":
    cli.add_command(add_user)
    cli.add_command(create)
    cli.add_command(add_bible)
    cli()
