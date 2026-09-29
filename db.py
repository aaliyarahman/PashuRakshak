import sqlite3

from pathlib import Path

from datetime import datetime


DB_PATH = (
    Path(__file__).parent
    / "data"
    / "pashurakshak.db"
)


DB_PATH.parent.mkdir(
    exist_ok=True
)


def conn():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def _now():

    return datetime.now().isoformat(
        timespec="seconds"
    )


def init_db():

    connection = conn()

    connection.executescript(
        """

        CREATE TABLE IF NOT EXISTS herds(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            species TEXT,

            breed TEXT,

            count INTEGER,

            district TEXT,

            taluk TEXT,

            location TEXT,

            created_at TEXT

        );


        CREATE TABLE IF NOT EXISTS health_cases(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            herd_id INTEGER,

            affected_count INTEGER,

            status TEXT,

            notes TEXT,

            created_at TEXT

        );


        CREATE TABLE IF NOT EXISTS vaccines(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            herd_id INTEGER,

            vaccine TEXT,

            next_due TEXT,

            created_at TEXT

        );


        CREATE TABLE IF NOT EXISTS movements(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            herd_id INTEGER,

            from_place TEXT,

            to_place TEXT,

            lat REAL,

            lon REAL,

            created_at TEXT

        );


        CREATE TABLE IF NOT EXISTS orders(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            pharmacy TEXT,

            item TEXT,

            qty INTEGER,

            status TEXT,

            created_at TEXT,

            price REAL DEFAULT 0,

            payment_method TEXT DEFAULT '',

            payment_status TEXT DEFAULT '',

            order_status TEXT DEFAULT 'Placed',

            pharmacy_phone TEXT DEFAULT ''

        );


        CREATE TABLE IF NOT EXISTS pharmacies(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            district TEXT,

            lat REAL,

            lon REAL,

            phone TEXT,

            upi_id TEXT

        );


        CREATE TABLE IF NOT EXISTS health_updates(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT,

            message TEXT,

            category TEXT,

            created_at TEXT

        );

        """
    )


    pharmacy_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM pharmacies
        """
    ).fetchone()[0]


    if pharmacy_count == 0:

        connection.executemany(
            """
            INSERT INTO pharmacies
            (
                name,
                district,
                lat,
                lon,
                phone,
                upi_id
            )

            VALUES (?, ?, ?, ?, ?, ?)
            """,

            [

                (
                    "Pashu Care Pharmacy",
                    "Davanagere",
                    14.4644,
                    75.9218,
                    "0000000000",
                    "pashucare@upi",
                ),

                (
                    "Animal Health Store",
                    "Bengaluru",
                    12.9716,
                    77.5946,
                    "0000000000",
                    "animalhealth@upi",
                ),

                (
                    "Veterinary Medicine Centre",
                    "Mysuru",
                    12.2958,
                    76.6394,
                    "0000000000",
                    "vetcare@upi",
                ),

            ],
        )


    update_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM health_updates
        """
    ).fetchone()[0]


    if update_count == 0:

        connection.executemany(
            """
            INSERT INTO health_updates
            (
                title,
                message,
                category,
                created_at
            )

            VALUES (?, ?, ?, ?)
            """,

            [

                (
                    "Daily Animal Health",
                    "Check animals for changes in appetite, movement, breathing and behaviour.",
                    "Daily Care",
                    _now(),
                ),

                (
                    "Clean Drinking Water",
                    "Make sure animals have access to clean drinking water every day.",
                    "Prevention",
                    _now(),
                ),

                (
                    "Seasonal Care",
                    "Increase observation during major changes in weather.",
                    "Seasonal",
                    _now(),
                ),

            ],
        )


    connection.commit()

    connection.close()


# ============================================================
# HERDS
# ============================================================

def add_herd(
    species,
    breed,
    count,
    district,
    taluk,
    location,
):

    connection = conn()

    connection.execute(
        """
        INSERT INTO herds
        (
            species,
            breed,
            count,
            district,
            taluk,
            location,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,

        (
            species,
            breed,
            count,
            district,
            taluk,
            location,
            _now(),
        ),
    )

    connection.commit()

    connection.close()


def list_herds():

    return _query_records(
        """
        SELECT
            id,
            species,
            breed,
            count,
            district,
            taluk,
            location,
            created_at

        FROM herds

        ORDER BY id DESC
        """
    )


# ============================================================
# HEALTH CASES
# ============================================================

def add_health_case(
    herd_id,
    affected_count,
    status,
    notes,
):

    connection = conn()

    connection.execute(
        """
        INSERT INTO health_cases
        (
            herd_id,
            affected_count,
            status,
            notes,
            created_at
        )

        VALUES (?, ?, ?, ?, ?)
        """,

        (
            herd_id,
            affected_count,
            status,
            notes,
            _now(),
        ),
    )

    connection.commit()

    connection.close()


def list_cases():

    return _query_records(
        """
        SELECT
            id,
            herd_id,
            affected_count,
            status,
            notes,
            created_at

        FROM health_cases

        ORDER BY id DESC
        """
    )


# ============================================================
# VACCINES
# ============================================================

def add_vaccine(
    herd_id,
    vaccine,
    next_due,
):

    connection = conn()

    connection.execute(
        """
        INSERT INTO vaccines
        (
            herd_id,
            vaccine,
            next_due,
            created_at
        )

        VALUES (?, ?, ?, ?)
        """,

        (
            herd_id,
            vaccine,
            next_due,
            _now(),
        ),
    )

    connection.commit()

    connection.close()


def list_vaccines():

    return _query_records(
        """
        SELECT
            id,
            herd_id,
            vaccine,
            next_due,
            created_at

        FROM vaccines

        ORDER BY next_due
        """
    )


# ============================================================
# MOVEMENTS
# ============================================================

def add_movement(
    herd_id,
    from_place,
    to_place,
    lat,
    lon,
):

    connection = conn()

    connection.execute(
        """
        INSERT INTO movements
        (
            herd_id,
            from_place,
            to_place,
            lat,
            lon,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,

        (
            herd_id,
            from_place,
            to_place,
            lat,
            lon,
            _now(),
        ),
    )

    connection.commit()

    connection.close()


def list_movements():

    return _query_records(
        """
        SELECT
            id,
            herd_id,
            from_place,
            to_place,
            lat,
            lon,
            created_at

        FROM movements

        ORDER BY id DESC
        """
    )


# ============================================================
# PHARMACY
# ============================================================

def add_order(
    pharmacy,
    item,
    qty,
    status,
    price,
    payment_method,
    payment_status,
    order_status,
    pharmacy_phone,
):

    connection = conn()

    connection.execute(
        """
        INSERT INTO orders
        (
            pharmacy,
            item,
            qty,
            status,
            created_at,
            price,
            payment_method,
            payment_status,
            order_status,
            pharmacy_phone
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            pharmacy,
            item,
            qty,
            status,
            _now(),
            price,
            payment_method,
            payment_status,
            order_status,
            pharmacy_phone,
        ),
    )

    connection.commit()

    connection.close()


def list_orders():

    return _query_records(
        """
        SELECT
            id,
            pharmacy,
            item,
            qty,
            price,
            payment_method,
            payment_status,
            order_status,
            pharmacy_phone,
            created_at

        FROM orders

        ORDER BY id DESC
        """
    )


def search_pharmacies(
    lat=None,
    lon=None,
):

    return _query_records(
        """
        SELECT
            id,
            name,
            district,
            lat,
            lon,
            phone,
            upi_id

        FROM pharmacies

        ORDER BY name
        """
    )


# ============================================================
# UPDATES
# ============================================================

def list_health_updates():

    return _query_records(
        """
        SELECT
            id,
            title,
            message,
            category,
            created_at

        FROM health_updates

        ORDER BY id DESC
        """
    )


# ============================================================
# HELPERS
# ============================================================

def _rows_to_records(rows):

    return [
        dict(row)
        for row in rows
    ]


def _query_records(
    sql,
    params=(),
):

    connection = conn()

    rows = connection.execute(
        sql,
        params,
    ).fetchall()

    connection.close()

    return _rows_to_records(
        rows
    )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_stats():

    connection = conn()


    animals = connection.execute(
        """
        SELECT
            COALESCE(
                SUM(count),
                0
            )

        FROM herds
        """
    ).fetchone()[0]


    diseased = connection.execute(
        """
        SELECT
            COALESCE(
                SUM(affected_count),
                0
            )

        FROM health_cases

        WHERE status IN
        (
            'Confirmed by Vet',
            'Suspected'
        )
        """
    ).fetchone()[0]


    observation = connection.execute(
        """
        SELECT
            COALESCE(
                SUM(affected_count),
                0
            )

        FROM health_cases

        WHERE status =
        'Under Observation'
        """
    ).fetchone()[0]


    deaths = connection.execute(
        """
        SELECT
            COALESCE(
                SUM(affected_count),
                0
            )

        FROM health_cases

        WHERE status =
        'Deceased'
        """
    ).fetchone()[0]


    connection.close()


    healthy = max(
        0,
        animals
        - diseased
        - observation
        - deaths,
    )


    return {
        "animals": animals,
        "healthy": healthy,
        "observation": observation,
        "diseased": diseased,
        "deaths": deaths,
    }