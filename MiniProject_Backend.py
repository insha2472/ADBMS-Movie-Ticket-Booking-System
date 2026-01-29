import sqlite3

def connect():
    return sqlite3.connect("movie1.db")

def MovieData():
    con = connect()
    cur = con.cursor()

    # Movies table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id TEXT,
        movie_name TEXT,
        release_date TEXT,
        director TEXT,
        cast TEXT,
        budget TEXT,
        duration TEXT,
        rating TEXT
    )
    """)

    # Shows table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS shows (
        show_id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id TEXT,
        show_date TEXT,
        show_time TEXT,
        total_seats INTEGER,
        available_seats INTEGER
    )
    """)

    # Bookings table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        show_id INTEGER,
        customer_name TEXT,
        seats_booked INTEGER
    )
    """)

    con.commit()
    con.close()

def AddMovieRec(movie_id, movie_name, release_date, director, cast, budget, duration, rating):
    con = connect()
    cur = con.cursor()
    cur.execute("""
    INSERT INTO movies
    (movie_id, movie_name, release_date, director, cast, budget, duration, rating)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (movie_id, movie_name, release_date, director, cast, budget, duration, rating))
    con.commit()
    con.close()

def ViewMovieData():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM movies")
    rows = cur.fetchall()
    con.close()
    return rows

def DeleteMovieRec(id):
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM movies WHERE id=?", (id,))
    con.commit()
    con.close()

def create_trigger():
    con = sqlite3.connect("movie1.db")
    cur = con.cursor()

    cur.execute("""
    CREATE TRIGGER IF NOT EXISTS prevent_overbooking
    BEFORE INSERT ON bookings
    BEGIN
        SELECT
        CASE
            WHEN (SELECT available_seats FROM shows WHERE show_id = NEW.show_id) < NEW.seats_booked
            THEN RAISE(ABORT, 'Seats not available')
        END;
    END;
    """)

    cur.execute("""
    CREATE TRIGGER IF NOT EXISTS reduce_seats_after_booking
    AFTER INSERT ON bookings
    BEGIN
        UPDATE shows
        SET available_seats = available_seats - NEW.seats_booked
        WHERE show_id = NEW.show_id;
    END;
    """)

    con.commit()
    con.close()      
def AddShow(movie_id, show_date, show_time, total_seats):
    con = connect()
    cur = con.cursor()
    cur.execute("""
    INSERT INTO shows (movie_id, show_date, show_time, total_seats, available_seats)
    VALUES (?, ?, ?, ?, ?)
    """, (movie_id, show_date, show_time, total_seats, total_seats))
    con.commit()
    con.close()
def ViewShows():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM shows")
    rows = cur.fetchall()
    con.close()
    return rows
def BookTicket(show_id, customer_name, seats):
    con = connect()
    cur = con.cursor()
    cur.execute("""
    INSERT INTO bookings (show_id, customer_name, seats_booked)
    VALUES (?, ?, ?)
    """, (show_id, customer_name, seats))
    con.commit()
    con.close()
def CheckSeats(show_id):
    con = connect()
    cur = con.cursor()
    cur.execute("""
    SELECT available_seats FROM shows WHERE show_id=?
    """, (show_id,))
    result = cur.fetchone()
    con.close()
    return result[0] if result else 0