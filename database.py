import hashlib
import hmac
import os
from pathlib import Path

import aiosqlite

DB_DIR = Path("/data")
DB_NAME = DB_DIR / "content.db"


async def init_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("PRAGMA foreign_keys = ON")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            login TEXT NOT NULL,
            password TEXT NOT NULL
            )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            price INTEGER,
            end_date TEXT NOT NULL,
            reminded_5_days INTEGER DEFAULT 0,
            reminded_1_day INTEGER DEFAULT 0,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS mail_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        await db.execute("""
        CREATE TABLE  IF NOT EXISTS mail_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mail_id INTEGER NOT NULL,
            service_name TEXT NOT NULL,
            login TEXT,
            comment TEXT,
            FOREIGN KEY(mail_id) REFERENCES mail_accounts(id) ON DELETE CASCADE
            )
        """)



 
#USER------------------------------------------------------------------------------------

async def add_user(telegram_id, login, password):
    password_hash = _hash_password(password)
    async with aiosqlite.connect(DB_NAME) as db:
        try:
            await db.execute("""
                INSERT INTO users (telegram_id, login, password)
                VALUES (?, ?, ?)
            """, (telegram_id, login, password_hash))
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def get_user_by_telegram_id(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
                    SELECT * FROM users WHERE telegram_id = ?
                """, (telegram_id,))
        return await cursor.fetchone()


async def get_user_by_id(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
                    SELECT * FROM users WHERE id = ?
                """, (user_id,))
        return await cursor.fetchone()


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    iterations = 100_000
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}"


def _verify_password(stored_hash: str, password: str) -> bool:
    try:
        algo, iterations_str, salt_hex, digest_hex = stored_hash.split("$", 3)
    except ValueError:
        return False
    if algo != "pbkdf2_sha256":
        return False
    try:
        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(digest.hex(), digest_hex)


async def verify_user_password(telegram_id, password):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
                    SELECT password FROM users WHERE telegram_id = ?
                """, (telegram_id,))
        row = await cursor.fetchone()
        if not row:
            return False
        return _verify_password(row[0], password)


#MOVIE------------------------------------------------------------------------------------

async def add_movie(user_id, title, type_, comment):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO movies (user_id, title, type, comment)
            VALUES (?, ?, ?, ?)
        """, (user_id, title, type_, comment))
        await db.commit()


async def get_movies(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""SELECT * FROM movies WHERE user_id = ?""", (user_id,))
        result = await cursor.fetchall()
        return result


async def delete_movie(user_id, movie_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""DELETE FROM movies WHERE id = ? AND user_id = ?""", (movie_id, user_id))
        await db.commit()

#NOTES------------------------------------------------------------------------------------

async def add_note(user_id, title, due_date=None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO notes (user_id, title, due_date)
            VALUES (?, ?, ?)
        """, (user_id, title, due_date))
        await db.commit()


async def get_notes(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT * FROM notes WHERE user_id = ?
        """, (user_id,))
        return await cursor.fetchall()


async def delete_note(user_id, note_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            DELETE FROM notes WHERE id = ? AND user_id = ?
        """, (note_id, user_id))
        await db.commit()

#SUBS------------------------------------------------------------------------------------

async def add_subscription(user_id, title, price, end_date, comment):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO subscriptions (user_id, title, price, end_date, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, title, price, end_date, comment))
        await db.commit()

async def get_subscriptions(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT * FROM subscriptions WHERE user_id = ? ORDER BY end_date ASC
            """, (user_id,))
        return await cursor.fetchall()


async def delete_subscription(user_id, subscription_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        DELETE FROM subscriptions WHERE id = ? AND user_id = ?
            """, (subscription_id, user_id))
        await db.commit()

#FLAG_SUBS-------------------------------------------------------------------------------------

async def get_all_subscriptions():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT * FROM subscriptions
            """)
        return await cursor.fetchall()

async def mark_reminded_5(subscription_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        UPDATE subscriptions SET reminded_5_days = 1 WHERE id = ?
            """, (subscription_id,))
        await db.commit()

async def mark_reminded_1(subscription_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        UPDATE subscriptions SET reminded_1_day = 1 WHERE id = ?
            """, (subscription_id,))
        await db.commit()

#MAIL-------------------------------------------------------------------------------------

async def add_mail(user_id, email):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("PRAGMA foreign_keys = ON")
        await db.execute("""
            INSERT INTO mail_accounts (user_id, email)
            VALUES (?, ?)
        """, (user_id, email))
        await db.commit()


async def get_mail(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("PRAGMA foreign_keys = ON")
        cursor = await db.execute("""SELECT * FROM mail_accounts WHERE user_id = ?""", (user_id,))
        return await cursor.fetchall()


async def delete_mail(user_id, mail_accounts_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("PRAGMA foreign_keys = ON")
        await db.execute("""DELETE FROM mail_accounts WHERE id = ? AND user_id = ?""", (mail_accounts_id, user_id))
        await db.commit()

#SERVICE-------------------------------------------------------------------------------------

async def add_service(user_id, mail_id, service_name, login, comment):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("PRAGMA foreign_keys = ON")
        cursor = await db.execute("""
            SELECT id FROM mail_accounts
            WHERE id = ? AND user_id = ?
        """, (mail_id, user_id))

        mail = await cursor.fetchone()

        if not mail:
            return False

        await db.execute("""
            INSERT INTO mail_services (mail_id, service_name, login, comment)
            VALUES (?, ?, ?, ?)
        """, (mail_id, service_name, login, comment))
        await db.commit()
        return True


async def get_services_by_mail(user_id, mail_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("PRAGMA foreign_keys = ON")
        cursor = await db.execute("""
            SELECT ms.*
            FROM mail_services ms
            JOIN mail_accounts ma ON ms.mail_id = ma.id
            WHERE ms.mail_id = ? AND ma.user_id = ?
            """, (mail_id, user_id))
        return await cursor.fetchall()


async def delete_service(user_id, service_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("PRAGMA foreign_keys = ON")
        await db.execute("""
            DELETE FROM mail_services 
            WHERE id = ?
            AND mail_id IN (
            SELECT id FROM mail_accounts
            WHERE user_id = ?
            )
        """, (service_id, user_id))
        await db.commit()
