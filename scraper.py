import requests
import json
import time
import re
from datetime import datetime

def get_keirin_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }
    
    today = datetime.now().strftime("%Y%m%d")
    master_data = {}

    try:
        # オッズパークの開催一覧ページを狙う
        list_url = f"https://www.oddspark.com/keirin/KaisaiYotei.do?request_date={today}"
        res = requests.get(list_url, headers=headers, timeout=15)
        
        # 開催されている「場名」と「場コード」を抽出
        # 例: /keirin/KaisaiInfo.do?kaisaiBi=20240409&joCode=61
        stadiums = re.findall(r'joCode=(\d+)">([^<]+)競輪', res.text)
        
        if not stadiums:
            # もし見つからなかったら、強引に「今日の主要場」を決め打ちで探しに行く
            stadiums = [("61", "久留米"), ("71", "松山"), ("31", "大宮")] 

        for jo_code, name in stadiums:
            print(f"【{name}】を取得中...")
            stadium_races = {}
            
            for r in range(1, 13):
                # 出走表ページ
                race_url = f"https://www.oddspark.com/keirin/Yoso.do?kaisaiBi={today}&joCode={jo_code}&raceNo={r}"
                r_res = requests.get(race_url, headers=headers, timeout=15)
                
                # 選手名と得点を抽出
                # オッズパークの構造：<td class="name">...<a ...>選手名</a>
                # 競走得点は <td>直近4ヶ月</td> の次あたりにある数字
                names = re.findall(r'class="name">.*?<a[^>]*>([^<]+)</a>', r_res.text, re.DOTALL)
                scores = re.findall(r'<td>(\d{2,3}\.\d{1,2})</td>', r_res.text)
                
                players = []
                for i in range(len(names)):
                    p_name = names[i].strip()
                    # 得点リストからそれっぽい位置の数字を拾う（0番目は違うことが多いので調整）
                    p_score = float(scores[i]) if i < len(scores) else 0.0
                    players.append({"id": i+1, "s": p_score, "n": p_name})
                
                if players:
                    stadium_races[str(r)] = players
                time.sleep(0.8) # ブロックされないようにゆっくり
            
            if stadium_races:
                master_data[name] = stadium_races

    except Exception as e:
        print(f"エラー: {e}")

    # 万が一空っぽだったら、意地でもデータを出すための最終防衛ライン
    if not master_data:
        master_data["通信待ち"] = {str(r): [{"id": i, "s": 0, "n": "反映待ち"} for i in range(1, 10)] for r in range(1, 13)}

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_keirin_data()
