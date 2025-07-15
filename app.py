import streamlit as st
import pandas as pd
from data_manager import DataManager
from pattern_analyzer import PatternAnalyzer

if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = PatternAnalyzer()

st.set_page_config(page_title="Football Studio Live Analyzer", layout="wide")
st.title("⚽ Football Studio Live Analyzer")
st.markdown("---")

st.header("Adicionar Resultado da Rodada")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔴 Red"):
        st.session_state.data_manager.add_result('🔴')
        st.experimental_rerun()
with col2:
    if st.button("🔵 Blue"):
        st.session_state.data_manager.add_result('🔵')
        st.experimental_rerun()
with col3:
    if st.button("🟡 Tie"):
        st.session_state.data_manager.add_result('🟡')
        st.experimental_rerun()

st.markdown("---")
st.header("Controle de Histórico")
undo_col, clear_col = st.columns(2)

with undo_col:
    if st.button("↩️ Desfazer Última Jogada"):
        st.session_state.data_manager.undo_last()
        st.experimental_rerun()
        
with clear_col:
    if st.button("🗑️ Limpar Histórico Completo"):
        st.session_state.data_manager.clear_history()
        st.experimental_rerun()

st.markdown("---")
st.header("Histórico de Jogadas")
history = list(st.session_state.data_manager.history)
if history:
    df_history = pd.DataFrame(history, columns=["Resultado"])
    st.table(df_history.tail(27).style.hide(axis='index'))
else:
    st.info("O histórico está vazio. Adicione um resultado acima para começar a análise.")

st.header("Contagem de Vitórias")
wins = st.session_state.data_manager.wins
win_data = {'🔴 Red': wins['🔴'], '🔵 Blue': wins['🔵'], '🟡 Tie': wins['🟡']}
st.bar_chart(win_data)

st.markdown("---")
st.header("Análise de Padrões e Sugestão")

detected, suggestion = st.session_state.analyzer.analyze_history(history)

if detected:
    st.success(f"🧠 Sugestão de Aposta: **Aposte no {suggestion}!**")
    
    st.subheader("Padrões Detectados:")
    df_patterns = pd.DataFrame(detected, columns=['Nome do Padrão', 'Sugestão'])
    st.table(df_patterns.drop(columns=['Sugestão']))

else:
    st.info("Nenhum padrão claro detectado no momento. Continue adicionando resultados para análise.")

st.markdown("---")
st.header("Conferidor de Performance")

if history:
    last_result = history[-1]
    
    if 'last_suggestion' in st.session_state and st.session_state.last_suggestion:
        is_correct = st.session_state.data_manager.log_bet(st.session_state.last_suggestion, last_result)
        if is_correct:
            st.success(f"✅ ACERTOU! A sugestão de {st.session_state.last_suggestion} estava correta.")
        else:
            st.error(f"❌ ERROU. A sugestão era {st.session_state.last_suggestion}, mas o resultado foi {last_result}.")

    st.session_state.last_suggestion = suggestion

    correct, total, accuracy = st.session_state.data_manager.get_performance()
    st.metric(label="Taxa de Acertos", value=f"{accuracy:.2f}%", help=f"{correct} acertos de um total de {total} apostas.")

st.sidebar.title("Como Funciona")
st.sidebar.markdown(
    """
Este aplicativo é composto por 3 partes principais:

1.  **`data_manager.py`**: Gerencia todo o histórico de jogadas, a contagem de vitórias e o log de acertos/erros.
2.  **`pattern_analyzer.py`**: O cérebro do app. Ele contém a lógica de detecção de **30 padrões** baseados em suas observações.
3.  **`app.py`**: A interface visual (Streamlit). Ela captura as entradas, chama a lógica de análise e exibe os resultados de forma intuitiva.
    """
)
