import sqlite3 as sql


def create_table(list):
    connection = sql.connect('records.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER,
            birth_year INTEGER
        )
    ''')
    connection.commit()

    connection.close()
    for i in range(len(list)-1):
        insert_record(i + 1, list[i])


def clear_all():
    connection = sql.connect('records.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM records')
    connection.commit()
    connection.close()


def insert_record(id, birth_year):
    connection = sql.connect('records.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO records (id, birth_year) VALUES (?, ?)
    ''', (id, birth_year))
    connection.commit()
    connection.close()


def display_records():
    connection = sql.connect('records.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM records')
    records = cursor.fetchall()
    connection.close()
    if not records:
        print("База данных пуста.")
    else:
        print("\nСодержимое базы данных:")
        for record in records:
            print("ID: {}, record: {}".format(*record))
        print('\n')
