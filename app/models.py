import logging
import sqlite3
from dataclasses import dataclass
from typing import Optional

from config import DATABASE, GOOD_TABLE, CATEGORY_TABLE

logger = logging.getLogger(__name__)


@dataclass
class Good:
    name: str
    price: float
    category_id: int
    id: Optional[int] = None

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class Category:
    name: str
    category_id: Optional[int] = None

    def __getitem__(self, item):
        return getattr(self, item)


def get_connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE)
    connection.execute('PRAGMA foreign_keys = ON')
    return connection


def init_db() -> None:
    logger.info('Initializing database')

    with get_connect() as connection:
        cursor = connection.cursor()

        cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {CATEGORY_TABLE} (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
            '''
        )

        cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {GOOD_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL DEFAULT 0,
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id)
                    REFERENCES {CATEGORY_TABLE}(category_id)
                    ON DELETE CASCADE
            );
            '''
        )

        default_categories = [
            'Books',
            'Clothes',
            'Phones',
            'For home',
            'Other',
        ]

        for category_name in default_categories:
            cursor.execute(
                f'''
                INSERT OR IGNORE INTO {CATEGORY_TABLE} (name)
                VALUES (?);
                ''',
                (category_name,)
            )

    logger.info('Database initialized')


def get_obj_good_from_row(row: tuple) -> Good:
    good_id, name, price, category_id = row
    return Good(id=good_id, name=name, price=price, category_id=category_id)


def get_obj_category_from_row(row: tuple) -> Category:
    category_id, name = row
    return Category(category_id=category_id, name=name)


def find_same_good_by_name(name: str) -> bool:
    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            SELECT id FROM {GOOD_TABLE}
            WHERE name = ?;
            ''',
            (name,)
        )
        return cursor.fetchone() is not None


def find_same_category_by_name(name: str) -> bool:
    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            SELECT category_id FROM {CATEGORY_TABLE}
            WHERE name = ?;
            ''',
            (name,)
        )
        return cursor.fetchone() is not None


def get_all_goods() -> list[Good]:
    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            SELECT id, name, price, category_id
            FROM {GOOD_TABLE};
            '''
        )
        rows = cursor.fetchall()
        return [get_obj_good_from_row(row) for row in rows]


def get_all_categories() -> list[Category]:
    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            SELECT category_id, name
            FROM {CATEGORY_TABLE};
            '''
        )
        rows = cursor.fetchall()
        return [get_obj_category_from_row(row) for row in rows]


def get_good_by_id(good_id: int) -> Optional[Good]:
    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            SELECT id, name, price, category_id
            FROM {GOOD_TABLE}
            WHERE id = ?;
            ''',
            (good_id,)
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return get_obj_good_from_row(row)


def get_category_by_id(category_id: int) -> Optional[Category]:
    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            SELECT category_id, name
            FROM {CATEGORY_TABLE}
            WHERE category_id = ?;
            ''',
            (category_id,)
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return get_obj_category_from_row(row)


def get_all_goods_by_category(category_id: int) -> list[Good]:
    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            SELECT id, name, price, category_id
            FROM {GOOD_TABLE}
            WHERE category_id = ?;
            ''',
            (category_id,)
        )
        rows = cursor.fetchall()
        return [get_obj_good_from_row(row) for row in rows]


def add_good(good: Good) -> Optional[Good]:
    if find_same_good_by_name(good.name):
        logger.warning('Good already exists: %s', good.name)
        return None

    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            INSERT INTO {GOOD_TABLE} (name, price, category_id)
            VALUES (?, ?, ?);
            ''',
            (good.name, good.price, good.category_id)
        )
        good.id = cursor.lastrowid
        logger.info('Good created: id=%s name=%s', good.id, good.name)
        return good


def add_category(category: Category) -> Optional[Category]:
    if find_same_category_by_name(category.name):
        logger.warning('Category already exists: %s', category.name)
        return None

    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            INSERT INTO {CATEGORY_TABLE} (name)
            VALUES (?);
            ''',
            (category.name,)
        )
        category.category_id = cursor.lastrowid
        logger.info(
            'Category created: id=%s name=%s',
            category.category_id,
            category.name
        )
        return category


def update_good_by_id(good_id: int, good: Good) -> Optional[Good]:
    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            UPDATE {GOOD_TABLE}
            SET name = ?, price = ?, category_id = ?
            WHERE id = ?;
            ''',
            (good.name, good.price, good.category_id, good_id)
        )

        if cursor.rowcount == 0:
            logger.warning('Good update failed, good not found: id=%s', good_id)
            return None

        good.id = good_id
        logger.info('Good updated: id=%s name=%s', good.id, good.name)
        return good


def delete_good_by_id(good_id: int) -> bool:
    with get_connect() as connection:
        cursor = connection.cursor()
        cursor.execute(
            f'''
            DELETE FROM {GOOD_TABLE}
            WHERE id = ?;
            ''',
            (good_id,)
        )
        is_deleted = cursor.rowcount > 0

        if is_deleted:
            logger.info('Good deleted: id=%s', good_id)
        else:
            logger.warning('Good delete failed, good not found: id=%s', good_id)

        return is_deleted
