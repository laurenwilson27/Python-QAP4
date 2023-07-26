"""
Software Development 9
QAP 4, Project 1: Sales Plot
Author: Lauren Wilson

Description: A program for a nonspecific company which requests sales per month from the user.
                Once all twelve months have been entered, displays a basic graph of sales for each
                month. Months with 0 sales are excluded from the plot.
"""

import matplotlib.pyplot as plt
import calendar

monthLabels = []
salesPerMonth = []

print()

# Iterate across the twelve months
for i in range(1, 13):
    monthLabels.append(calendar.month_abbr[i])

    # Get user input, add it to the sales list
    while True:
        try:
            # Use the 'calendar' module to find the name for each month
            sales = float(input("Enter the total sales for "+calendar.month_name[i]+": $"))
        except:
            print("Sales must be a valid number.")
        else:
            if sales < 0:
                print("Sales cannot be negative.")
            else:
                break
    # If sales were zero, set the sales variable to None before adding it to the list
    # (When displayed on a plot, None is hidden)
    if sales == 0.00:
        sales = None
    salesPerMonth.append(sales)

# Define the plot - we can use the 'calendar' module to retrieve a list of months for the x axis
# (The first month in the list is a blank month, so we slice the list to exclude it)
plt.plot(calendar.month_abbr[1:], salesPerMonth)

# Set up some labels for our graph
plt.title("Total Sales per Month")

plt.xlabel("Month")
plt.ylabel("Sales ($)")

# Display the plot in a window
plt.show()
