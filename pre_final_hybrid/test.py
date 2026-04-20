import joblib
import pandas as pd
import numpy as np

# defining the rules first

def rule_low_active(df): #Near-zero active time with high score
    return (df['active_days'] < 50) & (df['Score'] >= 10)

def rule_new_account_top_rank(df): #new user high rank
    return (df["ContestCnt"] <= 5) & (df["Rank"] < 200)

def rule_perfect_solve(df):
    return (df['total_fail'] == 0) & (df['Score'] >= 15) & (df['ContestCnt'] <= 5)

def rule_weak_profile(df): #Weak profile but top contest rank
    return (df['Total_solved'] < 200) & (df['Rank'] < 200)

def rule_low_solved_high_rating(df): #Low solved count but high rating
    return (df['Total_solved'] < 100) & (df['CurrRating'] > 1900)

def rule_zero_rating_jump(df):
    return (df['rating_jump'] == 0) & (df['CurrRating'] > 1500)

def rule_ghost_profile(df):
    return (df['Total_solved'] < 50) & (df['Rank'] < 5000)


# Loading Model
model = joblib.load("cheat_detection_model.pkl")

lof_models = model["lof_models"]
LOF_FEATURES = model["LOF_FEATURES"]
RATING_BINS = model["RATING_BINS"]
RATING_LABELS = model["RATING_LABELS"]
RULES = model["RULES"]
#efficiency_threshold = model["efficiency_threshold"]
threshold = model["Combined_threshold"]
lof_max = model["lof_max"]
lof_min = model["lof_min"]
print("Model loaded successfully")


RULE_FUNC_MAP = {
    'Near-zero active time with high score' : rule_low_active,
    'new user high rank'                    : rule_new_account_top_rank,
    'Perfect solve'                         : rule_perfect_solve,
    'Weak profile'                          : rule_weak_profile,
    'Low solved high rating'                : rule_low_solved_high_rating,
    # 'Extreme efficiency'                    : rule_extreme_efficiency,
    'Zero rating jump high rating'          : rule_zero_rating_jump,
    'Ghost profile high rank'               : rule_ghost_profile,
}

for rule in RULES:
    rule['func'] = RULE_FUNC_MAP[rule['name']]

# ── Predict Function ───────────────────────────────────────────────
def predict_user(user):
    df = pd.DataFrame([user])

    # Derived features
    df['score_per_time']     = df['CurrConSolved'] / df['time_taken'].clip(lower=1)
    df['hard_ratio']         = df['Hard'] / (df['Total_solved'] + 1)
    df['solved_per_contest'] = df['Total_solved'] / (df['ContestCnt'] + 1)
    df['rating_jump']        = df['CurrRating'] - df['rating_first']

    # Rating bucket
    df['rating_bucket'] = pd.cut(
        df['CurrRating'],
        bins=RATING_BINS,
        labels=RATING_LABELS
    )
    bucket = str(df['rating_bucket'].iloc[0])

    if bucket not in lof_models:
        return "Not enough data for this rating bucket"

    # LOF score
    scaler = lof_models[bucket]['scaler']
    lof    = lof_models[bucket]['lof']

    X        = df[LOF_FEATURES].fillna(0)
    X_scaled = scaler.transform(X)

    lof_score        = -lof.score_samples(X_scaled)[0]
    lof_score_clipped = min(lof_score, lof_max)          # clip to p99 to avoid compression
    lof_normalized   = ((lof_score_clipped - lof_min) / (lof_max - lof_min + 1e-9)) * 3

    # Rule score
    rule_score = 0
    triggered  = []
    for rule in RULES:
        if 'threshold' in rule:
            hit = rule['func'](df, rule['threshold']).iloc[0]
        else:
            hit = rule['func'](df).iloc[0]
        if hit:
            rule_score += rule['weight']
            triggered.append(rule['name'])


    if rule_score == 0:
        lof_normalized = 0
    

    final_score = rule_score + (lof_normalized * 0.3)
    thresh=threshold
    # print(thresh)
    if final_score >= 6:
        label = "HIGHLY SUSPICIOUS"
    elif final_score >= thresh:
        label = "SUSPICIOUS"
    else:
        label = "CLEAN"

    return {
        "lof_score":       round(lof_score, 4),
        "lof_normalized":  round(lof_normalized, 4),
        "rule_score":      rule_score,
        "final_score":     round(final_score, 4),
        "suspicious":      final_score >= thresh,
        "label":           label,
        "triggered_rules": triggered
    }


# TESTING
# Uncomment below to test on a testing data set

df_test = pd.read_csv("testing_data.csv")
results = []
for _, row in df_test.iterrows():
    result = predict_user(row.to_dict())
    results.append(result)

df_test['label']          = [r['label'] for r in results]
df_test['final_score']    = [r['final_score'] for r in results]
df_test['triggered_rules']= [r['triggered_rules'] for r in results]

df_test.to_csv("predictions.csv", index=False)
print("Saved to predictions.csv")

from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# true labels
y_true = df_test["ylabel"]

# predicted labels (0 = clean, 1 = suspicious)
y_pred = [0 if x == "CLEAN" else 1 for x in df_test["label"]]

# metrics
cm = confusion_matrix(y_true, y_pred)
acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred, zero_division=0)
rec = recall_score(y_true, y_pred, zero_division=0)
f1 = f1_score(y_true, y_pred, zero_division=0)


cm_df = pd.DataFrame(
    cm,
    index=["Actual Clean (0)", "Actual Suspicious (1)"],
    columns=["Pred Clean (0)", "Pred Suspicious (1)"]
)

print("Confusion Matrix:")
print(cm_df)

print("\nAccuracy :", round(acc, 4))
print("Precision:", round(prec, 4))
print("Recall   :", round(rec, 4))
print("F1 Score :", round(f1, 4))