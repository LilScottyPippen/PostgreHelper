import psycopg2
import os
import time
from prettytable import PrettyTable
from termcolor import colored
import getpass


print(colored(
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
,"green"))
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
            print(colored('Connection...', 'yellow'))
            self.conn = psycopg2.connect(database=self.db,
                                         user=self.user,
                                         password=self.password,
                                         host=self.host,
                                         port=self.port)
            if self.conn != None:
                print(colored('Connect done ✓', 'green'))
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')
        except:
            print(colored('Connect error!', 'red'))
            exit()

    def save_connection(self):
        lines = [f'DataBase:{self.db}\nUser:{self.user}\nPassword:{self.password}\nHost:{self.host}\nPort:{self.port}']

        if not os.path.exists('DB'):
            os.makedirs('DB')

        with open(f'DB/{self.db}.txt', 'w') as f:
            f.writelines(lines)

    def load_connection(self):
        with open(f'DB/{self.db}.txt') as f:
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
        column_names = [desc[0] for desc in cur.description]
        table = PrettyTable(column_names)

        for row in rows:
            table.add_row(row)
        print(table)

        cur.close()

    def select_tables(self):
        self.connection()
        cur = self.conn.cursor()
        try:
            column = input('Column: ')
            table = input('Table: ')
            cur.execute(f"SELECT {column.lower()} FROM {table.lower()}")

            rows = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            table = PrettyTable(column_names)
            for row in rows:
                table.add_row(row)
            print(table)
        except:
            print(colored('Input Error!', 'red'))

        cur.close()

    def create_table(self):
        self.connection()
        cur = self.conn.cursor()
        tables = []
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")

        rows = cur.fetchall()

        for row in rows:
            tables.append(row[0])

        try:
            table_name = input('Table name: ')
            if str.isalpha(table_name) == True:
                if table_name in tables:
                    print(colored('A table with the same name already exists!', 'red'))
                else:
                    num_columns = int(input('Number of columns: '))
                    columns = []
                    for i in range(num_columns):
                        col_name = input(f'Column {i + 1} name: ')
                        col_type = input(f'Column {i + 1} data type: ')
                        columns.append(f'{col_name} {col_type}')
                    columns_str = ', '.join(columns)

                    cur.execute(f"CREATE TABLE {table_name} ({(columns_str)})")
                    self.conn.commit()
                    print(colored('Table created ✓', 'green'))
            else:
                print(colored('Invalid table name!', 'red'))
        except:
            print(colored('Input Error!', 'red'))
        cur.close()

    def delete_table(self):
        self.connection()
        cur = self.conn.cursor()
        tables = []
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")

        rows = cur.fetchall()

        for row in rows:
            tables.append(row[0])

        try:
            table_name = input('Table name: ')
            if table_name in tables:
                is_delete = input(colored(f'Delete table "{table_name}"? [y/n]: ', 'yellow'))
                if is_delete == 'y':
                    cur.execute(f"DROP TABLE {table_name}")
                    self.conn.commit()
                    print(colored('Table deleted ✓', 'green'))
                else:
                    print(colored('Canceled', 'red'))
            else:
                print(colored('Table name not found', 'red'))
        except:
            print(colored('Input Error!', 'red'))

    def update_table(self):
        self.connection()
        cur = self.conn.cursor()
        tables = []
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")

        rows = cur.fetchall()

        for row in rows:
            tables.append(row[0])

        try:
            table_name = input('Table name: ')
            if table_name in tables:
                column_name = input('Set column name: ')
                column_value = input('Set column value: ')
                where_column_name = input('Update column name: ')
                where_value = input('Update column value: ')
                os.system('cls' if os.name == 'nt' else 'clear')

                cur.execute(f"SELECT data_type FROM information_schema.columns WHERE table_name='{table_name}' AND column_name = '{column_name}'")
                row = cur.fetchall()

                cur.execute(f"SELECT data_type FROM information_schema.columns WHERE table_name='{table_name}' AND column_name = '{where_column_name}'")
                update_row = cur.fetchall()

                text_types = ['text', 'char', 'varchar']
                number_types = ['integer', 'bigint', 'smallint', 'numerical', 'decimal', 'real', 'double precision',
                                'boolean']

                for r in row:
                    query = ""
                    print(r)
                    if r in text_types:
                        query += f"UPDATE {table_name} SET {column_name} = '{column_value} '"
                    elif r in number_types:
                        query += f"UPDATE {table_name} SET {column_name} = {column_value} "
                    print(query)

                    for u_r in update_row:
                        print(u_r)
                        if u_r in text_types:
                            query += f"WHERE {where_column_name} = '{where_value}'"
                        elif u_r in number_types:
                            query += f"WHERE {where_column_name} = '{where_value}'"

                    print(query)

                self.conn.commit()
                print(colored(f'Column "{column_name}" in table "{table_name}" updated', 'green'))
                cur.execute(f"SELECT * FROM {table_name} WHERE {where_column_name} = '{where_value}'")
                rows = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                table = PrettyTable(column_names)
                for row in rows:
                    table.add_row(row)
                print(table)
            else:
                print(colored('Table name not found', 'red'))
        except:
            print(colored('Input error!', 'red'))

if __name__ == '__main__':
    db = input('DataBase: ')
    connector = DB(db, '', '', '', '')
    if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'DB/{db}.txt')):
        is_load = input(colored('Load DB? [y/n]: ', 'yellow'))
        if is_load == 'y' or is_load == 'Y':
            loadCon = connector.load_connection()
        else:
            user = input('Username: ')
            password = getpass.getpass('Password: ')
            host = input('Host: ')
            port = input('Port: ')
            connector = DB(db, user, password, host, port)
            connector.connection()
            print(colored('Connect done ✓', 'green'))
            is_save = input(colored('Save connection? [y/n]: ', 'yellow'))
            if is_save == 'y' or 'Y':
                connector.save_connection()
    else:
        user = input('Username: ')
        password = getpass.getpass('Password: ')
        host = input('Host: ')
        port = input('Port: ')
        connector = DB(db, user, password, host, port)
        connector.connection()
        print(colored('Connect done ✓', 'green'))
        is_save = input(colored('Save connection? [y/n]: ', 'yellow'))
        if is_save == 'y' or is_save == 'Y':
            connector.save_connection()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('1. Show tables\n2. SELECT\n3. CREATE TABLE\n4. DROP TABLE\n5. UPDATE TABLE')
        choose = input('Choose: ')

        match choose:
            case '1':
                connector.show_tables()
                input('\nPress Enter')
            case '2':
                connector.select_tables()
                input('\nPress Enter')
            case '3':
                connector.create_table()
                input('\nPress Enter')
            case '4':
                connector.delete_table()
                input('\nPress Enter')
            case '5':
                connector.update_table()
                input('\nPress Enter')