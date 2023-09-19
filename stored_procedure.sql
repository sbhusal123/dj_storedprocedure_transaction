-- stored procedure
CREATE OR REPLACE FUNCTION buy_movie_ticket(
    p_movie_id INT,
    p_customer_email VARCHAR,
    OUT result_message VARCHAR,
    OUT status_code INT
) AS
$$
DECLARE
    v_movie_price DECIMAL;
    v_seats_available INT;
BEGIN
    -- Initialize the result_message to an empty string
    result_message := '';
    status_code := 200;

    -- Check if the movie exists and get its price and available seats
    SELECT price, seats_available
    INTO v_movie_price, v_seats_available
    FROM ticket_movie
    WHERE id = p_movie_id;

    -- Check if the movie exists
    IF NOT FOUND THEN
        result_message := 'Movie not found';
        status_code := 500;
    -- Check if there are available seats
    ELSIF v_seats_available <= 0 THEN
        result_message := 'No available seats for this movie';
        status_code := 500;
    ELSE
        -- Try to book the ticket
        INSERT INTO ticket_booking(movie_id, customer_email)
        VALUES (p_movie_id, p_customer_email);

        -- Check if the insertion was successful
        IF FOUND THEN
            -- Decrement available seats
            UPDATE ticket_movie
            SET seats_available = seats_available - 1
            WHERE id = p_movie_id;
            result_message := 'Ticket booked successfully';
            status_code := 200;
        ELSE
            result_message := 'Failed to book the ticket';
            status_code := 500;
        END IF;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- calling a stored procedure
select * from buy_movie_ticket(2, 'dmin@asd.asd')
