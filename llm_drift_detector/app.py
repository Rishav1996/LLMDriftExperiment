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


# --- App Logic ---
loader = get_loader()
evaluator = get_evaluator()
base_path = os.path.join(root_dir, "Research Runs")
analysis_output_dir = os.path.join(root_dir, "Drift Analysis")
os.makedirs(analysis_output_dir, exist_ok=True)

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
            results = {"pros_agent_scores": {}, "cons_agent_scores": {}}
            for r in range(1, num_rounds + 1):
                st.write(f"Processing Round {r}...")
                results["pros_agent_scores"][f"round_{r}"] = evaluator.evaluate_round(
                    run_data, r, "Pros", 
                    num_iterations=stability_passes,
                    target_metrics=selected_metrics if selected_metrics else None,
                    wait_time=throttling_delay
                )
                results["cons_agent_scores"][f"round_{r}"] = evaluator.evaluate_round(
                    run_data, r, "Cons", 
                    num_iterations=stability_passes,
                    target_metrics=selected_metrics if selected_metrics else None,
                    wait_time=throttling_delay
                )
            
            # Persistence inside sub-directory
            central_json = os.path.join(run_specific_dir, f"{base_name}_analysis.json")
            with open(central_json, "w") as f:
                json.dump(results, f, indent=4)

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
        p_scores = results.get("pros_agent_scores", {})
        c_scores = results.get("cons_agent_scores", {})
        last_round_key = sorted(p_scores.keys(), key=lambda x: int(x.split('_')[1]))[-1] if p_scores else None
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Rounds", len(p_scores))
        with m2:
            st.metric("Avg. Pros scores", f"{sum(d.get('overall_scores',0) for d in p_scores.values())/max(len(p_scores),1):.2f}")
        with m3:
            st.metric("Avg. Cons scores", f"{sum(d.get('overall_scores',0) for d in c_scores.values())/max(len(c_scores),1):.2f}")

        # --- Tabbed View ---
        tab_dash, tab_drift = st.tabs(["Dashboard", "Drift Analysis"])
        
        with tab_dash:
            # --- Analysis View ---
            st.subheader("Longitudinal Delta Analysis")
        overall_data = []
        for r_key in sorted(p_scores.keys(), key=lambda x: int(x.split('_')[1])):
            r_num = int(r_key.split('_')[1])
            overall_data.append({"Round": r_num, "Agent": "Pros", "Delta": p_scores[r_key].get("overall_scores", 0)})
            overall_data.append({"Round": r_num, "Agent": "Cons", "Delta": c_scores[r_key].get("overall_scores", 0)})
        
        df = pd.DataFrame(overall_data)
        fig = px.line(df, x="Round", y="Delta", color="Agent", line_shape="linear", markers=True,
                      title="Accumulated Delta over Conversational Rounds")
        fig.update_layout(yaxis_range=[0, 1], hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Multi-Dimensional Vector Evolution")
        st.markdown("Longitudinal evolution of behavioral categories across all rounds.")
        
        def prepare_multi_dim_data(p_data, c_data):
            plot_data = []
            rounds = sorted([int(k.split('_')[1]) for k in p_data.keys()])
            for r in rounds:
                r_key = f"round_{r}"
                for agent, data in [("Pros", p_data.get(r_key, {})), ("Cons", c_data.get(r_key, {}))]:
                    cat_scores = data.get("category_scores", {})
                    for cat, skills in cat_scores.items():
                        avg_val = sum(skills.values())/len(skills) if skills else 0
                        plot_data.append({
                            "Round": r, "Category": cat, "Score": avg_val, "Agent": agent
                        })
            return pd.DataFrame(plot_data)

        df_2d = prepare_multi_dim_data(p_scores, c_scores)
        
        if not df_2d.empty:
            fig_2d = px.line(
                df_2d, x="Round", y="Score", color="Category", 
                facet_col="Agent", markers=True,
                title="Behavioral Vector Evolution (2D)"
            )
            fig_2d.update_layout(yaxis_range=[0, 1])
            st.plotly_chart(fig_2d, use_container_width=True)
        else:
            st.info("No behavioral vector data found.")

        st.subheader("Sub-Category Metric Drill-down")
        all_cats = sorted(list(set().union(*(p_scores[r].get("category_scores", {}).keys() for r in p_scores))))
        selected_roots = st.multiselect("Select Root Categories", options=all_cats, default=all_cats)

        if selected_roots:
            def prepare_drilldown_data(p_data, c_data, roots):
                plot_data = []
                rounds = sorted([int(k.split('_')[1]) for k in p_data.keys()])
                for r in rounds:
                    r_key = f"round_{r}"
                    for agent, data in [("Pros", p_data.get(r_key, {})), ("Cons", c_data.get(r_key, {}))]:
                        cat_data = data.get("category_scores", {})
                        for root in roots:
                            cat_scores = cat_data.get(root, {})
                            for skill, val in cat_scores.items():
                                plot_data.append({
                                    "Round": r, "Metric": skill, "Score": val, "Agent": agent
                                })
                return pd.DataFrame(plot_data)

            df_drill = prepare_drilldown_data(p_scores, c_scores, selected_roots)
            if not df_drill.empty:
                fig_drill = px.line(
                    df_drill, x="Round", y="Score", color="Metric", 
                    facet_col="Agent", markers=True,
                    title=f"Sub-metrics for {', '.join(selected_roots)}"
                )
                fig_drill.update_layout(yaxis_range=[0, 1])
                st.plotly_chart(fig_drill, use_container_width=True)
            else:
                st.info("No sub-metrics found for selected categories.")

    else:
        st.info("Quantified analysis not found for this run. Use the sidebar to execute analysis.")
        with st.expander("View Experiment Configuration"):
            st.json(run_data.get('config_info', {}))
