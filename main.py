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
        seed = st.number_input('투자금액', value=80_000_000)
        history_table = History(st.session_state.universe, seed).table
        st.dataframe(history_table, use_container_width=True)

if __name__ == '__main__':
    etf_table()
    etf_history()
