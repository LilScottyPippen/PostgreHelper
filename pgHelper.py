import psycopg2
import os
import time
from prettytable import PrettyTable


print(
    "    _______  _______  _______  _________ _______  _______  _______ \n"
    "   (  ____ )(  ___  )(  ____ \ \__   __/( ____  \(  ____ )(  ____ \ \n"
    "   | (    )|| (   ) || (    \/    ) (   | (    \/| (    )|| (    \/\n"
    "   | (____)|| |   | || (_____     | |   | |      | (____)|| (__\n"
    "   |  _____)| |   | |(_____  )    | |   | | ____ |     __)|  __)\n"
    "   | (      | |   | |      ) |    | |   | | \_  )| (\ (   | (\n"
    "   | )      | (___) |/\____) |    | |   | (___) || ) \ \__| (____/\ \n"
    "   |/       (_______)\_______)    )_(   (_______)|/   \__/(_______/\n"

    "                  _______  _        _______  _______  _______\n"
    "        |\     /|(  ____ \( \      (  ____ )(  ____ \(  ____ )\n"
    "        | )   ( || (    \/| (      | (    )|| (    \/| (    )|\n"
    "        | (___) || (__    | |      | (____)|| (__    | (____)|\n"
    "        |  ___  ||  __)   | |      |  _____)|  __)   |     __)\n"
    "        | (   ) || (      | |      | (      | (      | (\ (\n"
    "        | )   ( || (____/\| (____/\| )      | (____/\| ) \ \__\n"
    "        |/     \|(_______/(_______/|/       (_______/|/   \__/\n"
)
class DB:
    def __init__(self, db, user, password, host, port):
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def connection(self):
        try:
            self.conn = psycopg2.connect(database=self.db,
                                         user=self.user,
                                         password=self.password,
                                         host=self.host,
                                         port=self.port)
            print('Connect done ✓')
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            print('Connect error!')
            exit()

    def save_connection(self):
        lines = [f'DataBase:{self.db}\nUser:{self.user}\nPassword:{self.password}\nHost:{self.host}\nPort:{self.port}']

        with open(f'{self.db}.txt', 'w') as f:
            f.writelines(lines)

    def load_connection(self):
        with open(f'{self.db}.txt') as f:
            lines = f.readlines()
        data = {}
        for line in lines:
            key, value = line.strip().split(':')
            data[key] = value
        self.user = data['User']
        self.password = data['Password']
        self.host = data['Host']
        self.port = data['Port']
        return True

    def show_tables(self):
        self.connection()
        cur = self.conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")

        rows = cur.fetchall()

        for row in rows:
            print(row[0])

        cur.close()

    def select_tables(self):
        self.connection()
        cur = self.conn.cursor()
        try:
            column = input('Column: ')
            table = input('Table: ')
            cur.execute(f'SELECT {column} FROM {table}')

            rows = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            table = PrettyTable(column_names)
            for row in rows:
                table.add_row(row)
            print(table)
        except:
            print('Error!')

        cur.close()

if __name__ == '__main__':
    db = input('DataBase: ')
    connector = DB(db, '', '', '', '')
    if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{db}.txt')):
        is_load = input('Load DB? [y/n]: ')
        if is_load == 'y' or is_load == 'Y':
            loadCon = connector.load_connection()
        else:
            user = input('Username: ')
            password = input('Password: ')
            host = input('Host: ')
            port = input('Port: ')
            connector = DB(db, user, password, host, port)
            is_save = input('Save connection? [y/n]: ')
            if is_save == 'y' or 'Y':
                connector.save_connection()
    else:
        user = input('Username: ')
        password = input('Password: ')
        host = input('Host: ')
        port = input('Port: ')
        connector = DB(db, user, password, host, port)
        is_save = input('Save connection? [y/n]: ')
        if is_save == 'y' or is_save == 'Y':
            connector.save_connection()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('1. Show tables\n2. SELECT')
        choose = input('Choose: ')

        if choose == '1':
            connector.show_tables()
            input('\nPress Enter')

        if choose == '2':
            connector.select_tables()
            input('\nPress Enter')