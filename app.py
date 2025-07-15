import streamlit as st
import pandas as pd
from gerenciador_de_dados import GerenciadorDeDados
from analisador_de_padroes import AnalisadorDePadroes

# Acesso ao estado da sessão para manter os dados
if 'gerenciador_de_dados' not in st.session_state:
    st.session_state.gerenciador_de_dados = GerenciadorDeDados()
if 'analisador_de_padroes' not in st.session_state:
    st.session_state.analisador_de_padroes = AnalisadorDePadroes()

# Título e cabeçalho da página
st.set_page_config(page_title="Football Studio Live Analyzer", layout="wide")
st.title("⚽ Football Studio Live Analyzer")
st.markdown("---")

# --- Interface para adicionar resultados ---
st.header("Adicionar Resultado da Rodada")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔴 Red"):
        st.session_state.gerenciador_de_dados.adicionar_resultado('🔴')
        st.experimental_rerun()
with col2:
    if st.button("🔵 Blue"):
        st.session_state.gerenciador_de_dados.adicionar_resultado('🔵')
        st.experimental_rerun()
with col3:
    if st.button("🟡 Tie"):
        st.session_state.gerenciador_de_dados.adicionar_resultado('🟡')
        st.experimental_rerun()

# Botões de controle
st.markdown("---")
st.header("Controle de Histórico")
undo_col, clear_col = st.columns(2)

with undo_col:
    if st.button("↩️ Desfazer Última Jogada"):
        st.session_state.gerenciador_de_dados.desfazer_ultimo()
        st.experimental_rerun()
        
with clear_col:
    if st.button("🗑️ Limpar Histórico Completo"):
        st.session_state.gerenciador_de_dados.limpar_historico()
        st.experimental_rerun()

# --- Exibir o histórico em um formato de painel (linhas de 9) ---
st.markdown("---")
st.header("Histórico de Jogadas")
history = list(st.session_state.gerenciador_de_dados.history)
if history:
    df_history = pd.DataFrame(history, columns=["Resultado"])
    st.table(df_history.tail(27).style.hide(axis='index'))
else:
    st.info("O histórico está vazio. Adicione um resultado acima para começar a análise.")

# --- Exibir a contagem de vitórias ---
st.header("Contagem de Vitórias")
wins = st.session_state.gerenciador_de_dados.wins
win_data = {'🔴 Red': wins['🔴'], '🔵 Blue': wins['🔵'], '🟡 Tie': wins['🟡']}
st.bar_chart(win_data)

# --- Análise e Sugestão de Aposta ---
st.markdown("---")
st.header("Análise de Padrões e Sugestão")

detected, suggestion = st.session_state.analisador_de_padroes.analyze_history(history)

if detected:
    st.success(f"🧠 Sugestão de Aposta: **Aposte no {suggestion}!**")
    
    st.subheader("Padrões Detectados:")
    df_patterns = pd.DataFrame(detected, columns=['Nome do Padrão', 'Sugestão'])
    st.table(df_patterns.drop(columns=['Sugestão']))

else:
    st.info("Nenhum padrão claro detectado no momento. Continue adicionando resultados para análise.")

# --- Conferidor Automático de Acertos e Erros ---
st.markdown("---")
st.header("Conferidor de Performance")

if history:
    last_result = history[-1]
    
    if 'last_suggestion' in st.session_state and st.session_state.last_suggestion:
        is_correct = st.session_state.gerenciador_de_dados.registrar_aposta(st.session_state.last_suggestion, last_result)
        if is_correct:
            st.success(f"✅ ACERTOU! A sugestão de {st.session_state.last_suggestion} estava correta.")
        else:
            st.error(f"❌ ERROU. A sugestão era {st.session_state.last_suggestion}, mas o resultado foi {last_result}.")

    st.session_state.last_suggestion = suggestion

    correct, total, accuracy = st.session_state.gerenciador_de_dados.obter_performance()
    st.metric(label="Taxa de Acertos", value=f"{accuracy:.2f}%", help=f"{correct} acertos de um total de {total} apostas.")

# --- Como o código se relaciona ---
st.sidebar.title("Como Funciona")
st.sidebar.markdown(
    """
Este aplicativo é composto por 3 partes principais:

1.  **`gerenciador_de_dados.py`**: Gerencia todo o histórico de jogadas, a contagem de vitórias e o log de acertos/erros.
2.  **`analisador_de_padroes.py`**: O cérebro do app. Ele contém a lógica de detecção de **30 padrões** baseados em suas observações.
3.  **`aplicativo.py`**: A interface visual (Streamlit). Ela captura as entradas, chama a lógica de análise e exibe os resultados de forma intuitiva.
    """
)
