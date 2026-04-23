from flask import Blueprint, render_template, request, redirect, url_for

manga_bp = Blueprint('manga', __name__)

@manga_bp.route('/manga/<int:manga_id>')
def detail(manga_id):
    """
    漫畫詳情頁：顯示簡介、作者、分類資訊及章節列表。
    """
    pass

@manga_bp.route('/manga/<int:manga_id>/read/<int:chapter_num>')
def reader(manga_id, chapter_num):
    """
    閱讀器頁面：提供下拉式與翻頁式模式切換，並載入章節圖片與留言。
    """
    pass

@manga_bp.route('/manga/<int:manga_id>/comment', methods=['POST'])
def add_comment(manga_id):
    """
    發表留言：接收使用者的評論並存入資料庫。
    """
    pass
