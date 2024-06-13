from mysql.connector import Error
from datetime import datetime

from configs import create_connection


def serializable():
    """
    Shows how SERIALIZABLE isolation level works.
    Solves previous issues.
    """
    cursor1 = None
    cursor2 = None
    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1 [BEFORE]: SERIALIZABLE
        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='SERIALIZABLE')
        cursor1.execute("SELECT COUNT(*) FROM accounts WHERE name = 'Tom'")
        count_serializable = cursor1.fetchone()[0]

        print(f"SERIALIZABLE BEFORE: count of rows = {count_serializable}")

        # Transaction 2: SERIALIZABLE
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='SERIALIZABLE')
        cursor2.execute("INSERT INTO accounts (name, balance) VALUES ('Tom', 1212)")
        print(f"Transaction 2 commit(): {datetime.now()}")
        connection2.commit()

        # Transaction 1 [AFTER]: SERIALIZABLE
        print(f"Transaction 1 continued: {datetime.now()}")
        cursor1.execute("SELECT COUNT(*) FROM accounts WHERE name = 'Tom'")
        count_serializable = cursor1.fetchone()[0]

        print(f"SERIALIZABLE AFTER: count of rows = {count_serializable}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()
