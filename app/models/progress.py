import sqlite3
from datetime import datetime

class ProgressModel:
    def __init__(self, db_path='instance/database.db'):
        self.db_path = db_path

    def _get_connection(self):
        """建立資料庫連線並設定 row_factory。"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_or_update(self, user_id, comic_id, current_chapter=None, status='reading', platform=None):
        """新增或更新閱讀進度。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            # Check if exists
            cursor.execute("SELECT id FROM progress WHERE user_id = ? AND comic_id = ?", (user_id, comic_id))
            row = cursor.fetchone()
            
            if row:
                # Update
                query = "UPDATE progress SET current_chapter = ?, status = ?, platform = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
                cursor.execute(query, (current_chapter, status, platform, row['id']))
                conn.commit()
                return row['id']
            else:
                # Insert
                query = "INSERT INTO progress (user_id, comic_id, current_chapter, status, platform) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(query, (user_id, comic_id, current_chapter, status, platform))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error updating progress: {e}")
            return None
        finally:
            conn.close()

    def get_user_library(self, user_id):
        """取得使用者的個人書櫃。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            query = """
                SELECT p.*, c.title, c.author, c.cover_url 
                FROM progress p
                JOIN comics c ON p.comic_id = c.id
                WHERE p.user_id = ?
                ORDER BY p.updated_at DESC
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching user library: {e}")
            return []
        finally:
            conn.close()

    def delete(self, progress_id):
        """刪除指定進度紀錄。"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM progress WHERE id = ?", (progress_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting progress: {e}")
            return False
        finally:
            conn.close()

