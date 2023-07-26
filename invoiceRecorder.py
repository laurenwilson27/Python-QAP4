"""
Software Development 9
QAP 4, Project 1: Sales Receipt
Author: Lauren Wilson

Description: A program for a hypothetical car insurance company. The user can input
                information for a new customer's policy, and the program will display
                a sales receipt for the policy, as well as recording the information
                to a file.
"""

import datetime
import FormatValues as FV

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
    print("One Stop Insurance Company")
    print("Sales Receipt")
    print()

    # Print the customer information onto the receipt
    print("Customer Information:")
    print("  " + "{:<30}".format(firstName + " " + lastName)+"    Premium Breakdown:")
    print("  " + "{:<30}".format(custAddr) +
          "      Vehicles insured: " + f'{carCount:<3d}' + " " + f"{FV.FDollar2(basicPremium):>10s}")

    if optExtraLiability == "Y":
        print("  " + "{:<30}".format(custCity + ", " + custProvince) +
              "      Extra liability:  Yes" + " " + f"{FV.FDollar2(LIABILITY_COV_COST):>10s}")
    else:
        print("  " + "{:<30}".format(custCity + ", " + custProvince) +
              "      Extra liability:  No       $0.00")

    if optGlassCover == "Y":
        print("  " + "{:<30}".format(custPostal) +
              "      Glass coverage:   Yes" + " " + f"{FV.FDollar2(GLASS_COV_COST):>10s}")
    else:
        print("  " + "{:<30}".format(custPostal) +
              "      Glass coverage:   No       $0.00")

    if optLoanCar == "Y":
        print("  " + "{:<30}".format(custPhone) +
              "      Loaner car:       Yes" + " " + f"{FV.FDollar2(LOAN_COV_COST):>10s}")
    else:
        print("  " + "{:<30}".format(custPhone) +
              "      Loaner car:       No       $0.00")

    print()

    # Print subtotals, taxes, etc.
    # print(" " * 27 + "_" * 33)
    print(" "*38+"Total extra costs:    " + f"{FV.FDollar2(extraCosts):>10s}")
    print(" "*38+"Total premium:        " + f"{FV.FDollar2(totalPremium):>10s}")
    print(" "*38+"Sales tax:            " + f"{FV.FDollar2(hst):>10s}")
    print(" " * 38 + "_" * 32)
    print(" "*38+"Total cost:           " + f"{FV.FDollar2(totalCost):>10s}")
    print()
    print("Payment plan selected:   " + paymentType)
    if paymentType == "Monthly":
        print("  Monthly payment:       " + FV.FDollar2(monthlyPayment))
    else:
        print("  Full payment:          " + FV.FDollar2(totalCost))
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
        file.write(line + "\n")
    file.close()

    print("Policy information processed and saved.")
    print()

    # Ask if the user wants to do this all again - if not, the current loop breaks
    writeAnother = askYorN("Do you want to add another invoice?")
    if writeAnother == "N":
        break
