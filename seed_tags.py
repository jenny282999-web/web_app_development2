import sqlite3

db_path = 'instance/database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 建立標籤
tags = [
    ('致鬱', 'emotion'),
    ('燃爆', 'emotion'),
    ('心靈療癒', 'emotion'),
    ('胃痛', 'emotion'),
    ('熱血', 'emotion'),
    ('冒險', 'category'),
    ('奇幻', 'category'),
    ('日常', 'category')
]

cursor.executemany("INSERT OR IGNORE INTO tags (name, type) VALUES (?, ?)", tags)

# 獲取 ID
cursor.execute("SELECT id, name FROM tags")
tag_map = {name: id for id, name in cursor.fetchall()}

cursor.execute("SELECT id, title FROM comics")
comic_map = {title: id for id, title in cursor.fetchall()}

# 建立關聯
associations = [
    (comic_map['葬送的芙莉蓮'], tag_map['心靈療癒']),
    (comic_map['葬送的芙莉蓮'], tag_map['冒險']),
    (comic_map['我推的孩子'], tag_map['致鬱']),
    (comic_map['我推的孩子'], tag_map['胃痛']),
    (comic_map['SPY×FAMILY 間諜家家酒'], tag_map['日常']),
    (comic_map['SPY×FAMILY 間諜家家酒'], tag_map['心靈療癒']),
    (comic_map['藍色監獄'], tag_map['燃爆']),
    (comic_map['藍色監獄'], tag_map['熱血'])
]

cursor.executemany("INSERT OR IGNORE INTO comic_tags (comic_id, tag_id) VALUES (?, ?)", associations)

conn.commit()
conn.close()
print("標籤與關聯數據注入完成。")
