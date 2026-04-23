from flask import Blueprint, render_template, request
from ..models.manga import Manga
from ..models.ranking import Ranking

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示熱門排行榜。
    """
    # 獲取不同類別的排行榜，例如 'weekly_hot'
    hot_rankings = Ranking.get_top_n('weekly_hot', n=10)
    new_rankings = Ranking.get_top_n('new_arrival', n=10)
    
    return render_template('index.html', hot_rankings=hot_rankings, new_rankings=new_rankings)

@main_bp.route('/search')
def search():
    """
    搜尋頁：根據書名關鍵字篩選漫畫。
    """
    query = request.args.get('q', '')
    if not query:
        return render_template('search.html', mangas=[], query=query)
    
    mangas = Manga.search(query)
    return render_template('search.html', mangas=mangas, query=query)

@main_bp.route('/categories')
def categories():
    """
    分類索引頁：提供各種語言、題材、性別傾向的選擇。
    """
    # 這裡可以預定義一些分類標籤，或從 DB 獲取已有的分類
    languages = ['繁體中文', '日文', '英文']
    content_types = ['冒險', '戀愛', '科幻', '懸疑', '日常']
    gender_prefs = ['少年向', '少女向', '青年向']
    
    return render_template('categories.html', 
                           languages=languages, 
                           content_types=content_types, 
                           gender_prefs=gender_prefs)

@main_bp.route('/category')
def category_filter():
    """
    分類結果頁：顯示特定分類條件下的漫畫列表。
    """
    lang = request.args.get('lang')
    ctype = request.args.get('type')
    gender = request.args.get('gender')
    
    mangas = Manga.filter(language=lang, content_type=ctype, gender_pref=gender)
    return render_template('manga_list.html', mangas=mangas, lang=lang, type=ctype, gender=gender)
