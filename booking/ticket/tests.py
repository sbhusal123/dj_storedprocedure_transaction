from django.test import TestCase

from .models import Movie, Booking
from django.db import connections

import threading


class BookingTestCase(TestCase):

    def call_stored_procedure(
            self,
            movie_id,
            customer_email,
            seat_number
    ):
        procedure_name = 'buy_movie_ticket'

        db_connection = connections['default']

        connection_copy = db_connection.copy()

        with connection_copy.cursor() as cursor:
            cursor.callproc(procedure_name, (
                movie_id, customer_email, seat_number))

            result = cursor.fetchall()
            print(result)

        db_connection.commit()

    def test_perform_multiple_booking(self):
        try:
            movie = Movie.objects.create(
                name="Movie Title",
                price=9.99,
                time="18:30:00",
                date="2023-09-19",
                seats_available=100
            )
            movie.save()
        except Exception as e:
            print("Error creating a movie", e)

        movie_id = movie.pk
        email = "faker@gmail.com"
        seat = "M20"

        threads = []
        for _ in range(5):
            thread = threading.Thread(
                target=self.call_stored_procedure,
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

        movie_booking_count = Booking.objects.filter(
            movie=movie,
            seat_number=seat
        ).count()

        self.assertEqual(movie_booking_count, 1)
