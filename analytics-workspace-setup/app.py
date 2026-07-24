import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Set page configuration
st.set_page_config(
    page_title="Seller Trust & Behaviour Analytics Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #0f111a;
        color: #e6e6fa;
    }
    
    /* Header card styling */
    .header-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 2rem;
        border: 1px solid #4338ca;
    }
    
    .header-title {
        color: #ffffff;
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(108, 99, 255, 0.4);
    }
    
    .header-subtitle {
        color: #93c5fd;
        font-size: 1.1rem;
        font-weight: 300;
    }
    
    /* Custom KPI Cards */
    .kpi-card {
        background-color: #161925;
        border: 1px solid #2d3142;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #6366f1;
        box-shadow: 0 6px 15px rgba(99, 102, 241, 0.2);
    }
    
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.2rem;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    .delta-up {
        color: #10b981;
    }
    
    .delta-down {
        color: #ef4444;
    }
    
    /* Segment headings */
    .section-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 4px solid #6366f1;
        padding-left: 0.5rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #0b0c10;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load data
@st.cache_data
def load_data():
    metrics_path = "data/processed/seller_weekly_metrics.csv"
    reviews_path = "data/processed/customer_reviews_sample.csv"
    
    if not os.path.exists(metrics_path) or not os.path.exists(reviews_path):
        # Fallback to absolute paths if running from a different subfolder
        metrics_path = "/Users/pranava.m/Documents/Datasights-python-e-commerce-dashboard/analytics-workspace-setup/data/processed/seller_weekly_metrics.csv"
        reviews_path = "/Users/pranava.m/Documents/Datasights-python-e-commerce-dashboard/analytics-workspace-setup/data/processed/customer_reviews_sample.csv"
        
    df_metrics = pd.read_csv(metrics_path)
    df_reviews = pd.read_csv(reviews_path)
    
    # Ensure date conversion
    df_metrics['week_start'] = pd.to_datetime(df_metrics['week_start'])
    df_reviews['review_date'] = pd.to_datetime(df_reviews['review_date'])
    
    return df_metrics, df_reviews

try:
    df_metrics, df_reviews = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}. Please make sure you have run the mock data generator first.")
    st.stop()

# Get available weeks and sellers
all_weeks = sorted(df_metrics['week_start'].unique())
latest_week = all_weeks[-1]
previous_week = all_weeks[-2] if len(all_weeks) > 1 else latest_week

# Sidebar controls
st.sidebar.image("https://img.icons8.com/nolan/96/shield.png", width=64)
st.sidebar.title("Trust Operations")
st.sidebar.markdown("---")

# Navigation Selector
page = st.sidebar.radio(
    "Navigation Menu",
    ["Marketplace Trust Health", "Seller Trust Audit", "Behavioral Cohorts & Simulator"],
    index=0
)

st.sidebar.markdown("---")

# Global Category Filter
available_categories = ["All"] + sorted(list(df_metrics['category'].unique()))
selected_category = st.sidebar.selectbox("Filter by Category", available_categories)

# Sidebar CTI Explanation Expander
with st.sidebar.expander("ℹ️ Customer Trust Index (CTI) Framework"):
    st.markdown("""
    The **Customer Trust Index (CTI)** evaluates seller reliability on a scale of **0 to 100**.
    
    **Penalties Applied:**
    - **Late Shipment (LSR)**: Max -25 pts (Penalty starts >0.5%)
    - **Seller Cancellations (SCR)**: Max -30 pts (Penalty starts >0.1%)
    - **Seller-Fault Returns (SFRR)**: Max -30 pts (Penalty starts >0.5%)
    - **Negative Sentiment Rate (NRR)**: Max -25 pts (Penalty starts >2%)
    
    **Trust Tiers:**
    - 🟢 **Excellent (90-100)**: Clean logs, high trust.
    - 🟡 **Good (80-89)**: Minor friction, operational.
    - 🟠 **At Risk (70-79)**: Trust decay, requires attention.
    - 🔴 **Critical Deficit (<70)**: Severe trust damage, immediate intervention.
    """)

# Filter metrics and reviews by category globally
if selected_category != "All":
    df_metrics_filtered = df_metrics[df_metrics['category'] == selected_category]
    df_reviews_filtered = df_reviews[df_reviews['category'] == selected_category]
else:
    df_metrics_filtered = df_metrics
    df_reviews_filtered = df_reviews

# Title Block
st.markdown("""
<div class="header-box">
    <div class="header-title">Seller Trust & Behaviour Analytics</div>
    <div class="header-subtitle">Identifying seller operational behaviors that degrade customer trust and sentiment over time</div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# PAGE 1: MARKETPLACE TRUST HEALTH
# ==========================================
if page == "Marketplace Trust Health":
    st.markdown('<div class="section-title">Marketplace Trust Overview</div>', unsafe_allow_html=True)
    
    # Calculate KPIs for latest week vs previous week
    latest_metrics = df_metrics_filtered[df_metrics_filtered['week_start'] == latest_week]
    prev_metrics = df_metrics_filtered[df_metrics_filtered['week_start'] == previous_week]
    
    avg_trust_latest = latest_metrics['trust_score'].mean()
    avg_trust_prev = prev_metrics['trust_score'].mean()
    trust_change = avg_trust_latest - avg_trust_prev
    
    avg_lsr_latest = latest_metrics['late_shipment_rate'].mean()
    avg_lsr_prev = prev_metrics['late_shipment_rate'].mean()
    lsr_change = avg_lsr_latest - avg_lsr_prev
    
    avg_scr_latest = latest_metrics['seller_cancellation_rate'].mean()
    avg_scr_prev = prev_metrics['seller_cancellation_rate'].mean()
    scr_change = avg_scr_latest - avg_scr_prev
    
    avg_sfrr_latest = latest_metrics['seller_fault_return_rate'].mean()
    avg_sfrr_prev = prev_metrics['seller_fault_return_rate'].mean()
    sfrr_change = avg_sfrr_latest - avg_sfrr_prev
    
    # Trust categories counts for latest week
    excellent_count = len(latest_metrics[latest_metrics['trust_score'] >= 90])
    good_count = len(latest_metrics[(latest_metrics['trust_score'] >= 80) & (latest_metrics['trust_score'] < 90)])
    at_risk_count = len(latest_metrics[(latest_metrics['trust_score'] >= 70) & (latest_metrics['trust_score'] < 80)])
    critical_count = len(latest_metrics[latest_metrics['trust_score'] < 70])
    total_sellers = len(latest_metrics)
    
    pct_critical_at_risk = ((at_risk_count + critical_count) / total_sellers) * 100 if total_sellers > 0 else 0
    
    # Render KPI Cards in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        delta_class = "delta-up" if trust_change >= 0 else "delta-down"
        delta_sign = "+" if trust_change >= 0 else ""
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_trust_latest:.1f}</div>
            <div class="kpi-label">Marketplace Trust Index</div>
            <div class="kpi-delta {delta_class}">{delta_sign}{trust_change:.2f} vs last week</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        # Lower LSR is better
        delta_class = "delta-up" if lsr_change <= 0 else "delta-down"
        delta_sign = "+" if lsr_change >= 0 else ""
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_lsr_latest*100:.2f}%</div>
            <div class="kpi-label">Avg Late Shipment Rate</div>
            <div class="kpi-delta {delta_class}">{delta_sign}{lsr_change*100:.2f}% vs last week</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        # Lower SCR is better
        delta_class = "delta-up" if scr_change <= 0 else "delta-down"
        delta_sign = "+" if scr_change >= 0 else ""
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_scr_latest*100:.2f}%</div>
            <div class="kpi-label">Avg Cancellation Rate</div>
            <div class="kpi-delta {delta_class}">{delta_sign}{scr_change*100:.2f}% vs last week</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        # Lower Return Rate is better
        delta_class = "delta-up" if sfrr_change <= 0 else "delta-down"
        delta_sign = "+" if sfrr_change >= 0 else ""
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_sfrr_latest*100:.2f}%</div>
            <div class="kpi-label">Avg Seller-Fault Return</div>
            <div class="kpi-delta {delta_class}">{delta_sign}{sfrr_change*100:.2f}% vs last week</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{pct_critical_at_risk:.1f}%</div>
            <div class="kpi-label">Sellers At Risk/Critical</div>
            <div class="kpi-delta {"delta-down" if pct_critical_at_risk > 10 else "delta-up"}">{at_risk_count + critical_count} of {total_sellers} sellers</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Main Charts: Distribution of Seller Health and Category Trends
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown('<div class="section-title">Seller Health Distribution (Latest Week)</div>', unsafe_allow_html=True)
        
        # Donut Chart for Trust Tiers
        tier_labels = ["Excellent (90-100)", "Good (80-89)", "At Risk (70-79)", "Critical Deficit (<70)"]
        tier_values = [excellent_count, good_count, at_risk_count, critical_count]
        tier_colors = ["#10b981", "#3b82f6", "#f59e0b", "#ef4444"]
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=tier_labels,
            values=tier_values,
            hole=.4,
            marker_colors=tier_colors,
            textinfo="percent+value",
            insidetextorientation="radial"
        )])
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6fa'),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            margin=dict(t=10, b=50, l=10, r=10),
            height=380
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with chart_col2:
        st.markdown('<div class="section-title">Trust Trends by Category Over Time</div>', unsafe_allow_html=True)
        
        # Line chart of average Trust Score by category over 52 weeks
        category_trends = df_metrics_filtered.groupby(['week_start', 'category'])['trust_score'].mean().reset_index()
        
        fig_trends = px.line(
            category_trends,
            x="week_start",
            y="trust_score",
            color="category",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"week_start": "Date", "trust_score": "Average Trust Score"}
        )
        fig_trends.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6fa'),
            xaxis=dict(showgrid=True, gridcolor='#2d3142', linecolor='#2d3142'),
            yaxis=dict(showgrid=True, gridcolor='#2d3142', linecolor='#2d3142', range=[70, 100]),
            margin=dict(t=10, b=20, l=10, r=10),
            height=380
        )
        st.plotly_chart(fig_trends, use_container_width=True)
        
    # Analysis Row: Correlation & Top Degrading Behaviors
    anal_col1, anal_col2 = st.columns(2)
    
    with anal_col1:
        st.markdown('<div class="section-title">Behavior-Trust Correlation Analysis</div>', unsafe_allow_html=True)
        
        # Calculate correlation matrix
        corr_cols = [
            "trust_score", 
            "late_shipment_rate", 
            "seller_cancellation_rate", 
            "seller_fault_return_rate", 
            "negative_review_rate",
            "avg_review_rating"
        ]
        corr_matrix = df_metrics_filtered[corr_cols].corr()
        
        # Pretty labels for heatmaps
        pretty_labels = [
            "Trust Score",
            "Late Shipment %",
            "Cancellation %",
            "Seller-Fault Return %",
            "Negative Reviews %",
            "Avg Rating"
        ]
        
        fig_heat = px.imshow(
            corr_matrix,
            x=pretty_labels,
            y=pretty_labels,
            color_continuous_scale="RdBu",
            zmin=-1,
            zmax=1,
            text_auto=".2f",
            labels=dict(color="Correlation")
        )
        fig_heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6fa'),
            margin=dict(t=10, b=10, l=10, r=10),
            coloraxis_colorbar=dict(title="Corr", thickness=15, len=0.8),
            height=380
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        st.caption("🔍 **Insight**: Negative correlations (red) show behaviors that degrade trust. Notice how return rate, cancellations, and shipping delays heavily pull down the Trust Score.")
        
    with anal_col2:
        st.markdown('<div class="section-title">Impact Weights of Trust Penalties</div>', unsafe_allow_html=True)
        
        # Calculated based on latest average scores
        # We can extract the penalty components across all sellers:
        # LSR Penalty: min(25, LSR * 150)
        # SCR Penalty: min(30, SCR * 250)
        # SFRR Penalty: min(30, SFRR * 200)
        # NRR Penalty: min(25, NRR * 150)
        
        avg_lsr_penalty = latest_metrics['late_shipment_rate'].apply(lambda x: min(25, x * 150)).mean()
        avg_scr_penalty = latest_metrics['seller_cancellation_rate'].apply(lambda x: min(30, x * 250)).mean()
        avg_sfrr_penalty = latest_metrics['seller_fault_return_rate'].apply(lambda x: min(30, x * 200)).mean()
        avg_nrr_penalty = latest_metrics['negative_review_rate'].apply(lambda x: min(25, x * 150)).mean()
        
        total_penalties = avg_lsr_penalty + avg_scr_penalty + avg_sfrr_penalty + avg_nrr_penalty
        
        penalty_data = pd.DataFrame({
            "Behavioral Driver": [
                "Seller-Fault Returns (SFRR)", 
                "Late Shipment (LSR)", 
                "Negative Reviews (NRR)", 
                "Seller Cancellations (SCR)"
            ],
            "Avg Penalty Points": [
                avg_sfrr_penalty,
                avg_lsr_penalty,
                avg_nrr_penalty,
                avg_scr_penalty
            ],
            "Percentage Contribution": [
                (avg_sfrr_penalty / total_penalties * 100) if total_penalties > 0 else 0,
                (avg_lsr_penalty / total_penalties * 100) if total_penalties > 0 else 0,
                (avg_nrr_penalty / total_penalties * 100) if total_penalties > 0 else 0,
                (avg_scr_penalty / total_penalties * 100) if total_penalties > 0 else 0
            ]
        }).sort_values(by="Avg Penalty Points", ascending=True)
        
        fig_bar = px.bar(
            penalty_data,
            y="Behavioral Driver",
            x="Avg Penalty Points",
            orientation="h",
            text="Percentage Contribution",
            color="Avg Penalty Points",
            color_continuous_scale=px.colors.sequential.Sunsetdark,
            labels={"Avg Penalty Points": "Average Deduction Points (Max 30)"}
        )
        fig_bar.update_traces(
            texttemplate="%{text:.1f}% of trust loss", 
            textposition="inside",
            insidetextanchor="middle"
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6fa'),
            xaxis=dict(showgrid=True, gridcolor='#2d3142', linecolor='#2d3142', range=[0, 15]),
            yaxis=dict(showgrid=False, linecolor='#2d3142'),
            margin=dict(t=10, b=20, l=10, r=10),
            coloraxis_showscale=False,
            height=380
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.caption("⚠️ **Deductions Break down**: Indicates which behaviors are responsible for the average Trust Index decline across the marketplace.")


# ==========================================
# PAGE 2: SELLER TRUST AUDIT (DEEP-DIVE)
# ==========================================
elif page == "Seller Trust Audit":
    st.markdown('<div class="section-title">Seller Detailed Performance Audit</div>', unsafe_allow_html=True)
    
    # Filter dropdown by globally selected category if applicable
    available_sellers = sorted(df_metrics_filtered['seller_id'].unique())
    
    # Select a seller
    selected_seller = st.selectbox("Select Seller for Full Audit", available_sellers)
    
    # Get this seller's specific data
    seller_metrics = df_metrics[df_metrics['seller_id'] == selected_seller].sort_values(by="week_start")
    seller_latest = seller_metrics.iloc[-1]
    
    # Current values
    current_trust = seller_latest['trust_score']
    current_lsr = seller_latest['late_shipment_rate']
    current_scr = seller_latest['seller_cancellation_rate']
    current_sfrr = seller_latest['seller_fault_return_rate']
    current_nrr = seller_latest['negative_review_rate']
    
    # Penalties
    lsr_penalty = min(25, current_lsr * 150)
    scr_penalty = min(30, current_scr * 250)
    sfrr_penalty = min(30, current_sfrr * 200)
    nrr_penalty = min(25, current_nrr * 150)
    
    # 1. Profile Panel
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    
    # Determine Tier Status
    if current_trust >= 90:
        tier_status = "🟢 Excellent (High Trust)"
        tier_color = "#10b981"
    elif current_trust >= 80:
        tier_status = "🔵 Good (Low Risk)"
        tier_color = "#3b82f6"
    elif current_trust >= 70:
        tier_status = "🟡 At Risk (Moderate Risk)"
        tier_color = "#f59e0b"
    else:
        tier_status = "🔴 Critical Deficit (Severe Risk)"
        tier_color = "#ef4444"
        
    with p_col1:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid {tier_color};">
            <div class="kpi-value" style="color: {tier_color}">{current_trust:.1f}</div>
            <div class="kpi-label">Current CTI Score</div>
            <div class="kpi-delta" style="color: {tier_color}">{tier_status}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with p_col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{seller_latest['sales_volume']:,}</div>
            <div class="kpi-label">Weekly Sales Volume</div>
            <div class="kpi-delta">Category: {seller_latest['category']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with p_col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">${seller_latest['revenue']:,.2f}</div>
            <div class="kpi-label">Weekly Revenue</div>
            <div class="kpi-delta">Item Price: ~${seller_latest['revenue']/seller_latest['sales_volume']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with p_col4:
        # Identify the biggest driver of trust loss
        penalties_dict = {
            "Late Shipment Penalty": lsr_penalty,
            "Seller Cancellations Penalty": scr_penalty,
            "Seller-Fault Return Penalty": sfrr_penalty,
            "Negative Reviews Penalty": nrr_penalty
        }
        max_penalty_name = max(penalties_dict, key=penalties_dict.get)
        max_penalty_val = penalties_dict[max_penalty_name]
        
        if max_penalty_val < 1.0:
            primary_driver = "No significant defects"
            driver_color = "#10b981"
        else:
            primary_driver = max_penalty_name.replace(" Penalty", "")
            driver_color = "#ef4444"
            
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="font-size: 1.5rem; color: {driver_color}; padding-top: 0.6rem; padding-bottom: 0.6rem;">{primary_driver}</div>
            <div class="kpi-label">Primary Operational Threat</div>
            <div class="kpi-delta">Deduction: -{max_penalty_val:.1f} pts</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Visualizing the CTI Score deduction waterfall
    st.markdown('<div class="section-title">Trust Score Attribution Waterfall</div>', unsafe_allow_html=True)
    
    fig_waterfall = go.Figure(go.Waterfall(
        name="CTI Score Attribution",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "relative", "total"],
        x=["Base Score", "Late Shipment LSR", "Cancellations SCR", "Fault Returns SFRR", "Negative Reviews NRR", "Final Trust Score"],
        textposition="outside",
        text=["+100.0", f"-{lsr_penalty:.1f}", f"-{scr_penalty:.1f}", f"-{sfrr_penalty:.1f}", f"-{nrr_penalty:.1f}", f"{current_trust:.1f}"],
        y=[100, -lsr_penalty, -scr_penalty, -sfrr_penalty, -nrr_penalty, 0],
        connector={"line": {"color": "#6366f1", "width": 1.5}},
        decreasing={"marker": {"color": "#ef4444"}},
        increasing={"marker": {"color": "#10b981"}},
        totals={"marker": {"color": tier_color}}
    ))
    
    fig_waterfall.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e6e6fa'),
        yaxis=dict(showgrid=True, gridcolor='#2d3142', range=[0, 110]),
        margin=dict(t=20, b=20, l=10, r=10),
        height=320
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)
    
    # Weekly Trends charts
    trend_col1, trend_col2 = st.columns(2)
    
    with trend_col1:
        st.markdown('<div class="section-title">Sales vs. Customer Trust Trend</div>', unsafe_allow_html=True)
        
        # Dual axis plot: Sales Volume and Trust Score
        fig_twin = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_twin.add_trace(
            go.Scatter(x=seller_metrics['week_start'], y=seller_metrics['trust_score'], name="Customer Trust Index", line=dict(color="#6366f1", width=3)),
            secondary_y=False,
        )
        
        fig_twin.add_trace(
            go.Bar(x=seller_metrics['week_start'], y=seller_metrics['sales_volume'], name="Sales Volume", marker_color="rgba(147, 197, 253, 0.3)"),
            secondary_y=True,
        )
        
        fig_twin.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6fa'),
            xaxis=dict(showgrid=True, gridcolor='#2d3142', linecolor='#2d3142'),
            yaxis=dict(title="Trust Score (CTI)", showgrid=True, gridcolor='#2d3142', linecolor='#2d3142', range=[0, 105]),
            yaxis2=dict(title="Orders per Week", showgrid=False, linecolor='#2d3142'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=30, b=20, l=10, r=10),
            height=350
        )
        st.plotly_chart(fig_twin, use_container_width=True)
        st.caption("💡 **Interpretation**: Observe if drops in Customer Trust are followed by corresponding drops in sales volume in subsequent weeks.")
        
    with trend_col2:
        st.markdown('<div class="section-title">Operational Defects Trend</div>', unsafe_allow_html=True)
        
        # Multi-line chart showing the rates
        fig_rates = go.Figure()
        fig_rates.add_trace(go.Scatter(x=seller_metrics['week_start'], y=seller_metrics['late_shipment_rate']*100, name="Late Shipment (LSR)", line=dict(color="#fb7185", width=2)))
        fig_rates.add_trace(go.Scatter(x=seller_metrics['week_start'], y=seller_metrics['seller_cancellation_rate']*100, name="Cancellation (SCR)", line=dict(color="#f43f5e", width=2)))
        fig_rates.add_trace(go.Scatter(x=seller_metrics['week_start'], y=seller_metrics['seller_fault_return_rate']*100, name="Fault Return (SFRR)", line=dict(color="#f59e0b", width=2)))
        fig_rates.add_trace(go.Scatter(x=seller_metrics['week_start'], y=seller_metrics['negative_review_rate']*100, name="Negative Review (NRR)", line=dict(color="#fbbf24", width=2)))
        
        fig_rates.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6fa'),
            xaxis=dict(showgrid=True, gridcolor='#2d3142', linecolor='#2d3142'),
            yaxis=dict(title="Defect Percentage (%)", showgrid=True, gridcolor='#2d3142', linecolor='#2d3142'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=30, b=20, l=10, r=10),
            height=350
        )
        st.plotly_chart(fig_rates, use_container_width=True)
        st.caption("📈 **Anomaly Timeline**: Use this graph to pin down the exact week an operational breakdown occurred.")

    # 3. Customer Sentiment and Search Reviews
    st.markdown('<div class="section-title">Customer Feedback Analysis</div>', unsafe_allow_html=True)
    
    rev_col1, rev_col2 = st.columns([1, 2])
    
    # Filter reviews for this seller
    seller_reviews = df_reviews[df_reviews['seller_id'] == selected_seller]
    
    with rev_col1:
        st.subheader("Sentiment Summary")
        
        # Rating distribution
        rating_counts = seller_reviews['rating'].value_counts().reindex([5, 4, 3, 2, 1], fill_value=0)
        rating_df = pd.DataFrame({"Rating": [f"⭐ {r}" for r in rating_counts.index], "Reviews": rating_counts.values})
        
        fig_ratings = px.bar(
            rating_df,
            y="Rating",
            x="Reviews",
            orientation="h",
            color="Rating",
            color_discrete_sequence=["#10b981", "#3b82f6", "#eab308", "#f97316", "#ef4444"],
            text_auto=True
        )
        fig_ratings.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6fa'),
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#2d3142'),
            yaxis=dict(showgrid=False),
            margin=dict(t=10, b=10, l=10, r=10),
            height=280
        )
        st.plotly_chart(fig_ratings, use_container_width=True)
        
        # Negative Review Key Phrases count
        st.subheader("Negative Feedback Tags")
        neg_reviews_text = " ".join(seller_reviews[seller_reviews['rating'] <= 2]['review_text'].str.lower().fillna(""))
        
        # Check frequencies of key indicator words
        tags = ["fake", "counterfeit", "late", "delayed", "damaged", "broken", "cancelled", "rotten", "spoiled", "cheap", "poor"]
        tag_counts = {t: neg_reviews_text.count(t) for t in tags if neg_reviews_text.count(t) > 0}
        
        if tag_counts:
            tag_df = pd.DataFrame({"Keyword": list(tag_counts.keys()), "Mentions": list(tag_counts.values())}).sort_values(by="Mentions", ascending=True)
            fig_tags = px.bar(tag_df, y="Keyword", x="Mentions", orientation="h", color="Mentions", color_continuous_scale="Reds")
            fig_tags.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e6e6fa'),
                showlegend=False,
                coloraxis_showscale=False,
                xaxis=dict(showgrid=True, gridcolor='#2d3142'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=220
            )
            st.plotly_chart(fig_tags, use_container_width=True)
        else:
            st.info("No negative tags found. Excellent review sentiment!")
            
    with rev_col2:
        st.subheader("Interactive Review Audit Log")
        
        # Keywords search in reviews
        search_query = st.text_input("🔍 Search reviews by keyword (e.g., 'quality', 'late', 'fake', 'cancel')", "")
        
        # Sentiment category filter
        selected_sent = st.multiselect("Filter by Sentiment", ["Positive", "Neutral", "Negative"], default=["Negative", "Neutral", "Positive"])
        
        # Apply filters
        display_reviews = seller_reviews[seller_reviews['sentiment_category'].isin(selected_sent)]
        if search_query:
            display_reviews = display_reviews[display_reviews['review_text'].str.contains(search_query, case=False, na=False)]
            
        display_reviews = display_reviews.sort_values(by="review_date", ascending=False).head(50)
        
        # Format table beautifully
        if not display_reviews.empty:
            formatted_df = display_reviews[['review_date', 'rating', 'review_text', 'sentiment_category', 'sentiment_score']].copy()
            formatted_df['review_date'] = formatted_df['review_date'].dt.strftime('%Y-%m-%d')
            
            # Map emoji to rating
            formatted_df['rating'] = formatted_df['rating'].apply(lambda x: "⭐" * x)
            
            st.dataframe(
                formatted_df,
                column_config={
                    "review_date": "Date",
                    "rating": "Stars",
                    "review_text": st.column_config.TextColumn("Review Comment", width="medium"),
                    "sentiment_category": "Sentiment Tier",
                    "sentiment_score": st.column_config.ProgressColumn("Sentiment Score", min_value=-1.0, max_value=1.0, format="%.2f")
                },
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Showing {len(display_reviews)} matching customer reviews.")
        else:
            st.info("No reviews match your filters.")


# ==========================================
# PAGE 3: BEHAVIORAL COHORTS & WHAT-IF SIMULATOR
# ==========================================
else:
    st.markdown('<div class="section-title">Cohort Explorer & Intervention Engine</div>', unsafe_allow_html=True)
    
    # 1. Behavioral Quadrant Scatter Plot (Cohort Analysis)
    # Aggregated averages for the latest 4 weeks to see recent seller performance
    latest_4_weeks = all_weeks[-4:]
    df_recent = df_metrics_filtered[df_metrics_filtered['week_start'].isin(latest_4_weeks)]
    
    cohort_data = df_recent.groupby(['seller_id', 'category']).agg(
        avg_trust=('trust_score', 'mean'),
        avg_lsr=('late_shipment_rate', 'mean'),
        avg_scr=('seller_cancellation_rate', 'mean'),
        avg_sfrr=('seller_fault_return_rate', 'mean'),
        avg_nrr=('negative_review_rate', 'mean'),
        total_revenue=('revenue', 'sum')
    ).reset_index()
    
    # Add status tier based on average trust score
    def get_tier(score):
        if score >= 90: return "Excellent"
        elif score >= 80: return "Good"
        elif score >= 70: return "At Risk"
        else: return "Critical Deficit"
        
    cohort_data['tier'] = cohort_data['avg_trust'].apply(get_tier)
    
    st.subheader("Operational Risk Quadrants (Recent 4-Week Average)")
    st.markdown("""
    This cohort map analyzes product quality defect rates (Return Rate) vs. fulfillment delay rates (Late Shipment Rate).
    Sellers fall into four strategic quadrants based on standard operational thresholds (LSR threshold = 4%, SFRR threshold = 2%).
    """)
    
    # Plotly Scatter Plot
    fig_quad = px.scatter(
        cohort_data,
        x="avg_lsr",
        y="avg_sfrr",
        size="total_revenue",
        color="avg_trust",
        hover_name="seller_id",
        hover_data=["category", "tier"],
        color_continuous_scale="RdYlGn",
        labels={
            "avg_lsr": "Late Shipment Rate (LSR)",
            "avg_sfrr": "Seller-Fault Return Rate (SFRR)",
            "avg_trust": "CTI Score"
        }
    )
    
    # Formatting X and Y as percentages
    fig_quad.update_layout(xaxis_tickformat='.1%', yaxis_tickformat='.1%')
    
    # Add vertical and horizontal lines representing operational thresholds
    fig_quad.add_shape(type="line", x0=0.04, y0=0, x1=0.04, y1=max(cohort_data['avg_sfrr'])*1.1, line=dict(color="rgba(255,255,255,0.5)", width=2, dash="dash"))
    fig_quad.add_shape(type="line", x0=0, y0=0.02, x1=max(cohort_data['avg_lsr'])*1.1, y1=0.02, line=dict(color="rgba(255,255,255,0.5)", width=2, dash="dash"))
    
    # Add annotations for quadrants
    fig_quad.add_annotation(x=0.01, y=max(cohort_data['avg_sfrr'])*0.95, text="<b>Fast Shippers / Low Quality</b><br>(High Returns)", showarrow=False, font=dict(color="#f3f4f6", size=10), bgcolor="rgba(15,17,26,0.8)", bordercolor="#f97316")
    fig_quad.add_annotation(x=0.01, y=0.005, text="<b>High Performers</b><br>(High Trust Core)", showarrow=False, font=dict(color="#f3f4f6", size=10), bgcolor="rgba(15,17,26,0.8)", bordercolor="#10b981")
    fig_quad.add_annotation(x=max(cohort_data['avg_lsr'])*0.9, y=max(cohort_data['avg_sfrr'])*0.95, text="<b>Severe Operational Risk</b><br>(High Returns & Delays)", showarrow=False, font=dict(color="#f3f4f6", size=10), bgcolor="rgba(15,17,26,0.8)", bordercolor="#ef4444")
    fig_quad.add_annotation(x=max(cohort_data['avg_lsr'])*0.9, y=0.005, text="<b>Slow Shippers / High Quality</b><br>(Fulfillment Bottlenecks)", showarrow=False, font=dict(color="#f3f4f6", size=10), bgcolor="rgba(15,17,26,0.8)", bordercolor="#f59e0b")
    
    fig_quad.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e6e6fa'),
        xaxis=dict(showgrid=True, gridcolor='#2d3142', linecolor='#2d3142'),
        yaxis=dict(showgrid=True, gridcolor='#2d3142', linecolor='#2d3142'),
        margin=dict(t=10, b=10, l=10, r=10),
        height=450
    )
    st.plotly_chart(fig_quad, use_container_width=True)
    
    # 2. Operational Intervention Engine
    st.markdown('<div class="section-title">Trust Action Control Center</div>', unsafe_allow_html=True)
    st.markdown("Automated operational directives for sellers whose Customer Trust index is decaying.")
    
    # Identify sellers at risk
    intervention_sellers = cohort_data[cohort_data['avg_trust'] < 80].copy()
    
    def calculate_recommendation(row):
        # Determine highest penalty driver
        lsr_p = min(25, row['avg_lsr'] * 150)
        scr_p = min(30, row['avg_scr'] * 250)
        sfrr_p = min(30, row['avg_sfrr'] * 200)
        nrr_p = min(25, row['avg_nrr'] * 150)
        
        penalties = {
            "Late Shipping Delay": lsr_p,
            "Seller Out of Stock Cancellations": scr_p,
            "Defective/Quality Returns": sfrr_p,
            "Negative Customer Sentiment": nrr_p
        }
        
        main_driver = max(penalties, key=penalties.get)
        
        if row['avg_trust'] < 70:
            severity = "🚨 CRITICAL AUDIT"
            if main_driver == "Defective/Quality Returns":
                rec = "Mandatory inventory quality checks. Temporarily restrict ASIN listing. Audit supplier source."
            elif main_driver == "Late Shipping Delay":
                rec = "Restrict merchant fulfillment capability. Enforce default warehouse dispatch logs. Force transition to marketplace shipping."
            elif main_driver == "Seller Out of Stock Cancellations":
                rec = "Inventory syncing API validation required. Suspended upload options. Enforce active reserve on payments."
            else:
                rec = "Review counterfeit reports. Suspend account pending active inspection of listings."
        else:
            severity = "⚠️ WARNING LOG"
            if main_driver == "Defective/Quality Returns":
                rec = "Send packaging standard guide. Request sizing chart review."
            elif main_driver == "Late Shipping Delay":
                rec = "Alert logistics manager. Request update on processing speed."
            elif main_driver == "Seller Out of Stock Cancellations":
                rec = "Warning on buffer stock parameters. Require daily inventory updates."
            else:
                rec = "Review review sentiment transcripts. Send buyer outreach guides."
                
        return pd.Series([main_driver, severity, rec])
        
    if not intervention_sellers.empty:
        intervention_sellers[['Primary Defect', 'Directive Severity', 'Action Directive']] = intervention_sellers.apply(calculate_recommendation, axis=1)
        
        display_int = intervention_sellers[['seller_id', 'category', 'avg_trust', 'Primary Defect', 'Directive Severity', 'Action Directive']].sort_values(by="avg_trust")
        
        st.dataframe(
            display_int,
            column_config={
                "seller_id": "Seller ID",
                "category": "Category",
                "avg_trust": st.column_config.NumberColumn("CTI Score", format="%.1f"),
                "Primary Defect": "Key Defect Driver",
                "Directive Severity": "Status Directive",
                "Action Directive": st.column_config.TextColumn("Prescribed Remedial Action", width="large")
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("🎉 All active sellers are operating within safe trust margins! No active interventions required.")
        
    # 3. What-If Trust Simulator
    st.markdown('<div class="section-title">Actionable What-If & CLV Simulator</div>', unsafe_allow_html=True)
    
    sim_col1, sim_col2 = st.columns([1, 1])
    
    with sim_col1:
        st.subheader("Scenario Parameters")
        
        # Select target seller
        sim_seller = st.selectbox("Select Seller to Model", sorted(cohort_data['seller_id'].unique()))
        seller_sim_data = cohort_data[cohort_data['seller_id'] == sim_seller].iloc[0]
        
        # Get category average price
        avg_price = 150.0 if seller_sim_data['category'] == "Electronics" else (45.0 if seller_sim_data['category'] == "Apparel" else (65.0 if seller_sim_data['category'] == "Home & Kitchen" else (20.0 if seller_sim_data['category'] == "Grocery" else 35.0)))
        
        # Current stats
        curr_lsr = seller_sim_data['avg_lsr']
        curr_scr = seller_sim_data['avg_scr']
        curr_sfrr = seller_sim_data['avg_sfrr']
        curr_nrr = seller_sim_data['avg_nrr']
        curr_trust = seller_sim_data['avg_trust']
        
        st.markdown(f"**Current CTI Score:** `{curr_trust:.1f}`")
        
        # Sliders for target behaviors
        target_lsr = st.slider("Target Late Shipment Rate (LSR)", 0.0, 0.40, float(curr_lsr), format="%.2f%%")
        target_scr = st.slider("Target Cancellation Rate (SCR)", 0.0, 0.20, float(curr_scr), format="%.2f%%")
        target_sfrr = st.slider("Target Seller-Fault Return Rate (SFRR)", 0.0, 0.20, float(curr_sfrr), format="%.2f%%")
        target_nrr = st.slider("Target Negative Review Rate (NRR)", 0.0, 0.40, float(curr_nrr), format="%.2f%%")
        
    with sim_col2:
        st.subheader("Financial and Operational Impact Projection")
        
        # Recalculate projected CTI
        target_lsr_penalty = min(25, target_lsr * 150)
        target_scr_penalty = min(30, target_scr * 250)
        target_sfrr_penalty = min(30, target_sfrr * 200)
        target_nrr_penalty = min(25, target_nrr * 150)
        
        projected_trust = 100.0 - (target_lsr_penalty + target_scr_penalty + target_sfrr_penalty + target_nrr_penalty)
        projected_trust = max(0.0, min(100.0, projected_trust))
        
        trust_diff = projected_trust - curr_trust
        
        # Business logic for CLV impact
        # Customers are 45% less likely to purchase from a seller/marketplace again after experiencing a critical delivery failure or product defect
        # Customer Lifetime Value (CLV) is estimated at $450 average across categories
        # Let's say: number of customers saved = weekly orders * trust increase (percentage improvement in safe transactions)
        # Revenue saved/gained = orders per week * (trust_diff / 100) * Repeat Purchase Probability * CLV
        
        weekly_orders = seller_sim_data['total_revenue'] / (4 * avg_price) # Estimate weekly orders
        clv = 450.0
        repeat_probability = 0.45
        
        # Calculate weekly financial loss saved
        weekly_savings = 0.0
        if trust_diff > 0:
            weekly_savings = weekly_orders * (trust_diff / 100) * repeat_probability * avg_price
            annual_impact = weekly_savings * 52
        else:
            weekly_savings = weekly_orders * (trust_diff / 100) * repeat_probability * avg_price
            annual_impact = weekly_savings * 52
            
        # Draw Gauge chart for CTI score
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = projected_trust,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Projected Trust Score (CTI)"},
            delta = {'reference': curr_trust, 'position': "top"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#6366f1"},
                'steps': [
                    {'range': [0, 70], 'color': "rgba(239, 68, 68, 0.2)"},
                    {'range': [70, 80], 'color': "rgba(245, 158, 11, 0.2)"},
                    {'range': [80, 90], 'color': "rgba(59, 130, 246, 0.2)"},
                    {'range': [90, 100], 'color': "rgba(16, 185, 129, 0.2)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': curr_trust
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e6e6fa'),
            margin=dict(t=30, b=10, l=10, r=10),
            height=260
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Financial card displaying results
        if trust_diff > 0:
            st.markdown(f"""
            <div style="background-color: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 8px; padding: 1rem; text-align: center;">
                <div style="color: #10b981; font-weight: bold; font-size: 1.1rem;">📈 Projected Customer Retention Gain</div>
                <div style="color: #ffffff; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;">+${annual_impact:,.2f} / year</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">Estimated value protected through reduced customer churn (estimated weekly saving of <b>${weekly_savings:,.2f}</b>)</div>
            </div>
            """, unsafe_allow_html=True)
        elif trust_diff < 0:
            st.markdown(f"""
            <div style="background-color: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; border-radius: 8px; padding: 1rem; text-align: center;">
                <div style="color: #ef4444; font-weight: bold; font-size: 1.1rem;">📉 Projected Customer Churn Loss</div>
                <div style="color: #ffffff; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;">-${abs(annual_impact):,.2f} / year</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">Degrading behavior projections predict active trust score erosion (estimated weekly churn impact: <b>-${abs(weekly_savings):,.2f}</b>)</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: rgba(148, 163, 184, 0.1); border: 1px solid #94a3b8; border-radius: 8px; padding: 1rem; text-align: center;">
                <div style="color: #94a3b8; font-weight: bold; font-size: 1.1rem;">⚖️ Status Quo (Baseline Model)</div>
                <div style="color: #ffffff; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;">$0.00 / year</div>
                <div style="color: #94a3b8; font-size: 0.85rem;">Adjust the behavior rates to simulate trust improvement and financial retention projections.</div>
            </div>
            """, unsafe_allow_html=True)
            
# Sidebar footer/branding
st.sidebar.markdown("---")
st.sidebar.caption("🛡️ Trust Ops Dashboard v1.0.0")
st.sidebar.caption("DataSights E-Commerce Engine")
