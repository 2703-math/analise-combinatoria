import streamlit as st
import math

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Análise Combinatória",
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
        margin-bottom: 2rem;
    }
    .concept-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid #27ae60;
        margin-bottom: 1.5rem;
    }
    .param-box {
        background: #fff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .resolution-box {
        background: #e8f5e9;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
        border: 1px solid #c8e6c9;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# TÍTULO PRINCIPAL
# ============================================
st.markdown('<div class="main-title">🎲 Análise Combinatória Visual</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explorando princípios de contagem, arranjos e combinações</div>', unsafe_allow_html=True)

# ============================================
# NAVEGAÇÃO NO CORPO DO SITE (ABAS)
# ============================================
tab1, tab2, tab3 = st.tabs([
    "1. Problema da Escada (Restrição)", 
    "2. Combinação Simples (Equipes)", 
    "3. Arranjo Simples (Senhas)"
])

# ============================================
# ABA 1: PROBLEMA DA ESCADA
# ============================================
with tab1:
    st.markdown("""
    <div class="concept-card">
        <b>📌 O Problema</b><br>
        Uma escada tem <b>n</b> degraus. Cada degrau deve ser pintado com uma de <b>k</b> cores diferentes. 
        <b>Regra:</b> Degraus consecutivos não podem ter a mesma cor. De quantas maneiras podemos pintar a escada?
    </div>
    """, unsafe_allow_html=True)
    
    col_ctrl, col_calc = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Controles")
        n_degraus = st.number_input("Número de Degraus (n)", min_value=2, max_value=20, value=6, step=1)
        k_cores = st.number_input("Número de Cores disponíveis (k)", min_value=2, max_value=10, value=4, step=1)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_calc:
        total_coloracoes = k_cores * ((k_cores - 1)**(n_degraus - 1))
        
        st.markdown("""
        <div style="font-size:1.1rem; font-weight:700; color:#27ae60; margin-bottom:0.5rem;">
            ✏️ Resolução
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="font-size:1rem; color:#333; line-height:1.8;">
            <b>1º degrau:</b> {k_cores} opções de cores.<br>
            <b>2º degrau em diante:</b> cada um tem {k_cores - 1} opções (não pode ser igual ao anterior).
        </div>
        """, unsafe_allow_html=True)
        
        # Matemática formatada corretamente em bloco
        st.markdown(rf"$$ Total = {k_cores} \times {k_cores - 1}^{{{n_degraus} - 1}} $$")
        st.markdown(rf"$$ Total = {k_cores} \times {(k_cores - 1)**(n_degraus - 1)} $$")
        st.markdown(rf"$$ \mathbf{{Total = {total_coloracoes} \text{{ maneiras}}}} $$")

    st.markdown("---")
    st.subheader("🔗 Relação com outros conceitos")
    st.markdown("Se **não houvesse a restrição** (degraus adjacentes podem ter a mesma cor), a fórmula seria uma potência simples:")
    
    # Frações e potências renderizadas centralizadas
    st.markdown(rf"$$ k^n = {k_cores}^{{{n_degraus}}} = \mathbf{{{k_cores ** n_degraus}}} \text{{ colorações (sem restrição)}} $$")
    
    st.markdown("Com a restrição, eliminamos as colorações inválidas, resultando na equação geral:")
    st.markdown(rf"$$ k \cdot (k - 1)^{{n-1}} = {k_cores} \cdot {k_cores - 1}^{{{n_degraus - 1}}} = \mathbf{{{total_coloracoes}}} \text{{ colorações (com restrição)}} $$")


# ============================================
# ABA 2: COMBINAÇÃO SIMPLES (FRAÇÕES EM 2 LINHAS)
# ============================================
with tab2:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>📌 Combinação Simples (A ordem NÃO importa)</b><br>
        Usado para formar grupos, equipes ou sorteios (ex: Mega-Sena). Se você escolher as pessoas A e B, 
        é o mesmo grupo que B e A.
    </div>
    """, unsafe_allow_html=True)
    
    col_ctrl, col_calc = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Controles")
        n_elementos = st.number_input("Total de Elementos (n)", min_value=1, max_value=50, value=10, step=1)
        p_escolhas = st.number_input("Elementos a Escolher (p)", min_value=1, max_value=n_elementos, value=3, step=1)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_calc:
        combinacao = math.comb(n_elementos, p_escolhas)
        n_p = n_elementos - p_escolhas
        
        st.markdown("A fórmula da Combinação utiliza frações verticais com fatoriais:")
        
        # O uso de \frac{}{} dentro de $$ garante que a fração fique em duas linhas perfeitas!
        st.markdown(rf"""
        $$ C_{{{n_elementos}, {p_escolhas}}} = \frac{{n!}}{{p!(n-p)!}} $$
        """)
        
        st.markdown("Substituindo os valores:")
        st.markdown(rf"""
        $$ C_{{{n_elementos}, {p_escolhas}}} = \frac{{{n_elementos}!}}{{{p_escolhas}! \cdot ({n_elementos} - {p_escolhas})!}} $$
        """)
        
        st.markdown("Resolvendo:")
        st.markdown(rf"""
        $$ C_{{{n_elementos}, {p_escolhas}}} = \frac{{{n_elementos}!}}{{{p_escolhas}! \cdot {n_p}!}} = \mathbf{{{combinacao}}} \text{{ grupos diferentes}} $$
        """)


# ============================================
# ABA 3: ARRANJO SIMPLES (FRAÇÕES EM 2 LINHAS)
# ============================================
with tab3:
    st.markdown("""
    <div class="concept-card" style="border-left-color: #e74c3c;">
        <b>📌 Arranjo Simples (A ordem IMPORTA)</b><br>
        Usado quando a posição muda o resultado (ex: senhas, pódios de corrida). 
        A senha "123" é completamente diferente da senha "321".
    </div>
    """, unsafe_allow_html=True)
    
    col_ctrl, col_calc = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("<div class='param-box'>", unsafe_allow_html=True)
        st.subheader("🎛️ Controles")
        n_arr = st.number_input("Total de Opções (n)", min_value=1, max_value=20, value=5, step=1)
        p_arr = st.number_input("Posições disponíveis (p)", min_value=1, max_value=n_arr, value=3, step=1)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_calc:
        arranjo = math.perm(n_arr, p_arr)
        n_p_arr = n_arr - p_arr
        
        st.markdown("Diferente da combinação, no Arranjo nós não dividimos por $p!$ (pois não removemos as repetições de ordem):")
        
        st.markdown(rf"""
        $$ A_{{{n_arr}, {p_arr}}} = \frac{{n!}}{{(n-p)!}} $$
        """)
        
        st.markdown("Substituindo os valores:")
        st.markdown(rf"""
        $$ A_{{{n_arr}, {p_arr}}} = \frac{{{n_arr}!}}{{({n_arr} - {p_arr})!}} = \frac{{{n_arr}!}}{{{n_p_arr}!}} $$
        """)
        
        st.markdown("Resolvendo:")
        st.markdown(rf"""
        $$ A_{{{n_arr}, {p_arr}}} = \mathbf{{{arranjo}}} \text{{ arranjos possíveis}} $$
        """)
