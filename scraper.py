import requests
import json
import time
from datetime import datetime

def get_keirin_data():
    # ユーザーエージェントをスマホ版 Safari に偽装してブロックを防ぐ
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }
    
    # 1. 今日の開催場リストを取得（もっとも安定している簡易API/jsonを狙う）
    # ※今回は確実に動かすため、netkeirinの番組表をより丁寧にパースする
    today = datetime.now().strftime("%Y%m%d")
    master_data = {}

    try:
        # 開催場を特定するためのトップページ
        base_url = f"https://keirin.netkeiba.com/db/program/?date={today}"
        res = requests.get(base_url, headers=headers, timeout=10)
        
        # 開催場名とIDを正規表現で強引に抜き出す（HTML構造の変化に強い）
        import re
        # 例: bankid=01" title="玉野"
        stadiums = re.findall(r'bankid=(\d+)".*?title="([^"]+)"', res.text)
        
        if not stadiums:
            print("開催場が見つかりません。テストデータを生成します。")
            master_data["(予備)玉野"] = {str(r): [{"id": i, "s": 80.0, "n": f"準備中{i}"} for i in range(1, 10)] for r in range(1, 13)}
        else:
            for bankid, name in stadiums:
                print(f"【{name}】を取得中...")
                stadium_races = {}
                
                for r in range(1, 13):
                    # 出走表ページ
                    race_url = f"https://keirin.netkeiba.com/db/shusso/?bankid={bankid}&race_no={r}"
                    r_res = requests.get(race_url, headers=headers, timeout=10)
                    
                    # 選手名と得点を抽出
                    # 選手名は <span class="PlayerName">...</span>
                    # 得点は <span class="Score">...</span>
                    names = re.findall(r'<span class="PlayerName">(.*?)</span>', r_res.text)
                    scores = re.findall(r'<span class="Score">(\d+\.\d+)</span>', r_res.text)
                    
                    players = []
                    for i in range(len(names)):
                        p_name = names[i].strip()
                        p_score = float(scores[i]) if i < len(scores) else 0.0
                        players.append({"id": i+1, "s": p_score, "n": p_name})
                    
                    if players:
                        stadium_races[str(r)] = players
                    time.sleep(0.5) # サーバーへの優しさ
                
                master_data[name] = stadium_races

    except Exception as e:
        print(f"エラー: {e}")
        master_data["エラー"] = {str(r): [{"id": i, "s": 0.0, "n": "再試行してね"} for i in range(1, 10)] for r in range(1, 13)}

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_keirin_data()

