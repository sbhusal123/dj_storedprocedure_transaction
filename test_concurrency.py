import psycopg2
import threading


# Function to simulate concurrent execution
def concurrent_insert(movie_id, customer_email, seat_number):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="booking",
            user="postgres",

            password="password"
        )

        cursor = conn.cursor()

        cursor.callproc("buy_movie_ticket", (
            movie_id, customer_email, seat_number))

        conn.commit()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


threads = []

movie_id = 1
email = "faker@gmail.com"
seat = "M20"

for i in range(20):
    thread = threading.Thread(
        target=concurrent_insert,
        args=(
            movie_id,
            email,
            seat
        )
    )
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()
