import streamlit as st
from universe import Universe
from history import History

def etf_table():
    with st.expander('🌌 투자 유니버스'):
        universe_table = Universe().table
        st.dataframe(universe_table, use_container_width=True)
        st.session_state['universe'] = universe_table 

def etf_history():
    with st.expander('💯 투자 점수표', expanded=True):
        seed = st.number_input('🥹 투자금액',
            value=80_000_000,
            step=1_000_000)
        with st.spinner('⌛️ 데이터 분석 및 로딩 중...'):
            history_table = History(st.session_state.universe, seed).table
        st.subheader('🐫 듀얼 모멘텀 TOP5')
        df = history_table.loc[(history_table.위험조정모멘텀 > 0)
            & (history_table.위험조정모멘텀 > history_table.loc['357870','위험조정모멘텀'])
        ].head()
        st.dataframe(df, use_container_width=True)
        cols = st.columns(len(df))
        for i in range(len(df)):
            s = df.head(i+1).투자유닛.sum()
            cols[i].write(f"**{i+1}종목**")
            cols[i].write(f"{s}원 ({(s * 100 / seed):.2f}%)")
        st.subheader('📈 수익 모멘텀 종목')
        st.dataframe(history_table.loc[history_table.위험조정모멘텀 > 0].iloc[:, 0:2],
                     height=200, use_container_width=True)
        st.subheader('📉 손실 모멘텀 종목')
        st.dataframe(history_table.loc[history_table.위험조정모멘텀 < 0].iloc[:, 0:2],
                     height=200, use_container_width=True)

if __name__ == '__main__':
    st.set_page_config(
        page_title='모멘텀 대시보드',
        page_icon='🏃‍♂️',
    )   
    etf_table()
    etf_history()
