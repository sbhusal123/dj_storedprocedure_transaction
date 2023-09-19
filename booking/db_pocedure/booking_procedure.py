BUY_MOVIE_TICKET_PROCEDURE = """
-- stored procedure
CREATE OR REPLACE FUNCTION buy_movie_ticket(
    p_movie_id INT,
    p_customer_email VARCHAR,
    p_seat_number VARCHAR,
    OUT result_message VARCHAR,
    OUT status_code INT
) AS
$$
DECLARE
    v_seats_available INT;
    v_bookings_made INT;
    v_lock_id BIGINT;
    v_movie_seat_book_count INT;
BEGIN
    result_message := '';
    status_code := 200;

    SELECT  COUNT(*) as movie_seat_booking_count
    INTO v_movie_seat_book_count FROM ticket_booking
    WHERE seat_number = p_seat_number AND movie_id = p_movie_id;

    SELECT seats_available
    INTO v_seats_available
    FROM ticket_movie
    WHERE id = p_movie_id;

    SELECT COUNT(*) AS booking_count
    INTO v_bookings_made
    FROM ticket_booking
    WHERE movie_id = p_movie_id;

    v_lock_id = hashtext(p_movie_id || p_seat_number);

    RAISE NOTICE 'bookings made for movie= %', v_bookings_made;
    RAISE NOTICE 'seats available for movie= %', v_seats_available;
    RAISE NOTICE 'lock id= %', v_lock_id;

    -- check if id exists
    IF NOT FOUND THEN
        result_message := 'Movie with id not found';
        status_code := 500;
    -- if id exits
    ELSE
        -- if seat for movie is already booked
        IF v_movie_seat_book_count = 1 THEN
            result_message := 'Provided seat has already been booked.';
            status_code := 500;
        ELSE
            -- if seat row itself is not locked
            IF NOT pg_try_advisory_lock(v_lock_id) THEN
                result_message := 'Seat is locked.';
                status_code := 500;

            -- if not locked
            ELSE
                -- checks if number of bookings made exceeds
                IF v_bookings_made = v_seats_available THEN
                    result_message := 'No seats are available for provided movie id.';
                    status_code := 200;
                ELSE
                    -- lock
                    PERFORM pg_advisory_lock(v_lock_id);

                    -- insert record
                    INSERT INTO ticket_booking(movie_id, customer_email, seat_number)
                        VALUES (p_movie_id, p_customer_email, p_seat_number);

                    result_message := 'Seat booked successfully.';
                    status_code := 200;

                    -- unlock
                    PERFORM pg_advisory_unlock(v_lock_id);
                END IF;
            END IF;
        END IF;
    END IF;
END
$$ LANGUAGE plpgsql;
"""

DROP_BUY_MOVIE_TICKET_PROCEDURE = """
drop function buy_movie_ticket(integer, varchar, varchar, out varchar, out integer);
"""
