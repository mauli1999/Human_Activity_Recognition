model_test = joblib.load("/content/trained_random_forest_model.pkl")

file_path = "/content/sensor_data.txt" 
data = pd.read_csv(file_path, skiprows=1, names=["Timestamp", "x", "y", "z"], sep=",")

# Apply preprocessing to the relevant columns
data['x'] = data['x'].apply(preprocess_data)
data['y'] = data['y'].apply(preprocess_data)
data['z'] = data['z'].apply(preprocess_data)

predicted_activities_rf = model_test.predict(phone_accel_data[['x', 'y', 'z']])

print(predicted_activities_rf)

# Define the activity key
activity_key = {
    'A': 'walking',
    'B': 'jogging',
    'C': 'stairs',
    'D': 'sitting',
    'E': 'standing',
    'F': 'typing',
    'G': 'teeth',
    'H': 'soup',
    'I': 'chips',
    'J': 'pasta',
    'K': 'drinking',
    'L': 'sandwich',
    'M': 'kicking',
    'O': 'catch',
    'P': 'dribbling',
    'Q': 'writing',
    'R': 'clapping',
    'S': 'folding'
}

predicted_activities_mapped_rf = []
for activity in predicted_activities_rf:
    if activity in activity_key:
        predicted_activities_mapped_rf.append(activity_key[activity])
    else:
        predicted_activities_mapped_rf.append("Unknown")

# Calculate activity durations for RF model
activity_durations_rf = []
current_activity_rf = predicted_activities_mapped_rf[0]
start_timestamp_rf = data.iloc[0]['Timestamp']

for i in range(1, len(predicted_activities_mapped_rf)):
    if predicted_activities_mapped_rf[i] != current_activity_rf:
        end_timestamp_rf = data.iloc[i-1]['Timestamp']
        activity_durations_rf.append((current_activity_rf, start_timestamp_rf, end_timestamp_rf))
        current_activity_rf = predicted_activities_mapped_rf[i]
        start_timestamp_rf = data.iloc[i]['Timestamp']

# Add the last activity duration for RF model
activity_durations_rf.append((current_activity_rf, start_timestamp_rf, data.iloc[-1]['Timestamp']))

# Output activity predictions and durations for RF model
for activity_rf, start_rf, end_rf in activity_durations_rf:
    duration_rf = end_rf - start_rf
    print(f"Activity predicted using RF model: {activity_rf}, Start: {start_rf}, End: {end_rf}, Duration: {duration_rf}")

# Dictionary to store total durations for each activity from RF model
total_durations_rf = {}

# Calculate total durations for each activity from RF model
for activity_rf, start_rf, end_rf in activity_durations_rf:
    duration_seconds_rf = (end_rf - start_rf) / 1_000_000  # Convert microseconds to seconds
    duration_minutes_rf = duration_seconds_rf / 60  # Convert seconds to minutes
    if activity_rf in total_durations_rf:
        total_durations_rf[activity_rf] += max(duration_minutes_rf, 0)  # Ensure duration is not negative
    else:
        total_durations_rf[activity_rf] = max(duration_minutes_rf, 0)  # Ensure duration is not negative

# Output total time spent on each activity from RF model in hours, minutes, and seconds format
for activity_rf, total_duration_rf in total_durations_rf.items():
    hours_rf = int(total_duration_rf // 60)
    minutes_rf = int(total_duration_rf % 60)
    seconds_rf = int((total_duration_rf - int(total_duration_rf)) * 60)
    print(f"Activity: {activity_rf}, Duration: {hours_rf}:{minutes_rf}:{seconds_rf}")

activity_dict = {
    "Activity": activity_rf,
    "Duration": f"{hours_rf}:{minutes_rf}:{seconds_rf}"
}

