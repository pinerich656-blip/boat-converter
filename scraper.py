import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime

def get_real_time_all_keirin():
    # ターゲットは解析しやすい netkeirin の番組表
    base_url = "https://keirin.netkeiba.com/db/program/?date=" + datetime.now().strftime("%Y%m%d")
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
    except:
        print("サイトにアクセスできなかったよ。")
        return

    # 1. 今日開催されている場とURLを特定
    stadium_links = soup.select(".RaceList_DataList li a")
    active_stadiums = {}
    for link in stadium_links:
        href = link.get("href")
        name = link.text.strip()
        # URLから場IDを抜き出す
        match = re.search(r"bankid=(\d+)", href)
        if match:
            active_stadiums[match.group(1)] = name

    if not active_stadiums:
        print("今日の開催が見つかりませんでした。")
        return

    master_data = {}

    # 2. 各場の全12レースを巡回
    for bankid, name in active_stadiums.items():
        print(f"【{name}】の本物データを取得中...")
        stadium_races = {}
        
        for r in range(1, 13):
            # 出走表ページへアクセス
            race_url = f"https://keirin.netkeiba.com/db/shusso/?bankid={bankid}&race_no={r}"
            try:
                r_res = requests.get(race_url, headers=headers)
                r_soup = BeautifulSoup(r_res.content, "html.parser")
                
                players = []
                # 選手名と得点の行を探す（サイトの構造に合わせたパース）
                rows = r_soup.select(".PlayerList_Row")
                for idx, row in enumerate(rows, 1):
                    p_name = row.select_one(".PlayerName").text.strip() if row.select_one(".PlayerName") else f"選手{idx}"
                    # 得点を取得（数字以外を除去）
                    score_tag = row.select_one(".Score")
                    p_score = float(re.findall(r"\d+\.\d+", score_tag.text)[0]) if score_tag else 0.0
                    
                    players.append({"id": idx, "s": p_score, "n": p_name})
                
                if players:
                    stadium_races[str(r)] = players
                time.sleep(0.5) # 負荷軽減
            except:
                continue
        
        if stadium_races:
            master_data[name] = stadium_races

    # 3. 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)
    print("本物データの同期がすべて完了したよ！")

if __name__ == "__main__":
    get_real_time_all_keirin()

