from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.comic import ComicModel
from ..models.comment import CommentModel

comic_bp = Blueprint('comic', __name__)
comic_model = ComicModel()
comment_model = CommentModel()

@comic_bp.route('/<int:id>')
def detail(id):
    """
    顯示漫畫詳情頁面，包含標籤與評論。
    """
    comic = comic_model.get_by_id(id)
    if not comic:
        flash('找不到該漫畫作品', 'error')
        return redirect(url_for('main.index'))
    
    comments = comment_model.get_by_comic(id)
    
    # 取得標籤 (MVP 階段簡單獲取，實際可透過 Model 優化)
    import sqlite3
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.name, t.type FROM tags t
        JOIN comic_tags ct ON t.id = ct.tag_id
        WHERE ct.comic_id = ?
    """, (id,))
    tags = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return render_template('comic/detail.html', comic=comic, comments=comments, tags=tags)

@comic_bp.route('/<int:id>/comment', methods=['POST'])
def add_comment(id):
    """
    為指定漫畫發表評論與雷點標籤。
    """
    user_id = session.get('user_id')
    if not user_id:
        flash('請先登入以發表評論', 'warning')
        return redirect(url_for('auth.login'))
        
    content = request.form.get('content')
    rating = request.form.get('rating', 5)
    warning_tags = request.form.get('warning_tags') # 以逗號分隔的字串
    
    if content:
        comment_model.create(user_id, id, content, int(rating), warning_tags)
        flash('評論已送出', 'success')
    else:
        flash('評論內容不能為空', 'error')
        
    return redirect(url_for('comic.detail', id=id))

