import sqlite3


class SQLUtils(object):

    def __init__(self, db_name, table_name):
        self._db_name = db_name
        self._table_name = table_name
        self._connection = None
        self._cursor = None

    def get_cursor(self):
        if not self._connection:
            self._connection = sqlite3.connect(self._db_name)
        if not self._cursor:
            self._cursor = self._connection.cursor()

    def create_table_if_not_exist(self):
        self.get_cursor()
        self._cursor.execute('CREATE TABLE IF NOT EXISTS {}(chars TEXT, helper TEXT)'.format(self._table_name))

    def write(self, first_column, second_column):
        self._cursor.execute('INSERT INTO {} VALUES("{}", "{}") '.format(self._table_name, first_column, second_column))
        self._connection.commit()

    def get_last_processed_char(self):
        self._cursor.execute('SELECT chars FROM {}'.format(self._table_name))
        try:
            result = sorted(self._cursor.fetchall(), key=lambda item: (len(item[0]), item[0]))
            result = result[-1][0]
        except IndexError:
            result = None
        return result

    def close_connection(self):
        self._cursor.close()
        self._cursor = None
        self._connection.close()
        self._connection = None
