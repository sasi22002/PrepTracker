import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from collections import defaultdict
import io, base64
import numpy as np
from models import Interview

def get_consecutive_dates(start_date, end_date):
    """Generate consecutive dates between start_date and end_date"""
    consecutive_dates = []
    current_date = start_date
    
    while current_date <= end_date:
        consecutive_dates.append(current_date)
        current_date += timedelta(days=1)

    return consecutive_dates

def plot_interview_status():
    try:
        weekstart = datetime(year=2024, month=9, day=20)
        current = datetime.now()
        
        # Calculate the number of days between the weekstart and the current date
        days = current - weekstart
        
        # Fetch all interview data
        int_data = Interview.query.filter_by(is_deleted=False).all()

        if days.days > len(int_data):
            # Get consecutive dates from weekstart to current
            dates = get_consecutive_dates(weekstart, current)

            # Generate xpoints and ypoints based on interview data
            ypoints = np.array([i.date.day for i in int_data])
            xpoints = ypoints
        else:
            return None  # If no data, return None or handle accordingly
        
        # Create a new figure
        plt.figure()

        # Loop through each interview data point and plot with a condition-based color
        for x, interview in zip(xpoints, int_data):
            if interview.status == 'Passed':
                plt.plot(x, interview.date.day, marker='o', color='green', label='Passed')
            elif interview.status == 'Failed':
                plt.plot(x, interview.date.day, marker='o', color='red', label='Failed')
            elif interview.status == 'WaitingList':
                plt.plot(x, interview.date.day, marker='o', color='blue', label='WaitingList')
            else:
                plt.plot(x, interview.date.day, marker='o', color='gray', label='Not Scheduled')

        # Set x-axis tick marks for all days of the month
        plt.xticks([i*7 for i in range(0, 6)])
        plt.yticks([i*2 for i in range(0, 16)])

        # Add labels and a title
        plt.title('Interview Status Plot')
        plt.xlabel('Week of the Month')
        plt.ylabel('Interview Day')
        
        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()

        # Return the image as a base64 string
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return image_base64
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def mm():
    """Alternative plotting function for weekly interview status"""
    try:
        # Get the current date and the date for 7 days ago
        today = datetime.now().date()
        week_start = today - timedelta(days=7)

        # Query interviews for the last week
        interviews = Interview.query.filter(
            Interview.date >= week_start,
            Interview.date <= today,
            Interview.is_deleted == False
        ).all()

        # Prepare data for plotting
        status_counts = defaultdict(lambda: {'passed': 0, 'failed': 0})

        for interview in interviews:
            week = interview.date.isocalendar()[1]  # Get the week number
            if interview.status.lower() == 'passed':
                status_counts[week]['passed'] += 1
            else:
                status_counts[week]['failed'] += 1

        # Prepare x and y data for plotting
        weeks = list(status_counts.keys())
        passed_counts = [status_counts[week]['passed'] for week in weeks]
        failed_counts = [status_counts[week]['failed'] for week in weeks]

        # Plotting
        plt.figure(figsize=(10, 6))

        bar_width = 0.35
        index = range(len(weeks))

        # Create bar plots for passed and failed
        plt.bar(index, passed_counts, bar_width, label='Passed', color='green')
        plt.bar([i + bar_width for i in index], failed_counts, bar_width, label='Failed', color='red')

        # Adding labels and titles
        plt.xlabel('Week')
        plt.ylabel('Number of Interviews')
        plt.title('Interview Status by Week')
        plt.xticks([i + bar_width / 2 for i in index], weeks)
        plt.legend()

        # Save plot to a BytesIO object and encode it as a base64 string
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()  # Close the plot to free up memory
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return image_base64

    except Exception as e:
        print(f"Error: {e}")
        return None
