import streamlit as st
from collections import deque, defaultdict, Counter

# ========== CONFIGURAÇÃO ==========
st.set_page_config(page_title="FS Pattern Master v1 – AI Estratégica 30x", layout="centered")
st.title("🎯 FS Pattern Master v1 – AI Estratégica 30x")

# ========== MAPA DE CORES ==========
cores = {
    "R": "🔴",
    "B": "🔵",
    "E": "🟡"
}

# ========== ESTADO ==========
# Inicializa o histórico como um deque com tamanho máximo de 27
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=27)

# Controla o modo G1 (repetir sugestão após erro)
if "modo_g1" not in st.session_state:
    st.session_state.modo_g1 = False

# Armazena a última sugestão que foi feita e está aguardando um resultado
# Armazena uma tupla (nome_do_padrao, cor_sugerida)
if "pending_suggestion_for_check" not in st.session_state:
    st.session_state.pending_suggestion_for_check = None 

# Armazena a sugestão que falhou na rodada anterior, para repetição no modo G1
if "g1_last_failed_suggestion" not in st.session_state:
    st.session_state.g1_last_failed_suggestion = None

# Armazena as estatísticas de acertos e erros por padrão
if "estatisticas" not in st.session_state:
    st.session_state.estatisticas = defaultdict(lambda: {"acertos": 0, "erros": 0})

# ========== INSERÇÃO ==========
st.subheader("📥 Inserir resultado")
col1, col2, col3 = st.columns(3)

# Função para lidar com cliques nos botões e verificação de resultados
def handle_input(color):
    # Antes de adicionar a nova entrada, verifica se havia uma sugestão pendente para avaliar
    if st.session_state.pending_suggestion_for_check:
        pending_pattern, pending_suggestion = st.session_state.pending_suggestion_for_check
        current_result = color # A cor recém-clicada é o resultado

        if current_result == pending_suggestion:
            st.session_state.estatisticas[pending_pattern]["acertos"] += 1
            st.success(f"✅ Entrada para o padrão '{pending_pattern}' foi um ACERTO!")
            st.session_state.g1_last_failed_suggestion = None # Limpa a repetição G1 se foi um acerto
        else:
            st.session_state.estatisticas[pending_pattern]["erros"] += 1
            st.error(f"❌ Entrada para o padrão '{pending_pattern}' foi um ERRO!")
            if st.session_state.modo_g1:
                st.session_state.g1_last_failed_suggestion = pending_suggestion # Armazena para repetição G1
            else:
                st.session_state.g1_last_failed_suggestion = None

        # Limpa a sugestão pendente após ela ter sido verificada
        st.session_state.pending_suggestion_for_check = None
    
    # Agora, adiciona a nova entrada ao histórico
    st.session_state.historico.append(color)

with col1:
    if st.button("🔴 Red"):
        handle_input("R")
with col2:
    if st.button("🟡 Empate"):
        handle_input("E")
with col3:
    if st.button("🔵 Blue"):
        handle_input("B")

# ========== EXIBIÇÃO HISTÓRICO ==========
st.subheader("📊 Histórico (últimos 27)")
# Itera sobre o histórico em ordem inversa para exibir os mais recentes primeiro,
# sem modificar o deque original.
reversed_historico_list = list(reversed(st.session_state.historico)) # Converte para lista para facilitar a iteração
current_line_elements = []
for i, c in enumerate(reversed_historico_list):
    # Adiciona o emoji correspondente à linha atual, com fallback para '?'
    current_line_elements.append(cores.get(c, "❓"))
    # Verifica se uma linha de 9 elementos está completa ou se é o último elemento total
    if (i + 1) % 9 == 0 or (i + 1) == len(reversed_historico_list):
        st.markdown("".join(current_line_elements))
        current_line_elements = [] # Reseta para a próxima linha

# ========== DETECÇÃO DE PADRÕES ==========
def detectar_padrao(h):
    # Garante que o histórico tenha pelo menos 6 elementos para iniciar a detecção
    if len(h) < 6:
        return None, None

    # ---------------------- Padrões 1 a 14 ----------------------
    if len(h) >= 4 and len(set(h[-4:])) == 1:
        return "Sequência Crescente", h[-1]
    if len(h) >= 4 and h[-4:-1] == [h[-1]] * 3 and h[-4] != h[-1]:
        return "Sequência com Quebra", h[-4]
    if len(h) >= 4 and h[-4:] in (["R", "B", "R", "B"], ["B", "R", "B", "R"]):
        return "Alternância Padrão", "R" if h[-1] == "B" else "B"
    if len(h) >= 6 and h[-6:-3] == ["R", "B", "R"] and h[-3:] == ["R", "R", "R"]:
        return "Alternância + Repetição", "R"
    if len(h) >= 9 and h[-9:-6] == h[-6:-3] == h[-3:]:
        return "Bloco 3x3", h[-1]
    if len(h) >= 6 and h[-6:] == h[-6:-3][::-1] + h[-3:]:
        return "Espelhamento Horizontal", h[-1]
    if len(h) >= 6 and h[-6:-4] == ["R", "R"] and h[-4:-2] == ["B", "B"]: # Comprimento corrigido
        return "2x Alternado", h[-1]
    if len(h) >= 7 and h[-7] == h[-6] and h[-5] == h[-4] and h[-3] == "E" and h[-2] == h[-1]:
        return "2x Alternado com Empate", h[-1]
    if len(h) >= 10 and h[-10:-5] == h[-5:]:
        return "Reescrita de Baralho", h[-1]
    if len(h) >= 4 and len(set(h[-4:])) == 4: # Nota: Este padrão nunca será verdadeiro com apenas 3 cores (R, B, E)
        return "Anti-Padrão", h[-1]
    if len(h) >= 3 and h[-2] == "E" and h[-3] == h[-1]:
        return "Empate Técnico", h[-1]
    if len(h) >= 6 and Counter(h[-6:]).most_common(1)[0][1] == 2:
        return "Falsa Tendência", Counter(h[-6:]).most_common(1)[0][0]
    if len(h) >= 18 and h[-9:] == h[-18:-9]:
        return "Repetição Vertical", h[-1]
    if len(h) >= 18 and h[-9:] == h[-18:-9][::-1]:
        return "Inversão Vertical", h[-1]

    # ---------------------- Padrões Psicológicos ----------------------
    if len(h) >= 4 and h[-4:] in (["R", "R", "R", "B"], ["B", "B", "B", "R"]):
        return "Indução de Ganância", h[-1]
    if len(h) >= 6 and h[-6:] in (["R", "B", "B", "R", "R", "B"], ["B", "R", "R", "B", "B", "R"]):
        return "Padrão de Gancho", h[-1]
    if len(h) >= 4 and h[-4] == h[-3] and h[-2] == "E" and h[-1] == h[-4]:
        return "Armadilha de Empate", h[-1]

    # ---------------------- Padrões Cíclicos ----------------------
    if len(h) >= 18 and h[-9:] == h[-18:-9][::-1]: # Duplicado de Inversão Vertical, mantido conforme original
        return "Ciclo 9 Invertido", h[-1]
    if len(h) >= 18 and Counter(h[-18:-9]) == Counter(h[-9:]):
        return "Reescrita de Bloco 18", h[-1]
    if len(h) >= 9 and h[-9] == h[-5] == h[-1]:
        return "Inversão Diagonal", h[-1]

    # ---------------------- Padrões Estatísticos ----------------------
    if len(h) >= 6 and h[-6:].count(h[-1]) == 5:
        return "Dominância 5x1", h[-1]
    if len(h) >= 18:
        freq = Counter(h[-18:])
        if freq["R"] < freq["B"]:
            return "Frequência Oculta", "R"
        elif freq["B"] < freq["R"]:
            return "Frequência Oculta", "B"
    if len(h) >= 12:
        for cor in ["R", "B"]:
            if cor not in h[-12:]:
                return "Zona Morta", cor

    # ---------------------- Padrões de Manipulação ----------------------
    if len(h) >= 6 and h[-6:-3] == h[-3:] and h[-1] != h[-4]:
        return "Inversão com Delay", h[-1]
    if len(h) >= 8 and h[-4:] == ["R", "B", "R", "B"] and h[-8:-4] == ["B", "R", "B", "R"]:
        return "Reflexo com Troca Lenta", h[-1]
    if len(h) >= 6 and h[-6:-4] == ["R", "R"] and h[-4:-2] == ["B", "B"]: # Comprimento corrigido, duplicado de "2x Alternado"
        return "Cascata Fragmentada", h[-1]
    if len(h) >= 5 and h[-5] == h[-4] and h[-3] == "E" and h[-1] == "E":
        return "Empate Enganoso", h[-2]

    # ---------------------- Padrões Dinâmicos ----------------------
    if len(h) >= 2 and h[-2:] == ["R", "R"]:
        return "Reação à Perda", "B"
    if len(h) >= 2 and h[-2:] == ["B", "B"]:
        return "Reação à Perda", "R"
    if len(h) >= 6 and h[-6:] in (["R", "E", "B", "E", "R", "B"], ["B", "E", "R", "E", "B", "R"]):
        return "Zebra Lenta", h[-1]
    if len(h) >= 4 and h[-4] == h[-3] == h[-2] and h[-1] != h[-2]:
        return "Padrão de Isca", h[-4]

    return None, None

# ========== SUGESTÃO AUTOMÁTICA ==========
st.subheader("🎯 Sugestão Automática")

current_padrao = None
current_sugestao = None

# Prioriza a repetição G1 se estiver ativo e houver uma sugestão que falhou anteriormente
if st.session_state.modo_g1 and st.session_state.g1_last_failed_suggestion:
    current_padrao = "G1 (Repetição após erro)"
    current_sugestao = st.session_state.g1_last_failed_suggestion
    st.session_state.g1_last_failed_suggestion = None # Limpa após usar
    st.info("🔁 Modo G1 Ativo: Repetindo sugestão anterior devido a erro.")
else:
    # Passa uma cópia da lista do histórico para a função de detecção
    current_padrao, current_sugestao = detectar_padrao(list(st.session_state.historico))

if current_padrao:
    st.success(f"Padrão Detectado: {current_padrao}")
    st.markdown(f"👉 Sugestão de entrada: {cores.get(current_sugestao, '?')} {current_sugestao}")
    # Define a sugestão pendente para a *próxima* entrada
    st.session_state.pending_suggestion_for_check = (current_padrao, current_sugestao)
else:
    st.warning("Nenhum padrão detectado.")
    st.session_state.pending_suggestion_for_check = None # Garante que esteja limpo se não houver sugestão

# ========== PAINEL DE DESEMPENHO ==========
st.subheader("📈 Desempenho por Padrão")
if not st.session_state.estatisticas:
    st.info("Nenhum dado de desempenho ainda. Insira resultados para começar.")
else:
    for padrao, stats in st.session_state.estatisticas.items():
        total = stats["acertos"] + stats["erros"]
        if total > 0:
            taxa = (stats["acertos"] / total) * 100
            st.markdown(f"**{padrao}** — ✅ {stats['acertos']} / ❌ {stats['erros']} — 🎯 {taxa:.1f}%")
        else:
            st.markdown(f"**{padrao}** — Sem dados ainda.")

# ========== CONTROLES ==========
st.subheader("⚙️ Controles")
col_controls1, col_controls2 = st.columns(2)

with col_controls1:
    if st.button("Alternar Modo G1"):
        st.session_state.modo_g1 = not st.session_state.modo_g1
        if st.session_state.modo_g1:
            st.success("Modo G1 ATIVADO.")
        else:
            st.warning("Modo G1 DESATIVADO.")
            st.session_state.g1_last_failed_suggestion = None # Limpa se o G1 for desativado

with col_controls2:
    if st.button("🧹 Limpar Histórico e Estatísticas"):
        st.session_state.historico.clear()
        st.session_state.pending_suggestion_for_check = None
        st.session_state.g1_last_failed_suggestion = None
        st.session_state.estatisticas.clear() # Limpa as estatísticas também
        st.success("Histórico e estatísticas limpos.")
        
# Exibe o status do modo G1
if st.session_state.modo_g1:
    st.info("🔁 G1 ATIVO: Se a próxima entrada for erro, repita a mesma sugestão.")
else:
    st.info("G1 DESATIVADO.")

