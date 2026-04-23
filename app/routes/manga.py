from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.manga import Manga
from ..models.chapter import Chapter
from ..models.comment import Comment

manga_bp = Blueprint('manga', __name__)

@manga_bp.route('/manga/<int:manga_id>')
def detail(manga_id):
    """
    漫畫詳情頁：顯示簡介、作者、分類資訊及章節列表。
    """
    manga = Manga.get_by_id(manga_id)
    if not manga:
        flash("找不到該漫畫。")
        return redirect(url_for('main.index'))
    
    chapters = Chapter.get_by_manga(manga_id)
    return render_template('manga_detail.html', manga=manga, chapters=chapters)

@manga_bp.route('/manga/<int:manga_id>/read/<int:chapter_num>')
def reader(manga_id, chapter_num):
    """
    閱讀器頁面：提供下拉式與翻頁式模式切換，並載入章節圖片與留言。
    """
    manga = Manga.get_by_id(manga_id)
    chapters = Chapter.get_by_manga(manga_id)
    
    # 找到對應章節數量的章節物件
    current_chapter = next((c for c in chapters if c['chapter_num'] == chapter_num), None)
    
    if not current_chapter:
        flash("找不到該章節。")
        return redirect(url_for('manga.detail', manga_id=manga_id))
    
    comments = Comment.get_by_chapter(current_chapter['id'])
    
    return render_template('reader.html', 
                           manga=manga, 
                           chapter=current_chapter, 
                           chapters=chapters,
                           comments=comments)

@manga_bp.route('/manga/<int:manga_id>/comment', methods=['POST'])
def add_comment(manga_id):
    """
    發表留言：接收使用者的評論並存入資料庫。
    """
    user_name = request.form.get('user_name', '匿名讀者')
    content = request.form.get('content')
    chapter_id = request.form.get('chapter_id')
    chapter_num = request.form.get('chapter_num')

    if not content:
        flash("留言內容不能為空！")
    else:
        success = Comment.create(manga_id, chapter_id, user_name, content)
        if success:
            flash("留言成功！")
        else:
            flash("留言失敗，請稍後再試。")

    # 重導向回剛才的閱讀頁面
    return redirect(url_for('manga.reader', manga_id=manga_id, chapter_num=chapter_num))
