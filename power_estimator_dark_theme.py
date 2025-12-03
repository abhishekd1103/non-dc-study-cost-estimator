import streamlit as st
import pandas as pd
import json
from datetime import datetime
import math

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Power Systems Cost Estimator v3.5",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ DARK THEME PREMIUM CSS DESIGN SYSTEM ============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

:root {
    /* Dark Theme Colors */
    --bg-primary: #0f1419;
    --bg-secondary: #1a2332;
    --bg-tertiary: #252d3d;
    --bg-hover: #2a3549;
    
    /* Primary Colors */
    --primary: #2563eb;
    --primary-dark: #1e40af;
    --primary-light: #3b82f6;
    
    /* Text Colors */
    --text-primary: #e8eef5;
    --text-secondary: #a8b5c7;
    --text-tertiary: #7a8696;
    
    /* Borders & Accents */
    --border: #3a4556;
    --border-light: #2a3549;
    
    /* Semantic Colors */
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --info: #06b6d4;
    
    /* Spacing */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;
    
    /* Radius */
    --radius-sm: 6px;
    --radius-md: 8px;
    --radius-lg: 12px;
    
    /* Shadows */
    --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.4);
    --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.5);
    --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.6);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-primary) !important;
    color: var(--text-primary);
    font-size: 14px;
    line-height: 1.6;
}

/* Main Container */
.main {
    background: var(--bg-primary) !important;
    padding-top: 0 !important;
}

[data-testid="stMainBlockContainer"] {
    padding-top: var(--space-lg) !important;
    background: var(--bg-primary) !important;
}

/* ========== HEADER ========== */
.header-premium {
    position: sticky;
    top: 0;
    z-index: 999;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    padding: 0 var(--space-xl);
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    margin-bottom: var(--space-lg);
}

.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.header-icon {
    font-size: 24px;
    color: var(--primary-light);
}

.header-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.header-subtitle {
    font-size: 12px;
    color: var(--text-secondary);
    margin: 0;
}

.header-right {
    display: flex;
    gap: 24px;
    align-items: center;
}

.header-link {
    font-size: 12px;
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s ease;
}

.header-link:hover {
    color: var(--primary-light);
}

/* ========== SECTION TITLES ========== */
.section-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: var(--space-md);
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: var(--space-xl);
}

.section-icon {
    font-size: 18px;
}

/* ========== DIVIDERS ========== */
.section-divider {
    height: 1px;
    background: var(--border);
    margin: var(--space-xl) 0;
    border: none;
}

/* ========== CARDS ========== */
.card-premium {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    box-shadow: var(--shadow-md);
    margin-bottom: var(--space-lg);
    transition: all 0.3s ease;
}

.card-premium:hover {
    box-shadow: var(--shadow-lg);
    border-color: var(--primary-dark);
    background: var(--bg-tertiary);
}

/* ========== INPUTS ========== */
input[type="number"],
input[type="text"],
select,
.stNumberInput > div > div > input,
.stSelectbox > div > div > select {
    width: 100% !important;
    padding: 10px 12px !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    font-size: 14px !important;
    background: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
    font-family: inherit !important;
    transition: all 0.2s ease !important;
}

input[type="number"]:focus,
input[type="text"]:focus,
select:focus,
.stNumberInput > div > div > input:focus,
.stSelectbox > div > div > select:focus {
    outline: none !important;
    border-color: var(--primary-light) !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2) !important;
    background: var(--bg-tertiary) !important;
}

input::placeholder {
    color: var(--text-tertiary) !important;
}

/* ========== BUTTONS ========== */
.stButton > button {
    padding: 12px 20px !important;
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    font-family: inherit !important;
    background: var(--primary-light) !important;
    color: white !important;
    box-shadow: var(--shadow-sm) !important;
}

.stButton > button:hover {
    background: var(--primary) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px);
}

.stButton > button:active {
    background: var(--primary-dark) !important;
    transform: translateY(0);
}

/* ========== LABELS & HELP TEXT ========== */
label {
    display: block;
    font-weight: 600;
    font-size: 12px;
    color: var(--text-primary);
    margin-bottom: 8px !important;
}

.help-text {
    font-size: 11px;
    color: var(--text-secondary);
    margin-top: 4px;
    display: block;
}

/* ========== CHECKBOXES ========== */
.stCheckbox > label {
    font-weight: 400 !important;
    font-size: 14px !important;
    margin-bottom: 0 !important;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-primary) !important;
}

/* ========== RADIO BUTTONS ========== */
.stRadio > label {
    font-weight: 500 !important;
    font-size: 13px !important;
    color: var(--text-primary) !important;
}

/* ========== SLIDERS ========== */
.stSlider {
    color: var(--primary-light) !important;
}

/* ========== KPI CARDS ========== */
.kpi-container {
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 20px;
    text-align: center;
    box-shadow: var(--shadow-md);
    transition: all 0.3s ease;
}

.kpi-container:hover {
    border-color: var(--primary-dark);
    box-shadow: var(--shadow-lg);
}

.kpi-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 18px;
    font-weight: 700;
    color: var(--primary-light);
    font-family: 'IBM Plex Mono', monospace;
}

/* ========== EXPANDERS ========== */
.streamlit-expanderHeader {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 16px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    transition: all 0.2s ease !important;
}

.streamlit-expanderHeader:hover {
    background: var(--bg-hover) !important;
    border-color: var(--primary-dark) !important;
}

.streamlit-expanderContent {
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    padding: 20px !important;
    background: var(--bg-secondary) !important;
}

/* ========== TABLES ========== */
.stDataFrame {
    width: 100%;
}

.stDataFrame thead {
    background: var(--bg-tertiary) !important;
}

.stDataFrame th {
    background: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border-bottom: 2px solid var(--border) !important;
    padding: 12px !important;
    text-align: left !important;
}

.stDataFrame td {
    padding: 12px !important;
    border-bottom: 1px solid var(--border-light) !important;
    font-size: 13px !important;
    color: var(--text-primary) !important;
    background: var(--bg-secondary) !important;
}

.stDataFrame tbody tr:nth-child(even) {
    background: var(--bg-tertiary) !important;
}

.stDataFrame tbody tr:hover {
    background: var(--bg-hover) !important;
}

/* ========== METRICS ========== */
.stMetric {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 20px;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
}

.stMetric:hover {
    border-color: var(--primary-dark);
    background: var(--bg-tertiary);
}

.stMetricLabel {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
}

.stMetricValue {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: var(--primary-light) !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ========== ALERTS ========== */
.stAlert {
    border-radius: var(--radius-md) !important;
    padding: 12px 16px !important;
    font-size: 13px !important;
    border-left: 4px solid !important;
    background: var(--bg-tertiary) !important;
}

.stAlert > div {
    color: var(--text-primary) !important;
}

/* Info Alert */
.stAlert > div:nth-child(1) {
    color: var(--text-secondary) !important;
}

/* ========== FOOTER ========== */
.footer-premium {
    position: sticky;
    bottom: 0;
    background: var(--bg-secondary);
    border-top: 1px solid var(--border);
    padding: 0 var(--space-xl);
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-secondary);
    z-index: 100;
    margin-top: var(--space-xl);
}

.footer-left {
    font-weight: 500;
}

.footer-center {
    text-align: center;
}

.footer-right {
    display: flex;
    gap: 12px;
}

.footer-link {
    color: var(--text-secondary);
    text-decoration: none;
    transition: color 0.2s ease;
}

.footer-link:hover {
    color: var(--primary-light);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1199px) {
    .header-premium {
        padding: 0 var(--space-lg);
    }
    
    .footer-premium {
        padding: 0 var(--space-lg);
    }
}

@media (max-width: 767px) {
    .header-premium {
        padding: 0 var(--space-md);
        height: 56px;
    }
    
    .footer-premium {
        padding: 0 var(--space-md);
        font-size: 10px;
    }
    
    .header-title {
        font-size: 14px;
    }
    
    .header-right {
        display: none;
    }
    
    .section-title {
        font-size: 14px;
    }
    
    .card-premium {
        padding: var(--space-md);
    }
}

/* Grid Helpers */
.grid-2-cols {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-lg);
    margin-bottom: var(--space-lg);
}

.grid-4-cols {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}

@media (max-width: 1199px) {
    .grid-2-cols, .grid-4-cols {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 767px) {
    .grid-2-cols, .grid-4-cols {
        grid-template-columns: 1fr;
    }
}

/* Streamlit specific overrides */
[data-testid="stMetricContainer"] {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 20px !important;
}

.stMarkdown {
    color: var(--text-primary) !important;
}

</style>
""", unsafe_allow_html=True)

# ============ CONSTANTS ============
MEETINGS_RATE = 800
MEETINGS_COUNT = 4
MEETINGS_HRS = 1.5
MODELLING_PERCENT = 0.30
MODELLING_RATE = 1200

PROJECT_FACTORS = {
    'Commercial': 0.85,
    'Industrial': 1.10,
    'Pharma': 1.20,
    'Hospital': 1.25,
    'Metro/Infrastructure': 1.30,
    'Oil & Gas': 1.40,
    'Business Park': 0.80
}

VOLTAGE_FACTORS = {
    '≤ 11 kV': 1.00,
    '33 kV': 1.15,
    '66 kV': 1.30,
    '110/132 kV': 1.50,
    '220 kV+': 1.75
}

REGION_FACTORS = {
    'Domestic India': 1.00,
    'South Asia': 1.05,
    'Southeast Asia': 1.35,
    'Middle East': 1.75,
    'APAC ex-SE': 1.55,
    'Europe/North America': 2.00
}

DEFAULT_STUDIES = {
    'Load Flow': {'baseHrs': 15, 'complexity': 1.0},
    'Short Circuit': {'baseHrs': 18, 'complexity': 1.1},
    'Protection Coordination': {'baseHrs': 25, 'complexity': 1.3},
    'Arc Flash': {'baseHrs': 16, 'complexity': 1.0},
    'Harmonics': {'baseHrs': 22, 'complexity': 1.2},
    'Transient Stability': {'baseHrs': 30, 'complexity': 1.4},
    'Motor Starting': {'baseHrs': 18, 'complexity': 1.05}
}

DEFAULT_TEAM = {
    'L1 (Senior)': {'rate': 2400, 'allocation': 0.15},
    'L2 (Mid)': {'rate': 1200, 'allocation': 0.35},
    'L3 (Junior)': {'rate': 900, 'allocation': 0.50}
}

# ============ HELPER FUNCTIONS ============
def format_currency(amount):
    return f"₹{amount:,.0f}"

def format_number(num):
    return f"{num:,.1f}"

def calculate_costs(facility_mw, mv_buses, lv_buses, project_type, voltage, region,
                   mw_exponent, bus_exponent, bus_confidence, buffer_percent,
                   report_mode, report_percent, report_fixed, report_complexity,
                   custom_studies, custom_team, selected_studies, custom_blended_rate):
    
    total_buses = mv_buses + lv_buses
    mw_per_bus = facility_mw / total_buses
    
    mw_factor = pow(facility_mw / 10, mw_exponent)
    bus_factor = pow(total_buses / 32, bus_exponent)
    project_factor = PROJECT_FACTORS[project_type]
    voltage_factor = VOLTAGE_FACTORS[voltage]
    region_factor = REGION_FACTORS[region]
    
    study_results = []
    total_study_hours = 0
    total_report_hours = 0
    total_study_cost = 0
    
    blended_rate = custom_blended_rate
    
    for study_name in selected_studies:
        if study_name not in DEFAULT_STUDIES:
            continue
            
        base_hrs = custom_studies[study_name]['baseHrs']
        complexity = custom_studies[study_name]['complexity']
        
        adjusted_study_hrs = base_hrs * bus_factor * mw_factor
        all_factors = project_factor * voltage_factor * region_factor * bus_confidence * complexity
        final_study_hrs = adjusted_study_hrs * all_factors
        study_cost = final_study_hrs * blended_rate
        
        report_hrs = 0
        if report_mode == "% of Study Cost":
            report_pct = report_percent / 100
            report_hrs = final_study_hrs * report_pct
        
        total_study_hours += final_study_hrs
        total_report_hours += report_hrs
        total_study_cost += study_cost
        
        study_results.append({
            'Study': study_name,
            'studyHrs': final_study_hrs,
            'reportHrs': report_hrs,
            'studyCost': study_cost,
            'reportCost': report_hrs * blended_rate * report_complexity
        })
    
    total_reporting_cost = 0
    if report_mode == "% of Study Cost":
        total_reporting_cost = total_report_hours * blended_rate * report_complexity
    else:
        total_reporting_cost = report_fixed * (len(selected_studies) / 7)
    
    total_project_hours = total_study_hours + total_report_hours + (MEETINGS_COUNT * MEETINGS_HRS)
    meetings_cost = MEETINGS_COUNT * MEETINGS_HRS * MEETINGS_RATE
    modelling_hours = total_project_hours * MODELLING_PERCENT
    modelling_cost = modelling_hours * MODELLING_RATE
    
    l1_hours = total_project_hours * custom_team['L1 (Senior)']['allocation']
    l2_hours = total_project_hours * custom_team['L2 (Mid)']['allocation']
    l3_hours = total_project_hours * custom_team['L3 (Junior)']['allocation']
    
    blended_rate = (l1_hours * custom_team['L1 (Senior)']['rate'] + 
                   l2_hours * custom_team['L2 (Mid)']['rate'] + 
                   l3_hours * custom_team['L3 (Junior)']['rate']) / total_project_hours
    
    total_study_cost = 0
    total_reporting_cost = 0
    for result in study_results:
        result['studyCost'] = result['studyHrs'] * blended_rate
        result['reportCost'] = result['reportHrs'] * blended_rate * report_complexity
        total_study_cost += result['studyCost']
        total_reporting_cost += result['reportCost']
    
    total_reporting_cost += (report_fixed if report_mode == "Fixed Amount ₹" else 0)
    
    subtotal = total_study_cost + total_reporting_cost + meetings_cost + modelling_cost
    buffer = subtotal * (buffer_percent / 100)
    grand_total = subtotal + buffer
    
    cost_per_bus = grand_total / total_buses
    studies_cost_per_bus = total_study_cost / total_buses
    reporting_cost_per_bus = total_reporting_cost / total_buses
    modelling_cost_per_bus = modelling_cost / total_buses
    
    return {
        'mw_factor': mw_factor,
        'bus_factor': bus_factor,
        'mw_per_bus': mw_per_bus,
        'total_buses': total_buses,
        'total_study_hours': total_study_hours,
        'total_report_hours': total_report_hours,
        'total_project_hours': total_project_hours,
        'total_study_cost': total_study_cost,
        'total_reporting_cost': total_reporting_cost,
        'meetings_cost': meetings_cost,
        'modelling_cost': modelling_cost,
        'subtotal': subtotal,
        'buffer': buffer,
        'grand_total': grand_total,
        'cost_per_bus': cost_per_bus,
        'studies_cost_per_bus': studies_cost_per_bus,
        'reporting_cost_per_bus': reporting_cost_per_bus,
        'modelling_cost_per_bus': modelling_cost_per_bus,
        'study_results': study_results,
        'blended_rate': blended_rate
    }

# ============ HEADER ============
st.markdown("""
<div class="header-premium">
    <div class="header-left">
        <div class="header-icon">⚡</div>
        <div>
            <div class="header-title">Power Systems</div>
            <div class="header-subtitle">Cost Estimator v3.5</div>
        </div>
    </div>
    <div class="header-right">
        <a href="#" class="header-link">Documentation</a>
        <a href="#" class="header-link">Settings</a>
        <a href="#" class="header-link">Help</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============
if 'custom_studies' not in st.session_state:
    st.session_state.custom_studies = DEFAULT_STUDIES.copy()
if 'custom_team' not in st.session_state:
    st.session_state.custom_team = DEFAULT_TEAM.copy()

# ============ MAIN CONTENT ============
main_container = st.container()

with main_container:
    # ========== SECTION 1: PROJECT BASICS & CONFIGURATION ==========
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown('<div class="section-title"><span class="section-icon">📋</span> Project Information</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="card-premium">', unsafe_allow_html=True)
            
            project_name = st.text_input(
                "Project Name",
                value="Project-Alpha",
                help="Enter project name"
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                facility_mw = st.number_input(
                    "IT Capacity (MW)",
                    value=4.0,
                    min_value=0.5,
                    max_value=500.0,
                    step=0.5,
                    help="IT facility capacity"
                )
            with col2:
                mechanical_mw = st.number_input(
                    "Mechanical Load (MW)",
                    value=1.0,
                    min_value=0.0,
                    max_value=500.0,
                    step=0.5,
                    help="Mechanical load"
                )
            with col3:
                auxiliary_mw = st.number_input(
                    "House/Auxiliary Load (MW)",
                    value=0.0,
                    min_value=0.0,
                    max_value=500.0,
                    step=0.5,
                    help="Auxiliary load"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="section-title"><span class="section-icon">⚙️</span> Tier & Delivery</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="card-premium">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                tier_level = st.selectbox(
                    "Tier Level",
                    ["Tier I", "Tier II", "Tier III", "Tier IV"],
                    index=3,
                    help="Select tier level"
                )
            with col2:
                delivery_type = st.selectbox(
                    "Delivery Type",
                    ["Standard", "Expedited", "Premium"],
                    help="Select delivery type"
                )
            
            col1, col2 = st.columns(2)
            with col1:
                report_complexity = st.selectbox(
                    "Report Complexity",
                    ["Standard", "Detailed", "Executive"],
                    help="Report complexity level"
                )
            with col2:
                client_meetings = st.number_input(
                    "Client Meetings",
                    value=3,
                    min_value=0,
                    max_value=20,
                    help="Number of client meetings"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== IMPORTANT NOTE ========== 
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%); 
                border: 1px solid rgba(239, 68, 68, 0.3); border-left: 4px solid #ef4444;
                border-radius: 8px; padding: 16px; margin-bottom: 24px;">
        <div style="display: flex; gap: 12px; margin-bottom: 12px;">
            <span style="font-size: 24px;">⚠️</span>
            <span style="font-size: 14px; font-weight: 600; color: #e8eef5;">Important Note</span>
        </div>
        <div style="color: #f59e0b; font-size: 13px; line-height: 1.6; margin-bottom: 8px;">
            <strong>Bus Count Estimation:</strong> This tool focuses on cost estimation for power system studies. Bus count calculations are handled by a separate specialized tool which will be integrated in future versions.
        </div>
        <div style="color: #f59e0b; font-size: 13px; line-height: 1.6;">
            <strong>Professional Application:</strong> Results are estimates based on industry standards. Always validate with qualified electrical engineers for actual project implementation.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== SECTION 2: STUDIES TO INCLUDE ==========
    st.markdown('<div class="section-title"><span class="section-icon">✓</span> Studies to Include</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card-premium">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        chk_lf = st.checkbox("Load Flow", value=True)
        chk_sc = st.checkbox("Short Circuit", value=True)
    
    with col2:
        chk_pdc = st.checkbox("Protection Coordination", value=True)
        chk_af = st.checkbox("Arc Flash", value=True)
    
    with col3:
        chk_har = st.checkbox("Harmonics", value=False)
        chk_ts = st.checkbox("Transient Stability", value=False)
    
    with col4:
        chk_ms = st.checkbox("Motor Starting", value=False)
    
    selected_studies = []
    if chk_lf: selected_studies.append('Load Flow')
    if chk_sc: selected_studies.append('Short Circuit')
    if chk_pdc: selected_studies.append('Protection Coordination')
    if chk_af: selected_studies.append('Arc Flash')
    if chk_har: selected_studies.append('Harmonics')
    if chk_ts: selected_studies.append('Transient Stability')
    if chk_ms: selected_studies.append('Motor Starting')
    
    col_calc, col_reset, col_space = st.columns([2, 2, 6])
    with col_calc:
        calc_button = st.button("🔄 Calculate Estimate", use_container_width=True, key="calc_btn")
    with col_reset:
        reset_button = st.button("↻ Reset All", use_container_width=True, key="reset_btn")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if reset_button:
        st.rerun()
    
    # ========== ADVANCED CUSTOMIZATION SECTION ==========
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title"><span class="section-icon">⚙️</span> Advanced Customization (35+ Parameters)</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card-premium">', unsafe_allow_html=True)
    
    # Accordion 1: Scaling
    with st.expander("▼ Scaling Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            mw_exponent = st.slider(
                "MW Exponent",
                0.5, 1.2, 0.8, 0.05,
                help="Controls scaling based on facility size (0.5-1.2, default 0.8)"
            )
            st.caption(f"Formula: MW_Factor = (MW/10)^{mw_exponent:.2f}")
        with col2:
            bus_exponent = st.slider(
                "Bus Exponent",
                0.7, 1.3, 0.9, 0.05,
                help="Controls scaling based on number of buses"
            )
            st.caption(f"Formula: Bus_Factor = (Buses/32)^{bus_exponent:.2f}")
    
    # Accordion 2: Base Hours
    with st.expander("▼ Base Study Hours"):
        st.markdown("**Customize base hours for each study type**")
        for study_name in DEFAULT_STUDIES.keys():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(study_name)
            with col2:
                st.caption(f"Default: {DEFAULT_STUDIES[study_name]['baseHrs']}h")
            with col3:
                custom_hrs = st.number_input(
                    f"hrs_{study_name}",
                    value=st.session_state.custom_studies[study_name]['baseHrs'],
                    min_value=5,
                    max_value=50,
                    step=1,
                    label_visibility="collapsed"
                )
                st.session_state.custom_studies[study_name]['baseHrs'] = custom_hrs
    
    # Accordion 3: Complexity
    with st.expander("▼ Complexity Factors"):
        st.markdown("**Adjust complexity multiplier for each study (0.5x - 2.0x)**")
        for study_name in DEFAULT_STUDIES.keys():
            col1, col2 = st.columns([3, 1])
            with col1:
                custom_complexity = st.slider(
                    f"{study_name}",
                    0.5, 2.0, st.session_state.custom_studies[study_name]['complexity'], 0.05,
                    key=f"complexity_{study_name}"
                )
            with col2:
                st.caption(f"{custom_complexity:.2f}x")
            st.session_state.custom_studies[study_name]['complexity'] = custom_complexity
    
    # Accordion 4: Reporting
    with st.expander("▼ Reporting Configuration"):
        st.markdown("**Choose reporting cost calculation method**")
        report_mode = st.radio(
            "Reporting Cost Mode",
            ["% of Study Cost", "Fixed Amount ₹"],
            horizontal=True
        )
        
        if report_mode == "% of Study Cost":
            report_percent = st.slider(
                "Report Cost % of Study Hours",
                10, 50, 35, 5,
                help="Percentage of study hours allocated to reporting"
            )
            report_fixed = 30000
        else:
            report_fixed = st.number_input(
                "Fixed Reporting Cost (₹)",
                value=30000,
                min_value=5000,
                max_value=100000,
                step=5000
            )
            report_percent = 35
        
        report_complexity = st.slider(
            "Report Complexity Factor",
            0.8, 1.5, 1.0, 0.1,
            help="Multiplier for reporting cost"
        )
    
    # Accordion 5: Team Costs
    with st.expander("▼ Team Rates & Allocation"):
        st.markdown("**Customize team member rates and work allocation**")
        for level in DEFAULT_TEAM.keys():
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                min_rate = 1200 if 'L1' in level else (600 if 'L2' in level else 450)
                max_rate = 3600 if 'L1' in level else (1800 if 'L2' in level else 1350)
                rate = st.number_input(
                    f"{level} Rate (₹/hr)",
                    value=st.session_state.custom_team[level]['rate'],
                    min_value=min_rate,
                    max_value=max_rate,
                    step=100
                )
                st.session_state.custom_team[level]['rate'] = rate
            
            with col2:
                min_alloc = 5 if 'L1' in level else (20 if 'L2' in level else 30)
                max_alloc = 25 if 'L1' in level else (50 if 'L2' in level else 70)
                alloc = st.slider(
                    f"{level} Alloc %",
                    min_alloc, max_alloc, int(st.session_state.custom_team[level]['allocation']*100), 1,
                    key=f"alloc_{level}"
                )
                st.session_state.custom_team[level]['allocation'] = alloc / 100
            
            with col3:
                st.metric("Value", f"{alloc}%")
    
    # Accordion 6: Buffers
    with st.expander("▼ Buffers & Confidence"):
        col1, col2 = st.columns(2)
        with col1:
            bus_confidence = st.slider(
                "Bus Confidence Level",
                0.9, 2.5, 1.0, 0.1,
                help="0.9x = High confidence, 2.5x = Low confidence"
            )
        with col2:
            buffer_percent = st.slider(
                "Contingency Buffer %",
                5, 25, 15, 1,
                help="Applied after all cost components"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== CALCULATE & RESULTS ==========
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    # Calculate blended rate
    total_project_hours_temp = 100
    l1_hours_temp = total_project_hours_temp * st.session_state.custom_team['L1 (Senior)']['allocation']
    l2_hours_temp = total_project_hours_temp * st.session_state.custom_team['L2 (Mid)']['allocation']
    l3_hours_temp = total_project_hours_temp * st.session_state.custom_team['L3 (Junior)']['allocation']
    custom_blended_rate = (l1_hours_temp * st.session_state.custom_team['L1 (Senior)']['rate'] +
                          l2_hours_temp * st.session_state.custom_team['L2 (Mid)']['rate'] +
                          l3_hours_temp * st.session_state.custom_team['L3 (Junior)']['rate']) / total_project_hours_temp
    
    results = calculate_costs(
        facility_mw, 24, 54, 'Commercial', '33 kV', 'Domestic India',
        mw_exponent, bus_exponent, bus_confidence, buffer_percent,
        report_mode, report_percent, report_fixed, report_complexity,
        st.session_state.custom_studies, st.session_state.custom_team,
        selected_studies, custom_blended_rate
    )
    
    # ========== KPI ROW 1 ==========
    st.markdown('<div class="section-title"><span class="section-icon">💰</span> Cost Estimation Results</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Study Hours", format_number(results['total_study_hours']))
    with col2:
        st.metric("Report Hours", format_number(results['total_report_hours']))
    with col3:
        st.metric("Total Hours", format_number(results['total_project_hours']))
    with col4:
        st.metric("Grand Total", format_currency(results['grand_total']))
    
    # ========== KPI ROW 2 ==========
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Study Cost", format_currency(results['total_study_cost']))
    with col2:
        st.metric("Report Cost", format_currency(results['total_reporting_cost']))
    with col3:
        st.metric("Modelling", format_currency(results['modelling_cost']))
    with col4:
        st.metric("Cost/Bus", format_currency(results['cost_per_bus']))
    
    # ========== PER-BUS COST BREAKDOWN ==========
    st.markdown('<div class="section-title"><span class="section-icon">📍</span> Per-Bus Cost Breakdown</div>', unsafe_allow_html=True)
    
    breakdown_data = [
        {
            'Component': 'Studies',
            'Total Cost': format_currency(results['total_study_cost']),
            'Cost Per Bus': format_currency(results['studies_cost_per_bus']),
            '% of Total': f"{(results['total_study_cost']/results['grand_total']*100):.1f}%"
        },
        {
            'Component': 'Reporting (Separate)',
            'Total Cost': format_currency(results['total_reporting_cost']),
            'Cost Per Bus': format_currency(results['reporting_cost_per_bus']),
            '% of Total': f"{(results['total_reporting_cost']/results['grand_total']*100):.1f}%"
        },
        {
            'Component': 'Modelling (30%)',
            'Total Cost': format_currency(results['modelling_cost']),
            'Cost Per Bus': format_currency(results['modelling_cost_per_bus']),
            '% of Total': f"{(results['modelling_cost']/results['grand_total']*100):.1f}%"
        },
        {
            'Component': 'Meetings & Misc',
            'Total Cost': format_currency(results['meetings_cost']),
            'Cost Per Bus': format_currency(results['meetings_cost']/results['total_buses']),
            '% of Total': f"{(results['meetings_cost']/results['grand_total']*100):.1f}%"
        },
        {
            'Component': 'Buffer',
            'Total Cost': format_currency(results['buffer']),
            'Cost Per Bus': format_currency(results['buffer']/results['total_buses']),
            '% of Total': f"{(results['buffer']/results['grand_total']*100):.1f}%"
        },
    ]
    
    st.dataframe(pd.DataFrame(breakdown_data), use_container_width=True)
    
    st.info("ℹ️ **Note:** Reporting cost calculated separately. Cost Per Bus includes: (Study Cost + Reporting + Modelling) / Buses")
    
    # ========== STUDIES BREAKDOWN ==========
    st.markdown('<div class="section-title"><span class="section-icon">📊</span> Studies Breakdown</div>', unsafe_allow_html=True)
    
    studies_df = pd.DataFrame([
        {
            'Study': s['Study'],
            'Study Hrs': format_number(s['studyHrs']),
            'Report Hrs': format_number(s['reportHrs']),
            'Total Hrs': format_number(s['studyHrs'] + s['reportHrs']),
            'Study Cost': format_currency(s['studyCost']),
            'Report Cost': format_currency(s['reportCost']),
            'Total': format_currency(s['studyCost'] + s['reportCost'])
        }
        for s in results['study_results']
    ])
    
    st.dataframe(studies_df, use_container_width=True)
    
    # ========== CONTRACTUAL PRICING ==========
    st.markdown('<div class="section-title"><span class="section-icon">💼</span> Contractual Pricing</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Buses", results['total_buses'])
    with col2:
        st.metric("Cost Per Bus", format_currency(results['cost_per_bus']))
    with col3:
        st.metric("With 20% Margin", format_currency(results['cost_per_bus'] * 1.20))
    with col4:
        st.metric("Total Revenue", format_currency(results['cost_per_bus'] * 1.20 * results['total_buses']))
    
    # ========== EXPORT SECTION ==========
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title"><span class="section-icon">📥</span> Export & Download</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'parameters': {
                'projectName': project_name,
                'facilityMW': facility_mw,
                'tierLevel': tier_level
            },
            'results': {
                'grandTotal': results['grand_total'],
                'costPerBus': results['cost_per_bus'],
                'totalHours': results['total_project_hours']
            }
        }
        json_str = json.dumps(export_data, indent=2)
        st.download_button(
            label="📥 JSON",
            data=json_str,
            file_name=f"estimate-{project_name}-{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        csv_data = f"""Power Systems Cost Estimate v3.5
Date,{datetime.now().isoformat()}
Project,{project_name}

Grand Total,{results['grand_total']}
Cost Per Bus,{results['cost_per_bus']}
Total Buses,{results['total_buses']}
Total Hours,{results['total_project_hours']}
"""
        st.download_button(
            label="📊 CSV",
            data=csv_data,
            file_name=f"estimate-{project_name}-{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        summary_text = f"""POWER SYSTEMS COST ESTIMATOR - Quotation Summary
Date: {datetime.now().strftime('%Y-%m-%d')}

PROJECT DETAILS:
Project Name: {project_name}
Tier Level: {tier_level}
Total Buses: {results['total_buses']}

COST BREAKDOWN:
Study Cost: {format_currency(results['total_study_cost'])}
Reporting Cost: {format_currency(results['total_reporting_cost'])}
Modelling Cost: {format_currency(results['modelling_cost'])}
Meetings: {format_currency(results['meetings_cost'])}
Subtotal: {format_currency(results['subtotal'])}
Buffer ({buffer_percent}%): {format_currency(results['buffer'])}

GRAND TOTAL: {format_currency(results['grand_total'])}
Cost Per Bus: {format_currency(results['cost_per_bus'])}
Total Project Hours: {format_number(results['total_project_hours'])}
"""
        st.download_button(
            label="📋 TXT",
            data=summary_text,
            file_name=f"estimate-{project_name}-{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col4:
        if st.button("↻ Start Over", use_container_width=True):
            st.rerun()

# ============ FOOTER ============
st.markdown("""
<div class="footer-premium">
    <div class="footer-left">© 2024 Developed by A.D | Power Systems Studies Department</div>
    <div class="footer-center">Built with Streamlit | v3.5 | Power Systems Consulting</div>
    <div class="footer-right">
        <a href="#" class="footer-link">Documentation</a> |
        <a href="#" class="footer-link">Support</a> |
        <a href="#" class="footer-link">Terms</a>
    </div>
</div>
""", unsafe_allow_html=True)
