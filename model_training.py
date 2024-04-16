# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from sklearn.preprocessing import StandardScaler
from google.colab import files

# Define the directory path containing the text files
data_path = "/content/data"

text_files = [file for file in os.listdir(data_path) if file.endswith('.txt')]
data_frames = []

# Iterate over each text file, read it, and append it to the list
for file in text_files:
    file_path = os.path.join(data_path, file)
    data_frames.append(pd.read_csv(file_path, header=None, names=["Subject-id", "Activity", "Timestamp", "x", "y", "z"], sep=","))

combined_data = pd.concat(data_frames, ignore_index=True)
print(combined_data.head())


selected_activities = ['A', 'D', 'E']

# Filter rows with selected activities
filtered_data = combined_data[combined_data['Activity'].isin(selected_activities)]
print(filtered_data)

rows, columns = filtered_data.shape
print("filtered_data Data (Rows, Columns):", rows, columns)

if len(filtered_data) < 2:
    print("Insufficient data for train-test split.")
else:
    X_train = filtered_data[["x", "y", "z"]]
    y_train = filtered_data["Activity"]
    X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

def preprocess_data(data):
    try:
        # Try converting to float directly
        return float(data)
    except ValueError:
        try:
            # Handle the case where the data contains non-numeric characters
            return float(data[:-1])  # Remove the last character (semicolon)
        except ValueError:
            # If it still fails, return NaN
            return float('nan')

# Apply preprocessing to the relevant columns in X_train and X_test
X_train['x'] = X_train['x'].apply(preprocess_data)
X_train['y'] = X_train['y'].apply(preprocess_data)
X_train['z'] = X_train['z'].apply(preprocess_data)

X_test['x'] = X_test['x'].apply(preprocess_data)
X_test['y'] = X_test['y'].apply(preprocess_data)
X_test['z'] = X_test['z'].apply(preprocess_data)

# Step 4: Build and Train the Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np


y_pred = model.predict(X_test)

# Compute confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(len(np.unique(y_test)))
plt.xticks(tick_marks, np.unique(y_test), rotation=45)
plt.yticks(tick_marks, np.unique(y_test))

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > cm.max() / 2. else "black")

plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.tight_layout()
plt.show()

# Step 5: Evaluate the Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print(f"Classification Report:\n{report}")

joblib.dump(model, "/content/trained_random_forest_model.pkl")