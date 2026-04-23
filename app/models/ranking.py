import sqlite3
import os

DATABASE = os.path.join('instance', 'database.db')

class Ranking:
    """
    排行榜模型：負責統計與獲取漫畫排行數據。
    """
    @staticmethod
    def get_db_connection():
        """
        建立資料庫連線。
        """
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def update_score(cls, manga_id, category, score):
        """
        更新或新增漫畫在特定類別的排行分數。
        """
        try:
            conn = cls.get_db_connection()
            # 檢查是否已存在
            existing = conn.execute('SELECT id FROM rankings WHERE manga_id = ? AND category = ?', (manga_id, category)).fetchone()
            if existing:
                conn.execute('UPDATE rankings SET score = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (score, existing['id']))
            else:
                conn.execute('INSERT INTO rankings (manga_id, category, score) VALUES (?, ?, ?)', (manga_id, category, score))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating ranking score: {e}")
            return False

    @classmethod
    def get_top_n(cls, category, n=10):
        """
        取得特定類別前 N 名的漫畫。
        """
        try:
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
        except Exception as e:
            print(f"Error fetching top rankings: {e}")
            return []
