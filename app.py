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
if "historico" not in st.session_state:
    st.session_state.historico = deque(maxlen=27)
if "pending_suggestion_for_check" not in st.session_state:
    st.session_state.pending_suggestion_for_check = None 
if "estatisticas" not in st.session_state:
    st.session_state.estatisticas = defaultdict(lambda: {"acertos": 0, "erros": 0})
# A variável 'modo_g1' agora é usada apenas para exibição
if "modo_g1" not in st.session_state:
    st.session_state.modo_g1 = False

# ========== INSERÇÃO ==========
st.subheader("📥 Inserir resultado")
col1, col2, col3 = st.columns(3)

def handle_input(color):
    if st.session_state.pending_suggestion_for_check:
        pending_pattern_name, pending_suggestion_color = st.session_state.pending_suggestion_for_check
        current_result = color

        if current_result == pending_suggestion_color:
            st.session_state.estatisticas[pending_pattern_name]["acertos"] += 1
            st.success(f"✅ Entrada para o padrão '{pending_pattern_name}' foi um ACERTO!")
            st.session_state.modo_g1 = False
        else:
            st.session_state.estatisticas[pending_pattern_name]["erros"] += 1
            st.error(f"❌ Entrada para o padrão '{pending_pattern_name}' foi um ERRO!")
            st.session_state.modo_g1 = True
            
        st.session_state.pending_suggestion_for_check = None
    
    st.session_state.historico.append(color)
    st.experimental_rerun()


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
reversed_historico_list = list(reversed(st.session_state.historico))
current_line_elements = []
for i, c in enumerate(reversed_historico_list):
    current_line_elements.append(cores.get(c, "❓"))
    if (i + 1) % 9 == 0 or (i + 1) == len(reversed_historico_list):
        st.markdown("".join(current_line_elements))
        current_line_elements = []

# ========== DETECÇÃO DE PADRÕES ==========
padroes_definitions = [
    # Padrões com Prioridade 10
    {"name": "Reação à Perda", "priority": 10, "min_len": 2, 
     "detect_func": lambda h: "B" if h[-2:] == ["R", "R"] else "R" if h[-2:] == ["B", "B"] else None},
    {"name": "Sequência Crescente", "priority": 10, "min_len": 4, 
     "detect_func": lambda h: h[-1] if len(set(h[-4:])) == 1 else None},
    
    # Padrões com Prioridade 9
    {"name": "Inversão com Delay", "priority": 9, "min_len": 6, 
     "detect_func": lambda h: h[-1] if h[-6:-3] == h[-3:] and h[-1] != h[-4] else None},
    {"name": "Padrão de Isca", "priority": 9, "min_len": 4, 
     "detect_func": lambda h: h[-4] if h[-4] == h[-3] == h[-2] and h[-1] != h[-2] else None},
    {"name": "Indução de Ganância", "priority": 9, "min_len": 4, 
     "detect_func": lambda h: h[-1] if h[-4:] in (["R", "R", "R", "B"], ["B", "B", "B", "R"]) else None},
    {"name": "Sequência com Quebra", "priority": 9, "min_len": 4, 
     "detect_func": lambda h: h[-4] if h[-4:-1] == [h[-1]] * 3 and h[-4] != h[-1] else None},

    # Padrões com Prioridade 8
    {"name": "Alternância Padrão", "priority": 8, "min_len": 4, 
     "detect_func": lambda h: "R" if h[-1] == "B" and h[-4:-1] == ["R", "B", "R"] else "B" if h[-1] == "R" and h[-4:-1] == ["B", "R", "B"] else None},
    {"name": "Alternância + Repetição", "priority": 8, "min_len": 6, 
     "detect_func": lambda h: "R" if h[-6:-3] == ["R", "B", "R"] and h[-3:] == ["R", "R", "R"] else None},
    {"name": "Padrão de Gancho", "priority": 8, "min_len": 6, 
     "detect_func": lambda h: h[-1] if h[-6:] in (["R", "B", "B", "R", "R", "B"], ["B", "R", "R", "B", "B", "R"]) else None},
    {"name": "Reflexo com Troca Lenta", "priority": 8, "min_len": 8, 
     "detect_func": lambda h: h[-1] if h[-4:] == ["R", "B", "R", "B"] and h[-8:-4] == ["B", "R", "B", "R"] else None},
    {"name": "Zebra Lenta", "priority": 8, "min_len": 6, 
     "detect_func": lambda h: h[-1] if h[-6:] in (["R", "E", "B", "E", "R", "B"], ["B", "E", "R", "E", "B", "R"]) else None},
    {"name": "Dominância 5x1", "priority": 8, "min_len": 6, 
     "detect_func": lambda h: h[-1] if h[-6:].count(h[-1]) == 5 else None},

    # Padrões com Prioridade 7
    {"name": "Repetição Vertical", "priority": 7, "min_len": 18, 
     "detect_func": lambda h: h[-1] if h[-9:] == h[-18:-9] else None},
    {"name": "Inversão Vertical", "priority": 7, "min_len": 18, 
     "detect_func": lambda h: h[-1] if h[-9:] == h[-18:-9][::-1] else None},
    {"name": "Bloco 3x3", "priority": 7, "min_len": 9, 
     "detect_func": lambda h: h[-1] if h[-9:-6] == h[-6:-3] == h[-3:] else None},
    {"name": "Espelhamento Horizontal", "priority": 7, "min_len": 6, 
     "detect_func": lambda h: h[-1] if h[-6:] == h[-6:-3][::-1] + h[-3:] else None},
    {"name": "Armadilha de Empate", "priority": 7, "min_len": 4, 
     "detect_func": lambda h: h[-1] if h[-4] == h[-3] and h[-2] == "E" and h[-1] == h[-4] else None},
    {"name": "Ciclo 9 Invertido", "priority": 7, "min_len": 18, 
     "detect_func": lambda h: h[-1] if h[-9:] == h[-18:-9][::-1] else None},
    {"name": "Cascata Fragmentada", "priority": 7, "min_len": 6, 
     "detect_func": lambda h: "B" if h[-6:-4] == ["R", "R"] and h[-4:-2] == ["B", "B"] else "R" if h[-6:-4] == ["B", "B"] and h[-4:-2] == ["R", "R"] else None},
    {"name": "Empate Enganoso", "priority": 7, "min_len": 5, 
     "detect_func": lambda h: h[-2] if h[-5] == h[-4] and h[-3] == "E" and h[-1] == "E" else None},
    {"name": "Frequência Oculta", "priority": 7, "min_len": 18, 
     "detect_func": lambda h: "R" if Counter(h[-18:])["R"] < Counter(h[-18:])["B"] else "B" if Counter(h[-18:])["B"] < Counter(h[-18:])["R"] else None},

    # Padrões com Prioridade 6
    {"name": "2x Alternado", "priority": 6, "min_len": 6, 
     "detect_func": lambda h: "B" if h[-6:-4] == ["R", "R"] and h[-4:-2] == ["B", "B"] else "R" if h[-6:-4] == ["B", "B"] and h[-4:-2] == ["R", "R"] else None},
    {"name": "2x Alternado com Empate", "priority": 6, "min_len": 7, 
     "detect_func": lambda h: h[-1] if h[-7] == h[-6] and h[-5] == h[-4] and h[-3] == "E" and h[-2] == h[-1] else None},
    {"name": "Reescrita de Bloco 18", "priority": 6, "min_len": 18, 
     "detect_func": lambda h: h[-1] if Counter(h[-18:-9]) == Counter(h[-9:]) else None},
    {"name": "Zona Morta", "priority": 6, "min_len": 12, 
     "detect_func": lambda h: "R" if "R" not in h[-12:] else "B" if "B" not in h[-12:] else None},

    # Padrões com Prioridade 5
    {"name": "Reescrita de Baralho", "priority": 5, "min_len": 10, 
     "detect_func": lambda h: h[-1] if h[-10:-5] == h[-5:] else None},
    {"name": "Empate Técnico", "priority": 5, "min_len": 3, 
     "detect_func": lambda h: h[-1] if h[-2] == "E" and h[-3] == h[-1] else None},
    {"name": "Inversão Diagonal", "priority": 5, "min_len": 9, 
     "detect_func": lambda h: h[-1] if h[-9] == h[-5] == h[-1] else None},

    # Padrões com Prioridade 4
    {"name": "Anti-Padrão", "priority": 4, "min_len": 4, 
     "detect_func": lambda h: h[-1] if len(set(h[-4:])) == 4 else None}, 
    {"name": "Falsa Tendência", "priority": 4, "min_len": 6, 
     "detect_func": lambda h: Counter(h[-6:]).most_common(1)[0][0] if Counter(h[-6:]).most_common(1)[0][1] == 2 else None},
]

def detectar_padrao_otimizado(h):
    detected_patterns = []
    
    for pattern_def in padroes_definitions:
        if len(h) >= pattern_def["min_len"]:
            sugestao = pattern_def["detect_func"](h)
            if sugestao:
                detected_patterns.append({
                    "name": pattern_def["name"],
                    "sugestao": sugestao,
                    "priority": pattern_def["priority"]
                })
    
    # Ordena os padrões detectados por prioridade (maior primeiro)
    detected_patterns.sort(key=lambda x: x["priority"], reverse=True)
    
    if detected_patterns:
        # Retorna o padrão de maior prioridade
        return detected_patterns[0]["name"], detected_patterns[0]["sugestao"]
    return None, None

# ========== SUGESTÃO AUTOMÁTICA ==========
st.subheader("🎯 Sugestão Automática")

current_padrao = None
current_sugestao = None

# A sugestão só aparece se houver 9 ou mais resultados no histórico
if len(st.session_state.historico) < 9:
    st.info(f"Aguardando mais {9 - len(st.session_state.historico)} resultados para começar a análise de padrões.")
    st.session_state.pending_suggestion_for_check = None
else:
    # A lógica G1 agora é uma reanálise, não uma repetição
    current_padrao, current_sugestao = detectar_padrao_otimizado(list(st.session_state.historico))
    
    if current_padrao and current_sugestao:
        if st.session_state.modo_g1:
            st.info("🔁 Modo G1 Ativo: Reanalisando após erro anterior.")
        st.success(f"Padrão Detectado: {current_padrao}")
        st.markdown(f"👉 Sugestão de entrada: {cores.get(current_sugestao, '?')} **{current_sugestao}**")
        st.session_state.pending_suggestion_for_check = (current_padrao, current_sugestao)
    else:
        st.warning("Nenhum padrão detectado no momento.")
        st.session_state.pending_suggestion_for_check = None
        st.session_state.modo_g1 = False

# ========== PAINEL DE DESEMPENHO ==========
st.subheader("📈 Desempenho por Padrão")
if not st.session_state.estatisticas:
    st.info("Nenhum dado de desempenho ainda. Insira resultados para começar.")
else:
    stats_list = sorted(st.session_state.estatisticas.items(), key=lambda item: (item[1]['acertos'] + item[1]['erros']), reverse=True)
    for padrao, stats in stats_list:
        total = stats["acertos"] + stats["erros"]
        if total > 0:
            taxa = (stats["acertos"] / total) * 100
            st.markdown(f"**{padrao}** — ✅ {stats['acertos']} / ❌ {stats['erros']} — 🎯 **{taxa:.1f}%**")
        else:
            st.markdown(f"**{padrao}** — Sem dados ainda.")

# ========== CONTROLES ==========
st.subheader("⚙️ Controles")
col_controls1, col_controls2 = st.columns(2)

with col_controls1:
    if st.button("Alternar Modo G1 (Manual)"):
        st.session_state.modo_g1 = not st.session_state.modo_g1
        if st.session_state.modo_g1:
            st.success("Modo G1 ATIVADO MANUALMENTE.")
        else:
            st.warning("Modo G1 DESATIVADO MANUALMENTE.")

with col_controls2:
    if st.button("🧹 Limpar Histórico e Estatísticas"):
        st.session_state.historico.clear()
        st.session_state.pending_suggestion_for_check = None
        st.session_state.estatisticas.clear()
        st.session_state.modo_g1 = False
        st.success("Histórico e estatísticas limpos.")
        st.experimental_rerun()
        
if st.session_state.modo_g1:
    st.info("🔁 G1 ATIVO: Reanalisando após erro anterior.")
else:
    st.info("G1 DESATIVADO.")
