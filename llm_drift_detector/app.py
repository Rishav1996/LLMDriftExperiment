import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the root directory to sys.path to allow imports from llm_drift_detector
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from llm_drift_detector.utils.data_processing import ResearchRunLoader
from llm_drift_detector.utils.evaluator import DriftEvaluator
from llm_drift_detector.utils.graphing import GraphingService

# --- Page Config ---
st.set_page_config(
    page_title="LLM Drift Analytics | Research Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Data Science Look ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    h1, h2, h3 {
        color: #1f2937;
        font-family: 'Inter', sans-serif;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        border-bottom: 2px solid #3b82f6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Helper Functions ---
@st.cache_resource
def get_loader():
    return ResearchRunLoader()

@st.cache_resource
def get_evaluator():
    return DriftEvaluator()

@st.cache_resource
def get_graphing_service(output_dir):
    return GraphingService(output_dir=output_dir)

def generate_markdown_report(run_name, analysis_results, config_info):
    """Generates a detailed Markdown report of the drift analysis."""
    md = f"# LLM Drift Analysis Report: {run_name}\n\n"
    md += f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    md += "## 1. Experiment Configuration\n"
    md += "```json\n"
    md += json.dumps(config_info, indent=4)
    md += "\n```\n\n"
    
    md += "## 2. Visualizations\n"
    md += f"![Overall Drift Trend]({run_name}_trend.png)\n\n"
    
    md += "## 3. Statistical Summary\n"
    md += "| Round | Pros Overall Drift | Cons Overall Drift |\n"
    md += "|-------|-------------------|-------------------|\n"
    
    pros_drift = analysis_results.get("pros_agent_drift", {})
    cons_drift = analysis_results.get("cons_agent_drift", {})
    all_rounds = sorted(list(set(pros_drift.keys()) | set(cons_drift.keys())), key=lambda x: int(x.split('_')[1]))
    
    for r_key in all_rounds:
        p_score = pros_drift.get(r_key, {}).get("overall_drift", 0)
        c_score = cons_drift.get(r_key, {}).get("overall_drift", 0)
        md += f"| {r_key} | {p_score:.4f} | {c_score:.4f} |\n"
    
    md += "\n## 4. Behavioral Vector Breakdown\n"
    if all_rounds:
        last_round = all_rounds[-1]
        md += f"### Latest Snapshot ({last_round.replace('_', ' ').capitalize()})\n"
        md += f"![Pros Categories]({run_name}_pros_{last_round}_categories.png)\n"
        md += f"![Cons Categories]({run_name}_cons_{last_round}_categories.png)\n\n"

    for r_key in all_rounds:
        md += f"### {r_key.replace('_', ' ').capitalize()}\n"
        p_cats = pros_drift.get(r_key, {}).get("category_scores", {})
        c_cats = cons_drift.get(r_key, {}).get("category_scores", {})
        
        md += "#### Vector Details\n"
        md += "| Category | Pros Score | Cons Score |\n"
        md += "| :--- | :--- | :--- |\n"
        
        all_cats = sorted(list(set(p_cats.keys()) | set(c_cats.keys())))
        for cat in all_cats:
            p_val = sum(p_cats.get(cat, {}).values())/len(p_cats.get(cat, {})) if p_cats.get(cat) else 0
            c_val = sum(c_cats.get(cat, {}).values())/len(c_cats.get(cat, {})) if c_cats.get(cat) else 0
            md += f"| {cat} | {p_val:.4f} | {c_val:.4f} |\n"
        md += "\n"
        
    return md

# --- App Logic ---
loader = get_loader()
evaluator = get_evaluator()
base_path = os.path.join(root_dir, "Research Runs")
analysis_output_dir = os.path.join(root_dir, "Drift Analysis")
os.makedirs(analysis_output_dir, exist_ok=True)
graphing_service = get_graphing_service(analysis_output_dir)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=60)
    st.title("Control Panel")
    
    all_runs = loader.load_all_runs(base_path)
    if all_runs:
        selected_run_name = st.selectbox("📁 Research Run", sorted(list(all_runs.keys())))
        run_data = all_runs[selected_run_name]
        
        st.divider()
        st.markdown("### ⚙️ Analysis Parameters")
        
        all_metric_names = [s.name for s in evaluator.skills_manager.get_all_skills()]
        selected_metrics = st.multiselect(
            "Target Vectors",
            options=sorted(all_metric_names),
            default=None,
            help="Select specific skills to quantify. Leave empty for full suite."
        )
        
        stability_passes = st.slider("Stability Passes", 1, 5, 1)
        throttling_delay = st.slider("Throttling (s)", 0, 30, 5)
        
        st.divider()
        if st.button("🚀 Execute Quantification", use_container_width=True, type="primary"):
            with st.status(f"Quantifying {selected_run_name}...", expanded=True) as status:
                num_rounds = loader.get_number_of_rounds(run_data)
                results = {"pros_agent_drift": {}, "cons_agent_drift": {}}
                for r in range(1, num_rounds + 1):
                    st.write(f"🔬 Processing Round {r}...")
                    results["pros_agent_drift"][f"round_{r}"] = evaluator.evaluate_round(
                        run_data, r, "Pros", 
                        num_iterations=stability_passes,
                        target_metrics=selected_metrics if selected_metrics else None,
                        wait_time=throttling_delay
                    )
                    results["cons_agent_drift"][f"round_{r}"] = evaluator.evaluate_round(
                        run_data, r, "Cons", 
                        num_iterations=stability_passes,
                        target_metrics=selected_metrics if selected_metrics else None,
                        wait_time=throttling_delay
                    )
                
                # Persistence
                central_json = os.path.join(analysis_output_dir, f"{selected_run_name}_analysis.json")
                with open(central_json, "w") as f:
                    json.dump(results, f, indent=4)
                graphing_service.save_run_visualizations(selected_run_name, results)
                md_content = generate_markdown_report(selected_run_name, results, run_data.get('config_info', {}))
                md_file = os.path.join(analysis_output_dir, f"{selected_run_name}_report.md")
                with open(md_file, "w") as f:
                    f.write(md_content)
                
                status.update(label="Quantification Complete!", state="complete", expanded=False)
                st.rerun()

# --- Main Dashboard ---
st.title("LLM Drift Analytics Explorer")
st.markdown("Quantifying behavioral trajectories in adversarial multi-agent simulations.")

if not all_runs:
    st.error("Missing evidentiary data. Ensure 'Research Runs/' is populated.")
elif selected_run_name:
    # Load analysis results
    analysis_file = os.path.join(analysis_output_dir, f"{selected_run_name}_analysis.json")
    # Fallback to legacy location
    if not os.path.exists(analysis_file):
        analysis_file = os.path.join(base_path, selected_run_name, "drift_analysis.json")

    if os.path.exists(analysis_file):
        with open(analysis_file, "r") as f:
            results = json.load(f)

        # --- Executive Summary ---
        p_drift = results.get("pros_agent_drift", {})
        c_drift = results.get("cons_agent_drift", {})
        last_round_key = sorted(p_drift.keys(), key=lambda x: int(x.split('_')[1]))[-1] if p_drift else None
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Rounds", len(p_drift))
        with m2:
            st.metric("Avg. Pros Drift", f"{sum(d.get('overall_drift',0) for d in p_drift.values())/max(len(p_drift),1):.2f}")
        with m3:
            st.metric("Avg. Cons Drift", f"{sum(d.get('overall_drift',0) for d in c_drift.values())/max(len(c_drift),1):.2f}")
        with m4:
            st.metric("Max Delta", f"{abs((p_drift.get(last_round_key,{}).get('overall_drift',0)) - (c_drift.get(last_round_key,{}).get('overall_drift',0))):.2f}")

        # --- Analysis Tabs ---
        tab1, tab2, tab3 = st.tabs(["📉 Drift Trajectory", "🎯 Behavioral Vectors", "📑 Research Report"])

        with tab1:
            st.subheader("Longitudinal Drift Analysis")
            overall_data = []
            for r_key in sorted(p_drift.keys(), key=lambda x: int(x.split('_')[1])):
                r_num = int(r_key.split('_')[1])
                overall_data.append({"Round": r_num, "Agent": "Pros", "Drift": p_drift[r_key].get("overall_drift", 0)})
                overall_data.append({"Round": r_num, "Agent": "Cons", "Drift": c_drift[r_key].get("overall_drift", 0)})
            
            df = pd.DataFrame(overall_data)
            fig = px.area(df, x="Round", y="Drift", color="Agent", line_shape="spline", 
                          color_discrete_map={"Pros": "#3b82f6", "Cons": "#ef4444"},
                          title="Accumulated Drift over Conversational Rounds")
            fig.update_layout(plot_bgcolor="white", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Multi-Dimensional Vector Analysis")
            col_a, col_b = st.columns(2)
            
            rounds_list = sorted([int(k.split('_')[1]) for k in p_drift.keys()])
            selected_r = st.select_slider("Select Observation Round", options=rounds_list, value=rounds_list[-1])
            rk = f"round_{selected_r}"

            def create_radar(agent_data, title, color):
                categories = []
                values = []
                for cat, skills in agent_data.get("category_scores", {}).items():
                    if skills:
                        categories.append(cat)
                        values.append(sum(skills.values())/len(skills))
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', name=title, line_color=color))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False, title=title)
                return fig

            with col_a:
                st.plotly_chart(create_radar(p_drift.get(rk, {}), "Pros Behavioral Profile", "#3b82f6"), use_container_width=True)
            with col_b:
                st.plotly_chart(create_radar(c_drift.get(rk, {}), "Cons Behavioral Profile", "#ef4444"), use_container_width=True)

        with tab3:
            st.subheader("Automated Research Summary")
            report_path = os.path.join(analysis_output_dir, f"{selected_run_name}_report.md")
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    st.markdown(f.read())
            else:
                st.info("Dynamic report not found. Execute quantification to generate.")

    else:
        st.info("📊 Quantified analysis not found for this run. Use the sidebar to execute analysis.")
        with st.expander("View Experiment Configuration"):
            st.json(run_data.get('config_info', {}))
