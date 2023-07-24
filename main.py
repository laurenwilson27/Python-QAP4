"""
Commentary
"""

import datetime
import math
# Using Maurice's FormatValues.py
import FormatValues as fv

# Define a list of provinces for validation later
# (Never know when we'll get a new territory!)
PROVINCES = ["AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", "QC", "SK", "YT"]


def askYorN(prompt):
    # Add a (Y/N): to the prompt, and ensure that the answer is "Y" or "N"
    while True:
        response = input(prompt + " (Y/N): ").upper()
        if response in ["Y", "N"]:
            return response
        else:
            print("Input must be Y or N")


def fmtCenterText(text, width):
    # Find the amount of whitespace needed to centre the given text over the given width
    # Returns the text with the appropriate amount of whitespace added to the left
    whitespace = width - len(text)
    return math.floor(whitespace / 2) * " " + text


# Load default values from a file
file = open("OSICDef.dat", "r")

NEXT_POLICY_NUM = int(file.readline())
BASIC_PREMIUM = float(file.readline())
ADD_CARS_DISCOUNT = float(file.readline())
LIABILITY_COV_COST = float(file.readline())
GLASS_COV_COST = float(file.readline())
LOAN_COV_COST = float(file.readline())
HST_RATE = float(file.readline())
PROC_FEE = float(file.readline())

# Close the file after defaults are read
file.close()

while True:
    # Ask user for customer info
    firstName = input("Enter the customer's first name: ").title()
    lastName = input("Enter the customer's last name: ").title()
    custAddr = input("Enter the address: ")
    custCity = input("Enter the city: ").title()
    # Customer province will be validated against a list of province codes
    while True:
        custProvince = input("Enter the province code: ").upper()
        if custProvince not in PROVINCES:
            print("You must enter a valid two-letter province code.")
        else:
            break
    custPostal = input("Enter the postal code: ").upper()
    custPhone = input("Enter the phone number: ")
    carCount = int(input("Enter the number of cars being insured: "))

    # Ask yes/no questions using a function for validation
    optExtraLiability = askYorN("Add extra liability up to $1,000,000?")
    optGlassCover = askYorN("Add optional glass coverage?")
    optLoanCar = askYorN("Add optional loaner car?")

    # Ask for the payment method, and validate it
    while True:
        paymentType = input("Enter the payment method (Monthly/Full): ").title()
        if paymentType not in ["Monthly", "Full"]:
            print("Payment method must be Monthly or Full.")
        else:
            break

    # Calculate the insurance premium using the default values
    basicPremium = BASIC_PREMIUM
    # Each car beyond the first is discounted
    basicPremium += (carCount - 1) * BASIC_PREMIUM * (1 - ADD_CARS_DISCOUNT)

    # Add extra optional costs
    extraCosts = 0.00
    if optExtraLiability == "Y":
        extraCosts += LIABILITY_COV_COST
    if optGlassCover == "Y":
        extraCosts += GLASS_COV_COST
    if optLoanCar == "Y":
        extraCosts += LOAN_COV_COST

    # Calculate premium, find the taxes-in cost
    totalPremium = basicPremium + extraCosts
    hst = totalPremium * HST_RATE
    totalCost = totalPremium + hst

    # Calculate monthly payment
    monthlyPayment = (totalCost + PROC_FEE) / 8

    # Find today's date, find 'the first of next month' by finding the first day of the current
    #   month, adding a month's worth of time, and finding the first day of the resulting month
    dateToday = datetime.date.today()
    dateNextPayment = (dateToday.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)

    # Print the receipt header
    print()
    print(fmtCenterText("One Stop Insurance Company", 60))
    print(fmtCenterText("Sales Receipt", 60))
    print("_" * 60)

    # Print the customer information onto the receipt
    print("  Customer Name: " + firstName + " " + lastName)
    print("  Address:       " + custAddr)
    print("                 " + custCity + ", " + custProvince)
    print("                 " + custPostal)
    print("  Phone Number:  " + custPhone)
    print()
    print()

    # Print values and costs incurred
    print("  Vehicles insured: " + str(carCount) + ' ' * 24 + f"{fv.FDollar2(basicPremium):>12s}")
    if optExtraLiability == "Y":
        print("  Extra liability:  Yes" + ' ' * 22 + f"{fv.FDollar2(LIABILITY_COV_COST):>12s}")
    else:
        print("  Extra liability:  No " + ' ' * 29 + "$0.00")

    if optGlassCover == "Y":
        print("  Glass coverage:   Yes" + ' ' * 22 + f"{fv.FDollar2(GLASS_COV_COST):>12s}")
    else:
        print("  Glass coverage:   No " + ' ' * 29 + "$0.00")

    if optLoanCar == "Y":
        print("  Loaner car:       Yes" + ' ' * 22 + f"{fv.FDollar2(LOAN_COV_COST):>12s}")
    else:
        print("  Loaner car:       No " + ' ' * 29 + "$0.00")

    # Print subtotals, taxes, etc.
    # print(" " * 27 + "_" * 33)
    print("{:>45}".format("Total extra costs:") + f"{fv.FDollar2(extraCosts):>12s}")
    print("{:>45}".format("Total premium:    ") + f"{fv.FDollar2(totalPremium):>12s}")
    print("{:>45}".format("Sales tax:        ") + f"{fv.FDollar2(hst):>12s}")
    print(" "*48+"-"*12)
    print("{:>45}".format("Total cost:       ") + f"{fv.FDollar2(totalCost):>12s}")
    print("_" * 60)
    print("  Payment plan selected: " + f"{paymentType:<10s}")
    if paymentType == "Monthly":
        print("  Monthly payment:       " + fv.FDollar2(monthlyPayment))
    else:
        print("  Full payment:          " + fv.FDollar2(totalCost))
    print()
    print("  Invoice Date:          " + str(dateToday))
    print("  Next Payment Date:     " + str(dateNextPayment))
    print()

    # Create a list of information to be stored in the policies file
    storedValues = [NEXT_POLICY_NUM, dateToday, firstName, lastName,
                    custAddr, custCity, custProvince, custPostal, custPhone,
                    carCount, optExtraLiability, optGlassCover, optLoanCar,
                    paymentType, totalPremium]
    # Make sure every value in the list is a string
    storedValues = [str(x) for x in storedValues]

    # Open the policies file in append mode, add the new data
    file = open("Policies.dat", "a")
    file.write(", ".join(storedValues) + "\n")
    file.close()

    # Increment the policy number and rewrite the defaults file
    NEXT_POLICY_NUM += 1

    # Make a list of new default values
    defaults = [NEXT_POLICY_NUM, BASIC_PREMIUM, ADD_CARS_DISCOUNT,
                LIABILITY_COV_COST, GLASS_COV_COST, LOAN_COV_COST, HST_RATE, PROC_FEE]
    # Make sure every value in the list is a string
    defaults = [str(x) for x in defaults]

    file = open("OSICDef.dat", "w")
    for line in defaults:
        file.write(line+"\n")
    file.close()

    print("Policy information processed and saved.")
    print()

    # Ask if the user wants to do this all again - if not, the current loop breaks
    writeAnother = askYorN("Do you want to add another invoice?")
    if writeAnother == "N":
        break
