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


if "modo_g1" not in st.session_state:
 st.session_state.modo_g1 = False


if "ultimo_padrao" not in st.session_state:
 st.session_state.ultimo_padrao = None


if "ultima_sugestao" not in st.session_state:
 st.session_state.ultima_sugestao = None


if "estatisticas" not in st.session_state:
 st.session_state.estatisticas = defaultdict(lambda: {"acertos": 0, "erros": 0})


# ========== INSERÇÃO ==========
st.subheader("📥 Inserir resultado")
col1, col2, col3 = st.columns(3)
with col1:
 if st.button("🔴 Red"):
 st.session_state.historico.append("R")
with col2:
 if st.button("🟡 Empate"):
 st.session_state.historico.append("E")
with col3:
 if st.button("🔵 Blue"):
 st.session_state.historico.append("B")


# ========== EXIBIÇÃO HISTÓRICO ==========
st.subheader("📊 Histórico (últimos 27)")
historico_lista = list(st.session_state.historico)
# Inverte a lista para exibir os mais recentes à direita
historico_lista.reverse()
for i in range(0, len(historico_lista), 9):
 linha = historico_lista[:9] # Pega os primeiros 9 após a inversão (os mais recentes)
 historico_lista = historico_lista[:9] # Remove os 9 já exibidos da lista para a próxima iteração
 
 linha_formatada = []
 for c in linha:
 if c in cores:
 linha_formatada.append(cores.get(c, "❓"))
 else:
 linha_formatada.append("❓")
 st.markdown("".join(linha_formatada))


# Refaz a inversão para as outras funcionalidades que possam depender da ordem original
st.session_state.historico.reverse()


# ========== DETECÇÃO DE PADRÕES ==========
def detectar_padrao(h):
 if len(h) < 6:
 return None, None


 # ---------------------- Padrões 1 a 14 ----------------------
 if len(set(h[-4:])) == 1:
 return "Sequência Crescente", h[-1]
 if h[-4:-1] == [h[-1]] * 3 and h[-4] != h[-1]:
 return "Sequência com Quebra", h[-4]
 if h[-4:] in (["R", "B", "R", "B"], ["B", "R", "B", "R"]):
 return "Alternância Padrão", "R" if h[-1] == "B" else "B"
 if h[-6:-3] == ["R", "B", "R"] and h[-3:] == ["R", "R", "R"]:
 return "Alternância + Repetição", "R"
 if len(h) >= 9 and h[-9:-6] == h[-6:-3] == h[-3:]:
 return "Bloco 3x3", h[-1]
 if h[-6:] == h[-6:-3][::-1] + h[-3:]:
 return "Espelhamento Horizontal", h[-1]
 if h[-6:-4] == ["R", "R"] and h[-4:-2] == ["B", "B"]:
 return "2x Alternado", h[-1]
 if h[-7] == h[-6] and h[-5] == h[-4] and h[-3] == "E" and h[-2] == h[-1]:
 return "2x Alternado com Empate", h[-1]
 if len(h) >= 10 and h[-10:-5] == h[-5:]:
 return "Reescrita de Baralho", h[-1]
 if len(set(h[-4:])) == 4:
 return "Anti-Padrão", h[-1]
 if h[-2] == "E" and h[-3] == h[-1]:
 return "Empate Técnico", h[-1]
 if Counter(h[-6:]).most_common(1)[0][1] == 2:
 return "Falsa Tendência", Counter(h[-6:]).most_common(1)[0][0]
 if len(h) >= 18 and h[-9:] == h[-18:-9]:
 return "Repetição Vertical", h[-1]
 if len(h) >= 18 and h[-9:] == h[-18:-9][::-1]:
 return "Inversão Vertical", h[-1]


 # ---------------------- Padrões Psicológicos ----------------------
 if h[-4:] in (["R", "R", "R", "B"], ["B", "B", "B", "R"]):
 return "Indução de Ganância", h[-1]
 if h[-6:] in (["R", "B", "B", "R", "R", "B"], ["B", "R", "R", "B", "B", "R"]):
 return "Padrão de Gancho", h[-1]
 if h[-4] == h[-3] and h[-2] == "E" and h[-1] == h[-4]:
 return "Armadilha de Empate", h[-1]


 # ---------------------- Padrões Cíclicos ----------------------
 if len(h) >= 18 and h[-9:] == h[-18:-9][::-1]:
 return "Ciclo 9 Invertido", h[-1]
 if len(h) >= 18 and Counter(h[-18:-9]) == Counter(h[-9:]):
 return "Reescrita de Bloco 18", h[-1]
 if h[-9] == h[-5] == h[-1]:
 return "Inversão Diagonal", h[-1]


 # ---------------------- Padrões Estatísticos ----------------------
 if h[-6:].count(h[-1]) == 5:
 return "Dominância 5x1", h[-1]
 if len(h) >= 18:
 freq = Counter(h[-18:])
 if freq["R"] < freq["B"]:
 return "Frequência Oculta", "R"
 elif freq["B"] < freq["R"]:
 return "Frequência Oculta", "B"
 for cor in ["R", "B"]:
 if cor not in h[-12:]:
 return "Zona Morta", cor


 # ---------------------- Padrões de Manipulação ----------------------
 if h[-6:-3] == h[-3:] and h[-1] != h[-4]:
 return "Inversão com Delay", h[-1]
 if h[-4:] == ["R", "B", "R", "B"] and h[-8:-4] == ["B", "R", "B", "R"]:
 return "Reflexo com Troca Lenta", h[-1]
 if h[-6:-4] == ["R", "R"] and h[-4:-2] == ["B", "B"]:
 return "Cascata Fragmentada", h[-1]
 if h[-5] == h[-4] and h[-3] == "E" and h[-1] == "E":
 return "Empate Enganoso", h[-2]


 # ---------------------- Padrões Dinâmicos ----------------------
 if h[-2:] == ["R", "R"]:
 return "Reação à Perda", "B"
 if h[-2:] == ["B", "B"]:
 return "Reação à Perda", "R"
 if h[-6:] in (["R", "E", "B", "E", "R", "B"], ["B", "E", "R", "E", "B", "R"]):
 return "Zebra Lenta", h[-1]
 if h[-4] == h[-3] == h[-2] and h[-1] != h[-2]:
 return "Padrão de Isca", h[-4]


 return None, None


# ========== SUGESTÃO ==========
st.subheader("🎯 Sugestão Automática")
padrao, sugestao = detectar_padrao(list(st.session_state.historico))


if padrao:
 st.success(f"Padrão Detectado: **{padrao}**")
 st.markdown(f"👉 Sugestão de entrada: **{cores.get(sugestao, '?')} {sugestao}**")
 st.session_state.ultimo_padrao = padrao
 st.session_state.ultima_sugestao = sugestao
 st.session_state.modo_g1 = True
else:
 st.warning("Nenhum padrão detectado.")


# ========== VERIFICAÇÃO DE RESULTADO ==========
if st.session_state.ultima_sugestao and len(st.session_state.historico) >= 2:
 if st.session_state.historico[-2] == st.session_state.ultima_sugestao:
 st.session_state.estatisticas.get(st.session_state.ultimo_padrao, {"acertos": 0, "erros": 0})["acertos"] += 1
 st.success("✅ Entrada anterior foi um ACERTO!")
 else:
 st.session_state.estatisticas.get(st.session_state.ultimo_padrao, {"acertos": 0, "erros": 0})["erros"] += 1
 st.error("❌ Entrada anterior foi um ERRO!")
 st.session_state.ultima_sugestao = None


# ========== PAINEL DE DESEMPENHO ==========
st.subheader("📈 Desempenho por Padrão")
for padrao, stats in st.session_state.estatisticas.items():
 total = stats["acertos"] + stats["erros"]
 if total > 0:
 taxa = (stats["acertos"] / total) * 100
 st.markdown(f"**{padrao}** — ✅ {stats['acertos']} / ❌ {stats['erros']} — 🎯 {taxa:.1f}%")


# ========== CONTROLES ==========
col1, col2 = st.columns(2)
with col1:
 if st.button("❌ Desativar G1"):
 st.session_state.modo_g1 = False
 st.success("Modo G1 desativado.")
with col2:
 if st.button("🧹 Limpar Histórico"):
 st.session_state.historico.clear()
 st.session_state.ultima_sugestao = None
 st.session_state.ultimo_padrao = None
 st.success("Histórico limpo.")


if st.session_state.modo_g1:
 st.info("🔁 G1 ATIVO: Se a próxima entrada for erro, repita a mesma sugestão.")
