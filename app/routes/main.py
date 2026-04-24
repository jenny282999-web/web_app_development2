from flask import Blueprint, render_template
from ..models.comic import ComicModel

main_bp = Blueprint('main', __name__)
comic_model = ComicModel()

@main_bp.route('/')
def index():
    """
    系統首頁，顯示熱門漫畫與情緒推薦入口。
    """
    # 取得一些推薦漫畫（MVP 暫時取得所有漫畫）
    comics = comic_model.get_all()
    return render_template('index.html', comics=comics)

