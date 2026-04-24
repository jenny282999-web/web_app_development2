import sqlite3
from datetime import datetime

class ProgressModel:
    def __init__(self, db_path='instance/database.db'):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_or_update(self, user_id, comic_id, current_chapter=None, status='reading', platform=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Check if exists
        cursor.execute("SELECT id FROM progress WHERE user_id = ? AND comic_id = ?", (user_id, comic_id))
        row = cursor.fetchone()
        
        if row:
            # Update
            query = "UPDATE progress SET current_chapter = ?, status = ?, platform = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            cursor.execute(query, (current_chapter, status, platform, row['id']))
            conn.commit()
            progress_id = row['id']
        else:
            # Insert
            query = "INSERT INTO progress (user_id, comic_id, current_chapter, status, platform) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (user_id, comic_id, current_chapter, status, platform))
            conn.commit()
            progress_id = cursor.lastrowid
            
        conn.close()
        return progress_id

    def get_user_library(self, user_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        query = """
            SELECT p.*, c.title, c.author, c.cover_url 
            FROM progress p
            JOIN comics c ON p.comic_id = c.id
            WHERE p.user_id = ?
            ORDER BY p.updated_at DESC
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def delete(self, progress_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM progress WHERE id = ?", (progress_id,))
        conn.commit()
        count = cursor.rowcount
        conn.close()
        return count > 0
