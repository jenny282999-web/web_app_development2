import sqlite3
import os

DATABASE = os.path.join('instance', 'database.db')

class Ranking:
    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def update_score(cls, manga_id, category, score):
        conn = cls.get_db_connection()
        # Check if exists
        existing = conn.execute('SELECT id FROM rankings WHERE manga_id = ? AND category = ?', (manga_id, category)).fetchone()
        if existing:
            conn.execute('UPDATE rankings SET score = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (score, existing['id']))
        else:
            conn.execute('INSERT INTO rankings (manga_id, category, score) VALUES (?, ?, ?)', (manga_id, category, score))
        conn.commit()
        conn.close()

    @classmethod
    def get_top_n(cls, category, n=10):
        conn = cls.get_db_connection()
        query = '''
            SELECT m.*, r.score, r.category
            FROM rankings r
            JOIN mangas m ON r.manga_id = m.id
            WHERE r.category = ?
            ORDER BY r.score DESC
            LIMIT ?
        '''
        rankings = conn.execute(query, (category, n)).fetchall()
        conn.close()
        return [dict(r) for r in rankings]
