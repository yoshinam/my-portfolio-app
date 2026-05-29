# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# ページ設定
st.set_page_config(page_title="ポートフォリオ推移", layout="wide")

st.title("📈 ポートフォリオ時価総額日々推移")

# Googleスプレッドシートとの接続
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=3600) # 1時間ごとに最新データを取得
def load_historical_data():
    df = conn.read(worksheet="履歴")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

try:
    with st.spinner("データを読み込み中..."):
        df_history = load_historical_data()

    df_history = df_history.sort_values("Date")
    latest_data = df_history.iloc[-1]
    previous_data = df_history.iloc[-2] if len(df_history) > 1 else latest_data

    latest_value = latest_data["Total_Value"]
    delta_value = latest_value - previous_data["Total_Value"]

    # メトリクス表示
    st.metric(
        label=f"最新の総資産 ({latest_data['Date'].strftime('%Y-%m-%d')})",
        value=f"¥{latest_value:,.0f}",
        delta=f"¥{delta_value:,.0f} (前日比)"
    )

    # 折れ線グラフ
    fig = px.line(df_history, x="Date", y="Total_Value", title="総資産額の推移")
    fig.update_traces(mode="lines+markers", marker=dict(size=6))
    st.plotly_chart(fig, use_container_width=True)

    # 履歴一覧の表
    st.dataframe(df_history.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)

except Exception as e:
    st.error("データの読み込みに失敗しました。")
    st.caption(f"エラー詳細: {e}")
