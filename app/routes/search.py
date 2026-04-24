from flask import Blueprint, render_template, request, flash
from ..models.comic import ComicModel

search_bp = Blueprint('search', __name__)
comic_model = ComicModel()

@search_bp.route('/ai', methods=['GET', 'POST'])
def ai_recommend():
    """
    處理情緒標籤推薦邏輯。
    """
    # 預定義的情緒標籤 (實際開發可從 DB 讀取)
    emotion_tags = ['致鬱', '燃爆', '心靈療癒', '胃痛', '熱血', '燒腦', '輕鬆', '暗黑']
    
    if request.method == 'POST':
        selected_tags = request.form.getlist('tags')
        if not selected_tags:
            flash('請至少選擇一個情緒標籤', 'warning')
            return render_template('search/ai.html', tags=emotion_tags)
        
        # 媒合邏輯：取得包含任一選擇標籤的漫畫
        results = []
        for tag in selected_tags:
            comics = comic_model.get_by_tag(tag)
            results.extend(comics)
        
        # 去重
        seen_ids = set()
        unique_results = []
        for c in results:
            if c['id'] not in seen_ids:
                unique_results.append(c)
                seen_ids.add(c['id'])
                
        return render_template('search/results.html', comics=unique_results, selected=selected_tags)

    return render_template('search/ai.html', tags=emotion_tags)

@search_bp.route('/art', methods=['GET', 'POST'])
def art_search():
    """
    處理畫風視覺搜尋邏輯 (MVP 階段以隨機推薦模擬)。
    """
    if request.method == 'POST':
        # 模擬圖片上傳處理
        comics = comic_model.get_all()
        import random
        results = random.sample(comics, min(len(comics), 3))
        return render_template('search/results.html', comics=results, is_art=True)
        
    return render_template('search/art.html')

