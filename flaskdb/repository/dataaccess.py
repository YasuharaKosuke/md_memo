from typing import Literal
from psycopg2 import sql, connect, ProgrammingError
import flaskdb.var as v
from flaskdb.model.memoModel import Memo


class DataAccess:

    # Constractor called when this class is used. 
    # It is set for hostname, port, dbname, useranme and password as parameters.
    def __init__(self, hostname, port, dbname, username, password):
        self.dburl = "host=" + hostname + " port=" + str(port) + \
                     " dbname=" + dbname + " user=" + username + \
                     " password=" + password

    # This method is used to actually issue query sql to database. 
    def execute(self, query, autocommit=True):
        with connect(self.dburl) as conn:
            if v.SHOW_SQL:
                print(query.as_string(conn))
            conn.autocommit = autocommit
            with conn.cursor() as cur:
                cur.execute(query)
                if not autocommit:
                    conn.commit()
                try:
                    return cur.fetchall()
                except ProgrammingError as e:
                    return None

    # For mainly debug, This method is used to show sql to be issued to database. 
    def show_sql(self, query):
        with connect(self.dburl) as conn:
            print(query.as_string(conn))

    
    def insert_memo(self, memo):
        query = sql.SQL("""
            INSERT INTO \"files\" ( {fields} ) VALUES ( {values} )
        """).format(
            tablename = sql.Identifier("files"),
            fields = sql.SQL(", ").join([
                sql.Identifier("file_name"),
                sql.Identifier("user_name"),
                sql.Identifier("share"),
                sql.Identifier("updated_at")
            ]),
            values = sql.SQL(", ").join([
                sql.Literal(memo.file_name),
                sql.Literal(memo.user_name),
                sql.Literal(memo.share),
                sql.Literal(memo.updated_at)
            ])
        )
        self.execute(query, autocommit=True)


    def search_memo_by_user_and_file(self, user_name, file_name):
        query = sql.SQL("""
            SELECT id FROM \"files\" WHERE user_name = {username} AND file_name = {filename}
        """).format(
            username = sql.Literal(user_name),
            filename = sql.Literal(file_name)
        )
        results = self.execute(query, autocommit=True)
        memo_list = []
        for r in results:
            memo = Memo()
            memo.id = r[0]
            memo.file_name = r[1]
            memo.user_id = r[2]
            memo.user_name = r[3]
            memo.share = r[4]
            memo.updated_at = r[5]
            memo.append(memo)
        return memo_list

