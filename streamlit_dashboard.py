"""
🚀 Aadhaar-Drishti: AI-Powered Demographic Insight Dashboard
A Decision Support System for Migration Tracking & Resource Allocation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="Aadhaar-Drishti | Decision Support System",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .alert-critical {
        background-color: #ffebee;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #f44336;
    }
    .alert-high {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #ff9800;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def create_sample_data():
    """Create sample data for demo purposes when actual data is not available"""
    # Sample stress data
    states = ['Uttar Pradesh', 'Maharashtra', 'Bihar', 'West Bengal', 'Madhya Pradesh', 
              'Tamil Nadu', 'Rajasthan', 'Karnataka', 'Gujarat', 'Andhra Pradesh']
    districts = ['District A', 'District B', 'District C', 'District D', 'District E']
    
    stress_data = pd.DataFrame({
        'state': np.random.choice(states, 100),
        'district': np.random.choice(districts, 100),
        'stress_index': np.random.uniform(20, 95, 100),
        'total_demographic_updates': np.random.randint(1000, 50000, 100),
        'total_enrolments': np.random.randint(5000, 100000, 100),
        'demo_age_5_17': np.random.randint(500, 20000, 100),
        'demo_age_17_': np.random.randint(500, 30000, 100),
        'recommended_capacity_increase': np.random.uniform(2, 10, 100)
    })
    stress_data['alert_level'] = pd.cut(
        stress_data['stress_index'],
        bins=[0, 25, 50, 75, 100],
        labels=['Low', 'Medium', 'High', 'Critical']
    )
    
    # Sample churn data
    churn_data = pd.DataFrame({
        'state': np.random.choice(states, 100),
        'district': np.random.choice(districts, 100),
        'churn_rate': np.random.uniform(10, 250, 100),
        'total_updates': np.random.randint(1000, 50000, 100),
        'record_count': np.random.randint(5000, 100000, 100)
    })
    churn_data['risk_level'] = pd.cut(
        churn_data['churn_rate'],
        bins=[0, 50, 100, 200, float('inf')],
        labels=['Stable', 'Moderate', 'High Activity', 'Critical']
    )
    churn_data = churn_data.set_index(['state', 'district'])
    
    # Sample seasonality data
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    seasonality_data = pd.DataFrame({
        'month_name': months,
        'total_monthly_updates': np.random.randint(50000, 200000, 12),
        'demo_age_5_17': np.random.randint(20000, 80000, 12),
        'demo_age_17_': np.random.randint(30000, 120000, 12)
    })
    
    # Sample migration data
    migration_data = pd.DataFrame({
        'state': np.random.choice(states, 50),
        'district': np.random.choice(districts, 50),
        'avg_updates_per_record': np.random.uniform(5, 25, 50)
    })
    
    # Dashboard data (combination)
    dashboard_data = stress_data.copy()
    
    return dashboard_data, churn_data, stress_data, seasonality_data, migration_data

@st.cache_data
def load_dashboard_data():
    """Load all processed analytics data"""
    import os
    
    # Check if analysis results exist
    files_exist = all([
        os.path.exists('analysis_results/dashboard_master_data.csv'),
        os.path.exists('analysis_results/churn_rate_analysis.csv'),
        os.path.exists('analysis_results/infrastructure_stress_index.csv'),
        os.path.exists('analysis_results/seasonality_analysis.csv'),
        os.path.exists('analysis_results/migration_hotspots.csv')
    ])
    
    if files_exist:
        try:
            dashboard_data = pd.read_csv('analysis_results/dashboard_master_data.csv')
            churn_data = pd.read_csv('analysis_results/churn_rate_analysis.csv')
            stress_data = pd.read_csv('analysis_results/infrastructure_stress_index.csv')
            seasonality_data = pd.read_csv('analysis_results/seasonality_analysis.csv')
            migration_data = pd.read_csv('analysis_results/migration_hotspots.csv')
            
            # Set index for churn_data if it has state and district columns
            if 'state' in churn_data.columns and 'district' in churn_data.columns:
                churn_data = churn_data.set_index(['state', 'district'])
            
            return dashboard_data, churn_data, stress_data, seasonality_data, migration_data
        except Exception as e:
            st.warning(f"⚠️ Error loading data files: {str(e)}")
            st.info("📊 Loading sample data for demonstration...")
            return create_sample_data()
    else:
        st.info("""
        📊 **Demo Mode Active**
        
        Analytics files not found. Displaying sample data for demonstration.
        
        **To use real data:**
        1. Ensure data files are in `data/` folder
        2. Run `python load_and_combine_data.py`
        3. Run `python advanced_analytics.py`
        4. Refresh this dashboard
        """)
        return create_sample_data()

# Load data
dashboard_data, churn_data, stress_data, seasonality_data, migration_data = load_dashboard_data()

# ============================================
# HEADER
# ============================================
st.markdown('<div class="main-header">🗺️ Aadhaar-Drishti: Decision Support System</div>', unsafe_allow_html=True)
st.markdown("**AI-Powered Demographic Insight & Migration Tracking System for Government Resource Allocation**")

# ============================================
# SIDEBAR CONTROLS
# ============================================
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("---")

# Tab Selection
tab_selection = st.sidebar.radio(
    "Select View:",
    ["🏠 National Overview", "📍 District Deep-Dive", "⚠️ Predictive Alerts", "📊 Analytics Reports"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**About Aadhaar-Drishti:**

This Decision Support System uses anonymized Aadhaar footprints to:
- Track migration patterns
- Predict infrastructure stress
- Optimize resource allocation
- Support policy decisions

**Powered by:** Quantum Ark Team
""")

# ============================================
# TAB 1: NATIONAL OVERVIEW
# ============================================
if tab_selection == "🏠 National Overview":
    st.header("🗺️ National Overview: Demographic Hotspots")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Districts Analyzed",
            f"{len(dashboard_data):,}",
            delta="100% Coverage"
        )
    
    with col2:
        critical_districts = len(stress_data[stress_data['alert_level'] == 'Critical'])
        st.metric(
            "Critical Alert Districts",
            critical_districts,
            delta=f"{(critical_districts/len(stress_data)*100):.1f}% of total",
            delta_color="inverse"
        )
    
    with col3:
        avg_stress = stress_data['stress_index'].mean()
        st.metric(
            "Avg Infrastructure Stress",
            f"{avg_stress:.1f}%",
            delta="Nationwide"
        )
    
    with col4:
        hotspots = len(migration_data)
        st.metric(
            "Migration Hotspots",
            hotspots,
            delta="Identified"
        )
    
    st.markdown("---")
    
    # Map View
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📍 Infrastructure Stress Map")
        
        # Prepare data for map
        map_data = stress_data.copy()
        
        # Create interactive map
        fig = px.scatter_geo(
            map_data.head(100),  # Limit for performance
            locations='state',
            locationmode='country names',
            size='stress_index',
            color='alert_level',
            hover_name='district',
            hover_data={'stress_index': ':.2f', 'total_demographic_updates': ':,'},
            color_discrete_map={
                'Low': '#4caf50',
                'Medium': '#ffeb3b',
                'High': '#ff9800',
                'Critical': '#f44336'
            },
            title="Infrastructure Stress by District",
            height=500
        )
        
        fig.update_geos(
            scope='asia',
            showcountries=True,
            countrycolor="lightgray",
            showcoastlines=True,
            projection_type='natural earth'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔥 Top 10 Stressed Districts")
        
        top_10_stressed = stress_data.nlargest(10, 'stress_index')[['state', 'district', 'stress_index', 'alert_level']]
        
        for idx, row in top_10_stressed.iterrows():
            alert_class = "alert-critical" if row['alert_level'] == 'Critical' else "alert-high"
            st.markdown(f"""
            <div class="{alert_class}">
                <strong>{row['district']}, {row['state']}</strong><br>
                Stress Index: {row['stress_index']:.1f}% | {row['alert_level']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Churn Rate Distribution
    st.markdown("---")
    st.subheader("📈 District Activity Distribution (Churn Rate)")
    
    fig = px.histogram(
        churn_data.reset_index(),
        x='churn_rate',
        nbins=50,
        color='risk_level',
        title="Distribution of District Churn Rates",
        labels={'churn_rate': 'Churn Rate (%)', 'count': 'Number of Districts'},
        color_discrete_map={
            'Stable': '#4caf50',
            'Moderate': '#ffeb3b',
            'High Activity': '#ff9800',
            'Critical': '#f44336'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 2: DISTRICT DEEP-DIVE
# ============================================
elif tab_selection == "📍 District Deep-Dive":
    st.header("📍 District-Level Analysis")
    
    # District Selection
    col1, col2 = st.columns(2)
    
    with col1:
        selected_state = st.selectbox(
            "Select State:",
            sorted(stress_data['state'].unique())
        )
    
    with col2:
        districts_in_state = stress_data[stress_data['state'] == selected_state]['district'].unique()
        selected_district = st.selectbox(
            "Select District:",
            sorted(districts_in_state)
        )
    
    # Get district data
    district_info = stress_data[
        (stress_data['state'] == selected_state) & 
        (stress_data['district'] == selected_district)
    ].iloc[0]
    
    st.markdown("---")
    
    # District Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Infrastructure Stress Index",
            f"{district_info['stress_index']:.1f}%",
            delta=district_info['alert_level']
        )
    
    with col2:
        st.metric(
            "Total Demographic Updates",
            f"{int(district_info['total_demographic_updates']):,}",
            delta="Updates"
        )
    
    with col3:
        st.metric(
            "Total Enrolments",
            f"{int(district_info['total_enrolments']):,}",
            delta="Enrolments"
        )
    
    with col4:
        st.metric(
            "Recommended Capacity ↑",
            f"{district_info['recommended_capacity_increase']:.1f}%",
            delta="Infrastructure"
        )
    
    # Detailed Analysis
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Age Group Distribution")
        
        age_data = pd.DataFrame({
            'Age Group': ['5-17 Years', '17+ Years'],
            'Count': [
                district_info['demo_age_5_17'],
                district_info['demo_age_17_']
            ]
        })
        
        fig = px.pie(
            age_data,
            values='Count',
            names='Age Group',
            title=f"Age Distribution in {selected_district}",
            color_discrete_sequence=['#667eea', '#764ba2']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Alert Status")
        
        alert_level = district_info['alert_level']
        
        if alert_level == 'Critical':
            st.error(f"""
            **🚨 CRITICAL ALERT**
            
            {selected_district} requires immediate attention:
            - Infrastructure stress: {district_info['stress_index']:.1f}%
            - Recommended action: Deploy resources immediately
            - Capacity increase needed: {district_info['recommended_capacity_increase']:.1f}%
            """)
        elif alert_level == 'High':
            st.warning(f"""
            **⚠️ HIGH PRIORITY**
            
            {selected_district} shows high stress levels:
            - Infrastructure stress: {district_info['stress_index']:.1f}%
            - Recommended action: Plan resource allocation
            - Monitor closely for escalation
            """)
        else:
            st.success(f"""
            **✅ STABLE**
            
            {selected_district} is currently stable:
            - Infrastructure stress: {district_info['stress_index']:.1f}%
            - Continue regular monitoring
            """)
    
    # Comparison with State Average
    st.markdown("---")
    st.subheader("📊 Comparison with State Average")
    
    state_avg = stress_data[stress_data['state'] == selected_state]['stress_index'].mean()
    
    comparison_data = pd.DataFrame({
        'Location': [selected_district, f'{selected_state} (Avg)'],
        'Stress Index': [district_info['stress_index'], state_avg]
    })
    
    fig = px.bar(
        comparison_data,
        x='Location',
        y='Stress Index',
        title=f"{selected_district} vs State Average",
        color='Location',
        color_discrete_sequence=['#667eea', '#764ba2']
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 3: PREDICTIVE ALERTS
# ============================================
elif tab_selection == "⚠️ Predictive Alerts":
    st.header("⚠️ Predictive Alerts & Resource Planning")
    
    # Alert Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        critical_count = len(stress_data[stress_data['alert_level'] == 'Critical'])
        st.metric("🚨 Critical Alerts", critical_count)
    
    with col2:
        high_count = len(stress_data[stress_data['alert_level'] == 'High'])
        st.metric("⚠️ High Priority", high_count)
    
    with col3:
        migration_count = len(migration_data)
        st.metric("🔥 Migration Hotspots", migration_count)
    
    st.markdown("---")
    
    # Critical Districts Table
    st.subheader("🚨 Critical Alert Districts - Immediate Action Required")
    
    critical_districts = stress_data[stress_data['alert_level'] == 'Critical'].sort_values(
        'stress_index', ascending=False
    )[['state', 'district', 'stress_index', 'recommended_capacity_increase', 'total_demographic_updates']]
    
    st.dataframe(
        critical_districts.style.background_gradient(cmap='Reds', subset=['stress_index']),
        use_container_width=True
    )
    
    # Migration Hotspots
    st.markdown("---")
    st.subheader("🔥 Migration Hotspots - Enhanced Monitoring Required")
    
    st.dataframe(
        migration_data[['state', 'district', 'avg_updates_per_record']].head(20),
        use_container_width=True
    )
    
    # Seasonality Insights
    st.markdown("---")
    st.subheader("📅 Seasonal Resource Planning")
    
    fig = px.bar(
        seasonality_data,
        x='month_name',
        y='total_monthly_updates',
        title="Monthly Update Patterns - Staff Deployment Planning",
        labels={'month_name': 'Month', 'total_monthly_updates': 'Total Updates'},
        color='total_monthly_updates',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **💡 Resource Deployment Recommendations:**
    - Deploy 30% extra Seva Kendra staff during peak months
    - Schedule maintenance during low-activity periods
    - Pre-position resources in high-stress districts before peak season
    """)

# ============================================
# TAB 4: ANALYTICS REPORTS
# ============================================
elif tab_selection == "📊 Analytics Reports":
    st.header("📊 Detailed Analytics & Insights")
    
    # Report Selection
    report_type = st.selectbox(
        "Select Report:",
        [
            "Infrastructure Stress Report",
            "Churn Rate Analysis",
            "Migration Patterns",
            "Seasonality Analysis",
            "State-wise Comparison"
        ]
    )
    
    if report_type == "Infrastructure Stress Report":
        st.subheader("🏗️ Infrastructure Stress Analysis")
        
        # Distribution by alert level
        alert_dist = stress_data['alert_level'].value_counts()
        
        fig = px.pie(
            values=alert_dist.values,
            names=alert_dist.index,
            title="Infrastructure Stress Distribution",
            color=alert_dist.index,
            color_discrete_map={
                'Low': '#4caf50',
                'Medium': '#ffeb3b',
                'High': '#ff9800',
                'Critical': '#f44336'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(stress_data, use_container_width=True)
    
    elif report_type == "Churn Rate Analysis":
        st.subheader("📈 Churn Rate Analysis")
        
        fig = px.scatter(
            churn_data.reset_index(),
            x='total_updates',
            y='churn_rate',
            color='risk_level',
            size='record_count',
            hover_data=['state', 'district'],
            title="Churn Rate vs Total Updates",
            labels={'total_updates': 'Total Updates', 'churn_rate': 'Churn Rate (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif report_type == "State-wise Comparison":
        st.subheader("🗺️ State-wise Comparison")
        
        state_summary = stress_data.groupby('state').agg({
            'stress_index': 'mean',
            'total_demographic_updates': 'sum',
            'total_enrolments': 'sum'
        }).reset_index().sort_values('stress_index', ascending=False)
        
        fig = px.bar(
            state_summary.head(20),
            x='state',
            y='stress_index',
            title="Top 20 States by Average Stress Index",
            labels={'state': 'State', 'stress_index': 'Avg Stress Index'}
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p><strong>Aadhaar-Drishti v1.0</strong> | Developed by Team Quantum Ark | Powered by Streamlit & Python</p>
    <p>A Decision Support System for Government Resource Allocation & Policy Planning</p>
</div>
""", unsafe_allow_html=True)
