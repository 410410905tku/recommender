import mysql.connector
import pandas as pd

def query_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="81643895mysql",
            database="recommender"
        )

        query = "SELECT * FROM merged_data"
        professor_history = pd.read_sql(query, conn)
        return professor_history

    except Exception as e:
        print("發生錯誤：", e)
        input("程式停止。請按 Enter 鍵繼續...")
        return None

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

query_database()
