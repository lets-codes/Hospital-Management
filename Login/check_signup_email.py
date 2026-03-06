import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'deepanshu'
}

def main():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
    except Exception as e:
        print(f"DB connect error: {e}")
        return
    cur = conn.cursor(dictionary=True)
    email = 'test_patient@test.com'
    try:
        cur.execute('SELECT * FROM login WHERE email = %s', (email,))
        rows = cur.fetchall()
        print(f"Found {len(rows)} rows for {email}:")
        for r in rows:
            print(r)
    except Exception as e:
        print(f"Query error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    main()
