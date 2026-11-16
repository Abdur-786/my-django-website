from django.db import migrations


def repair_legacy_booking_fk(apps, schema_editor):
    connection = schema_editor.connection
    if connection.vendor != 'sqlite':
        return

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'users_customuser'"
        )
        customuser_exists = cursor.fetchone() is not None

        cursor.execute("PRAGMA foreign_key_list('bookings_booking')")
        foreign_keys = cursor.fetchall()
        references_customuser = any(str(row[2]) == 'users_customuser' for row in foreign_keys)

        if not customuser_exists and references_customuser:
            cursor.execute("PRAGMA foreign_keys = OFF")
            cursor.execute("ALTER TABLE bookings_booking RENAME TO bookings_booking_legacy")
            cursor.execute(
                """
                CREATE TABLE bookings_booking (
                    booking_ID integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    date date NOT NULL,
                    time time NOT NULL,
                    address varchar(255) NULL,
                    reason text NOT NULL,
                    service_type_id integer NOT NULL
                        REFERENCES services_servicetype (service_type_ID)
                        DEFERRABLE INITIALLY DEFERRED,
                    user_id bigint NOT NULL
                        REFERENCES users_myuser (id)
                        DEFERRABLE INITIALLY DEFERRED
                )
                """
            )
            cursor.execute(
                """
                INSERT INTO bookings_booking
                    (booking_ID, date, time, address, reason, service_type_id, user_id)
                SELECT
                    booking_ID, date, time, address, reason, service_type_id, user_id
                FROM bookings_booking_legacy
                """
            )
            cursor.execute("DROP TABLE bookings_booking_legacy")
            cursor.execute(
                "CREATE INDEX bookings_booking_service_type_id_f69c7e30 "
                "ON bookings_booking (service_type_id)"
            )
            cursor.execute(
                "CREATE INDEX bookings_booking_user_id_834dfc23 "
                "ON bookings_booking (user_id)"
            )
            cursor.execute("PRAGMA foreign_keys = ON")


class Migration(migrations.Migration):
    dependencies = [
        ('bookings', '0002_use_myuser'),
    ]

    operations = [
        migrations.RunPython(repair_legacy_booking_fk, migrations.RunPython.noop),
    ]
