import collections

class GerenciadorDeDados:
    def __init__(self, history_size=27):
        self.history = collections.deque(maxlen=history_size)
        self.wins = collections.defaultdict(int)
        self.bets_log = []

    def adicionar_resultado(self, result):
        if len(self.history) == self.history.maxlen:
            old_result = self.history[0]
            self.wins[old_result] -= 1
        self.history.append(result)
        self.wins[result] += 1

    def desfazer_ultimo(self):
        if self.history:
            last_result = self.history.pop()
            self.wins[last_result] -= 1
            if self.bets_log:
                self.bets_log.pop()

    def limpar_historico(self):
        self.history.clear()
        self.wins = collections.defaultdict(int)
        self.bets_log.clear()

    def registrar_aposta(self, bet, actual_result):
        is_correct = (bet == actual_result)
        self.bets_log.append({
            'bet': bet,
            'actual': actual_result,
            'correct': is_correct
        })
        return is_correct

    def obter_performance(self):
        if not self.bets_log:
            return 0, 0, 0.0
        total_bets = len(self.bets_log)
        correct_bets = sum(1 for log in self.bets_log if log['correct'])
        accuracy = (correct_bets / total_bets) * 100
        return correct_bets, total_bets, accuracy
import collections

class AnalisadorDePadroes:
    def __init__(self):
        self.patterns = {
            'Sequência Crescente': self._check_growing_sequence,
            'Sequência com Quebra': self._check_break_sequence,
            'Alternância Padrão': self._check_alternating,
            'Alternância + Repetição': self._check_alternating_and_repeat,
            'Bloco 3x3': self._check_3x3_block,
            'Espelhamento Horizontal': self._check_horizontal_mirror,
            '2x Alternado': self._check_2x_alternating,
            '2x Alternado com Empate': self._check_2x_alternating_with_tie,
            'Reescrita de Baralho': self._check_deck_rewrite,
            'Anti-Padrão': self._check_anti_pattern,
            'Empate Técnico': self._check_technical_tie,
            'Falsa Tendência': self._check_false_trend,
            'Repetição Vertical': self._check_vertical_repetition,
            'Inversão Vertical Estrutural': self._check_structural_vertical_inversion,
            'Indução de Ganância': self._check_greed_induction,
            'Padrão de Gancho': self._check_hook_pattern,
            'Armadilha de Empate': self._check_tie_trap,
            'Ciclo 9 Invertido': self._check_inverted_9_cycle,
            'Reescrita de Bloco 18': self._check_block_18_rewrite,
            'Inversão Diagonal': self._check_diagonal_inversion,
            'Dominância 5x1': self._check_dominance_5x1,
            'Frequência Oculta': self._check_hidden_frequency,
            'Zona Morta': self._check_dead_zone,
            'Inversão com Delay': self._check_inversion_with_delay,
            'Reflexo com Troca Lenta': self._check_slow_swap_reflex,
            'Cascata Fragmentada': self._check_fragmented_cascade,
            'Empate Enganoso': self._check_deceptive_tie,
            'Reação à Perda do Jogador': self._check_player_loss_reaction,
            'Zebra Lenta': self._check_slow_zebra,
            'Padrão de Isca': self._check_bait_pattern,
        }

    def _get_last_n_results(self, history, n):
        return list(history)[-n:]

    def _check_growing_sequence(self, history):
        if len(history) >= 2 and history[-1] == history[-2]:
            return "Sequência Crescente", history[-1]
        return None

    def _check_break_sequence(self, history):
        if len(history) >= 3 and history[-3] == history[-2] and history[-3] != history[-1]:
            return "Sequência com Quebra", history[-3]
        return None

    def _check_alternating(self, history):
        if len(history) >= 4 and history[-1] == history[-3] and history[-2] == history[-4] and history[-1] != history[-2]:
            return "Alternância Padrão", history[-1]
        return None

    def _check_alternating_and_repeat(self, history):
        if len(history) >= 6 and history[-6:-2] == list(history)[-6:-2] and history[-2] == history[-1]:
            return "Alternância + Repetição", history[-1]
        return None

    def _check_3x3_block(self, history):
        if len(history) >= 3 and history[-1] == history[-2] == history[-3]:
            return "Bloco 3x3", history[-1]
        return None

    def _check_horizontal_mirror(self, history):
        if len(history) >= 6 and history[-3:] == list(reversed(history[-6:-3])):
            return "Espelhamento Horizontal", history[-1]
        return None

    def _check_2x_alternating(self, history):
        if len(history) >= 4 and history[-4:-2] == list(history)[-2:]:
            return "2x Alternado", history[-1]
        return None
    
    def _check_2x_alternating_with_tie(self, history):
        if len(history) >= 5 and history[-5] == history[-4] and history[-3] == '🟡' and history[-2] == history[-1]:
            return "2x Alternado com Empate", history[-2]
        return None

    def _check_deck_rewrite(self, history):
        if len(history) >= 6 and history[-3:] == list(reversed(history[-6:-3])) and history[-1] != history[-4]:
            return "Reescrita de Baralho", history[-1]
        return None

    def _check_anti_pattern(self, history):
        if len(history) >= 6 and (self._check_growing_sequence(history) or self._check_alternating(history)):
            return "Anti-Padrão", '🔴' if history[-1] == '🔵' else '🔵'
        return None

    def _check_technical_tie(self, history):
        if len(history) >= 4 and history[-4] == history[-3] and history[-2] == '🟡' and history[-1] == history[-4]:
            return "Empate Técnico", history[-1]
        return None

    def _check_false_trend(self, history):
        if len(history) >= 5:
            last_5 = self._get_last_n_results(history, 5)
            counts = collections.Counter(last_5)
            if len(counts) > 2:
                return "Falsa Tendência", counts.most_common(1)[0][0]
        return None

    def _check_vertical_repetition(self, history):
        if len(history) >= 18:
            lines = [history[i:i+9] for i in range(0, len(history), 9)]
            if len(lines) >= 2 and lines[-1] == lines[-2]:
                return "Repetição Vertical", history[-1]
        return None

    def _check_structural_vertical_inversion(self, history):
        if len(history) >= 6 and list(reversed(history[-3:])) == history[-6:-3]:
            return "Inversão Vertical Estrutural", history[-1]
        return None

    def _check_greed_induction(self, history):
        if len(history) >= 4 and history[-4] == history[-3] == history[-2] and history[-1] != history[-4]:
            return "Indução de Ganância", history[-1]
        return None

    def _check_hook_pattern(self, history):
        if len(history) >= 3 and history[-3] == history[-2] and history[-1] != history[-2]:
            return "Padrão de Gancho", history[-1]
        return None

    def _check_tie_trap(self, history):
        if len(history) >= 4 and history[-2] == '🟡' and history[-1] != history[-3] and history[-3] != history[-4]:
            return "Armadilha de Empate", history[-3]
        return None
    
    def _check_inverted_9_cycle(self, history):
        if len(history) >= 18 and list(reversed(history[-9:])) == history[-18:-9]:
            return "Ciclo 9 Invertido", history[-1]
        return None

    def _check_block_18_rewrite(self, history):
        if len(history) >= 18 and collections.Counter(history[-9:]) == collections.Counter(history[-18:-9]):
            return "Reescrita de Bloco 18", history[-1]
        return None
    
    def _check_diagonal_inversion(self, history):
        if len(history) >= 6 and history[-6] == history[-4] and history[-4] == history[-2] and history[-5] == history[-3] and history[-3] == history[-1] and history[-6] != history[-5]:
            return "Inversão Diagonal", history[-1]
        return None

    def _check_dominance_5x1(self, history):
        if len(history) >= 6 and history[-6:-1] == [history[-6]] * 5 and history[-1] != history[-6]:
            return "Dominância 5x1", history[-6]
        return None

    def _check_hidden_frequency(self, history):
        if len(history) >= 18:
            last_18 = self._get_last_n_results(history, 18)
            counts = collections.Counter(last_18)
            min_count = min(counts.values()) if counts else 0
            if min_count < 6:
                for color, count in counts.items():
                    if count == min_count:
                        return "Frequência Oculta", color
        return None

    def _check_dead_zone(self, history):
        if len(history) >= 12:
            last_12 = self._get_last_n_results(history, 12)
            counts = collections.Counter(last_12)
            for color in ['🔴', '🔵', '🟡']:
                if counts[color] == 0:
                    return "Zona Morta", color
        return None

    def _check_inversion_with_delay(self, history):
        if len(history) >= 6 and history[-6:-3] == history[-3:]:
            return "Inversão com Delay", '🔴' if history[-1] == '🔵' else '🔵'
        return None

    def _check_slow_swap_reflex(self, history):
        if len(history) >= 8 and history[-4] == history[-1] and history[-3] == history[-2] and history[-4] != history[-3] and history[-8:-4] == history[-4:]:
            return "Reflexo com Troca Lenta", history[-1]
        return None

    def _check_fragmented_cascade(self, history):
        if len(history) >= 6 and history[-6:-4] == [history[-6]]*2 and history[-4:-2] == [history[-4]]*2 and history[-2:] == [history[-2]]*2:
            return "Cascata Fragmentada", history[-1]
        return None

    def _check_deceptive_tie(self, history):
        if len(history) >= 5 and history[-3] == '🟡' and history[-1] != history[-4] and history[-2] != history[-4]:
            return "Empate Enganoso", history[-4]
        return None

    def _check_player_loss_reaction(self, history):
        if len(history) >= 4 and history[-4:-2] == history[-2:] and history[-2] != history[-4]:
            return "Reação à Perda do Jogador", history[-2]
        return None

    def _check_slow_zebra(self, history):
        if len(history) >= 6 and history[-1] == history[-3] and history[-2] == '🟡' and history[-4] == history[-6] and history[-5] == '🟡':
            return "Zebra Lenta", history[-1]
        return None
    
    def _check_bait_pattern(self, history):
        if len(history) >= 4 and history[-4] == history[-3] == history[-2] and history[-1] != history[-4]:
            return "Padrão de Isca", history[-4]
        return None
        
    def analyze_history(self, history):
        detected_patterns = []
        for name, check_function in self.patterns.items():
            result = check_function(history)
            if result:
                detected_patterns.append(result)
        
        if detected_patterns:
            best_suggestion = self._get_best_suggestion(detected_patterns)
            return detected_patterns, best_suggestion
        
        return [], None
    
    def _get_best_suggestion(self, detected_patterns):
        suggestions = collections.Counter(s[1] for s in detected_patterns)
        if suggestions:
            return suggestions.most_common(1)[0][0]
        return None
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
streamlit
pandas
