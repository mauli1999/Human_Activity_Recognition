// Sample data
const activityData = [
    { Activity: 'standing', Duration: '0:7:33' },
    { Activity: 'walking', Duration: '0:2:32' },
    { Activity: 'sitting', Duration: '0:24:20' }
];

// Function to display completed duration and calculate progress
function updateProgress(activityData, selectedActivity) {
    const completedSpan = document.getElementById('completed');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');

    // Find the selected activity's duration
    const selectedActivityData = activityData.find(activity => activity.Activity === selectedActivity);
    const selectedActivityDuration = selectedActivityData ? selectedActivityData.Duration : '0:00:00';

    // Parse duration from selected activity data and calculate total minutes
    const durationParts = selectedActivityDuration.split(':');
    const totalMinutes = parseInt(durationParts[0]) * 60 + parseInt(durationParts[1]);

    // Display completed duration
    completedSpan.textContent = selectedActivityDuration;

    // Get the target duration
    const targetDuration = parseInt(document.getElementById('targetDuration').value, 10);

    // Calculate progress percentage
    const progressPercent = (totalMinutes / targetDuration) * 100;
    progressFill.style.width = progressPercent + '%';

    // Update progress text
    progressText.textContent = progressPercent.toFixed(2) + '% completed';
}

// Call the function with sample data and initial selected activity
const initialSelectedActivity = document.getElementById('activity').value;
updateProgress(activityData, initialSelectedActivity);

// Add event listener to activity select
const activitySelect = document.getElementById('activity');
activitySelect.addEventListener('change', function() {
    const selectedActivity = this.value;
    updateProgress(activityData, selectedActivity);
});

// Add event listener to target duration select
const targetDurationSelect = document.getElementById('targetDuration');
targetDurationSelect.addEventListener('change', function() {
    const selectedActivity = document.getElementById('activity').value;
    updateProgress(activityData, selectedActivity);
});
