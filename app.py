import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO
import base64
import numpy as np
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Telangana Minorities Residential Educational Institutions Society",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for Professional UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    .kpi-container {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    .kpi-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: none;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .kpi-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .kpi-box:hover::before {
        left: 100%;
    }
    
    .kpi-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .kpi-value {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: white;
        margin: 0.5rem 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .kpi-label {
        font-size: 0.9rem !important;
        font-weight: 500;
        color: rgba(255,255,255,0.9);
        margin: 0;
    }
    
    .chart-container {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    .chart-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e3c72;
        margin-bottom: 1rem;
        text-align: center;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    .stSelectbox, .stRadio, .stMultiselect {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        color: #1a1a1a;
    }
    
    .stSelectbox label, .stRadio label, .stMultiselect label {
        color: #1a1a1a !important;
        font-weight: 600;
    }
    
    .stSelectbox .stSelectbox > div > div {
        color: #1a1a1a;
    }
    
    .stRadio > div > div > label {
        color: #1a1a1a !important;
    }
    
    .stMultiselect > div > div > div {
        color: #1a1a1a;
    }
    
    /* Sidebar Background Color */
    .css-1d391kg {
        background-color: #1E3C78 !important;
    }
    
    /* Sidebar Container */
    .css-1lcbmhc {
        background-color: #1E3C78 !important;
    }
    
    /* Sidebar Content */
    .css-17eq0hr {
        background-color: #1E3C78 !important;
    }
    
    /* Sidebar Widgets */
    .stSelectbox, .stRadio, .stMultiselect, .stSlider {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 10px !important;
        margin: 5px 0 !important;
    }
    
    /* Sidebar Labels - White text for better contrast */
    .stSelectbox label, .stRadio label, .stMultiselect label, .stSlider label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar Text */
    .stSelectbox .stSelectbox > div > div {
        color: white !important;
    }
    .stRadio > div > div > label {
        color: white !important;
    }
    .stMultiselect > div > div > div {
        color: white !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .dataframe {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
    }
    
    .filter-section {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .filter-title {
        color: white;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with enhanced styling
st.markdown("""
<div class="main-header">
    <h1>🎓 Telangana Minorities Residential Educational Institutions Society</h1>
    <p>Comprehensive Analytics Dashboard for Educational Excellence</p>
</div>
""", unsafe_allow_html=True)

# DATA UPLOAD SECTION
# ✅ SELECT FILE FROM SERVER DIRECTORY INSTEAD OF UPLOAD
FILE_DIR = "data_files"  # Folder on server containing files

if not os.path.exists(FILE_DIR):
    os.makedirs(FILE_DIR)
    st.warning(f"⚠️ Directory '{FILE_DIR}' created. Please place your files in it.")
else:
    available_files = [f for f in os.listdir(FILE_DIR) if f.endswith((".csv", ".xlsx"))]

    if available_files:
        selected_file = st.selectbox("📂 Select a file", available_files)
        file_path = os.path.join(FILE_DIR, selected_file)

        # Read selected file
        if selected_file.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        st.success(f"✅ Loaded: {selected_file}")

    else:
        st.error("❌ No CSV or Excel files found in the 'data_files' folder.")

    # Save to session state
    st.session_state["uploaded_df"] = df
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.fillna(0, inplace=True)
    
    # DYNAMIC COLUMN DETECTION
    def find_column(keyword):
        for col in df.columns:
            if keyword in col:
                return col
        return None
    
    columns = {
        "v_minority": {
            "sanctioned": find_column("vth_class_minority_sanction"),
            "admitted": find_column("vth_class_minority_admitted"),
            "vacancy": find_column("vth_class_minority_vacancies"),
            "attendance": find_column("total_school_attendance"),
        },
        "v_non_minority": {
            "sanctioned": find_column("vth_class_non_minority_sanction"),
            "admitted": find_column("vth_class_non_minority_admitted"),
            "vacancy": find_column("vth_class_non_minority_vacancies"),
            "attendance": find_column("total_school_attendance"),
        },
        "inter_minority": {
            "sanctioned": find_column("1st_year_minority_sanction"),
            "admitted": find_column("1st_year_minority_admitted"),
            "vacancy": find_column("1st_year_minority_vacancies"),
            "attendance": find_column("total_intermediate_attendance"),
        },
        "inter_non_minority": {
            "sanctioned": find_column("1st_year_non_minority_sanction"),
            "admitted": find_column("1st_year_non_minority_admitted"),
            "vacancy": find_column("1st_year_non_minority_vacancies"),
            "attendance": find_column("total_intermediate_attendance"),
        },
        "absentees": find_column("total_absentees"),
    }
    
    # ENHANCED SIDEBAR FILTERS
    st.sidebar.markdown("""
    <div class="filter-section">
        <div class="filter-title">🎛️ Dashboard Controls</div>
    </div>
    """, unsafe_allow_html=True)
    
    level_filter = st.sidebar.radio(
        "📚 Select Level", 
        ["V (School)", "Inter 1st Year", "Both"],
        help="Choose the educational level to analyze. Select 'Both' to include both levels."
    )
    
    category_filter = st.sidebar.radio(
        "👥 Select Category", 
        ["Minority", "Non-Minority"],
        help="Choose the student category to analyze"
    )
    
    # Enhanced District Filter with Select All option
    all_districts = sorted(df["district"].unique())
    
    # Add "Select All" option to the beginning
    district_options = ["Select All"] + all_districts
    
    selected_districts = st.sidebar.multiselect(
        "🗺️ Select District(s)", 
        options=district_options,
        default=["Select All"],
        help="Select districts to include in analysis. Choose 'Select All' to include all districts."
    )
    
    # Handle "Select All" logic
    if "Select All" in selected_districts:
        districts = all_districts
    else:
        districts = selected_districts
    
    search_college = st.sidebar.text_input(
        "🔍 Search College Name (Optional)",
        help="Filter by specific college names"
    )
    
    # Enhanced filter for top N values
    st.sidebar.markdown("""
    <div class="filter-section">
        <div class="filter-title">📊 Chart Controls</div>
    </div>
    """, unsafe_allow_html=True)
    
    top_n_filter = st.sidebar.slider(
        "📈 Show Top N Results", 
        min_value=3, 
        max_value=20, 
        value=10,
        help="Control how many top results to show in charts"
    )
    
    # Apply filters
    df = df[df["district"].isin(districts)]
    if search_college:
        df = df[df["college_name"].str.contains(search_college, case=False, na=False)]
    
    # Map columns dynamically
    if level_filter == "V (School)":
        key = "v_minority" if category_filter == "Minority" else "v_non_minority"
        sanctioned_col = columns[key]["sanctioned"]
        admitted_col = columns[key]["admitted"]
        vacant_col = columns[key]["vacancy"]
        attendance_col = columns[key]["attendance"]
        absentees_col = columns["absentees"]
    elif level_filter == "Inter 1st Year":
        key = "inter_minority" if category_filter == "Minority" else "inter_non_minority"
        sanctioned_col = columns[key]["sanctioned"]
        admitted_col = columns[key]["admitted"]
        vacant_col = columns[key]["vacancy"]
        attendance_col = columns[key]["attendance"]
        absentees_col = columns["absentees"]
    else:  # Both levels
        # For "Both" option, we'll use V (School) columns as primary and add Inter data
        v_key = "v_minority" if category_filter == "Minority" else "v_non_minority"
        inter_key = "inter_minority" if category_filter == "Minority" else "inter_non_minority"
        
        # Use V (School) columns as base
        sanctioned_col = columns[v_key]["sanctioned"]
        admitted_col = columns[v_key]["admitted"]
        vacant_col = columns[v_key]["vacancy"]
        attendance_col = columns[v_key]["attendance"]
        absentees_col = columns["absentees"]
        
        # Add Inter columns for combined analysis
        inter_sanctioned_col = columns[inter_key]["sanctioned"]
        inter_admitted_col = columns[inter_key]["admitted"]
        inter_vacant_col = columns[inter_key]["vacancy"]
        inter_attendance_col = columns[inter_key]["attendance"]
    
    # KPI CALCULATIONS
    if level_filter == "Both":
        # Combine data from both V (School) and Inter levels
        total_sanctioned = df[sanctioned_col].sum() + df[inter_sanctioned_col].sum()
        total_admitted = df[admitted_col].sum() + df[inter_admitted_col].sum()
        total_vacant = df[vacant_col].sum() + df[inter_vacant_col].sum()
        total_attendance = df[attendance_col].sum() + df[inter_attendance_col].sum()
        total_absentees = df[absentees_col].sum()
        attendance_pct = round((total_attendance / (total_attendance + total_absentees)) * 100, 2) if (total_attendance + total_absentees) > 0 else 0
    else:
        # Single level calculations
        total_sanctioned = df[sanctioned_col].sum()
        total_admitted = df[admitted_col].sum()
        total_vacant = df[vacant_col].sum()
        total_attendance = df[attendance_col].sum()
        total_absentees = df[absentees_col].sum()
        attendance_pct = round((total_attendance / (total_attendance + total_absentees)) * 100, 2) if (total_attendance + total_absentees) > 0 else 0
    
    # ENHANCED KPI DISPLAY
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    col1.markdown(f"""
    <div class="kpi-box">
        <span class="kpi-icon">🏫</span>
        <div class="kpi-value">{total_sanctioned:,}</div>
        <div class="kpi-label">Total Sanctioned</div>
    </div>
    """, unsafe_allow_html=True)
    
    col2.markdown(f"""
    <div class="kpi-box">
        <span class="kpi-icon">🎓</span>
        <div class="kpi-value">{total_admitted:,}</div>
        <div class="kpi-label">Total Admitted</div>
    </div>
    """, unsafe_allow_html=True)
    
    col3.markdown(f"""
    <div class="kpi-box">
        <span class="kpi-icon">📌</span>
        <div class="kpi-value">{total_vacant:,}</div>
        <div class="kpi-label">Total Vacant</div>
    </div>
    """, unsafe_allow_html=True)
    
    col4.markdown(f"""
    <div class="kpi-box">
        <span class="kpi-icon">✅</span>
        <div class="kpi-value">{total_attendance:,}</div>
        <div class="kpi-label">Total Attendance</div>
    </div>
    """, unsafe_allow_html=True)
    
    col5.markdown(f"""
    <div class="kpi-box">
        <span class="kpi-icon">❌</span>
        <div class="kpi-value">{total_absentees:,}</div>
        <div class="kpi-label">Total Absentees</div>
    </div>
    """, unsafe_allow_html=True)
    
    col6.markdown(f"""
    <div class="kpi-box">
        <span class="kpi-icon">📈</span>
        <div class="kpi-value">{attendance_pct}%</div>
        <div class="kpi-label">Attendance %</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # CALCULATE METRICS
    if level_filter == "Both":
        # For "Both" option, calculate combined metrics
        df["admission_rate"] = ((df[admitted_col] + df[inter_admitted_col]) / (df[sanctioned_col] + df[inter_sanctioned_col])) * 100
        df["vacancy_rate"] = ((df[vacant_col] + df[inter_vacant_col]) / (df[sanctioned_col] + df[inter_sanctioned_col])) * 100
        df["attendance_%"] = ((df[attendance_col] + df[inter_attendance_col]) / ((df[attendance_col] + df[inter_attendance_col]) + df[absentees_col])) * 100
    else:
        # Single level metrics
        df["admission_rate"] = (df[admitted_col] / df[sanctioned_col]) * 100
        df["vacancy_rate"] = (df[vacant_col] / df[sanctioned_col]) * 100
        df["attendance_%"] = (df[attendance_col] / (df[attendance_col] + df[absentees_col])) * 100
    
    # Clean data
    df_clean = df[df["admission_rate"].notna() & np.isfinite(df["admission_rate"])]
    
    # ENHANCED VISUALIZATIONS
    
    # 1. Enhanced Grouped Bar Chart for Admission vs Vacancy Analysis
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">🎯 Top {top_n_filter} Districts - Admission vs Vacancy Analysis</div>', unsafe_allow_html=True)
    
    # Get top N districts by total sanctioned seats
    district_analysis_data = df.groupby("district").agg({
        "admission_rate": 'mean',
        "vacancy_rate": 'mean',
        sanctioned_col: 'sum'
    }).reset_index()
    
    district_analysis_data = district_analysis_data.nlargest(top_n_filter, sanctioned_col)
    district_analysis_data = district_analysis_data.sort_values(sanctioned_col, ascending=True)
    
    # Create grouped bar chart
    fig_grouped_bars = go.Figure()
    
    # Add Admission Rate bars
    fig_grouped_bars.add_trace(go.Bar(
        x=district_analysis_data['district'],
        y=district_analysis_data['admission_rate'],
        name='Admission Rate',
        marker_color='#2E8B57',
        text=district_analysis_data['admission_rate'].round(1).astype(str) + '%',
        textposition='outside',
        textfont=dict(color='#1a1a1a', size=11),
        hovertemplate='<b>%{x}</b><br>' +
                     'Admission Rate: %{y:.1f}%<br>' +
                     '<extra></extra>'
    ))
    
    # Add Vacancy Rate bars
    fig_grouped_bars.add_trace(go.Bar(
        x=district_analysis_data['district'],
        y=district_analysis_data['vacancy_rate'],
        name='Vacancy Rate',
        marker_color='#DC143C',
        text=district_analysis_data['vacancy_rate'].round(1).astype(str) + '%',
        textposition='outside',
        textfont=dict(color='#1a1a1a', size=11),
        hovertemplate='<b>%{x}</b><br>' +
                     'Vacancy Rate: %{y:.1f}%<br>' +
                     '<extra></extra>'
    ))
    
    fig_grouped_bars.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color='#1a1a1a'),
        xaxis=dict(
            title=dict(text="District", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12),
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(text="Rate (%)", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12)
        ),
        height=500,
        legend=dict(
            font=dict(color='#1a1a1a', size=12),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#1a1a1a',
            borderwidth=1
        ),
        title=dict(
            text="Admission Rate vs Vacancy Rate by District",
            font=dict(color='#1a1a1a', size=16)
        )
    )
    
    st.plotly_chart(fig_grouped_bars, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Enhanced Stacked Bar Chart for Attendance Impact Analysis
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">📊 Top {top_n_filter} Districts - Attendance Impact Analysis</div>', unsafe_allow_html=True)
    
    # Create data for stacked bar chart
    if level_filter == "Both":
        attendance_impact_data = df.groupby("district").agg({
            attendance_col: 'sum',
            inter_attendance_col: 'sum',
            absentees_col: 'sum',
            "vacancy_rate": 'mean'
        }).reset_index()
        
        # Combine attendance from both levels
        attendance_impact_data['total_attendance'] = attendance_impact_data[attendance_col] + attendance_impact_data[inter_attendance_col]
        
        # Apply Top N filter - sort by total students (attendance + absentees) and take top N
        attendance_impact_data['total_students'] = attendance_impact_data['total_attendance'] + attendance_impact_data[absentees_col]
        attendance_impact_data = attendance_impact_data.nlargest(top_n_filter, 'total_students')
    else:
        attendance_impact_data = df.groupby("district").agg({
            attendance_col: 'sum',
            absentees_col: 'sum',
            "vacancy_rate": 'mean'
        }).reset_index()
        
        # Apply Top N filter - sort by total students (attendance + absentees) and take top N
        attendance_impact_data['total_students'] = attendance_impact_data[attendance_col] + attendance_impact_data[absentees_col]
        attendance_impact_data = attendance_impact_data.nlargest(top_n_filter, 'total_students')
    
    # Create stacked bar chart
    fig_stacked_attendance = go.Figure()
    
    # Add attendance bars
    if level_filter == "Both":
        fig_stacked_attendance.add_trace(go.Bar(
            x=attendance_impact_data['district'],
            y=attendance_impact_data['total_attendance'],
            name='Total Attendance (V + Inter)',
            marker_color='#2E8B57',
            text=attendance_impact_data['total_attendance'].round(0),
            textposition='auto',
        ))
    else:
        fig_stacked_attendance.add_trace(go.Bar(
            x=attendance_impact_data['district'],
            y=attendance_impact_data[attendance_col],
            name='Attendance',
            marker_color='#2E8B57',
            text=attendance_impact_data[attendance_col].round(0),
            textposition='auto',
        ))
    
    # Add absentees bars
    fig_stacked_attendance.add_trace(go.Bar(
        x=attendance_impact_data['district'],
        y=attendance_impact_data[absentees_col],
        name='Absentees',
        marker_color='#DC143C',
        text=attendance_impact_data[absentees_col].round(0),
        textposition='auto',
    ))
    
    fig_stacked_attendance.update_layout(
        barmode='stack',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color='#1a1a1a'),
        xaxis=dict(
            title=dict(text="District", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12),
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(text="Number of Students", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12)
        ),
        height=500,
        legend=dict(
            font=dict(color='#1a1a1a', size=12),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#1a1a1a',
            borderwidth=1
        ),
        title=dict(
            text="Attendance vs Absentees by District",
            font=dict(color='#1a1a1a', size=16)
        )
    )
    
    st.plotly_chart(fig_stacked_attendance, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Enhanced Bar Chart with Top N Filter
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">📋 Top {top_n_filter} Districts by Absenteeism</div>', unsafe_allow_html=True)
    
    absentee_summary = df.groupby("district")[absentees_col].sum().reset_index().sort_values(absentees_col, ascending=False).head(top_n_filter)
    
    fig_bar = px.bar(
        absentee_summary, 
        x="district", 
        y=absentees_col,
        color=absentees_col,
        color_continuous_scale="reds",
        title=""
    )
    
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color='#1a1a1a'),
        xaxis=dict(
            title=dict(text="District", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12),
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(text="Total Absentees", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12)
        ),
        height=500
    )
    
    fig_bar.update_traces(
        marker_line_color='white',
        marker_line_width=1,
        text=absentee_summary[absentees_col].round(0).astype(str),
        textposition='outside',
        textfont=dict(color='#1a1a1a', size=11)
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 4. Enhanced Lollipop Chart for Vacancy Rate Distribution
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">🍭 Top {top_n_filter} Districts - Vacancy Rate Distribution</div>', unsafe_allow_html=True)
    
    # Get top N districts by average vacancy rate
    vacancy_summary = df.groupby("district")["vacancy_rate"].mean().nlargest(top_n_filter).reset_index()
    vacancy_summary = vacancy_summary.sort_values("vacancy_rate", ascending=True)  # Sort for better visualization
    
    # Create lollipop chart
    fig_lollipop = go.Figure()
    
    # Add lollipop stems (vertical lines)
    fig_lollipop.add_trace(go.Scatter(
        x=vacancy_summary['vacancy_rate'],
        y=vacancy_summary['district'],
        mode='lines',
        line=dict(color='#667eea', width=3),
        name='Vacancy Rate',
        showlegend=False
    ))
    
    # Add lollipop heads (circles)
    fig_lollipop.add_trace(go.Scatter(
        x=vacancy_summary['vacancy_rate'],
        y=vacancy_summary['district'],
        mode='markers',
        marker=dict(
            size=15,
            color=vacancy_summary['vacancy_rate'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(
                title=dict(text="Vacancy Rate (%)", font=dict(color='#1a1a1a')),
                tickfont=dict(color='#1a1a1a')
            )
        ),
        text=vacancy_summary['vacancy_rate'].round(1).astype(str) + '%',
        textposition='middle right',
        textfont=dict(color='#1a1a1a', size=12),
        name='Districts',
        showlegend=False
    ))
    
    fig_lollipop.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color='#1a1a1a'),
        xaxis=dict(
            title=dict(text="Vacancy Rate (%)", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12),
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="District", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        height=500,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig_lollipop, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 5. Enhanced Stacked Bar Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">📊 Top {top_n_filter} Districts - Sanctioned vs Admitted Seats Comparison</div>', unsafe_allow_html=True)
    
    # Get top N districts by total sanctioned seats
    if level_filter == "Both":
        # Combine sanctioned seats from both levels for ranking
        df['total_sanctioned'] = df[sanctioned_col] + df[inter_sanctioned_col]
        top_districts_seats = df.groupby("district")['total_sanctioned'].sum().nlargest(top_n_filter).index.tolist()
        df_filtered_seats = df[df["district"].isin(top_districts_seats)]
        
        # Create combined data for both levels
        stacked = df_filtered_seats.groupby("district").agg({
            sanctioned_col: 'sum',
            admitted_col: 'sum',
            inter_sanctioned_col: 'sum',
            inter_admitted_col: 'sum'
        }).reset_index()
        
        # Rename columns for clarity
        stacked.columns = ['district', 'V_Sanctioned', 'V_Admitted', 'Inter_Sanctioned', 'Inter_Admitted']
        
        # Melt the data for plotting
        stacked = stacked.melt(id_vars="district", 
                             value_vars=['V_Sanctioned', 'V_Admitted', 'Inter_Sanctioned', 'Inter_Admitted'], 
                             var_name="Type", value_name="Seats")
    else:
        top_districts_seats = df.groupby("district")[sanctioned_col].sum().nlargest(top_n_filter).index.tolist()
        df_filtered_seats = df[df["district"].isin(top_districts_seats)]
        
        stacked = df_filtered_seats.groupby("district")[[sanctioned_col, admitted_col]].sum().reset_index()
        stacked = stacked.melt(id_vars="district", value_vars=[sanctioned_col, admitted_col], var_name="Type", value_name="Seats")
    
    fig_stacked = px.bar(
        stacked, 
        x="district", 
        y="Seats", 
        color="Type",
        barmode='group',
        title="",
        color_discrete_map={sanctioned_col: '#667eea', admitted_col: '#764ba2'}
    )
    
    fig_stacked.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color='#1a1a1a'),
        xaxis=dict(
            title=dict(text="District", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12),
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(text="Number of Seats", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12)
        ),
        height=500,
        legend=dict(
            font=dict(color='#1a1a1a', size=12),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#1a1a1a',
            borderwidth=1
        )
    )
    
    fig_stacked.update_traces(
        text=stacked['Seats'].round(0).astype(str),
        textposition='outside',
        textfont=dict(color='#1a1a1a', size=11)
    )
    
    st.plotly_chart(fig_stacked, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 6. Enhanced Performance Comparison
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">🏆 Top & Bottom {top_n_filter//2} Institutes Performance</div>', unsafe_allow_html=True)
    
    top_institutes = df.nlargest(top_n_filter//2, "attendance_%")[["college_name", "attendance_%", "district"]]
    bottom_institutes = df.nsmallest(top_n_filter//2, "attendance_%")[["college_name", "attendance_%", "district"]]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🏅 Top Performing Institutes")
        fig_top = px.bar(
            top_institutes, 
            x="attendance_%", 
            y="college_name",
            orientation='h',
            color="attendance_%",
            color_continuous_scale="greens",
            title=""
        )
        fig_top.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=10, color='#1a1a1a'),
            xaxis=dict(
                title=dict(text="Attendance %", font=dict(color='#1a1a1a', size=12)),
                tickfont=dict(color='#1a1a1a', size=10)
            ),
            yaxis=dict(
                title="",
                tickfont=dict(color='#1a1a1a', size=10)
            ),
            height=400,
            showlegend=False
        )
        
        fig_top.update_traces(
            text=top_institutes['attendance_%'].round(1).astype(str) + '%',
            textposition='inside',
            textfont=dict(color='#1a1a1a', size=10)
        )
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.markdown("##### ⚠️ Institutes Needing Attention")
        fig_bottom = px.bar(
            bottom_institutes, 
            x="attendance_%", 
            y="college_name",
            orientation='h',
            color="attendance_%",
            color_continuous_scale="reds",
            title=""
        )
        fig_bottom.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=10, color='#1a1a1a'),
            xaxis=dict(
                title=dict(text="Attendance %", font=dict(color='#1a1a1a', size=12)),
                tickfont=dict(color='#1a1a1a', size=10)
            ),
            yaxis=dict(
                title="",
                tickfont=dict(color='#1a1a1a', size=10)
            ),
            height=400,
            showlegend=False
        )
        
        fig_bottom.update_traces(
            text=bottom_institutes['attendance_%'].round(1).astype(str) + '%',
            textposition='inside',
            textfont=dict(color='#1a1a1a', size=10)
        )
        st.plotly_chart(fig_bottom, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 7. Enhanced District Drill-down
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🔍 District-wise Detailed Analysis</div>', unsafe_allow_html=True)
    
    selected_district = st.selectbox(
        "Select District for Detailed View", 
        df["district"].unique(),
        help="Choose a district to see detailed institute information"
    )
    
    drill_df = df[df["district"] == selected_district][
        ["college_name", sanctioned_col, admitted_col, vacant_col, attendance_col, absentees_col, "attendance_%"]
    ].round(2)
    
    # Rename columns for better display
    drill_df.columns = [
        "College Name", "Sanctioned", "Admitted", "Vacant", 
        "Attendance", "Absentees", "Attendance %"
    ]
    
    st.dataframe(
        drill_df,
        use_container_width=True,
        height=400
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 8. Enhanced College Vacancy Rate Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">🏫 Top {top_n_filter} Colleges - Vacancy Rate Analysis</div>', unsafe_allow_html=True)
    
    # Get top N colleges by vacancy rate
    college_vacancy_data = df.nlargest(top_n_filter, "vacancy_rate")[["college_name", "vacancy_rate", "district"]].copy()
    college_vacancy_data = college_vacancy_data.sort_values("vacancy_rate", ascending=True)  # Sort for better visualization
    
    # Create horizontal bar chart for college vacancy rates
    fig_college_vacancy = go.Figure()
    
    fig_college_vacancy.add_trace(go.Bar(
        x=college_vacancy_data['vacancy_rate'],
        y=college_vacancy_data['college_name'],
        orientation='h',
        marker=dict(
            color=college_vacancy_data['vacancy_rate'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(
                title=dict(text="Vacancy Rate (%)", font=dict(color='#1a1a1a')),
                tickfont=dict(color='#1a1a1a')
            )
        ),
        text=college_vacancy_data['vacancy_rate'].round(1).astype(str) + '%',
        textposition='auto',
        textfont=dict(color='#1a1a1a', size=11),
        hovertemplate='<b>%{y}</b><br>' +
                     'Vacancy Rate: %{x:.1f}%<br>' +
                     'District: %{customdata}<br>' +
                     '<extra></extra>',
        customdata=college_vacancy_data['district']
    ))
    
    fig_college_vacancy.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color='#1a1a1a'),
        xaxis=dict(
            title=dict(text="Vacancy Rate (%)", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=12),
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="College Name", font=dict(color='#1a1a1a', size=14)),
            tickfont=dict(color='#1a1a1a', size=11),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        height=500,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig_college_vacancy, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 9. Enhanced Summary Statistics
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Summary Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df['admission_rate'].mean():.1f}%</div>
            <div class="metric-label">Avg Admission Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df['vacancy_rate'].mean():.1f}%</div>
            <div class="metric-label">Avg Vacancy Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df['attendance_%'].mean():.1f}%</div>
            <div class="metric-label">Avg Attendance %</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df)}</div>
            <div class="metric-label">Total Institutes</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ENHANCED DOWNLOAD SECTION
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">💾 Export Data</div>', unsafe_allow_html=True)
    
    def download_excel(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            # Main data
            dataframe.to_excel(writer, index=False, sheet_name="Main_Data")
            
            # Summary statistics
            summary_stats = pd.DataFrame({
                'Metric': ['Total Sanctioned', 'Total Admitted', 'Total Vacant', 'Total Attendance', 'Total Absentees', 'Attendance %'],
                'Value': [total_sanctioned, total_admitted, total_vacant, total_attendance, total_absentees, f"{attendance_pct}%"]
            })
            summary_stats.to_excel(writer, index=False, sheet_name="Summary_Stats")
            
            # District-wise summary
            district_summary = df.groupby("district").agg({
                sanctioned_col: 'sum',
                admitted_col: 'sum',
                vacant_col: 'sum',
                attendance_col: 'sum',
                absentees_col: 'sum'
            }).round(2)
            district_summary.to_excel(writer, sheet_name="District_Summary")
            
            # Top and bottom performers
            top_performers = df.nlargest(10, "attendance_%")[["college_name", "district", "attendance_%"]]
            bottom_performers = df.nsmallest(10, "attendance_%")[["college_name", "district", "attendance_%"]]
            
            top_performers.to_excel(writer, index=False, sheet_name="Top_Performers")
            bottom_performers.to_excel(writer, index=False, sheet_name="Bottom_Performers")
        
        return output.getvalue()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            "📥 Download Complete Excel Report",
            data=download_excel(df),
            file_name=f"education_dashboard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col2:
        st.download_button(
            "📊 Download CSV Data",
            data=df.to_csv(index=False),
            file_name=f"education_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

#else:
#    # Enhanced welcome message
#    st.markdown("""
#    <div class="chart-container">
#        <div style="text-align: center; padding: 3rem;">
#            <h2 style="color: #1e3c72; margin-bottom: 1rem;">📊 Welcome to the Educational Analytics Dashboard</h2>
#            <p style="color: #666; font-size: 1.1rem; margin-bottom: 2rem;">
#                Upload your dataset to begin analyzing educational institution performance metrics.
#            </p>
#            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white;">
#                <h3>📋 Supported Features:</h3>
#                <ul style="text-align: left; list-style: none; padding: 0;">
#                    <li>✅ Interactive KPI Dashboard</li>
#                    <li>📈 Advanced Visualizations</li>
#                    <li>🔍 Dynamic Filtering</li>
#                    <li>📊 Performance Comparisons</li>
#                    <li>💾 Data Export Options</li>
#                </ul>
#            </div>
#        </div>
#   </div>
#   """, unsafe_allow_html=True#
