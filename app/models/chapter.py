import sqlite3
import os

DATABASE = os.path.join('instance', 'database.db')

class Chapter:
    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, manga_id, chapter_num, title, content_url):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chapters (manga_id, chapter_num, title, content_url)
            VALUES (?, ?, ?, ?)
        ''', (manga_id, chapter_num, title, content_url))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @classmethod
    def get_by_manga(cls, manga_id):
        conn = cls.get_db_connection()
        chapters = conn.execute('SELECT * FROM chapters WHERE manga_id = ? ORDER BY chapter_num ASC', (manga_id,)).fetchall()
        conn.close()
        return [dict(c) for c in chapters]

    @classmethod
    def get_by_id(cls, chapter_id):
        conn = cls.get_db_connection()
        chapter = conn.execute('SELECT * FROM chapters WHERE id = ?', (chapter_id,)).fetchone()
        conn.close()
        return dict(chapter) if chapter else None

    @classmethod
    def delete(cls, chapter_id):
        conn = cls.get_db_connection()
        conn.execute('DELETE FROM chapters WHERE id = ?', (chapter_id,))
        conn.commit()
        conn.close()
