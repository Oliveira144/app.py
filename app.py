import streamlit as st
from collections import deque, defaultdict, Counter
========== CONFIGURAÇÃO ==========
st.set_page_config(page_title="FS Pattern Master v1 – AI Estratégica 30x", layout="centered")
st.title("🎯 FS Pattern Master v1 – AI Estratégica 30x")
========== MAPA DE CORES ==========
cores = {
"R": "🔴",
"B": "🔵",
"E": "🟡"
}
========== ESTADO ==========
Inicializa o histórico como um deque com tamanho máximo de 27
if "historico" not in st.session_state:
st.session_state.historico = deque(maxlen=27)
Controla o modo G1 (repetir sugestão após erro)
if "modo_g1" not in st.session_state:
st.session_state.modo_g1 = False
Armazena o último padrão detectado
if "ultimo_padrao" not in st.session_state:
st.session_state.ultimo_padrao = None
Armazena a última sugestão feita
if "ultima_sugestao" not in st.session_state:
st.session_state.ultima_sugestao = None
Armazena as estatísticas de acertos e erros por padrão
if "estatisticas" not in st.session_state:
st.session_state.estatisticas = defaultdict(lambda: {"acertos": 0, "erros": 0})
========== INSERÇÃO ==========
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
========== EXIBIÇÃO HISTÓRICO ==========
st.subheader("📊 Histórico (últimos 27)")
CORREÇÃO: Itera sobre o histórico em ordem inversa para exibir os mais recentes primeiro,
sem modificar o deque original.
reversed_historico_iterator = reversed(st.session_state.historico)
current_line_elements = []
line_count = 0
for i, c in enumerate(reversed_historico_iterator):
# Adiciona o emoji correspondente à linha atual, com fallback para '?'
current_line_elements.append(cores.get(c, "❓"))
line_count += 1
# Se a linha atingiu 9 elementos ou é o último elemento do histórico, exibe a linha
if line_count % 9 == 0 or (i + 1) == len(st.session_state.historico):
st.markdown("".join(current_line_elements))
current_line_elements = [] # Reseta para a próxima linha
Caso haja elementos restantes na última linha (menos de 9)
if current_line_elements:
st.markdown("".join(current_line_elements))
========== DETECÇÃO DE PADRÕES ==========
def detectar_padrao(h):
# Garante que o histórico tenha pelo menos 6 elementos para iniciar a detecção
if len(h) < 6:
return None, None
# ---------------------- Padrões 1 a 14 ----------------------
# Verifica se há pelo menos 4 elementos para padrões que usam h[-4:]
if len(h) >= 4 and len(set(h[-4:])) == 1:
return "Sequência Crescente", h[-1]
if len(h) >= 4 and h[-4:-1] == [h[-1]] * 3 and h[-4] != h[-1]:
return "Sequência com Quebra", h[-4]
if len(h) >= 4 and h[-4:] in (["R", "B", "R", "B"], ["B", "R", "B", "R"]):
return "Alternância Padrão", "R" if h[-1] == "B" else "B"
# Verifica se há pelo menos 6 elementos para padrões que usam h[-6:-3]
if len(h) >= 6 and h[-6:-3] == ["R", "B", "R"] and h[-3:] == ["R", "R", "R"]:
return "Alternância + Repetição", "R"
# Verifica se há pelo menos 9 elementos para padrões que usam h[-9:]
if len(h) >= 9 and h[-9:-6] == h[-6:-3] == h[-3:]:
return "Bloco 3x3", h[-1]
if len(h) >= 6 and h[-6:] == h[-6:-3][::-1] + h[-3:]:
return "Espelhamento Horizontal", h[-1]
if len(h) >= 4 and h[-6:-4] == ["R", "R"] and h[-4:-2] == ["B", "B"]:
return "2x Alternado", h[-1]
# Verifica se há pelo menos 7 elementos para padrões que usam h[-7]
if len(h) >= 7 and h[-7] == h[-6] and h[-5] == h[-4] and h[-3] == "E" and h[-2] == h[-1]:
return "2x Alternado com Empate", h[-1]
# Verifica se há pelo menos 10 elementos para padrões que usam h[-10:]
if len(h) >= 10 and h[-10:-5] == h[-5:]:
return "Reescrita de Baralho", h[-1]
if len(h) >= 4 and len(set(h[-4:])) == 4: # Nota: Este padrão pode nunca ser verdadeiro com apenas 3 cores (R, B, E)
return "Anti-Padrão", h[-1]
# Verifica se há pelo menos 3 elementos para padrões que usam h[-3]
if len(h) >= 3 and h[-2] == "E" and h[-3] == h[-1]:
return "Empate Técnico", h[-1]
if len(h) >= 6 and Counter(h[-6:]).most_common(1)[0][1] == 2:
return "Falsa Tendência", Counter(h[-6:]).most_common(1)[0][0]
# Verifica se há pelo menos 18 elementos para padrões que usam h[-18:]
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
if len(h) >= 18 and h[-9:] == h[-18:-9][::-1]:
return "Ciclo 9 Invertido", h[-1]
if len(h) >= 18 and Counter(h[-18:-9]) == Counter(h[-9:]):
return "Reescrita de Bloco 18", h[-1]
# CORREÇÃO: Garante que há pelo menos 9 elementos para acessar h[-9], h[-5] e h[-1]
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
# CORREÇÃO: Garante que há pelo menos 12 elementos para verificar os últimos 12
if len(h) >= 12:
for cor in ["R", "B"]:
if cor not in h[-12:]:
return "Zona Morta", cor
# ---------------------- Padrões de Manipulação ----------------------
if len(h) >= 6 and h[-6:-3] == h[-3:] and h[-1] != h[-4]:
return "Inversão com Delay", h[-1]
# CORREÇÃO: Garante que há pelo menos 8 elementos para acessar h[-8:-4]
if len(h) >= 8 and h[-4:] == ["R", "B", "R", "B"] and h[-8:-4] == ["B", "R", "B", "R"]:
return "Reflexo com Troca Lenta", h[-1]
if len(h) >= 4 and h[-6:-4] == ["R", "R"] and h[-4:-2] == ["B", "B"]:
return "Cascata Fragmentada", h[-1]
# CORREÇÃO: Garante que há pelo menos 5 elementos para acessar h[-5]
if len(h) >= 5 and h[-5] == h[-4] and h[-3] == "E" and h[-1] == "E":
return "Empate Enganoso", h[-2]
# ---------------------- Padrões Dinâmicos ----------------------
# CORREÇÃO: Garante que há pelo menos 2 elementos para acessar h[-2:]
if len(h) >= 2 and h[-2:] == ["R", "R"]:
return "Reação à Perda", "B"
if len(h) >= 2 and h[-2:] == ["B", "B"]:
return "Reação à Perda", "R"
if len(h) >= 6 and h[-6:] in (["R", "E", "B", "E", "R", "B"], ["B", "E", "R", "E", "B", "R"]):
return "Zebra Lenta", h[-1]
# CORREÇÃO: Garante que há pelo menos 4 elementos para acessar h[-4]
if len(h) >= 4 and h[-4] == h[-3] == h[-2] and h[-1] != h[-2]:
return "Padrão de Isca", h[-4]
return None, None
========== SUGESTÃO ==========
st.subheader("🎯 Sugestão Automática")
Passa uma cópia da lista do histórico para a função de detecção
padrao, sugestao = detectar_padrao(list(st.session_state.historico))
if padrao:
st.success(f"Padrão Detectado: {padrao}")
# Usa .get() para evitar erro caso a sugestão seja inválida (embora improvável aqui)
st.markdown(f"👉 Sugestão de entrada: {cores.get(sugestao, '?')} {sugestao}")
st.session_state.ultimo_padrao = padrao
st.session_state.ultima_sugestao = sugestao
st.session_state.modo_g1 = True
else:
st.warning("Nenhum padrão detectado.")
========== VERIFICAÇÃO DE RESULTADO ==========
Verifica se há uma sugestão anterior e histórico suficiente para comparação
if st.session_state.ultima_sugestao and len(st.session_state.historico) >= 2:
# Compara o penúltimo resultado com a última sugestão
if st.session_state.historico[-2] == st.session_state.ultima_sugestao:
st.session_state.estatisticas[st.session_state.ultimo_padrao]["acertos"] += 1
st.success("✅ Entrada anterior foi um ACERTO!")
else:
st.session_state.estatisticas[st.session_state.ultimo_padrao]["erros"] += 1
st.error("❌ Entrada anterior foi um ERRO!")
# Limpa a última sugestão após a verificação
st.session_state.ultima_sugestao = None
========== PAINEL DE DESEMPENHO ==========
st.subheader("📈 Desempenho por Padrão")
for padrao, stats in st.session_state.estatisticas.items():
total = stats["acertos"] + stats["erros"]
if total > 0:
taxa = (stats["acertos"] / total) * 100
st.markdown(f"{padrao} — ✅ {stats['acertos']} / ❌ {stats['erros']} — 🎯 {taxa:.1f}%")
else:
st.markdown(f"{padrao} — Sem dados ainda.") # Mensagem para padrões sem estatísticas
========== CONTROLES ==========
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
st.session_state.estatisticas.clear() # Limpa as estatísticas também
st.success("Histórico e estatísticas limpos.")
Exibe o status do modo G1
if st.session_state.modo_g1:
st.info("🔁 G1 ATIVO: Se a próxima entrada for erro, repita a mesma sugestão.")
