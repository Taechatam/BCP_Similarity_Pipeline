import pandas as pd
from sklearn.metrics import roc_curve, auc, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import os

# === CONFIG ===
custom_threshold = None  # Example: 0.65, or keep None for best threshold

# === LABEL MAPPING ===
LABEL_MAP = {"sensitive": 0, "resistant": 1}
LABEL_MAP_INV = {v: k for k, v in LABEL_MAP.items()}  # {0: "sensitive", 1: "resistant"}

# Load CSV
df = pd.read_csv(r"C:\Workspace\Thesis\coding\Github_test\output6_ROC\combined_all_data_ROC.csv")

# After loading the CSV, validate before proceeding
assert "sample_profile" in df.columns, "Column 'sample_profile' not found in CSV"
assert "similarity" in df.columns, "Column 'similarity' not found in CSV"

# Check for unmapped labels (typos, unexpected values)
unexpected = set(df["sample_profile"].unique()) - set(LABEL_MAP.keys())
assert not unexpected, f"Unexpected label values found: {unexpected}"

# Check for NaNs
assert not df[["similarity", "sample_profile"]].isnull().any().any(), "NaN values detected in data"

# Extract scores and labels — map string labels to 0/1
similarity_scores = df["similarity"].values
labels = df["sample_profile"].map(LABEL_MAP).values  # "sensitive" -> 0, "resistant" -> 1

# Compute ROC curve
fpr, tpr, thresholds = roc_curve(labels, similarity_scores)

# Compute Youden's Index
youden_index = tpr - fpr
best_index = np.argmax(youden_index)
best_threshold = thresholds[best_index]

# AUC
roc_auc = auc(fpr, tpr)


def compute_fpr_tpr(y_true, y_scores, threshold):
    preds = (y_scores >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, preds).ravel()
    fpr_val = fp / (fp + tn) if (fp + tn) > 0 else 0
    tpr_val = tp / (tp + fn) if (tp + fn) > 0 else 0
    return fpr_val, tpr_val


# Compute custom threshold's actual ROC point
if custom_threshold is not None:
    custom_fpr, custom_tpr = compute_fpr_tpr(labels, similarity_scores, custom_threshold)

# Decide which threshold to use
if custom_threshold is not None:
    chosen_threshold = custom_threshold
    print(f"⚡ Using custom threshold: {chosen_threshold:.4f}")
else:
    chosen_threshold = best_threshold
    print(f"⚡ Using best threshold (Youden's Index): {chosen_threshold:.4f}")

# Convert scores to predictions (0 = sensitive, 1 = resistant)
predictions = (similarity_scores >= chosen_threshold).astype(int)

# Map numeric predictions back to string labels for display
pred_labels = pd.Series(predictions).map(LABEL_MAP_INV)
true_labels = pd.Series(labels).map(LABEL_MAP_INV)

# Calculate metrics (positive class = 1 = resistant)
accuracy  = accuracy_score(labels, predictions)
precision = precision_score(labels, predictions, zero_division=0)
recall    = recall_score(labels, predictions, zero_division=0)
f1        = f1_score(labels, predictions, zero_division=0)

# Print results
print(f"\nLabel mapping  : sensitive = 0  |  resistant = 1")
print(f"Threshold      : {chosen_threshold:.4f}")
print(f"Youden's Index : {youden_index[best_index]:.4f}  (at best threshold)")
print(f"AUC            : {roc_auc:.4f}")
print(f"Accuracy       : {accuracy:.4f}")
print(f"Precision      : {precision:.4f}  (resistant class)")
print(f"Recall (Sens.) : {recall:.4f}   (resistant class)")
print(f"F1 Score       : {f1:.4f}")

# Count predictions per class
pred_counts = pred_labels.value_counts().to_dict()
true_counts = true_labels.value_counts().to_dict()
print(f"\nTrue label counts    : {true_counts}")
print(f"Predicted label counts: {pred_counts}")

# Save results CSV
results = pd.DataFrame({
    "Threshold_Used":    [chosen_threshold],
    "Best_Threshold":    [best_threshold],
    "Youden_Index_Best": [youden_index[best_index]],
    "AUC":               [roc_auc],
    "Accuracy":          [accuracy],
    "Precision_Resistant":        [precision],
    "Recall_Resistant":           [recall],
    "F1_Score_Resistant":         [f1],
    "Label_Sensitive":   [0],
    "Label_Resistant":   [1],
})

output_dir = r"C:\Workspace\Thesis\coding\Github_test\output6_ROC"
os.makedirs(output_dir, exist_ok=True)


roc_df = pd.DataFrame({"FPR": fpr, "TPR": tpr, "Threshold": thresholds}) #FPR = false positive rate, TPR = true positive rate

results_path = os.path.join(output_dir, 'ATCC17978_roc_25_results.csv')
results.to_csv(results_path, index=False)
print(f"\nResults saved to: {results_path}")

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.4f})', lw=2)
plt.scatter(fpr[best_index], tpr[best_index], color='red', zorder=5,
            label=f'Best Thresh = {best_threshold:.4f} (Youden)')
if custom_threshold is not None:
    plt.scatter(custom_fpr, custom_tpr, color='blue', zorder=5,
                label=f'Custom Thresh = {custom_threshold:.4f}')

# Add threshold annotations directly on the plot
plt.annotate(f'{best_threshold:.3f}', 
             xy=(fpr[best_index], tpr[best_index]),
             xytext=(fpr[best_index] + 0.05, tpr[best_index] - 0.05),
             fontsize=8, color='red')

plt.plot([0, 1], [0, 1], 'k--', lw=1, label='Random Classifier')
plt.xlim([0, 1])
plt.ylim([0, 1.02])
plt.xlabel('False Positive Rate (1 − Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.title('ROC Curve — Sensitive (0) vs Resistant (1)')
plt.legend(loc='lower right', fontsize=8)
plt.grid(alpha=0.3)
plt.tight_layout()

plot_path = os.path.join(output_dir, 'ATCC17978_roc_curve.png')
plt.savefig(plot_path, dpi=600)
plt.show()
print(f"Plot saved to: {plot_path}")