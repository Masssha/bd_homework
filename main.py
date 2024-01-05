import psycopg2

with psycopg2.connect(database="data", user="postgres", password="LLllMMmmqwerty654321") as conn:
    with conn.cursor() as cur:
        def create_table(cursor):
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clients(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(40) NOT NULL,
                        surname VARCHAR(40) NOT NULL,
                        email VARCHAR(40) NOT NULL
                    );
                    """)
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clients_phones(
                        id SERIAL PRIMARY KEY,
                        phone VARCHAR(80),
                        client_id INTEGER NOT NULL REFERENCES clients(id),
                        CONSTRAINT phone_unique UNIQUE(phone)
                    );
                    """)
            conn.commit()
        # newtabl = create_table(cur)

        def new_client(cursor, name, surname, email, phone=None):
            cursor.execute("""
                    INSERT INTO clients(name, surname, email) VALUES(%s, %s, %s) RETURNING id;
                    """, (name, surname, email))
            id_cl = cur.fetchone()
            cursor.execute("""
                    INSERT INTO clients_phones(phone, client_id) VALUES(%s, %s);
                    """, (phone, id_cl))
            conn.commit()

        # newclient1 = new_client(cur, "John", "Lennon", "aaa@aa.ru", "222-3-22")
        # newclient2 = new_client(cur, "John", "Lennon", "aaa@aa.ru")

        def new_phone(cursor, client_id, phone):
            cursor.execute("""
                    INSERT INTO clients_phones(phone, client_id) VALUES(%s, %s);
                    """, (phone, client_id))
            conn.commit()

        # newphone = new_phone(cur, 7, "228-3-22")
        # newphone2 = new_phone(cur, 7, "555")

        def delete_phone(cursor, client_id, phone):
            cursor.execute("""
                    DELETE FROM clients_phones where phone=%s AND client_id=%s;
                    """, (phone, client_id))
            conn.commit()

        # delphone1 = delete_phone(cur, 7, "555")
        # delphone2 = delete_phone(cur, 14, "222-3-22")

        def change_client(cursor, client_id, name=None, surname=None, email=None, phone=None):
            cursor.execute("""
                    UPDATE clients SET name=%s, surname=%s, email=%s WHERE id=%s;
        """, (name, surname, email, client_id))
            cursor.execute("""
                        UPDATE clients_phones SET phone=%s WHERE client_id=%s;
            """, (phone, client_id))
            conn.commit()

        # updcl1 = change_client(cur, 9, surname="Petrov")
        # updcl2 = change_client(cur, 16, "Ivan", "Ivanov", "ssss@ee", "222-33-5566")

        def delete_client(cursor, client_id):
            cur.execute("""
                    DELETE FROM clients_phones WHERE client_id=%s;
                    """, (client_id,))
            cur.execute("""
                    DELETE FROM clients WHERE id=%s;
                    """, (client_id,))
            conn.commit()

        # delcl1 = delete_client(cur, 7)

        def find_client(cursor, name=None, surname=None, email=None, phone=None):
            cur.execute("""
                    SELECT c.id, c.name, c.surname, c.email, cl.phone FROM clients c
                    left join clients_phones cl on c.id = cl.client_id
                    WHERE c.name=%s
                    or c.surname=%s
                    or c.email=%s
                    or cl.phone=%s;
                    """, (name, surname, email, phone))
            id_cl = cur.fetchall()
            print(id_cl)

        # findcl1 = find_client(cur, " ", "Lennon", "", " ")
        # findcl2 = find_client(cur, " ", " ", "ssss@ee", " ")git
        # findcl3 = find_client(cur, "Ivan", "", " ", " ")
        # findcl4 = find_client(cur, " ", " ", " ", "222-33-5566")

