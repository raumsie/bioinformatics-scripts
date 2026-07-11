import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
# 1. Read training and test datasets
train_df = pd.read_csv("iris_training.csv")
test_df = pd.read_csv("iris_test.csv")

#print(test_df)

# 2. Prepare inputs (X) and labels (y)
X_train = train_df.iloc[:, :-1].values
y_train = train_df.iloc[:, -1]
# Encode class labels as numbers
le = LabelEncoder()
y_train_enc = le.fit_transform(y_train)
# 3. Create and train the model
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train_enc)
# 4. Predict labels for test set
X_test = test_df.iloc[:, :-1].values
actual_labels = test_df.iloc[:, -1].values
pred_labels = model.predict(X_test)
predicted_species = le.inverse_transform(pred_labels)
# 5. Print results
'''
print("X_train:")
print(X_train)
print("-" * 30)
print("y_train:")
print(y_train)
print("-" * 30)
'''

'''
print("y_train_enc:")
print(y_train_enc)
'''
print("\nPredictions vs Actual Labels:\n")
print("Row\tPredicted\t\t\tActual")
print("-------------------------------------------")
for i in range(len(predicted_species)):
    print(f"{i+1}\t{predicted_species[i]}\t\t\t{actual_labels[i]}")