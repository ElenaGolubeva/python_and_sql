import psycopg2

def create_table(cur):
    cur.execute("CREATE TABLE client(id SERIAL PRIMARY KEY, first_name VARCHAR(30), surname VARCHAR(30), email VARCHAR(40) NOT NULL);")
    cur.execute("CREATE TABLE number_phone(id SERIAL PRIMARY KEY, number VARCHAR(11), id_client INTEGER references client(id));")
    print("Таблицы созданы")

def delete_table(cur):
    cur.execute(f"DROP TABLE client CASCADE;")
    cur.execute(f"DROP TABLE number_phone CASCADE;")
    print("Таблицы удалены")

def add_client(cur, first_name, surname, email, number='Не указан'):
    cur.execute("INSERT INTO client(first_name, surname, email) VALUES (%s, %s, %s);", (first_name, surname, email))
    cur.execute("SELECT id FROM client;")
    id_ = cur.fetchall()[-1]
    cur.execute("INSERT INTO number_phone(number, id_client) VALUES (%s, %s);", (number, id_))
    print("Клиент добавлен")

def add_phone(cur, id_client, number):
    cur.execute("SELECT id, number FROM number_phone WHERE id_client=%s;",(id_client))
    rez = cur.fetchall()
    for i in rez:
        if i[1] == "Не указан" or not i[1]:
            cur.execute("UPDATE number_phone SET number=%s WHERE id = %s;", (number, i[0]))
            break
        else:
            cur.execute("INSERT INTO number_phone(number, id_client) VALUES (%s, %s);", (number, id_client))
    print("Номер добавлен")

def change_info(cur, client_id, first_name, surname, email, number):
    str = []
    tup = []
    if first_name is not None and first_name != "":
        str.append("first_name=%s")
        tup.append(first_name)
    if surname is not None and surname != "":
        str.append("surname=%s")
        tup.append(surname)
    if email is not None and email != "":
        str.append("email=%s")
        tup.append(email)
    and_str = ' '.join(str)
    cur.execute("SELECT id FROM client WHERE id=%s;", (client_id,))
    rez = cur.fetchall()
    if not rez:
        print("Клиента с таким идентификатором нет.") 
    else:
        cur.execute(f"UPDATE client SET {and_str} WHERE id = %s;", (tuple(tup), client_id))
        if number is not None and number != "":
            cur.execute("SELECT id FROM number_phone WHERE id_client=%s;", (client_id,))
            rez1 = cur.fetchone()
            cur.execute("UPDATE number_phone SET number=%s WHERE id=%s", (number, rez1[0]))  
    print("Данные обновлены")

def delete_phone(cur, id_client, number):
    cur.execute("SELECT id_client, number FROM number_phone;")
    rez = cur.fetchall()
    rez1 = [1 for k in rez if k[0] == id_client and k[1] == number]
    if len(rez1) == 0:
        print("Ошибка в введенных данных",)
    else:
        cur.execute("DELETE FROM number_phone WHERE id_client=%s AND number=%s;", (id_client, number))
        print("Телефон успешно удален.")

def delete_client(cur, id_client):
    cur.execute("SELECT id FROM client WHERE id=%s;", (id_client, ))
    rez = cur.fetchone()
    if len(rez) == 0:
        print("Такого клиента нет")
    else:
        cur.execute("DELETE FROM number_phone WHERE id_client=%s;", (id_client))
        cur.execute("DELETE FROM client WHERE id=%s;", (id_client, ))
        print("Информация о клиенте удалена")

def find_client(cur, first_name=None, surname=None, email=None, number=None):
    str = []
    tup = []
    if first_name is not None and first_name != "":
        str.append("first_name=%s")
        tup.append(first_name)
    if surname is not None and surname != "":
        str.append("surname=%s")
        tup.append(surname)
    if email is not None and email != "":
        str.append("email=%s")
        tup.append(email)
    if number is not None and number != "":
        str.append("number=%s")
        tup.append(number)
    and_str = ' AND '.join(str)

    cur.execute(f"""SELECT client.id, first_name, surname, email, number FROM client 
                RIGHT JOIN number_phone ON client.id = number_phone.id_client 
                WHERE {and_str}""" , (tuple(tup)))
    rez = cur.fetchall()
    if len(rez) == 0:
        print("Пользователя с такими данными нет")
    else:
        for i in rez:
            print(f"id: {i[0]}, Имя:{i[1]}, Фамилия:{i[2]}, Почта:{i[3]}, Телефон: {i[4]}")

if __name__ == "__main__":
    with psycopg2.connect(database='client_Python', user='postgres', password='29092003') as conn:
        with conn.cursor() as cur:

            while(True):
                print("""Что вам нужно сделать? Введите нужную цифру:
                    1. Создать таблицы для хранения данных;
                    2. Добавить нового клиента;
                    3. Добавить телефон существующему клиенту;
                    4. Изменить данные о клиенте;
                    5. Удалить телефон у существующего клиента;
                    6. Удалить существующего клиента;
                    7. Найти клиента по его данным;  
                    8. Все удалить;     
                    9. Выход      """)
                enter = int(input("Введите команду: "))
                if enter == 1:
                    create_table(cur)
                    input("Нажмите Enter чтобы продолжить...")

                elif enter == 2:
                    first_name = input("Введите имя клиента: ")
                    surname = input("Введите фамилию клиента: ")
                    email = input("Введите электронную почту клиента: ")
                    number = input("Введите мобильный номер телефона: ")
                    add_client(cur, first_name, surname, email, number)
                    input("Нажмите Enter чтобы продолжить...")

                elif enter == 3:
                    id_client = input("Введите id клиента: ")
                    number = input("Введите номер телефона клиента: ")
                    add_phone(cur, id_client, number)
                    input("Нажмите Enter чтобы продолжить...")

                elif enter == 4:
                    client_id = input("Введите идентификатор клиента: ")
                    first_name = input("Введите имя клиента: ")
                    surname = input("Введите фамилию клиента: ")
                    email = input("Введите электронную почту клиента: ")
                    phones = input("Введите мобильный номер телефона: ")
                    change_info(cur, client_id, first_name, surname, email, phones)
                    input("Нажмите Enter чтобы продолжить...")

                elif enter == 5:
                    id_client = int(input("Введите идентификатор клиента: "))
                    phones = input("Введите мобильный номер телефона: ")
                    delete_phone(cur, id_client, phones)
                    input("Нажмите Enter чтобы продолжить...")
                
                elif enter == 6:
                    id_client = input("Введите идентификатор клиента: ")
                    delete_client(cur, id_client)
                    input("Нажмите Enter чтобы продолжить...")

                elif enter == 7:
                    first_name = input("Введите имя клиента: ")
                    surname = input("Введите фамилию клиента: ")
                    email = input("Введите электронную почту клиента: ")
                    number = input("Введите мобильный номер телефона: ")
                    find_client(cur, first_name, surname, email, number)
                    input("Нажмите Enter чтобы продолжить...")

                elif enter == 8:
                    delete_table(cur)
                    input("Нажмите Enter чтобы продолжить...")
                else:
                    print("Вы вышли из программы! Улюлюлюлю")

                    break
        
                

    conn.close()  