# app.py
import streamlit as st
import pandas as pd
from data_manager import DataManager
from pattern_analyzer import PatternAnalyzer

# Acesso ao estado da sessão para manter os dados
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = PatternAnalyzer()

# Título e cabeçalho da página
st.set_page_config(page_title="Football Studio Live Analyzer", layout="wide")
st.title("⚽ Football Studio Live Analyzer")
st.markdown("---")

# --- Interface para adicionar resultados ---
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

# Botões de controle
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

# --- Exibir o histórico em um formato de painel (linhas de 9) ---
st.markdown("---")
st.header("Histórico de Jogadas")
history = list(st.session_state.data_manager.history)
if history:
    # Transforma a lista em um DataFrame para exibir em uma tabela
    df_history = pd.DataFrame({'Histórico': history}).transpose()
    st.table(df_history)
else:
    st.info("O histórico está vazio. Adicione um resultado acima para começar a análise.")

# --- Exibir a contagem de vitórias ---
st.header("Contagem de Vitórias")
wins = st.session_state.data_manager.wins
win_data = {'🔴 Red': wins['🔴'], '🔵 Blue': wins['🔵'], '🟡 Tie': wins['🟡']}
st.bar_chart(win_data)

# --- Análise e Sugestão de Aposta ---
st.markdown("---")
st.header("Análise de Padrões e Sugestão")

detected, suggestion = st.session_state.analyzer.analyze_history(history)

if detected:
    st.success(f"🧠 Sugestão de Aposta: **Aposte no {suggestion}!**")
    
    st.subheader("Padrões Detectados:")
    # Exibir os padrões detectados de forma mais organizada
    df_patterns = pd.DataFrame(detected, columns=['Nome do Padrão', 'Sugestão'])
    st.table(df_patterns.drop(columns=['Sugestão'])) # Sugestão já é mostrada acima

else:
    st.info("Nenhum padrão claro detectado no momento. Continue adicionando resultados para análise.")

# --- Conferidor Automático de Acertos e Erros ---
st.markdown("---")
st.header("Conferidor de Performance")

# Lógica para registrar o último resultado e comparar com a sugestão
if history:
    last_result = history[-1]
    last_bet_log = None
    if st.session_state.data_manager.bets_log and last_result == st.session_state.data_manager.bets_log[-1]['actual']:
        last_bet_log = st.session_state.data_manager.bets_log[-1]

    if suggestion and last_bet_log and last_bet_log['bet'] != suggestion:
        is_correct = st.session_state.data_manager.log_bet(suggestion, last_result)
        if is_correct:
            st.success(f"✅ ACERTOU! A sugestão de {suggestion} estava correta.")
        else:
            st.error(f"❌ ERROU. A sugestão era {suggestion}, mas o resultado foi {last_result}.")
    
    correct, total, accuracy = st.session_state.data_manager.get_performance()
    st.metric(label="Taxa de Acertos", value=f"{accuracy:.2f}%", help=f"{correct} acertos de um total de {total} apostas.")

# --- Como o código se relaciona ---
st.sidebar.title("Como Funciona")
st.sidebar.markdown(
    """
Este aplicativo é composto por 3 partes principais:

1.  **`data_manager.py`**: Gerencia todo o histórico de jogadas, a contagem de vitórias e o log de acertos/erros.
2.  **`pattern_analyzer.py`**: O cérebro do app. Ele contém a lógica de detecção de **30 padrões** baseados em suas observações.
3.  **`app.py`**: A interface visual (Streamlit). Ela captura as entradas, chama a lógica de análise e exibe os resultados de forma intuitiva.
    """
)
