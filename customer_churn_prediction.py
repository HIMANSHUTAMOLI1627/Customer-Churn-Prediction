# -*- coding: utf-8 -*-
"""Customer churn prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KbqrtEF1USPSeBGZhxCNSphFSKa_g_6m
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

df = pd.read_csv("/content/Churn_Modelling.csv")

df.head()

#dropping useless columns
df.drop(columns=['Surname', 'RowNumber', 'CustomerId'], inplace=True)

df.info()

df["Geography"].unique()

#One-hot encoding
df = pd.get_dummies(df, columns = ['Geography','Gender'], drop_first = True)

df.head()

df["Exited"].value_counts().plot(kind = "bar")
plt.xticks(rotation=0)

not_Exited = df[df["Exited"] == 0]
Exited = df[df["Exited"] == 1]

print(not_Exited.shape[0])
print(Exited.shape[0])

not_Exited = not_Exited.sample(Exited.shape[0], random_state=42)

df_new = pd.concat([not_Exited , Exited])

df_new["Exited"].value_counts().plot(kind = "bar")
plt.xticks(rotation=0)

corr = df_new.corr()

plt.figure(figsize = (16, 9))
sns.heatmap(corr, annot = True)

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

X = df_new.drop(columns = "Exited" , axis = 1)
y = df_new["Exited"]

from sklearn.preprocessing import StandardScaler

columns = df_new.columns.tolist()
columns.remove('Exited')

scaler = StandardScaler()

X[columns] = scaler.fit_transform(X[columns])
df_new[X.columns] = X
df_new

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the models
models = {
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(random_state=18),
    'Gradient Boosting': GradientBoostingClassifier()
}

# Function to evaluate models
def evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    return accuracy, precision, recall, f1

# Evaluate each model
results = {}
for name, model in models.items():
    accuracy, precision, recall, f1 = evaluate_model(model, X_train, y_train, X_test, y_test)
    results[name] = {
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1
    }
# Create a DataFrame to display the results
results_df = pd.DataFrame(results).T
results_df

Gradient_model = GradientBoostingClassifier()
Gradient_model.fit(X_train, y_train)

from sklearn.metrics import confusion_matrix, classification_report
# Print confusion matrix and classification report
y_pred = Gradient_model.predict(X_test)
conf_matrix = confusion_matrix(y_test, y_pred)
print('Confusion Matrix:')
print(conf_matrix)
print('\nClassification Report:')
print(classification_report(y_test, y_pred))

# Create a heatmap of the confusion matrix
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d',cmap = 'Blues', xticklabels=['Not Exited', 'Exited'], yticklabels=['Not Exited', 'Exited'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix Heatmap')
plt.show()