import sqlite3
from functools import cached_property


class Liter:
    """ usage
        cls = Liter("dbname")

        # CREATE table
        cls.exec_sql("CREATE TABLE IF NOT EXISTS")

        # ALTER table
            # add col
            cls.exec_sql(f"ALTER TABLE {tbl} ADD COLUMN xxx INTEGER")
            # del col
            cls.exec_sql(f"ALTER TABLE {tbl} DROP COLUMN xxx")
            # rename table
            cls.exec_sql(f"ALTER TABLE {tbl} RENAME TO xxx")

        # DROP table
        cls.exec_sql(f"DROP TABLE IF EXISTS {tbl}")

        # INSERT - pass 2 args (sql, insert value)
        cls.exec_sql(f"INSERT INTO {tbl} (col1, col2) VALUES (?, ?)", ('val1', 'val2'))

        # DELETE row
        cls.exec_sql(f"DELETE FROM {tbl} WHERE xxx=xxx")

        # SELECT table
        res = cls.exec_sql(f"SELECT * FROM {tbl}")

        # UNION
        res = cls.exec_sql(f"SELECT * FROM {tbl} UNION SELECT * FROM {tbl2}")

        # JOIN
        join_type = 'INNER'
        join_type = 'LEFT'
        sql = f'''
            SELECT a.*, b.addr
            FROM {tbl} a
            {join_type} JOIN {tbl3} b
            ON a.username = b.username
        '''
        res = cls.exec_sql(sql)

    """
    master_table_name = 'sqlite_master'

    def __init__(self, db_name):
        self.db_name = db_name

    @cached_property
    def con(self):
        return sqlite3.connect(f'{self.db_name}.db')

    @cached_property
    def cursor(self):
        return self.con.cursor()

    def exec_sql(self, sql, extra=None):
        if not extra:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, extra)
        return self.cursor.fetchall()

    def get_show_create_table(self, table):
        return self.exec_sql(f"SELECT * FROM sqlite_master WHERE name = '{table}'")

    def get_cols_info(self, table):
        """
        (0, 'type', 'text', 0, None, 0): Information about the first column
            0:      Column ID (ordinal position of the column in the table, starting from 0).
            'type': Column name.
            'text': Data type of the column.
            0:      Indicates whether the column can store NULL values (0 for no, 1 for yes).
            None:   Default value of the column (in this case, it's not applicable or NULL).
            0:      Indicates whether the column is part of the primary key (0 for no, 1 for yes).
        :param table:
        :return:
        """
        return self.exec_sql(f"PRAGMA table_info({table})")

    def get_col_list(self, table):
        """
        [{"name": "", "type": ""}]
        :return:
        """
        li = []
        for row in self.get_cols_info(table):
            col_name = row[1]
            col_data_type = row[2]
            li.append({"name": col_name, "type": col_data_type})
        return li

    def commit(self):
        self.con.commit()

    def close(self):
        self.cursor.close()
        self.con.close()


if __name__ == '__main__':
    cls = Liter("next")
    tbl = 'users'
    tbl2 = 'another'
    tbl3 = 'addr'

    # create table
    sql = f'''
        CREATE TABLE IF NOT EXISTS {tbl} (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            addr TEXT NOT NULL
        )
    '''
    cls.exec_sql(sql)

    # insert table
    cls.exec_sql(f"INSERT INTO {tbl} (username, email) VALUES (?, ?)", ('john', 'john@example.com'))

    # alter - add col
    # cls.exec_sql(f"ALTER TABLE {tbl} ADD COLUMN age INTEGER")
    # alter - del col
    # cls.exec_sql(f"ALTER TABLE {tbl} DROP COLUMN email")
    # alter - rename table
    # cls.exec_sql(f"ALTER TABLE {tbl} RENAME TO hack")

    # delete row
    # cls.exec_sql(f"DELETE FROM {tbl} WHERE id=1")

    # delete table
    # cls.exec_sql(f"DROP TABLE IF EXISTS {tbl}")

    # get cols
    res = cls.get_col_list(tbl)
    for row in res:
        print(row)

    # select
    res = cls.exec_sql(f"SELECT * FROM {tbl}")
    res = cls.exec_sql(f"SELECT * FROM {tbl3}")
    # res = cls.exec_sql(f"SELECT * FROM hack")
    # union
    # res = cls.exec_sql(f"SELECT * FROM {tbl} UNION SELECT * FROM {tbl2}")
    # join
    # join_type = 'INNER'
    # join_type = 'LEFT'
    # sql = f"""
    # SELECT a.*, b.addr
    # FROM {tbl} a
    # {join_type} JOIN {tbl3} b
    # ON a.username = b.username
    # """
    # res = cls.exec_sql(sql)

    for row in res:
        print(row)

    cls.commit()
    cls.close()
