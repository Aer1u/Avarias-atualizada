import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page config for a widescreen layout
st.set_page_config(
    page_title="Gestão de Avarias PRO",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Extreme Transformation
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    
    <style>
    /* Global Styles */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #fcfcfd !important;
    }

    /* Keyframes for Staggered Animations */
    @keyframes slideUpFade {
        0% { opacity: 0; transform: translateY(30px) scale(0.98); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    /*
    - [x] Extreme UI Transformation (Professional & Animated) <!-- id: 21 -->
    - [x] Force system-level light theme (config.toml) <!-- id: 22 -->
    - [x] Implement Glassmorphism and Backdrop filters <!-- id: 23 -->
    - [x] Add staggered entrance animations <!-- id: 24 -->
    - [x] Integrate Google Fonts (Inter) <!-- id: 25 -->
    */
    @keyframes grain {
        0%, 100% { transform:translate(0, 0) }
        10% { transform:translate(-5%, -10%) }
        20% { transform:translate(-15%, 5%) }
        30% { transform:translate(7%, -25%) }
        40% { transform:translate(-5%, 25%) }
        50% { transform:translate(-15%, 10%) }
        60% { transform:translate(15%, 0) }
        70% { transform:translate(0, 15%) }
        80% { transform:translate(3%, 35%) }
        90% { transform:translate(-10%, 10%) }
    }

    /* Professional Background & Containers */
    .stApp {
        background: radial-gradient(circle at top right, #f0f4ff 0%, #ffffff 100%) !important;
    }
    
    [data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px);
    }

    /* Metric Cards - Glassmorphism PRO */
    .metric-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 28px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        margin-bottom: 20px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        opacity: 0;
        animation: slideUpFade 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }

    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 45px rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
        background: rgba(255, 255, 255, 0.95);
    }

    .stagger-1 { animation-delay: 0.1s; }
    .stagger-2 { animation-delay: 0.2s; }
    .stagger-3 { animation-delay: 0.3s; }
    .stagger-4 { animation-delay: 0.4s; }
    .stagger-5 { animation-delay: 0.5s; }

    .metric-title {
        color: #64748b !important;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Fixed Table Glitch - Force White */
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        background-color: white !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid #f1f5f9 !important;
    }

    /* Header Styling */
    .header-main {
        padding: 2rem 0;
        animation: slideUpFade 0.6s ease-out forwards;
    }

    .status-badge {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        color: #065f46;
        padding: 8px 20px;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: inline-flex;
        align-items: center;
        border: 1px solid #a7f3d0;
    }

    .status-dot {
        height: 10px;
        width: 10px;
        background: #10b981;
        border-radius: 50%;
        margin-right: 10px;
        box-shadow: 0 0 10px #10b981;
    }

    /* Chart Containers */
    .chart-container {
        background: white;
        border-radius: 20px;
        padding: 20px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        animation: slideUpFade 0.8s ease-out 0.4s forwards;
        opacity: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to load and clean data
@st.cache_data
def load_data():
    file_path = r'c:\Users\Pichau\Downloads\Avaria\Drive atualizado.xlsx'
    try:
        df = pd.read_excel(file_path)
        
        # Fixing column names (robust approach for encoding issues)
        new_cols = {}
        for col in df.columns:
            if 'Posi' in col: new_cols[col] = 'Posição atual'
            elif 'Altera' in col: new_cols[col] = 'Data de Alteração'
            elif 'Obsevar' in col: new_cols[col] = 'Observação'
        
        df = df.rename(columns=new_cols)
        
        # Fill missing values
        df['Produto'] = df['Produto'].fillna('Não Identificado')
        df['Drive Misturado'] = df['Drive Misturado'].fillna('Não')
        df['Quantidade Total'] = df['Quantidade Total'].fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

# Main Application logic
def main():
    df_raw = load_data()
    
    if df_raw.empty:
        st.warning("Nenhum dado encontrado no arquivo.")
        return

    # --- Header ---
    st.markdown("""
        <div class="header-main">
            <h1 style='margin-bottom: 0; font-weight: 800; font-size: 2.8rem; color: #1e293b;'>Gestão de Avarias PRO</h1>
            <p style='color: #64748b; margin-top: 5px; font-size: 1.2rem; font-weight: 400;'>Painel executivo de controle de estoque e auditoria</p>
            <div style="margin-top: 20px;">
                <div class="status-badge">
                    <span class="status-dot"></span> Operação Ativa
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- Filters (Sidebar) ---
    st.sidebar.markdown("### 🔍 Filtros")
    
    all_products = sorted(df_raw['Produto'].unique().tolist())
    selected_products = st.sidebar.multiselect("Produto", options=all_products)
    
    all_levels = sorted(df_raw['Nivel'].dropna().unique().tolist())
    selected_levels = st.sidebar.multiselect("Nível", options=all_levels)
    
    mixed_filter = st.sidebar.radio("Drive Misturado", options=["Todos", "Sim", "Não"], horizontal=True)

    # Apply Filters
    df = df_raw.copy()
    if selected_products:
        df = df[df['Produto'].isin(selected_products)]
    if selected_levels:
        df = df[df['Nivel'].isin(selected_levels)]
    if mixed_filter != "Todos":
        df = df[df['Drive Misturado'] == mixed_filter]

    # Calculate Occupancy
    df['Ocupacao_%'] = (df['Quantidade Total'] / df['Capacidade'] * 100).clip(0, 100).fillna(0)

    # --- KPI Section ---
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns([1, 1, 1, 1, 1.5])
    
    with kpi1:
        total_pallets = df['Qtd. de Palete'].sum()
        st.markdown(f"""
            <div class="metric-card stagger-1">
                <div class="metric-title">PALETES 📦</div>
                <div class="metric-value">{int(total_pallets)}</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi2:
        total_qty = df['Quantidade Total'].sum()
        st.markdown(f"""
            <div class="metric-card stagger-2">
                <div class="metric-title">QUANTIDADE 📊</div>
                <div class="metric-value">{int(total_qty):,}</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi3:
        unique_pos = df['Posição atual'].nunique()
        st.markdown(f"""
            <div class="metric-card stagger-3">
                <div class="metric-title">POSIÇÕES 🛡️</div>
                <div class="metric-value">{unique_pos}</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi4:
        unique_skus = df['Produto'].nunique()
        st.markdown(f"""
            <div class="metric-card stagger-4">
                <div class="metric-title">PRODUTOS 📈</div>
                <div class="metric-value">{unique_skus}</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi5:
        # Gauge for Overall Occupancy
        total_cap = df['Capacidade'].sum()
        if total_cap > 0:
            avg_occupancy = (total_qty / total_cap) * 100
        else:
            avg_occupancy = 0
            
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_occupancy,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Ocupação Geral (%)", 'font': {'size': 14}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "#0066cc"},
                'steps': [
                    {'range': [0, 70], 'color': "#e8f0fe"},
                    {'range': [70, 90], 'color': "#fff3e0"},
                    {'range': [90, 100], 'color': "#ffebee"}],
            }
        ))
        fig_gauge.update_layout(
            height=160, 
            margin=dict(l=10, r=10, t=30, b=10), 
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#0f172a", 'family': "Inter, sans-serif"}
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    # --- Visual Analytics Section (Decorations) ---
    st.markdown("<h2 style='font-size: 1.5rem; margin-top: 2rem; margin-bottom: 1.5rem; color: #1e293b; font-weight: 700;'>Análise Visual de Performance</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Top 10 Products by Quantity
        top_prods = df.groupby('Produto')['Quantidade Total'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(
            top_prods, 
            x='Quantidade Total', 
            y='Produto', 
            orientation='h',
            title='TOP 10 PRODUTOS POR VOLUME',
            color='Quantidade Total',
            color_continuous_scale='Blues',
            template='plotly_white'
        )
        fig_bar.update_layout(
            showlegend=False, 
            height=400, 
            margin=dict(l=0, r=0, t=60, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "#0f172a", 'family': "Inter, sans-serif"},
            title_font={'size': 14, 'color': '#64748b'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Mixed vs Not Mixed Distribution
        mixed_counts = df['Drive Misturado'].value_counts().reset_index()
        fig_pie = px.pie(
            mixed_counts, 
            values='count', 
            names='Drive Misturado',
            title='AUDITORIA DE DRIVES',
            hole=0.4,
            color='Drive Misturado',
            color_discrete_map={'Não': '#3b82f6', 'Sim': '#ef4444'},
            template='plotly_white'
        )
        fig_pie.update_layout(
            height=400, 
            margin=dict(l=0, r=0, t=60, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "#0f172a", 'family': "Inter, sans-serif"},
            title_font={'size': 14, 'color': '#64748b'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Main Content Section ---
    st.markdown("<h2 style='font-size: 1.5rem; margin-top: 2rem;'>Registros de Estoque</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #718096; margin-top: -10px;'>{len(df)} de {len(df_raw)} registros exibidos</p>", unsafe_allow_html=True)

    tab_pos, tab_prod = st.tabs(["📍 Posições", "📦 Produtos"])

    with tab_pos:
        # Search component
        search_query = st.text_input("Buscar e Filtrar", placeholder="Pesquisar por produto, posição ou palete...", label_visibility="collapsed")
        
        if search_query:
            # Search across all relevant columns
            mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
            display_df = df[mask]
        else:
            display_df = df

        # Customizing the dataframe display
        st.dataframe(
            display_df,
            column_config={
                "Posição atual": st.column_config.TextColumn("Posição"),
                "Quantidade Total": st.column_config.NumberColumn("Qtd", format="%d"),
                "Capacidade": st.column_config.NumberColumn("Cap", format="%d"),
                "Ocupacao_%": st.column_config.ProgressColumn(
                    "Ocupação",
                    help="Percentual de ocupação da posição",
                    format="%d%%",
                    min_value=0,
                    max_value=100,
                ),
                "Drive Misturado": st.column_config.TextColumn("Status"),
            },
            width="stretch",
            hide_index=True
        )

    with tab_prod:
        # Aggregated view for Products
        df_prod_summary = df.groupby('Produto').agg({
            'Quantidade Total': 'sum',
            'Qtd. de Palete': 'sum',
            'Posição atual': 'count'
        }).reset_index().rename(columns={'Posição atual': 'Qtd. de Posições'})
        
        st.dataframe(
            df_prod_summary,
            width="stretch",
            hide_index=True,
            column_config={
                "Quantidade Total": st.column_config.NumberColumn("Qtd. Total", format="%d"),
                "Qtd. de Palete": st.column_config.NumberColumn("Paletes", format="%d"),
            }
        )

    # Export button (Streamlit standard)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exportar Dados como CSV",
        data=csv,
        file_name="estoque_avarias.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    main()
