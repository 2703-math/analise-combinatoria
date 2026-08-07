import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import permutations, combinations, product
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
    .formula-box {
        background: #1a1a2e;
        color: #fff;
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .step-box {
        background: #fff8e1;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
    .result-box {
        background: #e8f5e9;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 700;
        color: #2e7d32;
        border: 2px solid #4caf50;
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
</style>
""", unsafe_allow_html=True)

# ============================================
# PALETA DE CORES
# ============================================
CORES = [
    "#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6",
    "#1abc9c", "#e91e63", "#ff5722", "#607d8b", "#795548"
]
NOMES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

# ============================================
# FUNÇÕES AUXILIARES
# ============================================
def gerar_bolas_html(elementos, cores=None, tamanho=42):
    """Gera HTML de bolas coloridas para os elementos"""
    if cores is None:
        cores = CORES
    html = '<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:6px; margin:10px 0;">'
    for i, elem in enumerate(elementos):
        cor = cores[i % len(cores)]
        html += f'<div class="object-ball" style="width:{tamanho}px;height:{tamanho}px;background:{cor};font-size:{tamanho*0.5}px;">{elem}</div>'
    html += '</div>'
    return html

def gerar_slots_html(elementos, n_slots, tamanho=50):
    """Gera HTML de slots preenchidos"""
    html = '<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:6px; margin:10px 0;">'
    for i in range(n_slots):
        if i < len(elementos):
            html += f'<div class="slot-box slot-filled" style="width:{tamanho}px;height:{tamanho}px;font-size:1.2rem;font-weight:bold;color:#333;">{elementos[i]}</div>'
        else:
            html += f'<div class="slot-box" style="width:{tamanho}px;height:{tamanho}px;">_{i+1}</div>'
    html += '</div>'
    return html

def plot_permutacoes_grid(perms_list, elementos, max_cols=6):
    """Plota grade de permutações com Plotly"""
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

        fig.update_xaxes(range=[-0.5, len(perm)-0.5], showgrid=False, zeroline=False, 
                        showticklabels=False, row=r, col=c)
        fig.update_yaxes(range=[-0.5, 0.5], showgrid=False, zeroline=False, 
                        showticklabels=False, row=r, col=c)

    fig.update_layout(
        height=120 * rows + 50,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(text=f'Todas as {n} permutações', font=dict(size=16))
    )
    return fig

def plot_combinacoes_circulo(elementos, combs_list, n_total):
    """Plota combinações como subconjuntos destacados em círculo"""
    n = len(combs_list)
    cols = min(5, n)
    rows = math.ceil(n / cols)

    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=[f"#{i+1}: {{{', '.join(c)}}}" for i, c in enumerate(combs_list)],
        horizontal_spacing=0.08, vertical_spacing=0.12
    )

    # Posições circulares para os elementos totais
    angles = np.linspace(0, 2*np.pi, n_total, endpoint=False)
    radius = 1
    x_pos = radius * np.cos(angles)
    y_pos = radius * np.sin(angles)

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

        fig.update_xaxes(range=[-1.4, 1.4], showgrid=False, zeroline=False, 
                        showticklabels=False, row=r, col=c)
        fig.update_yaxes(range=[-1.4, 1.4], showgrid=False, zeroline=False, 
                        showticklabels=False, row=r, col=c)

    fig.update_layout(
        height=220 * rows + 30,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def plot_arranjo_slots(elementos, arranjo, n_slots):
    """Plota arranjo como preenchimento de slots"""
    fig = go.Figure()

    # Slots
    for i in range(n_slots):
        fig.add_trace(go.Scatter(
            x=[i], y=[0],
            mode='markers',
            marker=dict(size=50, color='#f0f0f0', symbol='square', 
                       line=dict(width=2, color='#999', dash='dash')),
            hoverinfo='skip',
            showlegend=False
        ))
        fig.add_annotation(x=i, y=0, text=f'{i+1}º', showarrow=False,
                          font=dict(size=10, color='#999'))

    # Elementos preenchidos
    for i, elem in enumerate(arranjo):
        cor_idx = elementos.index(elem)
        fig.add_trace(go.Scatter(
            x=[i], y=[0],
            mode='markers+text',
            marker=dict(size=45, color=CORES[cor_idx], symbol='circle',
                       line=dict(width=2, color='#333')),
            text=[elem],
            textfont=dict(size=18, color='white', family='Arial Black'),
            textposition='middle center',
            hoverinfo='skip',
            showlegend=False
        ))

    fig.update_layout(
        xaxis=dict(range=[-0.6, n_slots-0.4], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-0.6, 0.6], showgrid=False, zeroline=False, showticklabels=False),
        height=180,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=30, b=20),
        title=dict(text=f'Arranjo: ordem importa! Posições 1 a {n_slots}', font=dict(size=14))
    )
    return fig

# ============================================
# TÍTULO
# ============================================
st.markdown('<div class="main-title">🎲 Análise Combinatória Visual</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Permutação, Arranjo e Combinação de forma concreta e interativa</div>', unsafe_allow_html=True)

# ============================================
# BARRA LATERAL — CONTROLES GLOBAIS
# ============================================
with st.sidebar:
    st.header("⚙️ Controles")
    st.markdown("---")

    conceito = st.radio(
        "📚 Escolha o conceito:",
        ["Permutação Simples", "Permutação com Repetição", "Arranjo Simples", "Combinação"],
        index=0
    )

    st.markdown("---")

    # Controles específicos por conceito
    if conceito == "Permutação Simples":
        n_perm = st.slider("🔢 Quantidade de objetos distintos (n)", 2, 6, 4)
        elementos_perm = NOMES[:n_perm]
        st.markdown("**Objetos disponíveis:**")
        st.markdown(gerar_bolas_html(elementos_perm), unsafe_allow_html=True)

    elif conceito == "Permutação com Repetição":
        n_total_rep = st.slider("🔢 Total de objetos (n)", 3, 8, 5)
        st.markdown("Defina quantos são iguais entre si:")
        n_tipo1 = st.number_input("Quantidade do tipo 1 (🔴)", 1, n_total_rep-1, 2)
        n_tipo2 = st.number_input("Quantidade do tipo 2 (🔵)", 0, n_total_rep-n_tipo1, 2)
        n_tipo3 = n_total_rep - n_tipo1 - n_tipo2
        st.markdown(f"Tipo 3 (🟢): **{n_tipo3}** objeto(s) — calculado automaticamente")

        # Validar
        if n_tipo3 < 0:
            st.error("A soma dos tipos 1 e 2 não pode ultrapassar o total!")
            n_tipo3 = 0

        elementos_rep = ["A"] * n_tipo1 + ["B"] * n_tipo2 + ["C"] * n_tipo3
        cores_rep = ["#e74c3c"] * n_tipo1 + ["#3498db"] * n_tipo2 + ["#2ecc71"] * n_tipo3
        st.markdown("**Objetos:**")
        st.markdown(gerar_bolas_html(elementos_rep, cores_rep), unsafe_allow_html=True)

    elif conceito == "Arranjo Simples":
        n_arr = st.slider("🔢 Total de objetos disponíveis (n)", 3, 8, 5)
        k_arr = st.slider("📥 Quantidade a escolher (k)", 1, min(n_arr, 5), 3)
        elementos_arr = NOMES[:n_arr]
        st.markdown("**Objetos disponíveis:**")
        st.markdown(gerar_bolas_html(elementos_arr), unsafe_allow_html=True)
        st.markdown(f"**Slots a preencher:** {k_arr} posições")

    elif conceito == "Combinação":
        n_comb = st.slider("🔢 Total de objetos disponíveis (n)", 3, 10, 6)
        k_comb = st.slider("📥 Quantidade a escolher (k)", 1, min(n_comb, 5), 3)
        elementos_comb = NOMES[:n_comb]
        st.markdown("**Objetos disponíveis:**")
        st.markdown(gerar_bolas_html(elementos_comb), unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 **Dica:** Ajuste os sliders para explorar diferentes cenários. Observe como a ordem importa (ou não) em cada caso!")

# ============================================
# CONTEÚDO PRINCIPAL POR CONCEITO
# ============================================

# ============================================
# 1. PERMUTAÇÃO SIMPLES
# ============================================
if conceito == "Permutação Simples":
    st.markdown("---")
    st.header("🔄 Permutação Simples")

    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>Definição:</b> Permutação simples é o número de maneiras de organizar <b>n objetos distintos</b> em fila.
        A <b>ordem importa</b> e todos os objetos são usados.
    </div>
    """, unsafe_allow_html=True)

    # Fórmula
    resultado = math.factorial(n_perm)
    st.markdown(f"""
    <div class="formula-box">
        P(n) = n! = {n_perm}! = {' × '.join([str(i) for i in range(n_perm, 0, -1)])} = {resultado}
    </div>
    """, unsafe_allow_html=True)

    # Visualização
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📦 Objetos a permutar")
        st.markdown(gerar_bolas_html(elementos_perm, tamanho=50), unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;color:#777;font-size:0.9rem;'>Todos distintos, todos serão usados</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("🧮 Cálculo")
        st.markdown(f"""
        <div style="font-size:1.1rem;line-height:1.8;">
        Temos <b>{n_perm}</b> objetos distintos.<br>
        Para a 1ª posição: <b>{n_perm}</b> opções<br>
        Para a 2ª posição: <b>{n_perm-1}</b> opções<br>
        {"Para a 3ª posição: <b>" + str(n_perm-2) + "</b> opções<br>" if n_perm >= 3 else ""}
        {"...<br>" if n_perm > 3 else ""}
        Para a última: <b>1</b> opção<br><br>
        Total = <b>{' × '.join([str(i) for i in range(n_perm, 0, -1)])} = {resultado}</b>
        </div>
        """, unsafe_allow_html=True)

    # Grade de permutações
    st.markdown("---")
    st.subheader(f"📋 Todas as {resultado} permutações possíveis")

    if resultado <= 120:  # Limitar para não travar
        perms = list(permutations(elementos_perm))
        fig = plot_permutacoes_grid(perms, elementos_perm, max_cols=6)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Muitas permutações para exibir visualmente. Reduza n para ver a grade.")

    # Destaque conceitual
    st.markdown("""
    <div class="step-box">
        <b>💡 Observação importante:</b> Em permutação simples, cada objeto aparece exatamente uma vez em cada fila.
        Trocar dois objetos de lugar gera uma <b>permutação diferente</b>.
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 2. PERMUTAÇÃO COM REPETIÇÃO
# ============================================
elif conceito == "Permutação com Repetição":
    st.markdown("---")
    st.header("🔁 Permutação com Repetição")

    st.markdown("""
    <div class="concept-card" style="border-left-color: #e74c3c;">
        <b>Definição:</b> Quando temos objetos <b>repetidos</b>, trocar dois objetos iguais entre si 
        <b>não gera uma permutação nova</b>. Precisamos dividir pelo fatorial das repetições.
    </div>
    """, unsafe_allow_html=True)

    n_total_rep = n_tipo1 + n_tipo2 + n_tipo3
    if n_total_rep > 0:
        denominador = math.factorial(n_tipo1) * math.factorial(n_tipo2) * math.factorial(n_tipo3)
        resultado_rep = math.factorial(n_total_rep) // denominador

        st.markdown(f"""
        <div class="formula-box">
            P(n; n₁, n₂, n₃) = n! / (n₁! · n₂! · n₃!)<br>
            = {n_total_rep}! / ({n_tipo1}! · {n_tipo2}! · {n_tipo3}!)<br>
            = {math.factorial(n_total_rep)} / ({math.factorial(n_tipo1)} · {math.factorial(n_tipo2)} · {math.factorial(n_tipo3)})<br>
            = {math.factorial(n_total_rep)} / {denominador} = <b>{resultado_rep}</b>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📦 Objetos (com repetições)")
            st.markdown(gerar_bolas_html(elementos_rep, cores_rep, tamanho=50), unsafe_allow_html=True)
            st.markdown(f"""
            <div style="text-align:center;font-size:0.95rem;color:#555;margin-top:8px;">
            🔴 Tipo A: <b>{n_tipo1}</b> &nbsp;|&nbsp; 
            🔵 Tipo B: <b>{n_tipo2}</b> &nbsp;|&nbsp; 
            🟢 Tipo C: <b>{n_tipo3}</b>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("🧮 Por que dividir?")
            st.markdown(f"""
            <div style="font-size:1.05rem;line-height:1.8;">
            Sem considerar repetições, teríamos <b>{n_total_rep}!</b> = {math.factorial(n_total_rep)} filas.<br><br>
            Mas os <b>{n_tipo1}</b> objetos A iguais podem ser trocados entre si de <b>{n_tipo1}!</b> = {math.factorial(n_tipo1)} formas 
            <b>sem mudar a fila</b>.<br><br>
            O mesmo para B ({math.factorial(n_tipo2)} formas) e C ({math.factorial(n_tipo3)} formas).<br><br>
            Então dividimos: <b>{math.factorial(n_total_rep)} ÷ {denominador} = {resultado_rep}</b> permutações <b>distintas</b>.
            </div>
            """, unsafe_allow_html=True)

        # Exemplo comparativo
        st.markdown("---")
        st.subheader("🔍 Comparando: com vs sem repetição")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div style="background:#ffeaea;border-radius:10px;padding:1rem;text-align:center;">
                <b>Se TODOS fossem distintos</b><br>
                <div style="font-size:2rem;font-weight:700;color:#e74c3c;">{0}</div>
                <div style="font-size:0.9rem;color:#777;">permutações</div>
            </div>
            """.format(math.factorial(n_total_rep)), unsafe_allow_html=True)

        with col_b:
            st.markdown("""
            <div style="background:#e8f5e9;border-radius:10px;padding:1rem;text-align:center;">
                <b>Com repetições (reais)</b><br>
                <div style="font-size:2rem;font-weight:700;color:#2e7d32;">{0}</div>
                <div style="font-size:0.9rem;color:#777;">permutações distintas</div>
            </div>
            """.format(resultado_rep), unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:center;margin-top:1rem;font-size:1.1rem;color:#555;">
            Diferença: <b>{math.factorial(n_total_rep) - resultado_rep}</b> permutações são "repetidas" (iguais visualmente)
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 3. ARRANJO SIMPLES
# ============================================
elif conceito == "Arranjo Simples":
    st.markdown("---")
    st.header("📥 Arranjo Simples")

    st.markdown("""
    <div class="concept-card" style="border-left-color: #f39c12;">
        <b>Definição:</b> Arranjo é o número de maneiras de escolher <b>k objetos</b> de um total de <b>n</b>, 
        onde a <b>ordem importa</b>. Nem todos os objetos precisam ser usados.
    </div>
    """, unsafe_allow_html=True)

    resultado_arr = math.factorial(n_arr) // math.factorial(n_arr - k_arr)

    st.markdown(f"""
    <div class="formula-box">
        A(n, k) = n! / (n - k)!<br>
        = {n_arr}! / ({n_arr} - {k_arr})!<br>
        = {math.factorial(n_arr)} / {math.factorial(n_arr - k_arr)}<br>
        = <b>{resultado_arr}</b>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📦 Objeto disponíveis (n)")
        st.markdown(gerar_bolas_html(elementos_arr, tamanho=45), unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;color:#777;'>Total: <b>{n_arr}</b> objetos</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("📥 Slots a preencher (k)")
        slots_vazios = ["_"] * k_arr
        st.markdown(gerar_slots_html(slots_vazios, k_arr), unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;color:#777;'>Escolher <b>{k_arr}</b> em ordem</div>", unsafe_allow_html=True)

    # Explicação passo a passo
    st.markdown("---")
    st.subheader("🧮 Raciocínio passo a passo")

    passos = []
    for i in range(k_arr):
        restantes = n_arr - i
        passos.append(f"<b>{i+1}ª posição:</b> {restantes} opções")

    st.markdown(f"""
    <div style="font-size:1.1rem;line-height:2;">
    {'<br>'.join(passos)}<br><br>
    Total = <b>{' × '.join([str(n_arr - i) for i in range(k_arr)])} = {resultado_arr}</b>
    </div>
    """, unsafe_allow_html=True)

    # Visualização de arranjos
    st.markdown("---")
    st.subheader(f"📋 Exemplos de arranjos (A({n_arr},{k_arr}) = {resultado_arr})")

    if resultado_arr <= 60:
        arranjos = list(permutations(elementos_arr, k_arr))
        # Mostrar alguns exemplos
        n_exibir = min(12, len(arranjos))
        cols_por_linha = 3

        for i in range(0, n_exibir, cols_por_linha):
            cols = st.columns(cols_por_linha)
            for j in range(cols_por_linha):
                idx = i + j
                if idx < n_exibir:
                    arr = arranjos[idx]
                    with cols[j]:
                        st.markdown(f"<div style='text-align:center;font-size:0.85rem;color:#777;margin-bottom:4px;'>Arranjo #{idx+1}</div>", unsafe_allow_html=True)
                        st.plotly_chart(plot_arranjo_slots(elementos_arr, arr, k_arr), use_container_width=True, height=150)
    else:
        st.info("Muitos arranjos para exibir. Ajuste n e k para valores menores.")

    st.markdown("""
    <div class="step-box">
        <b>💡 Diferença da Permutação:</b> Em arranjo, escolhemos <b>apenas k</b> objetos de n disponíveis.
        A ordem importa: (A, B, C) ≠ (C, B, A). Se k = n, o arranjo vira permutação!
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 4. COMBINAÇÃO
# ============================================
elif conceito == "Combinação":
    st.markdown("---")
    st.header("🤝 Combinação")

    st.markdown("""
    <div class="concept-card" style="border-left-color: #2ecc71;">
        <b>Definição:</b> Combinação é o número de maneiras de escolher <b>k objetos</b> de um total de <b>n</b>, 
        onde a <b>ordem NÃO importa</b>. {A, B, C} é o mesmo que {C, B, A}.
    </div>
    """, unsafe_allow_html=True)

    resultado_comb = math.comb(n_comb, k_comb)

    st.markdown(f"""
    <div class="formula-box">
        C(n, k) = (n k) = n! / (k! · (n - k)!)<br>
        = {n_comb}! / ({k_comb}! · {n_comb - k_comb}!)<br>
        = {math.factorial(n_comb)} / ({math.factorial(k_comb)} · {math.factorial(n_comb - k_comb)})<br>
        = {math.factorial(n_comb)} / {math.factorial(k_comb) * math.factorial(n_comb - k_comb)}<br>
        = <b>{resultado_comb}</b>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📦 Conjunto original")
        st.markdown(gerar_bolas_html(elementos_comb, tamanho=45), unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;color:#777;'>n = <b>{n_comb}</b> elementos</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("🤝 Subconjuntos de k")
        st.markdown(f"""
        <div style="font-size:1.05rem;line-height:1.8;">
        Queremos formar grupos de <b>{k_comb}</b> elementos.<br><br>
        A ordem <b>NÃO importa</b>:<br>
        {{A, B, C}} = {{C, A, B}} = {{B, C, A}}<br><br>
        São a <b>mesma combinação</b>!<br><br>
        Por isso dividimos por <b>{k_comb}!</b> = {math.factorial(k_comb)}.
        </div>
        """, unsafe_allow_html=True)

    # Visualização das combinações
    st.markdown("---")
    st.subheader(f"📋 Todas as {resultado_comb} combinações possíveis")

    if resultado_comb <= 30:
        combs = list(combinations(elementos_comb, k_comb))
        fig = plot_combinacoes_circulo(elementos_comb, combs, n_comb)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Muitas combinações para exibir. Reduza n ou k.")

    # Relação com arranjo
    st.markdown("---")
    st.subheader("🔗 Relação: Combinação vs Arranjo")

    arranjo_equiv = math.factorial(n_comb) // math.factorial(n_comb - k_comb)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(f"""
        <div style="background:#fff8e1;border-radius:10px;padding:1rem;text-align:center;">
            <b>Arranjo A({n_comb},{k_comb})</b><br>
            <div style="font-size:1.8rem;font-weight:700;color:#f39c12;">{arranjo_equiv}</div>
            <div style="font-size:0.85rem;color:#777;">ordem importa</div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div style="background:#f8f9fa;border-radius:10px;padding:1rem;text-align:center;">
            <b>Divisão por k!</b><br>
            <div style="font-size:1.8rem;font-weight:700;color:#555;">÷ {math.factorial(k_comb)}</div>
            <div style="font-size:0.85rem;color:#777;">cada grupo tem {math.factorial(k_comb)} ordenações</div>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown(f"""
        <div style="background:#e8f5e9;border-radius:10px;padding:1rem;text-align:center;">
            <b>Combinação C({n_comb},{k_comb})</b><br>
            <div style="font-size:1.8rem;font-weight:700;color:#2e7d32;">{resultado_comb}</div>
            <div style="font-size:0.85rem;color:#777;">ordem NÃO importa</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;margin-top:1rem;font-size:1.1rem;color:#555;">
        <b>C({n_comb},{k_comb}) = A({n_comb},{k_comb}) / {k_comb}!</b> = {arranjo_equiv} / {math.factorial(k_comb)} = {resultado_comb}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="step-box">
        <b>💡 Resumo:</b> Para obter a combinação, pegamos o arranjo (onde a ordem importa) e 
        <b>dividimos pelo número de formas de ordenar os k elementos escolhidos</b> (k!), 
        eliminando as repetições causadas pela ordem.
    </div>
    """, unsafe_allow_html=True)

# ============================================
# RODAPÉ COMPARATIVO (sempre visível)
# ============================================
st.markdown("---")
st.header("📊 Quadro Comparativo")

st.markdown("""
<div style="overflow-x:auto;">
<table style="width:100%;border-collapse:collapse;font-size:0.95rem;">
    <thead>
        <tr style="background:#1a1a2e;color:white;">
            <th style="padding:12px;border:1px solid #333;text-align:left;">Conceito</th>
            <th style="padding:12px;border:1px solid #333;text-align:center;">Ordem importa?</th>
            <th style="padding:12px;border:1px solid #333;text-align:center;">Usa todos?</th>
            <th style="padding:12px;border:1px solid #333;text-align:center;">Fórmula</th>
        </tr>
    </thead>
    <tbody>
        <tr style="background:#e8f4ff;">
            <td style="padding:10px;border:1px solid #ddd;font-weight:600;">🔄 Permutação Simples</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;">✅ Sim</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;">✅ Sim</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;font-family:monospace;">n!</td>
        </tr>
        <tr style="background:#ffeaea;">
            <td style="padding:10px;border:1px solid #ddd;font-weight:600;">🔁 Permutação c/ Repetição</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;">✅ Sim</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;">✅ Sim</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;font-family:monospace;">n!/(n₁!·n₂!·...)</td>
        </tr>
        <tr style="background:#fff8e1;">
            <td style="padding:10px;border:1px solid #ddd;font-weight:600;">📥 Arranjo Simples</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;">✅ Sim</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;">❌ Não (k ≤ n)</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;font-family:monospace;">n!/(n-k)!</td>
        </tr>
        <tr style="background:#e8f5e9;">
            <td style="padding:10px;border:1px solid #ddd;font-weight:600;">🤝 Combinação</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;">❌ Não</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;">❌ Não (k ≤ n)</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;font-family:monospace;">n!/(k!(n-k)!)</td>
        </tr>
    </tbody>
</table>
</div>
""", unsafe_allow_html=True)

# ============================================
# RODAPÉ
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    🎲 <b>Análise Combinatória Visual</b> — Ferramenta educacional para o ensino de Matemática<br>
    Use a barra lateral para navegar entre os conceitos e ajustar os parâmetros.
</div>
""", unsafe_allow_html=True)
