import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from collections import defaultdict
import io, base64
import numpy as np
from models import Interview
from dbhelper import statistics_db

# Set matplotlib style for better looking plots
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

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

def plot_status_pie_chart():
    """Generate a pie chart showing interview status distribution with proper color coding"""
    try:
        stats = statistics_db.get_interview_statistics()
        status_breakdown = stats.get('status_breakdown', {})
        
        if not status_breakdown:
            return None
        
        # Define colors based on status categories
        def get_status_color(status):
            positive_statuses = ['Offered', 'Passed', 'Selected', 'Joined']
            negative_statuses = ['Rejected', 'Failed', 'Withdrawn']
            
            if status in positive_statuses:
                return '#28a745'  # Green
            elif status in negative_statuses:
                return '#dc3545'  # Red
            else:
                return '#ffc107'  # Yellow/Orange for neutral
        
        # Prepare data with colors
        labels = list(status_breakdown.keys())
        sizes = list(status_breakdown.values())
        colors = [get_status_color(status) for status in labels]
        
        # Create pie chart with better styling
        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                          autopct='%1.1f%%', startangle=90, 
                                          textprops={'fontsize': 10, 'fontweight': '500'},
                                          wedgeprops={'edgecolor': 'white', 'linewidth': 2})
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        plt.title('Interview Status Distribution (Normalized)', fontsize=16, fontweight='bold', pad=20)
        
        # Add legend
        ax.legend(wedges, labels, title="Status", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Save plot to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=120)
        plt.close()
        
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return image_base64
        
    except Exception as e:
        print(f"Error in pie chart: {e}")
        return None

def plot_monthly_trend():
    """Generate a line chart showing interview trends over months"""
    try:
        stats = statistics_db.get_interview_statistics()
        monthly_breakdown = stats.get('monthly_breakdown', {})
        
        if not monthly_breakdown:
            return None
        
        # Prepare data
        months = sorted(monthly_breakdown.keys())
        counts = [monthly_breakdown[month] for month in months]
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(months, counts, marker='o', linewidth=3, markersize=8, 
                color='#667eea', markerfacecolor='#764ba2')
        
        ax.set_title('Interview Trend Over Time', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Number of Interviews', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return image_base64
        
    except Exception as e:
        print(f"Error in monthly trend chart: {e}")
        return None

def plot_company_distribution():
    """Generate a bar chart showing interview distribution by company"""
    try:
        stats = statistics_db.get_interview_statistics()
        company_breakdown = stats.get('company_breakdown', {})
        
        if not company_breakdown:
            return None
        
        # Take top 10 companies
        sorted_companies = sorted(company_breakdown.items(), key=lambda x: x[1], reverse=True)[:10]
        
        if not sorted_companies:
            return None
        
        # Prepare data
        companies = [item[0] for item in sorted_companies]
        counts = [item[1] for item in sorted_companies]
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(companies, counts, color='#667eea')
        
        # Add value labels on bars
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                   str(count), va='center', fontsize=10)
        
        ax.set_title('Interview Distribution by Company', fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Number of Interviews', fontsize=12)
        ax.set_ylabel('Company', fontsize=12)
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        # Save plot to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return image_base64
        
    except Exception as e:
        print(f"Error in company distribution chart: {e}")
        return None
