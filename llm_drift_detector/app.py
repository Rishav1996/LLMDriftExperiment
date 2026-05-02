import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import sys
from dotenv import load_dotenv
from sklearn.metrics import pairwise_distances
import numpy as np

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


def calculate_drift_distances(scores_dict, metric='euclidean', filter_categories=None):
    """
    Calculates distance between consecutive rounds and computes cumulative average.
    """
    rounds_sorted = sorted(scores_dict.keys(), key=lambda x: int(x.split('_')[1]))
    if len(rounds_sorted) < 2:
        return None
    
    vectors = []
    round_labels = []
    
    for r_key in rounds_sorted:
        flat_vector = []
        cat_scores = scores_dict[r_key].get("category_scores", {})
        target_cats = filter_categories if filter_categories else sorted(cat_scores.keys())
        
        for cat in sorted(target_cats):
            if cat in cat_scores:
                skills = cat_scores[cat]
                for skill in sorted(skills.keys()):
                    flat_vector.append(skills[skill])
        
        if flat_vector:
            vectors.append(flat_vector)
            round_labels.append(int(r_key.split('_')[1]))

    if len(vectors) < 2:
        return None

    vectors_np = np.array(vectors)
    distances = []
    intervals = []

    for i in range(len(vectors_np) - 1):
        v1 = vectors_np[i].reshape(1, -1)
        v2 = vectors_np[i+1].reshape(1, -1)
        dist = pairwise_distances(v1, v2, metric=metric)[0][0]
        distances.append(dist)
        intervals.append(f"R{round_labels[i]}→R{round_labels[i+1]}")
        
    df = pd.DataFrame({"Interval": intervals, "Original Value": distances})
    df["Cumulative Average"] = df["Original Value"].expanding().mean()
    return df

def plot_drift_toggle(df, title, show_avg):
    """
    Plots either original drift or cumulative average based on the toggle state.
    """
    y_col = "Cumulative Average" if show_avg else "Original Value"
    
    fig = px.line(
        df, 
        x="Interval", 
        y=y_col, 
        color="Agent", 
        markers=True,
        title=f"{title} ({y_col})",
        labels={y_col: "Distance Score"}
    )
    fig.update_layout(hovermode="x unified", yaxis_range=[-1, 1])
    return fig


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
        max_rounds = st.number_input("Max Rounds to Evaluate", min_value=1, value=10, help="Limit the number of rounds to process.")
        force_rerun = st.checkbox("Force Re-run", help="If checked, ignores existing results and evaluates from scratch.")
        
        st.divider()
        execute_clicked = st.button("Execute Quantification", width='stretch')

# --- Main Dashboard ---
st.title("LLM Drift Analytics Explorer")
st.markdown("Quantifying behavioral trajectories in adversarial multi-agent simulations.")

if not all_runs:
    st.error("Missing evidentiary data. Ensure 'Research Runs/' is populated.")
elif selected_run_name:
    if execute_clicked:
        with st.status(f"Quantifying {selected_run_name}...", expanded=True) as status:
            base_name = selected_run_name.replace("memory-", "analysis-")
            if not base_name.startswith("analysis-"):
                base_name = f"analysis-{selected_run_name}"

            run_specific_dir = os.path.join(analysis_output_dir, base_name)
            os.makedirs(run_specific_dir, exist_ok=True)
            central_json = os.path.join(run_specific_dir, f"{base_name}_analysis.json")

            # Load existing results if any, unless forcing a re-run
            results = {"pros_agent_scores": {}, "cons_agent_scores": {}}
            if not force_rerun and os.path.exists(central_json):
                with open(central_json, "r") as f:
                    results = json.load(f)

            num_rounds = min(loader.get_number_of_rounds(run_data), max_rounds)
            for r in range(1, num_rounds + 1):
                r_key = f"round_{r}"
                
                # Check if this round is already fully evaluated (both agents present)
                round_exists = r_key in results["pros_agent_scores"] and r_key in results["cons_agent_scores"]
                
                # If skipping, ensure we don't re-run. If forcing, we re-run.
                if not force_rerun and round_exists:
                    st.write(f"Skipping Round {r} (already processed)...")
                    continue
                
                st.write(f"Processing Round {r}...")
                
                # Always evaluate both agents for the round
                pros_res = evaluator.evaluate_round(
                    run_data, r, "Pros", 
                    num_iterations=stability_passes,
                    target_metrics=selected_metrics if selected_metrics else None,
                    wait_time=throttling_delay
                )
                cons_res = evaluator.evaluate_round(
                    run_data, r, "Cons", 
                    num_iterations=stability_passes,
                    target_metrics=selected_metrics if selected_metrics else None,
                    wait_time=throttling_delay
                )
                
                # Merge/Update results
                results["pros_agent_scores"][r_key] = pros_res
                results["cons_agent_scores"][r_key] = cons_res
                
                # Save incrementally
                with open(central_json, "w") as f:
                    json.dump(results, f, indent=4)
            
            status.update(label="Quantification Complete!", state="complete", expanded=False)
            st.rerun()

    base_name = selected_run_name.replace("memory-", "analysis-")
    if not base_name.startswith("analysis-"):
        base_name = f"analysis-{selected_run_name}"

    analysis_file = os.path.join(analysis_output_dir, base_name, f"{base_name}_analysis.json")
    if not os.path.exists(analysis_file):
        analysis_file = os.path.join(analysis_output_dir, f"{base_name}_analysis.json")
    if not os.path.exists(analysis_file):
        analysis_file = os.path.join(analysis_output_dir, f"{selected_run_name}_analysis.json")
    if not os.path.exists(analysis_file):
        analysis_file = os.path.join(base_path, selected_run_name, "drift_analysis.json")

    if os.path.exists(analysis_file):
        with open(analysis_file, "r") as f:
            results = json.load(f)

        # --- Report Generation Function ---
        def generate_markdown_report(results, run_name, run_data, output_dir, figures):
            report_path = os.path.join(output_dir, f"{run_name.replace('memory', 'report')}.md")
            config = run_data.get('config_info', {})
            p_scores = results.get("pros_agent_scores", {})
            c_scores = results.get("cons_agent_scores", {})
            
            markdown = f"# Drift Analysis Report: {run_name}\n\n"
            markdown += "## Experiment Configuration\n"
            for k, v in config.items():
                markdown += f"- **{k}**: {v}\n"
            
            markdown += "\n## Summary Metrics\n"
            p_avg = sum(d.get('overall_scores', 0) for d in p_scores.values()) / max(len(p_scores), 1)
            c_avg = sum(d.get('overall_scores', 0) for d in c_scores.values()) / max(len(c_scores), 1)
            markdown += f"- **Pros Avg. Score**: {p_avg:.2f}\n"
            markdown += f"- **Cons Avg. Score**: {c_avg:.2f}\n"
            markdown += f"- **Total Rounds Analyzed**: {len(p_scores)}\n"
            
            markdown += "\n## Analysis Visualizations\n"
            for name, fig in figures.items():
                img_path = os.path.join(output_dir, f"{name}.png")
                fig.write_image(img_path)
                markdown += f"### {name}\n![{name}]({name}.png)\n\n"
            
            with open(report_path, "w") as f:
                f.write(markdown)
            return report_path

        # --- Sidebar Export Button ---
        with st.sidebar:
            st.divider()
            
            # Prepare data for dashboard charts (need to do this before sidebar logic for export)
            p_scores = results.get("pros_agent_scores", {})
            c_scores = results.get("cons_agent_scores", {})
            overall_data = []
            for r_key in sorted(p_scores.keys(), key=lambda x: int(x.split('_')[1])):
                r_num = int(r_key.split('_')[1])
                overall_data.append({"Round": r_num, "Agent": "Pros", "Delta": p_scores[r_key].get("overall_scores", 0)})
                overall_data.append({"Round": r_num, "Agent": "Cons", "Delta": c_scores[r_key].get("overall_scores", 0)})
            df_long = pd.DataFrame(overall_data)

            # Multi-Dim Data
            def prepare_multi_dim_data(p_data, c_data):
                plot_data = []
                rounds = sorted([int(k.split('_')[1]) for k in p_data.keys()])
                for r in rounds:
                    r_key = f"round_{r}"
                    for agent, data in [("Pros", p_data.get(r_key, {})), ("Cons", c_data.get(r_key, {}))]:
                        cat_scores = data.get("category_scores", {})
                        for cat, skills in cat_scores.items():
                            avg_val = sum(skills.values())/len(skills) if skills else 0
                            plot_data.append({"Round": r, "Category": cat, "Score": avg_val, "Agent": agent})
                return pd.DataFrame(plot_data)
            df_2d = prepare_multi_dim_data(p_scores, c_scores)

        # Extract available categories for the UI
        sample_round = next(iter(p_scores.values())) if p_scores else {}
        available_categories = sorted(list(sample_round.get("category_scores", {}).keys()))

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Rounds", len(p_scores))
        with m2:
            st.metric("Avg. Pros scores", f"{sum(d.get('overall_scores',0) for d in p_scores.values())/max(len(p_scores),1):.2f}")
        with m3:
            st.metric("Avg. Cons scores", f"{sum(d.get('overall_scores',0) for d in c_scores.values())/max(len(c_scores),1):.2f}")

        # --- Tabbed View ---
        tab_dash, tab_drift = st.tabs(["Dashboard", "Drift Analysis"])
        
        with tab_dash:
            st.subheader("Longitudinal Delta Analysis")
            overall_data = []
            for r_key in sorted(p_scores.keys(), key=lambda x: int(x.split('_')[1])):
                r_num = int(r_key.split('_')[1])
                overall_data.append({"Round": r_num, "Agent": "Pros", "Delta": p_scores[r_key].get("overall_scores", 0)})
                overall_data.append({"Round": r_num, "Agent": "Cons", "Delta": c_scores[r_key].get("overall_scores", 0)})
            
            df = pd.DataFrame(overall_data)
            if not df.empty:
                fig = px.line(df, x="Round", y="Delta", color="Agent", line_shape="linear", markers=True,
                             title="Accumulated Delta over Conversational Rounds")
                fig.update_layout(yaxis_range=[-1, 1], hovermode="x unified")
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("Multi-Dimensional Vector Evolution")
            def prepare_multi_dim_data(p_data, c_data):
                plot_data = []
                rounds = sorted([int(k.split('_')[1]) for k in p_data.keys()])
                for r in rounds:
                    r_key = f"round_{r}"
                    for agent, data in [("Pros", p_data.get(r_key, {})), ("Cons", c_data.get(r_key, {}))]:
                        cat_scores = data.get("category_scores", {})
                        for cat, skills in cat_scores.items():
                            avg_val = sum(skills.values())/len(skills) if skills else 0
                            plot_data.append({"Round": r, "Category": cat, "Score": avg_val, "Agent": agent})
                return pd.DataFrame(plot_data)

            df_2d = prepare_multi_dim_data(p_scores, c_scores)
            if not df_2d.empty:
                fig_2d = px.line(df_2d, x="Round", y="Score", color="Category", facet_col="Agent", markers=True,
                                title="Behavioral Vector Evolution (2D)")
                fig_2d.update_layout(yaxis_range=[-1, 1])
                st.plotly_chart(fig_2d, use_container_width=True)

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
                                    plot_data.append({"Round": r, "Metric": skill, "Score": val, "Agent": agent})
                    return pd.DataFrame(plot_data)

                df_drill = prepare_drilldown_data(p_scores, c_scores, selected_roots)
                if not df_drill.empty:
                    fig_drill = px.line(df_drill, x="Round", y="Score", color="Metric", facet_col="Agent", markers=True,
                                       title=f"Sub-metrics for {', '.join(selected_roots)}")
                    fig_drill.update_layout(yaxis_range=[-1, 1])
                    st.plotly_chart(fig_drill, use_container_width=True)

        with tab_drift:
            # --- Chart 1: Global Drift ---
            st.subheader("Global Behavioral Drift")
            distance_algo = st.selectbox(
                "Distance Metric", 
                ["euclidean", "cosine", "manhattan", "chebyshev"],
                help="Mathematical method to calculate drift between round vectors."
            )
            use_avg = st.toggle("Show Cumulative Average", value=False, help="Switch between raw step-wise drift and the smoothed trend.")
            df_p_global = calculate_drift_distances(p_scores, metric=distance_algo)
            df_c_global = calculate_drift_distances(c_scores, metric=distance_algo)
            
            if df_p_global is not None and df_c_global is not None:
                df_p_global["Agent"], df_c_global["Agent"] = "Pros", "Cons"
                global_df = pd.concat([df_p_global, df_c_global])
                st.plotly_chart(plot_drift_toggle(global_df, "Global Vector Evolution", use_avg), use_container_width=True)
            
            st.divider()

            # --- Chart 2: Category Specific Drift ---
            st.subheader("Targeted Category Drift")
            selected_drift_cats = st.multiselect("Select Categories", options=available_categories, default=available_categories[:1])

            if selected_drift_cats:
                df_p_cat = calculate_drift_distances(p_scores, metric=distance_algo, filter_categories=selected_drift_cats)
                df_c_cat = calculate_drift_distances(c_scores, metric=distance_algo, filter_categories=selected_drift_cats)
                
                if df_p_cat is not None and df_c_cat is not None:
                    df_p_cat["Agent"], df_c_cat["Agent"] = "Pros", "Cons"
                    cat_drift_df = pd.concat([df_p_cat, df_c_cat])
                    title_cat = f"Drift for: {', '.join(selected_drift_cats)}"
                    st.plotly_chart(plot_drift_toggle(cat_drift_df, title_cat, use_avg), use_container_width=True)
                else:
                    st.warning("Insufficient data for the selected filter.")

    else:
        st.info("Quantified analysis not found for this run. Use the sidebar to execute analysis.")
        with st.expander("View Experiment Configuration"):
            st.json(run_data.get('config_info', {}))