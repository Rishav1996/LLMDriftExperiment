import numpy as np
import pandas as pd
import ruptures as rpt
from scipy import stats
import statsmodels.api as sm

def detect_ruptures_pelt(data, penalty=1.0):
    """
    Detects structural changes using the PELT algorithm from the 'ruptures' library.
    """
    if len(data) < 4:
        return []
    
    # Convert data to numpy array
    signal = np.array(data).reshape(-1, 1)
    
    try:
        # Using L2 cost function (finds change in mean)
        algo = rpt.Pelt(model="l2").fit(signal)
        # result is a list of change point indices (including the last index)
        result = algo.predict(pen=penalty)
        
        # Exclude the last index which is just the end of the signal
        return [idx - 1 for idx in result[:-1]]
    except Exception as e:
        return []

def detect_zscore_anomalies(data, threshold=2.0):
    """
    Detects point anomalies using Z-score thresholding.
    """
    if len(data) < 3:
        return []
    
    # Check for constant series
    if np.std(data) == 0:
        return []
        
    z_scores = np.abs(stats.zscore(data))
    anomalies = np.where(z_scores > threshold)[0]
    return anomalies.tolist()

def detect_statsmodels_breaks(data):
    """
    Detects structural breaks using CUSUM OLS residuals test from statsmodels.
    Returns the index where the break is most likely to have started.
    """
    if len(data) < 5:
        return []
    
    try:
        # Perform OLS on a constant to get residuals
        y = np.array(data)
        x = np.ones(len(y))
        model = sm.OLS(y, x).fit()
        
        # CUSUM test for structural stability
        # A simple way to find the break point is to look at where the cumulative sum of residuals is max.
        residuals = model.resid
        cusum = np.cumsum(residuals)
        break_point = np.argmax(np.abs(cusum))
        
        # Only return if it's not the start or end
        if 0 < break_point < len(data) - 1:
            return [break_point]
        return []
    except Exception:
        return []

def find_deviations(p_scores, c_scores, algorithm="PELT", sensitivity=1.0, level="Category"):
    """
    Orchestrates deviation detection for both agents across the specified hierarchy level.
    level: "Overall", "Category", or "Sub-category"
    """
    rounds = sorted(p_scores.keys(), key=lambda x: int(x.split('_')[1]))
    if not rounds:
        return []

    deviation_results = []
    sample_round = p_scores[rounds[0]]
    categories = sample_round.get("category_scores", {})

    # Define the targets based on level
    targets = []
    if level == "Overall":
        targets.append(("Overall", "N/A"))
    elif level == "Category":
        for cat in categories.keys():
            targets.append((cat, "Average"))
    elif level == "Sub-category":
        for cat, metrics in categories.items():
            for metric in metrics.keys():
                targets.append((cat, metric))

    for agent_name, agent_data in [("Pros", p_scores), ("Cons", c_scores)]:
        for cat_name, metric_name in targets:
            # Extract data series
            series = []
            for r in rounds:
                if level == "Overall":
                    series.append(agent_data[r].get("overall_scores", 0))
                elif level == "Category":
                    cat_m = agent_data[r].get("category_scores", {}).get(cat_name, {})
                    series.append(sum(cat_m.values())/len(cat_m) if cat_m else 0)
                elif level == "Sub-category":
                    series.append(agent_data[r].get("category_scores", {}).get(cat_name, {}).get(metric_name, 0))
            
            # Detect
            points = []
            if algorithm == "PELT (Structural)":
                points = detect_ruptures_pelt(series, penalty=sensitivity)
            elif algorithm == "Z-Score (Anomaly)":
                points = detect_zscore_anomalies(series, threshold=sensitivity)
            elif algorithm == "CUSUM (Statistical Break)":
                points = detect_statsmodels_breaks(series)
            
            for pt in points:
                deviation_results.append({
                    "Agent": agent_name,
                    "Category": cat_name,
                    "Metric": metric_name,
                    "Round": int(rounds[pt].split('_')[1]),
                    "Value": series[pt],
                    "Algorithm": algorithm
                })
                
    return pd.DataFrame(deviation_results)
