from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示各類別排行榜與熱門漫畫。
    """
    pass

@main_bp.route('/search')
def search():
    """
    搜尋頁：根據書名關鍵字篩選漫畫。
    """
    pass

@main_bp.route('/categories')
def categories():
    """
    分類索引頁：提供各種語言、題材、性別傾向的選擇。
    """
    pass

@main_bp.route('/category')
def category_filter():
    """
    分類結果頁：顯示特定分類條件下的漫畫列表。
    """
    pass
