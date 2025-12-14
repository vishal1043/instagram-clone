import pymysql

def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="0808",
        database="instagram_clone",
        cursorclass=pymysql.cursors.DictCursor
    )
