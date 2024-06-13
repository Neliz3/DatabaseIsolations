"""
Works as SERIALIZABLE
"""

from mysql.connector import Error
from datetime import datetime

from configs import create_connection


def phantom_reads():
    """
    Shows how REPEATABLE READ isolation level works.
    Shows phantom read: different count of rows during one transaction.
    """
    cursor1 = None
    cursor2 = None
    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1 [BEFORE]: REPEATABLE READ
        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='REPEATABLE READ')
        cursor1.execute("SELECT COUNT(*) FROM accounts WHERE name = 'Tom'")
        count_phantom_reads = cursor1.fetchone()[0]

        print(f"Phantom Read (REPEATABLE READ) BEFORE: count of rows = {count_phantom_reads}")

        # Transaction 2: REPEATABLE READ
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='REPEATABLE READ')
        cursor2.execute("INSERT INTO accounts (name, balance) VALUES ('Tom', 1212)")
        print(f"Transaction 2 commit(): {datetime.now()}")
        connection2.commit()

        # Transaction 1 [AFTER]: REPEATABLE READ
        print(f"Transaction 1 continued: {datetime.now()}")
        cursor1.execute("SELECT COUNT(*) FROM accounts WHERE name = 'Tom'")
        count_phantom_reads = cursor1.fetchone()[0]

        print(f"Phantom Read (REPEATABLE READ) AFTER: count of rows = {count_phantom_reads}")

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
