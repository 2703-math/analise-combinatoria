import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import permutations, combinations
import math

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Análise Combinatória Visual",
    page_icon="🎲",
    layout="wide"
)

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .concept-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid;
        margin-bottom: 1rem;
    }
    .param-box {
        background: #fff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .step-box {
        background: #fff8e1;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
    .object-ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 50%;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 3px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .slot-box {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        border: 2px dashed #999;
        border-radius: 8px;
        margin: 3px;
        background: #fafafa;
        font-size: 0.75rem;
        color: #777;
    }
    .slot-filled {
        border: 2px solid #333;
        background: #fff;
    }
    .restriction-note {
        background: #ffeaea;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        color: #c0392b;
        font-size: 0.95rem;
        font-weight: 600;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# PALETA DE CORES
# ============================================
CORES = [
    "#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6",
    "#1abc9c", "#e91e63", "#ff5722", "#607d8b", "#795548"
]
NOMES_CORES = ["Vermelho", "Azul", "Verde", "Laranja", "Roxo", "Ciano", "Rosa", "Coral", "Cinza", "Marrom"]
NOMES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

# ============================================
# FUNÇÕES AUXILIARES DE PLOTAGEM
# ============================================
def gerar_bolas_html(elementos, cores=None, tamanho=42):
    if cores is None:
        cores = CORES
    html = '<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:6px; margin:10px 0;">'
    for i, elem in enumerate(elementos):
        cor = cores[i % len(cores)]
        html += f'<div class="object-ball" style="width:{tamanho}px;height:{tamanho}px;background:{cor};font-size:{tamanho*0.5}px;">{elem}</div>'
    html += '</div>'
    return html

def gerar_slots_html(elementos, n_slots, tamanho=50):
    html = '<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:6px; margin:10px 0;">'
    for i in range(n_slots):
        if i < len(elementos):
            html += f'<div class="slot-box slot-filled" style="width:{tamanho}px;height:{tamanho}px;font-size:1.2rem;font-weight:bold;color:#333;">{elementos[i]}</div>'
        else:
            html += f'<div class="slot-box" style="width:{tamanho}px;height:{tamanho}px;">_{i+1}</div>'
    html += '</div>'
    return html

def plot_permutacoes_grid(perms_list, elementos, max_cols=6):
    n = len(perms_list)
    cols = min(max_cols, n)
    rows = math.ceil(n / cols)

    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=[f"#{i+1}" for i in range(n)],
        horizontal_spacing=0.05, vertical_spacing=0.1
    )

    for idx, perm in enumerate(perms_list):
        r = idx // cols + 1
        c = idx % cols + 1

        for pos, elem in enumerate(perm):
            cor_idx = elementos.index(elem)
            cor = CORES[cor_idx % len(CORES)]

            fig.add_trace(go.Scatter(
                x=[pos], y=[0],
                mode='markers+text',
                marker=dict(size=35, color=cor, symbol='circle'),
                text=[elem],
                textfont=dict(size=16, color='white', family='Arial Black'),
                textposition='middle center',
                hoverinfo='skip',
                showlegend=False
            ), row=r, col=c)

        fig.update_xaxes(range=[-0.5, len(perm)-0.5], showgrid=False, zeroline=False, showticklabels=False, row=r, col=c)
        fig.update_yaxes(range=[-0.5, 0.5], showgrid=False, zeroline=False, showticklabels=False, row=r, col=c)

    fig.update_layout(
        height=120 * rows + 50, showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20), title=dict(text=f'Todas as {n} permutações', font=dict(size=16))
    )
    return fig

def plot_combinacoes_circulo(elementos, combs_list, n_total):
    n = len(combs_list)
    cols = min(5, n)
    rows = math.ceil(n / cols)

    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=[f"#{i+1}: {{{', '.join(c)}}}" for i, c in enumerate(combs_list)],
        horizontal_spacing=0.08, vertical_spacing=0.12
    )

    angles = np.linspace(0, 2*np.pi, n_total, endpoint=False)
    x_pos = np.cos(angles)
    y_pos = np.sin(angles)

    for idx, comb in enumerate(combs_list):
        r = idx // cols + 1
        c = idx % cols + 1
        comb_set = set(comb)

        for i, elem in enumerate(elementos):
            is_selected = elem in comb_set
            fig.add_trace(go.Scatter(
                x=[x_pos[i]], y=[y_pos[i]],
                mode='markers+text',
                marker=dict(
                    size=28 if is_selected else 20,
                    color=CORES[i] if is_selected else '#ddd',
                    symbol='circle',
                    line=dict(width=2, color='#333' if is_selected else '#bbb')
                ),
                text=[elem],
                textfont=dict(size=14 if is_selected else 11, color='white' if is_selected else '#999', family='Arial Black'),
                textposition='middle center',
                hoverinfo='skip',
                showlegend=False
            ), row=r, col=c)

        fig.update_xaxes(range=[-1.4, 1.4], showgrid=False, zeroline=False, showticklabels=False, row=r, col=c)
        fig.update_yaxes(range=[-1.4, 1.4], showgrid=False, zeroline=False, showticklabels=False, row=r, col=c)

    fig.update_layout(
        height=220 * rows + 30, showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def plot_arranjo_slots(elementos, arranjo, n_slots):
    fig = go.Figure()
    for i in range(n_slots):
        fig.add_trace(go.Scatter(
            x=[i], y=[0], mode='markers',
            marker=dict(size=50, color='#f0f0f0', symbol='square', line=dict(width=2, color='#999', dash='dash')),
            hoverinfo='skip', showlegend=False
        ))
        fig.add_annotation(x=i, y=0, text=f'{i+1}º', showarrow=False, font=dict(size=10, color='#999'))

    for i, elem in enumerate(arranjo):
        cor_idx = elementos.index(elem)
        fig.add_trace(go.Scatter(
            x=[i], y=[0], mode='markers+text',
            marker=dict(size=45, color=CORES[cor_idx], symbol='circle', line=dict(width=2, color='#333')),
            text=[elem], textfont=dict(size=18, color='white', family='Arial Black'),
            textposition='middle center', hoverinfo='skip', showlegend=False
        ))

    fig.update_layout(
        xaxis=dict(range=[-0.6, n_slots-0.4], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-0.6, 0.6], showgrid=False, zeroline=False, showticklabels=False),
        height=180, plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=20, r=20, t=30, b=20),
        title=dict(text=f'Arranjo: ordem importa! Posições 1 a {n_slots}', font=dict(size=14))
    )
    return fig

def gerar_coloracoes_validas(n_degraus, k_cores, max_exibir=12):
    coloracoes = []
    def backtrack(pos, atual):
        if pos == n_degraus:
            coloracoes.append(tuple(atual))
            return
        for cor in range(k_cores):
            if pos == 0 or cor != atual[-1]:
                atual.append(cor)
                backtrack(pos + 1, atual)
                atual.pop()
    backtrack(0, [])
    return coloracoes

def plot_coloracao_sequencia(cores_indices, n_degraus, k_cores):
    fig = go.Figure()
    for i, cor_idx in enumerate(cores_indices):
        cor = CORES[cor_idx % len(CORES)]
        nome = NOMES_CORES[cor_idx % len(NOMES_CORES)]

        fig.add_trace(go.Scatter(
            x=[i], y=[0], mode='markers+text',
            marker=dict(size=55, color=cor, symbol='square', line=dict(width=3, color='#333')),
            text=[f'D{i+1}'], textfont=dict(size=14, color='white', family='Arial Black'),
            textposition='middle center', hovertemplate=f'Degrau {i+1}<br>Cor: {nome}<extra></extra>', showlegend=False
        ))

        if i < len(cores_indices) - 1:
            fig.add_annotation(
                x=i + 0.5, y=0.05, ax=i + 0.5, ay=0.05,
                xref='x', yref='y', axref='x', ayref='y',
                showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#e74c3c'
            )
            fig.add_annotation(x=i + 0.5, y=0.35, text='≠', showarrow=False, font=dict(size=18, color='#e74c3c', family='Arial Black'))

    fig.update_layout(
        xaxis=dict(range=[-0.5, n_degraus-0.5], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-0.5, 0.8], showgrid=False, zeroline=False, showticklabels=False),
        height=220, plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=20, r=20, t=30, b=20),
        title=dict(text=f'Sequência de {n_degraus} degraus — adjacentes com cores diferentes', font=dict(size=14))
    )
    return fig

def plot_coloracoes_grid(coloracoes, n_degraus, k_cores, max_cols=6):
    n = len(coloracoes)
    cols = min(max_cols, n)
    rows = math.ceil(n / cols)

    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=[f"#{i+1}" for i in range(n)],
        horizontal_spacing=0.05, vertical_spacing=0.15
    )

    for idx, coloracao in enumerate(coloracoes):
        r = idx // cols + 1
        c = idx % cols + 1

        for pos, cor_idx in enumerate(coloracao):
            cor = CORES[cor_idx % len(CORES)]
            fig.add_trace(go.Scatter(
                x=[pos], y=[0], mode='markers+text',
                marker=dict(size=30, color=cor, symbol='square', line=dict(width=2, color='#333')),
                text=[str(pos+1)], textfont=dict(size=12, color='white', family='Arial Black'),
                textposition='middle center', hoverinfo='skip', showlegend=False
            ), row=r, col=c)

            if pos < len(coloracao) - 1:
                fig.add_annotation(
                    x=pos + 0.5, y=0, ax=pos + 0.5, ay=0,
                    xref=f'x{idx+1 if idx > 0 else ""}', yref=f'y{idx+1 if idx > 0 else ""}',
                    axref=f'x{idx+1 if idx > 0 else ""}', ayref=f'y{idx+1 if idx > 0 else ""}',
                    showarrow=True, arrowhead=2, arrowsize=0.8, arrowwidth=1.5, arrowcolor='#e74c3c'
                )

        fig.update_xaxes(range=[-0.5, n_degraus-0.5], showgrid=False, zeroline=False, showticklabels=False, row=r, col=c)
        fig.update_yaxes(range=[-0.4, 0.4], showgrid=False, zeroline=False, showticklabels=False, row=r, col=c)

    fig.update_layout(
        height=100 * rows + 40, showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20), title=dict(text=f'Exemplos de colorações válidas', font=dict(size=16))
    )
    return fig

# ============================================
# TÍTULO PRINCIPAL
# ============================================
st.markdown('<div class="main-title">🎲 Análise Combinatória Visual</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explorando princípios de contagem diretamente com gráficos animados</div>', unsafe_allow_html=True)

# ============================================
# NAVEGAÇÃO EM ABAS (SEM BARRA LATERAL)
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Permutação", 
    "2. Permutação c/ Repetição", 
    "3. Arranjo", 
    "4. Combinação", 
    "5. Coloração (Escada)"
])

# ============================================
# ABA 1: PERMUTAÇÃO SIMPLES
# ============================================
with tab1:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>Definição:</b> Permutação simples é o número de maneiras de organizar <b>n objetos distintos</b> em fila.
        A <b>ordem importa</b> e todos os objetos são usados.
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_calc = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        n_perm = st.slider("Quantidade de objetos (n)", 2, 6, 4, key='perm')
        elementos_perm = NOMES[:n_perm]
        st.markdown("**Objetos disponíveis:**")
        st.markdown(gerar_bolas_html(elementos_perm, tamanho=50), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_calc:
        resultado = math.factorial(n_perm)
        st.subheader("🧮 Cálculo Matemático")
        # LaTeX formatado corretamente para permutação
        st.markdown(rf"$$ P_{{{n_perm}}} = {n_perm}! = {' \times '.join([str(i) for i in range(n_perm, 0, -1)])} = \mathbf{{{resultado}}} $$")
        
        st.markdown(f"""
        <div style="font-size:1.1rem;line-height:1.8;">
        Para a 1ª posição: <b>{n_perm}</b> opções<br>
        Para a 2ª posição: <b>{n_perm-1}</b> opções<br>
        Para a última: <b>1</b> opção
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(f"📋 Todas as {resultado} permutações possíveis")
    if resultado <= 120:
        perms = list(permutations(elementos_perm))
        fig = plot_permutacoes_grid(perms, elementos_perm, max_cols=6)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# ABA 2: PERMUTAÇÃO COM REPETIÇÃO
# ============================================
with tab2:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #e74c3c;">
        <b>Definição:</b> Quando temos objetos <b>repetidos</b>, trocar dois objetos iguais entre si 
        <b>não gera uma nova fila</b>. Precisamos dividir pelo fatorial das repetições usando uma <b>fração</b>.
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_calc = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        n_total_rep = st.slider("Total de objetos (n)", 3, 8, 5)
        n_tipo1 = st.number_input("Qtd tipo 1 (🔴)", 1, n_total_rep-1, 2)
        n_tipo2 = st.number_input("Qtd tipo 2 (🔵)", 0, n_total_rep-n_tipo1, 2)
        n_tipo3 = n_total_rep - n_tipo1 - n_tipo2
        st.markdown(f"Tipo 3 (🟢): **{n_tipo3}** objetos restantes")
        
        if n_tipo3 < 0:
            st.error("A soma excedeu o total!")
            n_tipo3 = 0
            
        elementos_rep = ["A"] * n_tipo1 + ["B"] * n_tipo2 + ["C"] * n_tipo3
        cores_rep = ["#e74c3c"] * n_tipo1 + ["#3498db"] * n_tipo2 + ["#2ecc71"] * n_tipo3
        st.markdown(gerar_bolas_html(elementos_rep, cores_rep, tamanho=45), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_calc:
        if n_total_rep > 0:
            denominador = math.factorial(n_tipo1) * math.factorial(n_tipo2) * math.factorial(n_tipo3)
            resultado_rep = math.factorial(n_total_rep) // denominador
            
            st.subheader("🧮 Fração em Duas Linhas")
            # Fração vertical perfeita renderizada com LaTeX
            st.markdown(rf"""
            $$ P_{{{n_total_rep}}}^{{{n_tipo1}, {n_tipo2}, {n_tipo3}}} = \frac{{{n_total_rep}!}}{{{n_tipo1}! \cdot {n_tipo2}! \cdot {n_tipo3}!}} $$
            """)
            
            st.markdown("Calculando os fatoriais:")
            st.markdown(rf"""
            $$ P = \frac{{{math.factorial(n_total_rep)}}}{{{math.factorial(n_tipo1)} \cdot {math.factorial(n_tipo2)} \cdot {math.factorial(n_tipo3)}}} = \frac{{{math.factorial(n_total_rep)}}}{{{denominador}}} = \mathbf{{{resultado_rep}}} \text{{ permutações}} $$
            """)

# ============================================
# ABA 3: ARRANJO SIMPLES
# ============================================
with tab3:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #f39c12;">
        <b>Definição:</b> Escolher <b>k objetos</b> de um total de <b>n</b>, 
        onde a <b>ordem importa</b>.
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_calc = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        n_arr = st.slider("Total disponíveis (n)", 3, 8, 5, key='n_arr')
        k_arr = st.slider("Posições a preencher (k)", 1, min(n_arr, 5), 3, key='k_arr')
        elementos_arr = NOMES[:n_arr]
        st.markdown("**Objetos disponíveis:**")
        st.markdown(gerar_bolas_html(elementos_arr, tamanho=40), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_calc:
        resultado_arr = math.factorial(n_arr) // math.factorial(n_arr - k_arr)
        
        st.subheader("🧮 Fração de Arranjo")
        st.markdown(rf"""
        $$ A_{{{n_arr}, {k_arr}}} = \frac{{{n_arr}!}}{{({n_arr} - {k_arr})!}} $$
        """)
        
        st.markdown("Resolvendo:")
        st.markdown(rf"""
        $$ A = \frac{{{math.factorial(n_arr)}}}{{{math.factorial(n_arr - k_arr)}}} = \mathbf{{{resultado_arr}}} \text{{ arranjos}} $$
        """)

    st.markdown("---")
    if resultado_arr <= 60:
        arranjos = list(permutations(elementos_arr, k_arr))
        n_exibir = min(12, len(arranjos))
        cols = st.columns(3)
        for idx in range(n_exibir):
            with cols[idx % 3]:
                st.plotly_chart(plot_arranjo_slots(elementos_arr, arranjos[idx], k_arr), use_container_width=True, height=150)

# ============================================
# ABA 4: COMBINAÇÃO SIMPLES
# ============================================
with tab4:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #2ecc71;">
        <b>Definição:</b> Escolher <b>k objetos</b> de um total de <b>n</b>, 
        onde a <b>ordem NÃO importa</b> (ex: formar equipes).
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_calc = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        n_comb = st.slider("Total disponíveis (n)", 3, 10, 6, key='n_comb')
        k_comb = st.slider("Tamanho do grupo (k)", 1, min(n_comb, 5), 3, key='k_comb')
        elementos_comb = NOMES[:n_comb]
        st.markdown("**Objetos disponíveis:**")
        st.markdown(gerar_bolas_html(elementos_comb, tamanho=40), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_calc:
        resultado_comb = math.comb(n_comb, k_comb)
        
        st.subheader("🧮 Fração de Combinação")
        st.markdown(rf"""
        $$ C_{{{n_comb}, {k_comb}}} = \frac{{{n_comb}!}}{{{k_comb}! \cdot ({n_comb} - {k_comb})!}} $$
        """)
        
        st.markdown("Resolvendo a fração dividindo pelo fatorial de k (para remover as repetições de ordem):")
        st.markdown(rf"""
        $$ C = \frac{{{math.factorial(n_comb)}}}{{{math.factorial(k_comb)} \cdot {math.factorial(n_comb - k_comb)}}} = \mathbf{{{resultado_comb}}} \text{{ grupos}} $$
        """)

    st.markdown("---")
    if resultado_comb <= 30:
        combs = list(combinations(elementos_comb, k_comb))
        fig = plot_combinacoes_circulo(elementos_comb, combs, n_comb)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# ABA 5: COLORAÇÃO COM RESTRIÇÃO (ESCADA)
# ============================================
with tab5:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #9b59b6;">
        <b>📌 Problema da Escada:</b> Uma escada tem <b>n degraus</b>. Cada degrau deve ser pintado com uma de <b>k cores</b>. 
        <b>Restrição:</b> Degraus consecutivos (vizinhos) não podem ter a mesma cor.
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_calc = st.columns([1, 2])

    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        n_degraus = st.slider("Quantidade de degraus (n)", 2, 8, 6)
        k_cores = st.slider("Cores disponíveis (k)", 2, 6, 4)
        
        cores_disp = NOMES_CORES[:k_cores]
        html_cores = '<div style="display:flex; flex-wrap:wrap; gap:6px; margin:10px 0;">'
        for i in range(k_cores):
            html_cores += f'<div style="display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:20px;background:{CORES[i]}22;border:2px solid {CORES[i]};"><div style="width:16px;height:16px;border-radius:50%;background:{CORES[i]};"></div><span style="font-size:0.85rem;font-weight:600;color:#333;">{cores_disp[i]}</span></div>'
        html_cores += '</div>'
        st.markdown(html_cores, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_calc:
        total_coloracoes = k_cores * ((k_cores - 1) ** (n_degraus - 1))
        
        st.subheader("✏️ Resolução em LaTeX")
        st.markdown(f"""
        <div style="font-size:1rem; color:#333; line-height:1.8;">
            <b>1º degrau:</b> {k_cores} opções de cores.<br>
            <b>2º degrau em diante:</b> cada um tem {k_cores - 1} opções (não pode ser igual ao anterior).
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(rf"""
        $$ \text{{Total}} = k \cdot (k - 1)^{{n - 1}} $$
        """)
        
        st.markdown(rf"""
        $$ \text{{Total}} = {k_cores} \cdot ({k_cores} - 1)^{{{n_degraus} - 1}} = {k_cores} \cdot {k_cores - 1}^{{{n_degraus - 1}}} = \mathbf{{{total_coloracoes}}} \text{{ maneiras}} $$
        """)

    st.markdown("---")
    st.subheader("🖌️ Exemplo de uma pintura válida da escada")
    np.random.seed(42)
    coloracao_exemplo = [np.random.randint(0, k_cores)]
    for i in range(1, n_degraus):
        cor_anterior = coloracao_exemplo[-1]
        opcoes = [c for c in range(k_cores) if c != cor_anterior]
        coloracao_exemplo.append(np.random.choice(opcoes))

    st.plotly_chart(plot_coloracao_sequencia(coloracao_exemplo, n_degraus, k_cores), use_container_width=True)

    st.markdown("---")
    st.subheader(f"📋 Algumas colorações válidas (Total: {total_coloracoes})")
    if total_coloracoes <= 60:
        coloracoes = gerar_coloracoes_validas(n_degraus, k_cores, max_exibir=12)
        fig = plot_coloracoes_grid(coloracoes[:min(12, len(coloracoes))], n_degraus, k_cores, max_cols=4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        coloracoes = gerar_coloracoes_validas(n_degraus, k_cores, max_exibir=6)
        fig = plot_coloracoes_grid(coloracoes[:min(6, len(coloracoes))], n_degraus, k_cores, max_cols=3)
        st.plotly_chart(fig, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    🎲 <b>Análise Combinatória Visual</b> — Ferramenta educacional para o ensino de Matemática<br>
</div>
""", unsafe_allow_html=True)
