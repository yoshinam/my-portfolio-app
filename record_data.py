import os
import datetime
import yfinance as yf
import requests

def main():
    # 1. GitHubのSecretsからGASのURLを取得
    gas_url = os.environ.get("GAS_WEBAPP_URL")
    if not gas_url:
        print("エラー: GAS_WEBAPP_URL が設定されていません。")
        return

    try:
        # 2. yfinanceでTOPIX（コード: ^TOPX）の最新データを取得
        print("市場データを取得中...")
        topix = yf.Ticker("^TOPX")
        hist = topix.history(period="1d")
        
        if hist.empty:
            print("エラー: データの取得に失敗しました。")
            return
            
        latest_close = float(hist['Close'].iloc[-1])
        
        # 3. 今日の日付（日本時間 UTC+9）を計算
        today_jst = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y-%m-%d")
        
        # 4. GAS（Google Apps Script）へ送るデータを作成
        payload = {
            "date": today_jst,
            "value": round(latest_close, 2) # 小数点第2位で四捨五入
        }
        
        # 5. データを送信（POSTリクエスト）
        print(f"GASへデータを送信中... [{today_jst} : {latest_close}]")
        response = requests.post(gas_url, json=payload)
        
        if response.status_code == 200 and "Success" in response.text:
            print("🎉 スプレッドシートへの記録が正常に完了しました！")
        else:
            print(f"⚠️ 送信はされましたが、GAS側でエラーの可能性があります: {response.text}")
            
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()
