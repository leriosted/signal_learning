from datetime import datetime, timedelta
from icalendar import Calendar, Event

# Initialize calendar
cal = Calendar()

# Start date for the lecture series
start_date = datetime(2025, 1, 13)
weeks = 12
days_per_week = 3  # Assuming 3 lectures per week (e.g., Mon, Wed, Fri)

# Topics for each week
topics = [
    "Introduction to Signals and Systems",
    "Time-Domain Analysis of Signals",
    "Fourier Series and Fourier Transform",
    "Laplace Transform and Applications",
    "State-Space Representation",
    "Sampling Theorem and Discrete-Time Signals",
    "Z-Transform and Discrete-Time Systems",
    "Frequency Response and Bode Plots",
    "Stability Analysis in Frequency Domain",
    "Mechanical Systems Modeling in Frequency Domain",
    "Advanced Topics: Nonlinear Systems & Signal Modulation",
    "Review and Case Studies"
]

# Learning objectives for each week
learning_objectives = [
    "Understand the basic concepts of signals and systems, types of signals, and system classifications.",
    "Analyze signals in the time domain, including impulse and step responses.",
    "Learn Fourier series and Fourier transform for continuous-time signal analysis.",
    "Apply Laplace transform to solve differential equations and analyze systems.",
    "Introduce state-space representation and its applications in mechanical systems.",
    "Understand the sampling theorem and how to represent discrete-time signals.",
    "Learn Z-transform for discrete-time system analysis and solve difference equations.",
    "Analyze the frequency response of systems and understand Bode plots.",
    "Study stability in the frequency domain using Nyquist and Bode criteria.",
    "Model mechanical systems in the frequency domain and understand resonance.",
    "Explore advanced topics, including nonlinear systems and signal modulation techniques.",
    "Consolidate learning through review sessions and case studies."
]

# Schedule creation loop
current_date = start_date
for week in range(weeks):
    for day in range(days_per_week):
        event = Event()
        event.add('summary', f'Lecture {week * days_per_week + day + 1}: {topics[week]}')
        event.add('dtstart', current_date)
        event.add('dtend', current_date + timedelta(hours=1))  # Assuming 1-hour lecture
        event.add('description', f'Learning Objectives: {learning_objectives[week]}')
        cal.add_component(event)
        current_date += timedelta(days=2)  # Assuming lectures on alternate days (Mon, Wed, Fri)

# Save calendar to file
with open('Signals_and_Systems_Lecture_Schedule.ics', 'wb') as f:
    f.write(cal.to_ical())

print("Calendar file 'Signals_and_Systems_Lecture_Schedule.ics' has been created.")
