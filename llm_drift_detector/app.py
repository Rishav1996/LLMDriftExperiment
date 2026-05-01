import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import sys
import base64
import re
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
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def get_image_base64(image_path):
    """Converts a local image to a base64 string."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None

def render_markdown_with_images(md_content, base_dir):
    """Replaces local image links in markdown with base64 data URIs."""
    def replace_image(match):
        alt_text = match.group(1)
        img_filename = match.group(2)
        img_path = os.path.join(base_dir, img_filename)
        
        if os.path.exists(img_path):
            b64_str = get_image_base64(img_path)
            if b64_str:
                return f'![{alt_text}](data:image/png;base64,{b64_str})'
        return match.group(0) # Fallback to original

    # Regex for ![alt](path)
    img_regex = r'!\[(.*?)\]\((.*?)\)'
    return re.sub(img_regex, replace_image, md_content)

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
    
    md += "## 3. Longitudinal Behavioral Matrix\n"
    md += "Consolidated vector scores across all conversational rounds.\n\n"
    
    pros_drift = analysis_results.get("pros_agent_drift", {})
    cons_drift = analysis_results.get("cons_agent_drift", {})
    all_rounds = sorted(list(set(pros_drift.keys()) | set(cons_drift.keys())), key=lambda x: int(x.split('_')[1]))
    
    # Identify all unique categories
    all_cats = set()
    for r_data in pros_drift.values():
        all_cats.update(r_data.get("category_scores", {}).keys())
    for r_data in cons_drift.values():
        all_cats.update(r_data.get("category_scores", {}).keys())
    sorted_cats = sorted(list(all_cats))

    # Build Matrix Data
    # Header Row 1: Groupings
    md += "| Round | " + " | ".join(["Pros"] * (len(sorted_cats) + 1)) + " | " + " | ".join(["Cons"] * (len(sorted_cats) + 1)) + " |\n"
    # Header Row 2: Categories
    cat_headers = ["Overall"] + sorted_cats
    md += "| --- | " + " | ".join([f"**{c}**" for c in cat_headers]) + " | " + " | ".join([f"**{c}**" for c in cat_headers]) + " |\n"
    
    for r_key in all_rounds:
        row_data = [r_key.replace('_', ' ').capitalize()]
        
        # Add Scores for Pros
        row_data.append(f"{pros_drift.get(r_key, {}).get('overall_drift', 0):.4f}")
        p_cats = pros_drift.get(r_key, {}).get("category_scores", {})
        for cat in sorted_cats:
            skills = p_cats.get(cat, {})
            val = sum(skills.values())/len(skills) if skills else 0
            row_data.append(f"{val:.4f}")
            
        # Add Scores for Cons
        row_data.append(f"{cons_drift.get(r_key, {}).get('overall_drift', 0):.4f}")
        c_cats = cons_drift.get(r_key, {}).get("category_scores", {})
        for cat in sorted_cats:
            skills = c_cats.get(cat, {})
            val = sum(skills.values())/len(skills) if skills else 0
            row_data.append(f"{val:.4f}")
            
        md += "| " + " | ".join(row_data) + " |\n"
    md += "\n\n"
    
    md += "## 4. Visualization Breakdown\n"
    if all_rounds:
        last_round = all_rounds[-1]
        md += f"### Latest Snapshot ({last_round.replace('_', ' ').capitalize()})\n"
        md += f"![Pros Categories]({run_name}_pros_{last_round}_categories.png)\n"
        md += f"![Cons Categories]({run_name}_cons_{last_round}_categories.png)\n\n"
        
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
    st.title("Control Panel")
    
    all_runs = loader.load_all_runs(base_path)
    if all_runs:
        selected_run_name = st.selectbox("Research Run", sorted(list(all_runs.keys())))
        run_data = all_runs[selected_run_name]
        
        st.divider()
        st.markdown("### Analysis Parameters")
        
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
        execute_clicked = st.button("Execute Quantification", use_container_width=True)

# --- Main Dashboard ---
st.title("LLM Drift Analytics Explorer")
st.markdown("Quantifying behavioral trajectories in adversarial multi-agent simulations.")

if not all_runs:
    st.error("Missing evidentiary data. Ensure 'Research Runs/' is populated.")
elif selected_run_name:
    if execute_clicked:
        with st.status(f"Quantifying {selected_run_name}...", expanded=True) as status:
            # Standardize output naming: analysis-[version]-{rest of config}
            base_name = selected_run_name.replace("memory-", "analysis-")
            if not base_name.startswith("analysis-"):
                base_name = f"analysis-{selected_run_name}"

            # Create run-specific sub-directory
            run_specific_dir = os.path.join(analysis_output_dir, base_name)
            os.makedirs(run_specific_dir, exist_ok=True)

            num_rounds = loader.get_number_of_rounds(run_data)
            results = {"pros_agent_drift": {}, "cons_agent_drift": {}}
            for r in range(1, num_rounds + 1):
                st.write(f"Processing Round {r}...")
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
            
            # Persistence inside sub-directory
            central_json = os.path.join(run_specific_dir, f"{base_name}_analysis.json")
            with open(central_json, "w") as f:
                json.dump(results, f, indent=4)
            
            # Visualizations inside sub-directory
            run_graphing_service = GraphingService(output_dir=run_specific_dir)
            run_graphing_service.save_run_visualizations(base_name, results)
            
            # Report inside sub-directory
            md_content = generate_markdown_report(base_name, results, run_data.get('config_info', {}))
            md_file = os.path.join(run_specific_dir, f"{base_name}_report.md")
            with open(md_file, "w") as f:
                f.write(md_content)
            
            status.update(label="Quantification Complete!", state="complete", expanded=False)
            st.rerun()

    # Standardize lookup naming
    base_name = selected_run_name.replace("memory-", "analysis-")
    if not base_name.startswith("analysis-"):
        base_name = f"analysis-{selected_run_name}"

    # Load analysis results (Check sub-directory first)
    analysis_file = os.path.join(analysis_output_dir, base_name, f"{base_name}_analysis.json")
    # Fallback to legacy root location
    if not os.path.exists(analysis_file):
        analysis_file = os.path.join(analysis_output_dir, f"{base_name}_analysis.json")
    if not os.path.exists(analysis_file):
        analysis_file = os.path.join(analysis_output_dir, f"{selected_run_name}_analysis.json")
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
        tab1, tab2, tab3 = st.tabs(["Drift Trajectory", "Behavioral Vectors", "Research Report"])

        with tab1:
            st.subheader("Longitudinal Drift Analysis")
            overall_data = []
            for r_key in sorted(p_drift.keys(), key=lambda x: int(x.split('_')[1])):
                r_num = int(r_key.split('_')[1])
                overall_data.append({"Round": r_num, "Agent": "Pros", "Drift": p_drift[r_key].get("overall_drift", 0)})
                overall_data.append({"Round": r_num, "Agent": "Cons", "Drift": c_drift[r_key].get("overall_drift", 0)})
            
            df = pd.DataFrame(overall_data)
            fig = px.line(df, x="Round", y="Drift", color="Agent", line_shape="linear", markers=True,
                          title="Accumulated Drift over Conversational Rounds")
            fig.update_layout(yaxis_range=[0, 1], hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Multi-Dimensional Behavioral Transition")
            st.markdown("Tracking the longitudinal evolution of behavioral categories across all rounds.")
            
            def prepare_multi_dim_data(agent_drift_data, agent_name):
                plot_data = []
                rounds = sorted([int(k.split('_')[1]) for k in agent_drift_data.keys()])
                for r in rounds:
                    r_key = f"round_{r}"
                    cat_scores = agent_drift_data[r_key].get("category_scores", {})
                    for cat, skills in cat_scores.items():
                        if skills:
                            avg_val = sum(skills.values()) / len(skills)
                            plot_data.append({
                                "Round": r,
                                "Category": cat,
                                "Score": avg_val,
                                "Agent": agent_name
                            })
                return pd.DataFrame(plot_data)

            df_p_multi = prepare_multi_dim_data(p_drift, "Pros")
            df_c_multi = prepare_multi_dim_data(c_drift, "Cons")

            col_p, col_c = st.columns(2)
            
            with col_p:
                if not df_p_multi.empty:
                    fig_p = px.line(df_p_multi, x="Round", y="Score", color="Category", markers=True,
                                    title="Pros Agent: Vector Transitions",
                                    line_shape="linear")
                    fig_p.update_layout(yaxis_range=[0, 1], hovermode="x unified")
                    st.plotly_chart(fig_p, use_container_width=True)
                else:
                    st.info("No behavioral data available for Pros.")

            with col_c:
                if not df_c_multi.empty:
                    fig_c = px.line(df_c_multi, x="Round", y="Score", color="Category", markers=True,
                                    title="Cons Agent: Vector Transitions",
                                    line_shape="linear")
                    fig_c.update_layout(yaxis_range=[0, 1], hovermode="x unified")
                    st.plotly_chart(fig_c, use_container_width=True)
                else:
                    st.info("No behavioral data available for Cons.")

        with tab3:
            st.subheader("Automated Research Summary")
            # Check sub-directory first
            report_dir = os.path.join(analysis_output_dir, base_name)
            report_path = os.path.join(report_dir, f"{base_name}_report.md")
            
            # Fallbacks
            if not os.path.exists(report_path):
                report_dir = analysis_output_dir
                report_path = os.path.join(analysis_output_dir, f"{base_name}_report.md")
            if not os.path.exists(report_path):
                report_dir = analysis_output_dir
                report_path = os.path.join(analysis_output_dir, f"{selected_run_name}_report.md")
            
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    content = f.read()
                    # Render with embedded base64 images
                    rendered_content = render_markdown_with_images(content, report_dir)
                    st.markdown(rendered_content)
            else:
                st.info("Dynamic report not found. Execute quantification to generate.")

    else:
        st.info("Quantified analysis not found for this run. Use the sidebar to execute analysis.")
        with st.expander("View Experiment Configuration"):
            st.json(run_data.get('config_info', {}))
