"""Last Catch: MODEL 2 (ML model)

Predicts how a catch's freshness score changes over time.

    b = starting score            -> from Model 1's global variables (description score, danger flag)
    m = spoilage rate per hour    -> predicted by a trained regression model from:
                                     fish group, fat level, stored in ice, description score, weight
    x = hours since caught

Spoilage speeds up over time (bacteria multiply), so the score follows exponential decay:
    score(x) = b * e^(-m * x)
Taking the log turns this into a straight line, y = mx + b:
    ln(score) = ln(b) - m * x

Training data is SYNTHETIC: generated from the placeholder shelf-life estimates in fish_catalog.py.
A real version would retrain on fishers' logged outcomes (sold fresh vs. spoiled).

Run:  pip install numpy scikit-learn
      python3 train_model2.py
"""
import json
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from fish_catalog import BASE_HOURS_ON_ICE, FISH, GROUP_NAMES, lookup_fish

SAFE_CUTOFF = 40   # below this score the catch goes grey (not food-safe)
rng = np.random.default_rng(42)


# ---------------- b: starting score from Model 1 ----------------
def initial_score(description_score, must_go_grey):
    """Model 1 gives a description score of 0-10. Turn it into a starting score of 0-100."""
    if must_go_grey:
        return 0.0                              # danger word found -> grey immediately
    return 75 + 2.5 * description_score         # 0 -> 75, 5 (neutral) -> 87.5, 10 -> 100


# ---------------- features for the ML model ----------------
FEATURE_NAMES = [f"group_{g}" for g in GROUP_NAMES] + ["fat_level", "stored_in_ice", "description_score", "log_weight"]

def make_features(group, fat, iced, description_score, weight_kg):
    one_hot = [1.0 if group == g else 0.0 for g in GROUP_NAMES]
    return one_hot + [fat, float(iced), description_score, math.log(max(weight_kg, 0.1))]


# ---------------- synthetic training data ----------------
def simulate_hours_until_unsafe(group, fat, iced, description_score, weight_kg):
    """Placeholder 'ground truth' used to generate training data."""
    hours = BASE_HOURS_ON_ICE[group]
    hours *= 1 - 0.12 * fat                          # fattier fish spoil faster
    if not iced:
        hours *= 0.10                                # no ice: roughly 10x faster
        hours *= (weight_kg / 20) ** 0.08            # big piles stay cool slightly longer
    hours *= 0.7 + 0.06 * description_score          # good handling (score 10) = 1.3x longer
    return hours * rng.lognormal(0, 0.12)            # real-world noise

def build_dataset(n=6000):
    X, y = [], []
    for _ in range(n):
        name, group, fat = FISH[rng.integers(len(FISH))]
        iced = bool(rng.integers(0, 2))
        desc = float(rng.uniform(0, 10))
        weight = float(rng.uniform(1, 200))
        hours = simulate_hours_until_unsafe(group, fat, iced, desc, weight)
        m = math.log(100 / SAFE_CUTOFF) / hours      # rate that takes 100 -> 40 in `hours`
        X.append(make_features(group, fat, iced, desc, weight))
        y.append(math.log(m))                        # learn log(m): keeps m positive
    return np.array(X), np.array(y)


# ---------------- train + evaluate ----------------
X, y = build_dataset()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
model = LinearRegression().fit(X_train, y_train)

pred = model.predict(X_test)
r2 = r2_score(y_test, pred)
hours_true = math.log(100 / SAFE_CUTOFF) / np.exp(y_test)
hours_pred = math.log(100 / SAFE_CUTOFF) / np.exp(pred)
median_err_pct = float(np.median(np.abs(hours_pred - hours_true) / hours_true) * 100)
print(f"Test R^2 (log m): {r2:.3f}")
print(f"Median error in predicted food-safe hours: {median_err_pct:.1f}%")


# ---------------- use the model ----------------
def predict_m(fish_name, stored_in_ice, description_score, weight_kg):
    group, fat, _ = lookup_fish(fish_name)
    features = np.array([make_features(group, fat, stored_in_ice, description_score, weight_kg)])
    return float(np.exp(model.predict(features)[0]))

def score_at(b, m, hours):
    return b * math.exp(-m * hours)

def hours_until_grey(b, m):
    return 0.0 if b <= SAFE_CUTOFF else math.log(b / SAFE_CUTOFF) / m


# Example: these values would come from Model 1's global variables
examples = [
    ("Snoek", 20.5, False, 3.0, False),
    ("Kob", 12, True, 8.5, False),
    ("Yellowfin Tuna", 40, False, 5.0, False),
    ("Mussel", 5, False, 5.0, False),
    ("Hake", 8, True, 0.0, True),
]
print("\nfish             iced  desc   b      m/hour   food-safe for")
for fish, weight, iced, desc, grey in examples:
    b = initial_score(desc, grey)
    m = predict_m(fish, iced, desc, weight)
    print(f"{fish:16s} {str(iced):5s} {desc:4.1f}  {b:5.1f}  {m:.4f}   {hours_until_grey(b, m):6.1f} h")


# ---------------- export for the website ----------------
export = {
    "feature_names": FEATURE_NAMES,
    "coefficients": [round(float(c), 5) for c in model.coef_],
    "intercept": round(float(model.intercept_), 5),
    "groups": GROUP_NAMES,
    "safe_cutoff": SAFE_CUTOFF,
    "fish": [{"name": n, "group": g, "fat": f} for n, g, f in FISH],
    "test_r2": round(r2, 4),
    "median_error_pct": round(median_err_pct, 1),
}
with open("model2_data.js", "w") as f:
    f.write("// Generated by train_model2.py. Do not edit by hand; retrain instead.\n")
    f.write("const MODEL2_DATA = " + json.dumps(export) + ";\n")
print(f"\nExported model2_data.js ({len(FISH)} fish)")
