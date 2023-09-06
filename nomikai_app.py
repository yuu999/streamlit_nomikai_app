import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt


# 職位とそのデフォルトウェイト
default_weights = {
    'GM': 20,
    'M': 15,
    'PM': 10,
    'PAM': 7,
    'T': 5,
}


# 会費分配計算
def calculate_amount(total_amount, position_counts, rounding_digit, weights):
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
            rounded_amount = max(100, math.ceil(raw_amount / rounding_digit) * rounding_digit)
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
with st.expander("オプション設定"):
    st.caption("各職位の重みを設定")
    weights = {position: st.slider(f"{position}のウェイト", 1, 100, default_weights[position]) for position in default_weights}
    st.caption("切り捨てる桁数の設定")
    rounding_digit = st.selectbox('切り上げる桁数を選択', [10, 100, 1000], index=1)
# 計算
if st.button("分配を計算"):
    st.header('3. 計算結果')
    result, organizer_share = calculate_amount(
        total_amount,
        position_counts,
        rounding_digit,
        weights)
    if result:
        df = pd.DataFrame(
            [(k, v['1人当たりの請求額'], v['人数']) for k, v in result.items()],
            columns=['職位', '1人当たりの請求額 [円]', '人数'])
        st.table(df)
        st.write(f"🎉 幹事の取り分（切り上げによる余剰額）： {organizer_share}円 🎉")
        st.balloons()

        # ...（前部分は同じ）

        # チャートの表示
        fig, ax = plt.subplots(figsize=(12,6))

        # 支払額が多い順にソート
        sorted_result = sorted(result.items(), key=lambda x: x[1]['1人当たりの請求額'], reverse=False)
        labels = [k for k, v in sorted_result]
        amount = [v['1人当たりの請求額'] for k, v in sorted_result]

        ax.barh(labels, amount, color='skyblue')
        ax.set_xlabel('Amount per Person [JPY]')
        ax.set_title('Payment by Position')

        for i, (label, value) in enumerate(zip(labels, amount)):
            ax.text(value, i, str(value), ha='center', va='center')

        st.pyplot(fig)

st.write('---')
st.write('開発者: yuu999')
