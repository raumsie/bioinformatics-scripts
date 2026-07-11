from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.utils import class_weight
from sklearn.feature_extraction.text import CountVectorizer

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

'''
LogisticRegression just predicts 0 every time,
so I found a different model (Random Forest)
'''


#training_data = pd.read_csv(DATA_DIR / "human_training_data.csv", sep='\t', dtype={'a': bool, 'b': str, 'c': str})

# Header=None prevents first row from being treated as labels
training_data = pd.read_fwf(DATA_DIR / "human_training_data.csv", header=None)
if training_data.empty:
    print("Training data not found.")
else:
    print("Training data loaded.")

test_human = pd.read_fwf(DATA_DIR / "human_test_data.csv", header=None)
test_mouse = pd.read_fwf(DATA_DIR / "mouse_test_data.csv", header=None)

label_train = training_data.iloc[:, 0].tolist()
#print(label_train)

RNA_train = training_data.iloc[:, 1].tolist()
#print(RNA_train)

target_train = training_data.iloc[:, 2].tolist()
#print(target_train)
#print(len(target_train))

#le = LabelEncoder()


# For microRNA sequences that are shorter than 25 characters, use
# a matrix of [0, 0, 0, 0] to make the sum of characters 25
# zeroes can be at start or end, but must be consistent between data

def seq_to_matrix(sequences, max_length=25):
    letter_to_index = {'A': 0, 'C': 1, 'G': 2, 'U': 3}
    features_list = []

    for seq in sequences:
        # convert sequence to matrix
        features = []
        # one hot encoding converts categorical data into numerical
        one_hot = []
        for i in range(max_length):
            if i < len(seq):
                letter = seq[i]
                matrix = [0, 0, 0, 0]
                if letter in letter_to_index:
                    matrix[letter_to_index[letter]] = 1
                one_hot.extend(matrix)
            else:
                # Pad with zeros
                one_hot.extend([0, 0, 0, 0])

        features.extend(one_hot)

        # sequence length
        features.append(len(seq))

        # letter percentages
        total = max(len(seq), 1)
        for letter in 'ACGU':
            features.append(seq.count(letter) / total)

        # High GC content makes bonding more likely
        gc_content = (seq.count('G') + seq.count('C')) / total
        features.append(gc_content)

        features_list.append(features)


    return np.array(features_list)


# Convert training data to matrices
RNA_train_matrix = seq_to_matrix(RNA_train)
target_train_matrix = seq_to_matrix(target_train)

# Combine microRNA & target matrices
x_train_human = np.hstack([RNA_train_matrix, target_train_matrix])
y_train_human = np.array(label_train)


# Prepare test data
label_test = test_human.iloc[:, 0].tolist()
RNA_test = test_human.iloc[:, 1].tolist()
target_test = test_human.iloc[:, 2].tolist()

# Convert test data to matrices
RNA_test_matrix = seq_to_matrix(RNA_test)
target_test_matrix = seq_to_matrix(target_test)
x_test_human = np.hstack([RNA_test_matrix, target_test_matrix])
y_test_human = np.array(label_test)

# Prepare mouse data
label_test_mouse = test_mouse.iloc[:, 0].tolist()
RNA_test_mouse = test_mouse.iloc[:, 1].tolist()
target_test_mouse = test_mouse.iloc[:, 2].tolist()

# Convert mouse test data to matrices
RNA_test_mouse_matrix = seq_to_matrix(RNA_test_mouse)
target_test_mouse_matrix = seq_to_matrix(target_test_mouse)
x_test_mouse = np.hstack([RNA_test_mouse_matrix, target_test_mouse_matrix])
y_test_mouse = np.array(label_test_mouse)


# Weights to handle label imbalance
# Without weights, the models will predict 0 every time
class_weights = class_weight.compute_class_weight(
    'balanced',
    classes = np.unique(y_train_human),
    y=y_train_human
)
class_weight_dict = {0: class_weights[0], 1: class_weights[1]}
print(f"Class weights: {class_weight_dict}")

# Create & train model
rand_forest = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=33,
    class_weight=class_weight_dict
)
rand_forest.fit(x_train_human, y_train_human)

y_pred = rand_forest.predict(x_test_human)
y_pred_probs = rand_forest.predict_proba(x_test_human)

y_pred_mouse = rand_forest.predict(x_test_mouse)
y_pred_probs_mouse = rand_forest.predict_proba(x_test_mouse)

print("Training Logistic Regression model...")
logistic_reg = LogisticRegression(
    max_iter=1000,
    random_state=22,
    class_weight=class_weight_dict,
    C=0.1,
    penalty='l2'
)
logistic_reg.fit(x_train_human, y_train_human)

# Make predictions with Logistic Regression
y_pred_lr = logistic_reg.predict(x_test_human)
accuracy_lr = accuracy_score(y_test_human, y_pred_lr)


print("Human Test:")
print("Row\tPredicted\tActual\tP")
print("-" * 30)
for i in range(len(y_pred)):
    prob_bind = y_pred_probs[i][1]
    print(f"{i+1}\t{y_pred[i]}\t\t{y_test_human[i]}\t{prob_bind:.3f}")

# Calculate accuracy
accuracy = (y_pred == y_test_human).mean()
print(f"Accuracy: {accuracy:.4f}")

print("-" * 30)
print("Mouse Test:")
print("Row\tPredicted\tActual\tP")
print("-" * 30)
for i in range(len(y_pred_mouse)):
    prob_bind = y_pred_probs_mouse[i][1]
    print(f"{i+1}\t{y_pred_mouse[i]}\t\t{y_test_mouse[i]}\t{prob_bind:.3f}")

# Calculate accuracy
accuracy = (y_pred_mouse == y_test_mouse).mean()
print(f"Accuracy: {accuracy:.4f}")

print(f"Logistic Regression Accuracy: {accuracy_lr:.4f}")