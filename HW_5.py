import psycopg2
import psycopg2.errors as errors


def create_tables():
    """Создаёт таблицы БД"""
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        firstname VARCHAR(40),
        lastname VARCHAR(40), 
        mail VARCHAR(40) UNIQUE NOT NULL,
        CHECK (mail ~ '^[ -~]*$')                 
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone(
        id SERIAL PRIMARY KEY,
        number VARCHAR(12) UNIQUE,
        client_id INTEGER NOT NULL REFERENCES client(id),
        CHECK (number ~ '^[+-9]*$')
    );
    """)
    conn.commit()
    print('Таблицы успешно созданы')


def delete_tables():
    """Удаляет таблицы из БД"""
    cur.execute("""DROP TABLE client, phone;""")


def add_client(firstname=str, lastname=str, mail=str):
    """Добавляет нового клиента в БД"""
    try:
        cur.execute("""
        INSERT INTO client(firstname, lastname, mail) VALUES(%s, %s, %s);
        """, (firstname, lastname, mail))
        conn.commit()
        print('Клиент добавлен в БД')
    except errors.CheckViolation as error:
        print(f'Ошибка ввода данных: {error}')


def add_phone(number=str, client_id=int):
    """Добаляет новый номер телефона клиента в БД"""
    try:
        cur.execute("""
        INSERT INTO phone(number, client_id) VALUES(%s, %s);
        """, (number, client_id))
        conn.commit()
        print('Номер телефона добавлен в БД')
    except errors.CheckViolation as error:
        print(f'Ошибка ввода данных: {error}')


def update_client(firstname=str, lastname=str, mail=str, client_id=int):
    """Изменяет данные клиента в БД"""
    cur.execute("""
    UPDATE client SET firstname=%s, lastname=%s, mail=%s WHERE id=%s;
    """, (firstname, lastname, mail, client_id))
    conn.commit()
    print('Изменения клиента успешно внесены в БД')


def update_phone(number=str, phone_id=int):
    """Изменяет номер телефона клиента в БД"""
    cur.execute("""
    UPDATE phone SET number=%s WHERE id=%s;
    """, (number, phone_id))
    conn.commit()
    print('Номер телефона клиента изменён в БД')


def delete_phone(phone_id=int):
    """Удаляет номер телефона клиента из БД"""
    cur.execute("""
    DELETE FROM phone WHERE id=%s;
    """, (phone_id,))
    conn.commit()
    print('Номер телефона успешно удалён из БД')


def delete_client(client_id=int):
    """Удаляет данные клиенте из БД"""
    if _search_has_phone(client_id):
        print(f'У клиента с id={client_id} есть привязанные номера телефона')
        return
    cur.execute("""
    DELETE FROM client WHERE id=%s;
    """, (client_id,))
    conn.commit()
    print('Клиент успешно удалён из БД')


def search_firstname(firstname=str):
    """Ищет данные клиента в БД по имени клиента"""
    cur.execute("""
    SELECT client.id, firstname, lastname, mail, number FROM client
    LEFT JOIN phone ON client.id = phone.client_id
    WHERE firstname=%s;
    """, (firstname,))
    _print_search(cur.fetchall())


def search_lastname(lastname=str):
    """Ищет данные клиента в БД по фамилии клиента"""
    cur.execute("""
    SELECT client.id, firstname, lastname, mail, number FROM client
    LEFT JOIN phone ON client.id = phone.client_id
    WHERE lastname=%s;
    """, (lastname,))
    _print_search(cur.fetchall())


def search_mail(mail=str):
    """Ищет данные клиента в БД по почте клиента"""
    cur.execute("""
    SELECT client.id, firstname, lastname, mail, number FROM client
    LEFT JOIN phone ON client.id = phone.client_id
    WHERE mail=%s;
    """, (mail,))
    _print_search(cur.fetchall())


def search_phone(number=str):
    """Ищет данные клиента в БД по номеру телефона клиента"""
    cur.execute("""
    SELECT client.id, firstname, lastname, mail, number FROM client
    LEFT JOIN phone ON client.id = phone.client_id
    WHERE number=%s;
    """, (number,))
    _print_search(cur.fetchall())


def _search_has_phone(client_id):
    """Ищет телефоны у клиента по его id"""
    cur.execute("""
    SELECT number FROM client
    LEFT JOIN phone ON client.id = phone.client_id
    WHERE client.id=%s;
    """, (client_id,))
    return cur.fetchone()[0]


def _print_search(data=list):
    """Печатает результаты поиска"""
    for d in data:
        client_id, fname, lname, mail, number = d[0], d[1], d[2], d[3], d[4]
        print(f'{client_id} - {fname} {lname}, {mail}, {number}')


if __name__ == "__main__":
    with psycopg2.connect(database="hw_sql_5", user="postgres", password="gfhjkm") as conn:
        with conn.cursor() as cur:
            delete_tables()
            create_tables()
            add_client('Ivan', 'Ivanov', 'iivanov1987@mail.ru')
            add_phone('5553307', 1)
            add_client('John', 'Stone', 'grebeshok@gmail.com')
            add_phone('1010864', 2)
            add_phone('4455087', 2)
            add_client('Мария', 'Сидорова', 'msidor@bk.com')
            search_firstname('Мария')
            search_lastname('Stone')
            update_client('Игорь', 'Петров', 'ipetrov12@yandex.ru', 2)
            search_mail('ipetrov12@yandex.ru')
            update_phone('777888', 1)
            search_phone('777888')
            delete_phone(3)
            search_firstname('Игорь')
            delete_client(1)
            delete_phone(1)
            delete_client(1)
conn.close()
