import duckdb
import pandas as pd
class DuckClient:
    def __init__(self,db_path:str="riskengine.duckdb"):
        self.conn=duckdb.connect(db_path)
    def create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prices (
                Date TIMESTAMP,
                Open DOUBLE,
                High DOUBLE,
                Low DOUBLE,
                Close DOUBLE,
                Volume DOUBLE
            )
            """
        )
    def insert_data(self,df:pd.DataFrame):
        self.conn.register("temp_df", df)
        self.conn.execute("INSERT INTO prices SELECT * FROM temp_df")
    def query(self,sql:str):
        return self.conn.execute(sql).fetchdf()
    