import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests
import warnings

def perform_granger_causality(data_a, data_b, maxlag=1):
    """
    Performs Granger Causality test to see if A causes B.
    Returns the minimum p-value across all lags.
    """
    if len(data_a) < 2 * maxlag + 2: # Heuristic for minimum data points
        return None
    
    # Check for constant series
    if np.std(data_a) == 0 or np.std(data_b) == 0:
        return None

    # Granger causality expects a 2D array where the first column is the target (B) 
    # and the second column is the predictor (A).
    # We want to know if A influences B.
    df = pd.DataFrame({'B': data_b, 'A': data_a})
    
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            gc_res = grangercausalitytests(df[['B', 'A']], maxlag=maxlag, verbose=False)
            
        # Extract p-values for each lag and return the minimum one
        p_values = [gc_res[lag][0]['ssr_ftest'][1] for lag in range(1, maxlag + 1)]
        return min(p_values)
    except Exception as e:
        # print(f"Error in Granger Causality: {e}")
        return None

def analyze_causality(results):
    """
    Analyzes causality and correlation between Pros and Cons across all levels.
    """
    p_scores = results.get("pros_agent_scores", {})
    c_scores = results.get("cons_agent_scores", {})
    
    rounds = sorted(p_scores.keys(), key=lambda x: int(x.split('_')[1]))
    if len(rounds) < 5: # Minimum rounds for meaningful causality
        return None

    causality_results = []

    # 1. Overall Causality & Correlation
    p_overall = [p_scores[r].get("overall_scores", 0) for r in rounds]
    c_overall = [c_scores[r].get("overall_scores", 0) for r in rounds]
    
    p_to_c = perform_granger_causality(p_overall, c_overall)
    c_to_p = perform_granger_causality(c_overall, p_overall)
    corr = pd.Series(p_overall).corr(pd.Series(c_overall))
    
    causality_results.append({
        "Level": "Overall",
        "Category": "N/A",
        "Metric": "Overall Delta",
        "Pros -> Cons (p)": p_to_c,
        "Cons -> Pros (p)": c_to_p,
        "Correlation (r)": corr,
        "Direction": "Pros -> Cons" if (p_to_c is not None and (c_to_p is None or p_to_c < c_to_p)) else "Cons -> Pros"
    })

    # 2. Category and Sub-category wise
    # Get all categories and metrics
    sample_round = p_scores[rounds[0]]
    categories = sample_round.get("category_scores", {})
    
    for cat_name, metrics in categories.items():
        # Category-wise average
        p_cat_avg = []
        c_cat_avg = []
        for r in rounds:
            p_m = p_scores[r].get("category_scores", {}).get(cat_name, {})
            c_m = c_scores[r].get("category_scores", {}).get(cat_name, {})
            p_cat_avg.append(sum(p_m.values())/len(p_m) if p_m else 0)
            c_cat_avg.append(sum(c_m.values())/len(c_m) if c_m else 0)
            
        p_to_c = perform_granger_causality(p_cat_avg, c_cat_avg)
        c_to_p = perform_granger_causality(c_cat_avg, p_cat_avg)
        corr = pd.Series(p_cat_avg).corr(pd.Series(c_cat_avg))
        
        causality_results.append({
            "Level": "Category",
            "Category": cat_name,
            "Metric": "Average",
            "Pros -> Cons (p)": p_to_c,
            "Cons -> Pros (p)": c_to_p,
            "Correlation (r)": corr,
            "Direction": "Pros -> Cons" if (p_to_c is not None and (c_to_p is None or p_to_c < c_to_p)) else "Cons -> Pros"
        })
        
        # Sub-category wise
        for metric_name in metrics.keys():
            p_series = [p_scores[r].get("category_scores", {}).get(cat_name, {}).get(metric_name, 0) for r in rounds]
            c_series = [c_scores[r].get("category_scores", {}).get(cat_name, {}).get(metric_name, 0) for r in rounds]
            
            p_to_c = perform_granger_causality(p_series, c_series)
            c_to_p = perform_granger_causality(c_series, p_series)
            corr = pd.Series(p_series).corr(pd.Series(c_series))
            
            causality_results.append({
                "Level": "Sub-category",
                "Category": cat_name,
                "Metric": metric_name,
                "Pros -> Cons (p)": p_to_c,
                "Cons -> Pros (p)": c_to_p,
                "Correlation (r)": corr,
                "Direction": "Pros -> Cons" if (p_to_c is not None and (c_to_p is None or p_to_c < c_to_p)) else "Cons -> Pros"
            })

    return pd.DataFrame(causality_results)
