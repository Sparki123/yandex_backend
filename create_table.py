import psycopg2
from config import config


def create_tables():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute('''
         CREATE TABLE product (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL, 
            parent_id VARCHAR(255),
            price INTEGER,
            type VARCHAR(255) NOT NULL,
            update  VARCHAR(255) NOT NULL
        )''')
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
