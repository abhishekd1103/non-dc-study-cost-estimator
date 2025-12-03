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
    initial_sidebar_state="expanded"
)

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
    
    # Calculate factors
    mw_factor = pow(facility_mw / 10, mw_exponent)
    bus_factor = pow(total_buses / 32, bus_exponent)
    project_factor = PROJECT_FACTORS[project_type]
    voltage_factor = VOLTAGE_FACTORS[voltage]
    region_factor = REGION_FACTORS[region]
    
    # Calculate studies
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
        
        # Reporting
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
    
    # Reporting cost
    total_reporting_cost = 0
    if report_mode == "% of Study Cost":
        total_reporting_cost = total_report_hours * blended_rate * report_complexity
    else:
        total_reporting_cost = report_fixed * (len(selected_studies) / 7)
    
    # Additional costs
    total_project_hours = total_study_hours + total_report_hours + (MEETINGS_COUNT * MEETINGS_HRS)
    meetings_cost = MEETINGS_COUNT * MEETINGS_HRS * MEETINGS_RATE
    modelling_hours = total_project_hours * MODELLING_PERCENT
    modelling_cost = modelling_hours * MODELLING_RATE
    
    # Team allocation recalculation
    l1_hours = total_project_hours * custom_team['L1 (Senior)']['allocation']
    l2_hours = total_project_hours * custom_team['L2 (Mid)']['allocation']
    l3_hours = total_project_hours * custom_team['L3 (Junior)']['allocation']
    
    blended_rate = (l1_hours * custom_team['L1 (Senior)']['rate'] + 
                   l2_hours * custom_team['L2 (Mid)']['rate'] + 
                   l3_hours * custom_team['L3 (Junior)']['rate']) / total_project_hours
    
    # Recalculate with new blended rate
    total_study_cost = 0
    total_reporting_cost = 0
    for result in study_results:
        result['studyCost'] = result['studyHrs'] * blended_rate
        result['reportCost'] = result['reportHrs'] * blended_rate * report_complexity
        total_study_cost += result['studyCost']
        total_reporting_cost += result['reportCost']
    
    total_reporting_cost += (report_fixed if report_mode == "Fixed Amount ₹" else 0)
    
    # Final costs
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
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #2080c0 0%, #1a6aa6 100%); border-radius: 12px; color: white; margin-bottom: 30px;">
        <h1 style="margin: 0; font-size: 36px;">⚡ Power Systems Cost Estimator v3.5</h1>
        <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">35+ Customizable Parameters • Real-World Calibration • Detailed Per-Bus Pricing</p>
    </div>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============
if 'custom_studies' not in st.session_state:
    st.session_state.custom_studies = DEFAULT_STUDIES.copy()
if 'custom_team' not in st.session_state:
    st.session_state.custom_team = DEFAULT_TEAM.copy()

# ============ MAIN LAYOUT ============
col_left, col_right = st.columns(2)

# LEFT COLUMN: INPUTS
with col_left:
    st.subheader("📋 Project Basics")
    
    facility_mw = st.number_input("Facility Capacity (MW)", value=10.0, min_value=0.5, max_value=500.0, step=0.5)
    col_mv, col_lv = st.columns(2)
    with col_mv:
        mv_buses = st.number_input("MV Buses", value=24, min_value=1, max_value=200, step=1)
    with col_lv:
        lv_buses = st.number_input("LV Buses", value=54, min_value=1, max_value=300, step=1)
    
    st.subheader("⚙️ Configuration")
    
    project_type = st.selectbox("Project Type", list(PROJECT_FACTORS.keys()), index=0)
    voltage = st.selectbox("Highest Voltage (kV)", list(VOLTAGE_FACTORS.keys()), index=1)
    region = st.selectbox("Region", list(REGION_FACTORS.keys()), index=0)
    
    st.subheader("✓ Studies to Include")
    
    col1, col2 = st.columns(2)
    with col1:
        chk_lf = st.checkbox("Load Flow", value=True)
        chk_sc = st.checkbox("Short Circuit", value=True)
        chk_pdc = st.checkbox("Protection Coordination", value=True)
        chk_af = st.checkbox("Arc Flash", value=True)
    with col2:
        chk_har = st.checkbox("Harmonics", value=False)
        chk_ts = st.checkbox("Transient Stability", value=False)
        chk_ms = st.checkbox("Motor Starting", value=False)
    
    selected_studies = []
    if chk_lf: selected_studies.append('Load Flow')
    if chk_sc: selected_studies.append('Short Circuit')
    if chk_pdc: selected_studies.append('Protection Coordination')
    if chk_af: selected_studies.append('Arc Flash')
    if chk_har: selected_studies.append('Harmonics')
    if chk_ts: selected_studies.append('Transient Stability')
    if chk_ms: selected_studies.append('Motor Starting')

# RIGHT COLUMN: RESULTS
with col_right:
    st.subheader("📊 Cost Summary")
    
    # Calculate
    calc_button = st.button("🔄 Calculate Cost Estimate", use_container_width=True)

# ============ ADVANCED CUSTOMIZATION ============
st.markdown("---")
st.subheader("⚙️ Advanced Customization (35+ Parameters)")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Scaling", "Base Hours", "Complexity", "Reporting", "Team Costs", "Buffers"]
)

with tab1:
    st.write("**Customize scaling exponents for MW & Bus complexity**")
    col1, col2 = st.columns(2)
    with col1:
        mw_exponent = st.slider("MW Exponent (default 0.8)", 0.5, 1.2, 0.8, 0.05)
        st.caption(f"Formula: MW_Factor = (MW/10)^{mw_exponent:.2f}")
    with col2:
        bus_exponent = st.slider("Bus Exponent (default 0.9)", 0.7, 1.3, 0.9, 0.05)
        st.caption(f"Formula: Bus_Factor = (Buses/32)^{bus_exponent:.2f}")

with tab2:
    st.write("**Customize base study hours for each study**")
    for study_name in DEFAULT_STUDIES.keys():
        default_hrs = DEFAULT_STUDIES[study_name]['baseHrs']
        custom_hrs = st.number_input(
            f"{study_name} Base Hours",
            value=default_hrs,
            min_value=5,
            max_value=50,
            step=1,
            key=f"basehrs_{study_name}"
        )
        st.session_state.custom_studies[study_name]['baseHrs'] = custom_hrs

with tab3:
    st.write("**Customize complexity factor for each study (0.5x - 2.0x)**")
    for study_name in DEFAULT_STUDIES.keys():
        default_complexity = DEFAULT_STUDIES[study_name]['complexity']
        custom_complexity = st.slider(
            f"{study_name} Complexity",
            0.5, 2.0, default_complexity, 0.05,
            key=f"complexity_{study_name}"
        )
        st.session_state.custom_studies[study_name]['complexity'] = custom_complexity

with tab4:
    st.write("**Customize reporting cost: Choose % of study cost OR fixed amount**")
    
    report_mode = st.radio("Reporting Cost Mode", ["% of Study Cost", "Fixed Amount ₹"])
    
    if report_mode == "% of Study Cost":
        report_percent = st.slider("Report Cost % of Study Hours (default 35%)", 10, 50, 35, 5)
        report_fixed = 30000
    else:
        report_fixed = st.number_input("Fixed Reporting Cost (₹)", value=30000, min_value=5000, max_value=100000, step=5000)
        report_percent = 35
    
    report_complexity = st.slider("Report Complexity Factor (default 1.0x)", 0.8, 1.5, 1.0, 0.1)

with tab5:
    st.write("**Customize team member rates and work allocations**")
    
    for level in DEFAULT_TEAM.keys():
        col1, col2 = st.columns(2)
        with col1:
            min_rate = 1200 if 'L1' in level else (600 if 'L2' in level else 450)
            max_rate = 3600 if 'L1' in level else (1800 if 'L2' in level else 1350)
            rate = st.number_input(f"{level} Rate (₹/hr)", value=DEFAULT_TEAM[level]['rate'], min_value=min_rate, max_value=max_rate, step=100)
            st.session_state.custom_team[level]['rate'] = rate
        
        with col2:
            min_alloc = 5 if 'L1' in level else (20 if 'L2' in level else 30)
            max_alloc = 25 if 'L1' in level else (50 if 'L2' in level else 70)
            alloc = st.slider(f"{level} Allocation %", min_alloc, max_alloc, int(DEFAULT_TEAM[level]['allocation']*100), 1)
            st.session_state.custom_team[level]['allocation'] = alloc / 100

with tab6:
    st.write("**Customize confidence levels and final contingency buffer**")
    col1, col2 = st.columns(2)
    with col1:
        bus_confidence = st.slider("Bus Confidence Level (default 1.0x)", 0.9, 2.5, 1.0, 0.1)
        st.caption("0.9x = Very High | 2.5x = Very Low")
    with col2:
        buffer_percent = st.slider("Contingency Buffer % (default 15%)", 5, 25, 15, 1)
        st.caption("Applied after all cost components")

# ============ CALCULATE & DISPLAY RESULTS ============
if calc_button or True:  # Auto-calculate
    
    # Calculate blended rate
    total_project_hours_temp = 100  # temporary
    l1_hours_temp = total_project_hours_temp * st.session_state.custom_team['L1 (Senior)']['allocation']
    l2_hours_temp = total_project_hours_temp * st.session_state.custom_team['L2 (Mid)']['allocation']
    l3_hours_temp = total_project_hours_temp * st.session_state.custom_team['L3 (Junior)']['allocation']
    custom_blended_rate = (l1_hours_temp * st.session_state.custom_team['L1 (Senior)']['rate'] +
                          l2_hours_temp * st.session_state.custom_team['L2 (Mid)']['rate'] +
                          l3_hours_temp * st.session_state.custom_team['L3 (Junior)']['rate']) / total_project_hours_temp
    
    results = calculate_costs(
        facility_mw, mv_buses, lv_buses, project_type, voltage, region,
        mw_exponent, bus_exponent, bus_confidence, buffer_percent,
        report_mode, report_percent, report_fixed, report_complexity,
        st.session_state.custom_studies, st.session_state.custom_team,
        selected_studies, custom_blended_rate
    )
    
    st.markdown("---")
    st.subheader("💰 Results & Pricing")
    
    # Summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Study Hours", format_number(results['total_study_hours']))
    with col2:
        st.metric("Report Hours", format_number(results['total_report_hours']))
    with col3:
        st.metric("Total Hours", format_number(results['total_project_hours']))
    with col4:
        st.metric("Grand Total", format_currency(results['grand_total']), delta=f"Buses: {results['total_buses']}")
    
    # Cost breakdown
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info(f"**Study Cost**\n{format_currency(results['total_study_cost'])}")
    with col2:
        st.warning(f"**Reporting (Separate)**\n{format_currency(results['total_reporting_cost'])}")
    with col3:
        st.info(f"**Modelling (30%)**\n{format_currency(results['modelling_cost'])}")
    with col4:
        st.success(f"**Cost Per Bus**\n{format_currency(results['cost_per_bus'])}")
    
    # Per-bus breakdown table
    st.subheader("📍 Per-Bus Cost Breakdown")
    
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
    
    st.info("ℹ️ **Note:** Reporting cost calculated separately and NOT included in base study cost. Cost Per Bus shows: (Study Cost + Reporting + Modelling) / Buses")
    
    # Studies table
    st.subheader("📊 Studies Breakdown")
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
    
    # Contractual pricing
    st.subheader("💼 Contractual Pricing")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Buses", results['total_buses'])
    with col2:
        st.metric("Cost Per Bus", format_currency(results['cost_per_bus']))
    with col3:
        st.metric("With 20% Margin", format_currency(results['cost_per_bus'] * 1.20))
    with col4:
        st.metric("Total Revenue", format_currency(results['cost_per_bus'] * 1.20 * results['total_buses']))
    
    # Export
    st.markdown("---")
    st.subheader("📥 Export Results")
    
    col1, col2 = st.columns(2)
    with col1:
        # JSON Export
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'parameters': {
                'facilityMW': facility_mw,
                'mvBuses': mv_buses,
                'lvBuses': lv_buses,
                'projectType': project_type
            },
            'results': {
                'grandTotal': results['grand_total'],
                'costPerBus': results['cost_per_bus'],
                'totalHours': results['total_project_hours']
            }
        }
        json_str = json.dumps(export_data, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"cost-estimate-{datetime.now().strftime('%Y-%m-%d')}.json",
            mime="application/json"
        )
    
    with col2:
        # CSV Export
        csv_data = f"""Power Systems Cost Estimation Report v3.5
Date,{datetime.now().isoformat()}

Grand Total,{format_currency(results['grand_total'])}
Cost Per Bus,{format_currency(results['cost_per_bus'])}
Total Buses,{results['total_buses']}
Total Hours,{format_number(results['total_project_hours'])}
"""
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name=f"cost-estimate-{datetime.now().strftime('%Y-%m-%d')}.csv",
            mime="text/csv"
        )

st.markdown("---")
st.caption("Power Systems Cost Estimator v3.5 | All 35+ Parameters Customizable | Real-World Calibration Ready")
