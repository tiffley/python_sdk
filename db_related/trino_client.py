import trino


host = ''
port = 400
user = ''
pw = ''

# inherit this class
class TrinoClient:
    def __init__(self, host, port, user, pw):
        self.conn = trino.dbapi.connect(
            host=host,
            port=port,
            user=user,
            http_scheme='https',
            auth=trino.auth.BasicAuthentication(user, pw),
            verify=False,
            request_timeout=trino.constants.DEFAULT_REQUEST_TIMEOUT
        )

    def get_conn(self):
        return self.conn

    def execute(self, sql, return_response=True) -> list:
        cur = self.conn.cursor()
        cur.execute(sql)
        if return_response:
            return cur.fetchall()

    @classmethod
    def print_sql(cls, sql):
        print(">>> generated SQL ---")
        print(sql)
        print("--- --- --- ---")


class TrinoParser(TrinoClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.catalogs = None

    def get_catalogs(self) -> list:
        if not self.catalogs:
            sql = "SHOW catalogs"
            rows = self.execute(sql)
            self.catalogs = [x[0] for x in rows]
        return self.catalogs

    def get_schemas(self, catalog) -> list:
        # = show databases
        sql = f"SHOW schemas from {catalog}"
        rows = self.execute(sql)
        return [x[0] for x in rows]

    def get_tables(self, catalog, schema) -> list:
        sql = f"SHOW tables from {catalog}.{schema}"
        rows = self.execute(sql)
        return [x[0] for x in rows]

    def get_table_schema(self, catalog, schema, table) -> str:
        sql = f"SHOW create table {catalog}.{schema}.{table}"
        rows = self.execute(sql)
        return rows[0][0]

    def get_table_schema_as_dict(self, catalog, schema, table) -> dict:
        txt = self.get_table_schema(catalog, schema, table)
        for row in txt.split('\n'):
            # name
            if row.startswith('CREATE TABLE'):
                pass
            # cols
            # params

    def get_columns(self, catalog, schema, table) -> list[dict]:
        # [{'Column': 'easy_id', 'Type': 'bigint', 'Extra': '', 'Comment': ''}, ...]
        sql = f'SHOW COLUMNS FROM {catalog}.{schema}.{table}'
        rows = self.execute(sql)
        #  Column   |     Type     | Extra | Comment
        # rows = [['easy_id', 'bigint', '', ''], ['edu_id', 'integer', '', ''], ...]
        return [{"Column": x[0], "Type": x[1], "Extra": x[2], "Comment": x[3]} for x in rows]


if __name__ == '__main__':
    kw = {"host":host, "port": port, "user":user, "pw":pw}
    cls = TrinoParser(**kw)

    res = cls.get_catalogs()
    print(res)


