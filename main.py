import psycopg2, secrets
password = secrets.pg_password


def create_db():
    with conn.cursor() as cur:
        cur.execute("""DROP TABLE IF EXISTS Phone_numbers;
                       DROP TABLE IF EXISTS Users;
                    """)
        cur.execute("""
                    CREATE TABLE Users(
                                       user_id SERIAL PRIMARY KEY,
                                       name VARCHAR(40) NOT NULL,
                                       surname VARCHAR(40) NOT NULL,
                                       email VARCHAR(120) NOT NULL
                                       );
                    CREATE TABLE Phone_numbers(
                                               id SERIAL PRIMARY KEY, 
                                               user_id INTEGER NOT NULL REFERENCES Users(user_id), 
                                               phone_number VARCHAR(12)
                                               )
                    """)
        conn.commit()


def add_client(name:str, surname:str, email:str):
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO Users(name, surname, email)
                    VALUES (%s, %s, %s)
                    """, (name, surname, email))

        conn.commit()


def add_phone_number(user_id:int, phone_number:str):
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO Phone_numbers(user_id, phone_number)
                    VALUES (%s, %s)
                    """, (user_id, phone_number))
        conn.commit()


def edit_client_info(user_id:int, **kwargs):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT * FROM Users
                    WHERE user_id = %s
                    """, (user_id, ))
        data = cur.fetchone()
        cur.execute("""
                    SELECT phone_number FROM Phone_numbers
                    WHERE user_id = %s
                    """, (user_id, ))
        phone_number = cur.fetchone()
        if kwargs.get("name") is None:
            kwargs["name"] = data[1]
        if kwargs.get("surname") is None:
            kwargs["surname"] = data[2]
        if kwargs.get("email") is None:
            kwargs["email"] = data[3]
        if kwargs.get("phone_number") is None:
            kwargs["phone_number"] = phone_number

        cur.execute("""
                    UPDATE Users
                    SET name = %s,
                        surname = %s,
                        email = %s
                    WHERE user_id = %s
                    """, (kwargs["name"], kwargs["surname"], kwargs["email"], user_id))
        cur.execute("""
                    UPDATE Phone_numbers
                    SET phone_number = %s
                    WHERE user_id = %s
                    """, (kwargs["phone_number"], user_id))


def del_phone_number(user_id:int, phone_number:str):
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM Phone_numbers
                    WHERE phone_number = %s AND user_id = %s
                    """, (phone_number, user_id))
        conn.commit()


def del_client(user_id:int):
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM Users
                    WHERE user_id = %s
                    DELETE FROM Phone_numbers
                    WHERE user_id = %s
                    """, (user_id, user_id))


def search_client(user_id:int, name:str, surname:str, email:str, phone_number:str):
    with conn.cursor() as cur:
        cur.execute()


if __name__ == "__main__":
    conn = psycopg2.connect(database="personal_info", user="postgres", password=password)
    create_db()
    add_client("Иван", "Иванов", "example@mail.com")
    add_phone_number(1, "+79999999999")
    add_phone_number(1, "+79999999998")
    edit_client_info(1, name="Антон")
    del_phone_number("1", "+79999999999")
    del_client(1)
    search_client()
    conn.close()
