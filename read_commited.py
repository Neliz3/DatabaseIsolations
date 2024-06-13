from mysql.connector import Error
from datetime import datetime

from configs import create_connection


def non_repeatable_reads():
    """
    Shows how READ COMMITED isolation level works.
    Shows non-repeatable read: different results during one transaction.
    """
    cursor1 = None
    cursor2 = None
    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1 [BEFORE]: Non-repeatable Reads
        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='READ COMMITTED')
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_non_repeatable_reads = cursor1.fetchone()[0]

        print(f"Non-repeatable Reads (READ COMMITTED) BEFORE: Alice's balance = {balance_non_repeatable_reads}")

        # Transaction 2: Non-repeatable Reads
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='READ COMMITTED')
        cursor2.execute("UPDATE accounts SET balance = 7777 WHERE name = 'Alice'")
        print(f"Transaction 2 commit(): {datetime.now()}")
        connection2.commit()

        # Transaction 1 [AFTER]: Non-repeatable Reads
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_non_repeatable_reads = cursor1.fetchone()[0]

        print(f"Non-repeatable Reads (READ COMMITTED) AFTER: Alice's balance = {balance_non_repeatable_reads}")

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
