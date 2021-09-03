import sqlite3
import json
import logging


def get_db():
    database = None
    try:
        database = sqlite3.connect('end-game.db')
        logging.debug(f"SQL database is connected")
        cursor = database.cursor()
        query = """CREATE TABLE IF NOT EXISTS requests(
						Method TEXT,
						URL TEXT,
						Params BLOB,
						Headers BLOB,
						Auth BLOB,
						Status INTEGER,
						Response BLOB,
						Body BLOB);"""
        logging.debug(f"SQL Query: {query}")
        cursor.execute(query)
        logging.info("Table init Done")
    except Exception as e:
        logging.error(e)

    return database


def add_history(data):
    try:
        database = get_db()
        cursor = database.cursor()
        col = ', '.join(data.keys())
        ph = ', '.join('?' * len(data))
        query = 'INSERT INTO requests ({}) VALUES ({})'.format(col, ph)
        logging.debug(f"SQL Query: {query}")
        values = [json.dumps(x) if type(x) == dict else x for x in data.values()]
        logging.debug(f"SQL Values: {values}")
        cursor.execute(query, values)
        database.commit()
        if cursor.rowcount:
            logging.info("Request added to Database")
    except Exception as e:
        logging.error(e)
    finally:
        if database:
            database.close()


def history():
    result = list()
    rows = []
    like = ""
    try:
        db = get_db()
        cursor = db.cursor()
        query = """SELECT * from (SELECT rowid as "..",Method,URL, PARAMS, BODY as "Request body", STATUS FROM "requests" order BY rowid DESC limit 10) order by ".." ASC"""
        logging.debug(f"SQL Query: {query}")
        results = cursor.execute(query).fetchall()
        if results == []:
            logging.warning("Table doesn't exist")
        else:
            widths = []
            columns = []
            tavnit = ' '
            separator = ' '

            column_num = 0
            for cd in cursor.description:
                if len(results) != 0:
                    element_max_width = max(list(map(lambda x: len(str(x[column_num])), results)))
                else:
                    element_max_width = 0
                widths.append(max(element_max_width, len(cd[0])) + 2)
                column_num += 1
                # widths.append(max(cd[2], len(cd[0])))
                columns.append(cd[0])

            for w in widths:
                tavnit += " %-" + "%ss   " % (w,)
                separator += '=' * w + '==  '

            print('---Request history---')
            print(separator)
            print(tavnit % tuple(columns))
            print(separator)

            printable_rows = list()
            callable_rows = list()

            for row in results:
                row_as_list = list(row)
                for n, column in enumerate(row_as_list):
                    if column == None:
                        row_as_list[n] = ""

                if row[3] != None:
                    PARAMS = json.loads(row[3])
                    for i, item in enumerate(PARAMS.items()):
                        if i == 0:
                            new_row = row_as_list
                            new_row[3] = f"{item[0]}: {item[1]}"
                            printable_rows.append(new_row)
                            callable_rows.append(new_row[0])
                        else:
                            new_row = ["", "", "", f"{item[0]}: {item[1]}", "", ""]
                            printable_rows.append(new_row)
                elif row[4] != None:
                    PARAMS = json.loads(row[4])
                    for i, item in enumerate(PARAMS.items()):
                        if i == 0:
                            new_row = row_as_list
                            new_row[3] = f"{item[0]}: {item[1]}"
                            printable_rows.append(new_row)
                            callable_rows.append(new_row[0])
                        else:
                            new_row = ["", "", "", f"{item[0]}: {item[1]}", "", ""]
                            printable_rows.append(new_row)
                else:
                    printable_rows.append(row_as_list)
                    callable_rows.append(row_as_list[0])

            for row in printable_rows:
                print(tavnit % tuple(row))

            print(separator)
            return callable_rows
    except Exception as e:
        logging.error(e)
    finally:
        if db:
            db.close()


def clear_history():
    try:
        db = get_db()
        cursor = db.cursor()
        query = """delete from "requests" """
        logging.debug(f"SQL Query: {query}")
        cursor.execute(query)
        db.commit()
    except Exception as e:
        print(f"Error clearing history {e}")
        logging.error(f"Error clearing history {e}")
    finally:
        if db:
            db.close()


def show_index_from_history(index):
    result_index = dict()
    try:
        db = get_db()
        cursor = db.cursor()
        query = f"""SELECT * FROM "requests" WHERE rowid in ({index})"""
        logging.debug(f"SQL Query: {query}")
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) > 0:
            for i in range(len(result[0])):
                result_index[cursor.description[i][0]] = result[0][i]
        else:
            logging.error(f"No such {index} in table")
    except Exception as e:
        print(f"Error showing history item {e}")
        logging.error(f"Error showing history item {e}")
    finally:
        if db:
            db.close()

    print(f'---Request {index}---')
    column_1_length = len("Basic Authentication")
    column_2_length = 0
    separator_1 = ""
    separator_2 = ""

    for element in result_index.items():
        if len(element[0]) > column_1_length:
            column_1_length = len(element[0])
        if element[1] != None and element[0] != "Response":
            if len(str(element[1])) > column_2_length:
                column_2_length = len(str(element[1]))

        # Check PARAMS Length

    separator_1 += '=' * column_1_length + '==  '
    separator_2 += '=' * column_2_length + '==  '

    print(separator_1, separator_2)
    print(f"Method" + " " * (column_1_length + 4 - len('Method')), result_index['Method'])
    print(f"URL" + " " * (column_1_length + 4 - len('URL')), result_index['URL'])

    if result_index['Params']:
        PARAMS = json.loads(result_index['Params'])
        for i, item in enumerate(PARAMS.items()):
            if i == 0:
                print(f"Params" + " " * (column_1_length + 4 - len('Params')), item[0], "=", item[1])

            else:
                print(" " * (column_1_length + 4), item[0], " = ", item[1])
    else:
        print("Params")
    if result_index['Headers']:
        HEADERS = json.loads(result_index['Headers'])
        for i, item in enumerate(HEADERS.items()):
            if i == 0:
                print(f"Headers" + " " * (column_1_length + 4 - len('Headers')), item[0], ":", item[1])

            else:
                print(" " * (column_1_length + 4), item[0], " = ", item[1])
    else:
        print("Headers")
    print(f"Request Body" + " " * (column_1_length + 4 - len('Request Body')),
          "" if result_index['Body'] is None else result_index['Body'])
    if result_index['Auth']:
        auth = result_index['Auth'].split("'")
        print(f"Basic Authentication" + " " * (column_1_length + 4 - len('Basic Authentication')), "User: ", auth[1])
        print(" " * (column_1_length + 4), "Pasword: ", auth[3])
    else:
        print("Basic Authentication")
    print(f"Status" + " " * (column_1_length + 4 - len('Status')), result_index['Status'])
    print(separator_1, separator_2)
    print("---Response---")
    print(result_index['Response'])
