from mysql.connector import Error
from datetime import datetime

from configs import create_connection


def deadlock():
    """
    Shows how a deadlock occurs.
    """
    cursor1 = None
    cursor2 = None
    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        connection1.start_transaction()
        connection2.start_transaction()

        # Transaction 1: Deadlock
        print(f"Transaction 1 started: {datetime.now()}")
        cursor1.execute("UPDATE accounts SET balance = 7899 WHERE id = 1")
        cursor1.execute("UPDATE accounts SET balance = 6969 WHERE id = 3")
        print(f"Transaction 1 commit(): {datetime.now()}")

        # Transaction 2: Deadlock
        print(f"Transaction 2 started: {datetime.now()}")
        cursor2.execute("UPDATE accounts SET balance = 6969 WHERE id = 3")
        cursor2.execute("UPDATE accounts SET balance = 7899 WHERE id = 1")
        print(f"Transaction 2 commit(): {datetime.now()}")

        connection1.commit()
        connection2.commit()

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
