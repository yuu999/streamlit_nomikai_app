import streamlit as st
import pandas as pd
import math

# 職位とそのデフォルトウェイト
default_weights = {
    'GM': 15,
    'M': 10,
    'PM': 7,
    'PAM': 5,
    'T': 3,
}

# 会費分配計算
def calculate_amount(total_amount, position_counts, weights):
    total_weights = sum([weights[position] * count for position, count in position_counts.items()])
    if total_weights == 0:
        st.warning("合計のウェイトが0です。人数を設定してください。")
        return None, 0
    
    per_weight_amount = total_amount / total_weights
    result = {}
    total_collected = 0
    for position, count in position_counts.items():
        if count > 0:
            raw_amount = weights[position] * per_weight_amount
            rounded_amount = max(100, math.ceil(raw_amount / 100) * 100)
            total_per_position = rounded_amount * count
            total_collected += total_per_position
            result[position] = {'1人当たりの請求額': rounded_amount, '人数': count}
    
    organizer_share = total_collected - total_amount
    return result, organizer_share

# UIデザイン
st.title('飲み会の会費分配アプリ🍻')
st.write('このアプリを使用して、飲み会の会費を職位に応じて分配しましょう。')

# 会費情報入力
st.header('1. 会費情報')
total_amount = st.number_input('飲み会の合計金額 [円]', value=0, step=100)

# 職位と人数入力
st.header('2. 参加者情報')
position_counts = {position: st.slider(f"{position}の人数", 0, 10) for position in default_weights}

# ウェイト設定（オプション）
with st.expander("ウェイト設定（オプション）"):
    weights = {position: st.slider(f"{position}のウェイト", 1, 100, default_weights[position]) for position in default_weights}

# 計算
if st.button("分配を計算"):
    st.header('3. 計算結果')
    result, organizer_share = calculate_amount(total_amount, position_counts, weights)
    if result:
        df = pd.DataFrame(
            [(k, v['1人当たりの請求額'], v['人数']) for k, v in result.items()],
            columns=['職位', '1人当たりの請求額 [円]', '人数'])
        st.table(df)
        st.write(f"🎉 幹事の取り分（切り上げによる余剰額）： {organizer_share}円 🎉")
        
st.write('---')
st.write('開発者: yuu999')
