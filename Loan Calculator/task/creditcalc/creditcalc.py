import math
import argparse
import sys


parser = argparse.ArgumentParser(description="This program assists you with calculating your loan payments. \
                                             Please specify the type of calculation, and three arguments. \
                                             The one which is not provided - will be calculated for you ")

parser.add_argument("--type", choices=["diff", "annuity"], dest='type',
                    help="You need to choose the loan interest calculation way.")
parser.add_argument("--principal", dest='principal')
parser.add_argument("--periods", dest='period')
parser.add_argument("--interest", dest='interest')
parser.add_argument("--payment", dest='payment')

args = parser.parse_args()


def stop_me():
    print("Incorrect parameters")
    sys.exit()


def overpayment(quantity, payment, principle):

    overpayment = int(quantity * payment - principle)
    print(f"Overpayment = {overpayment}")


def month():

    try:
        principle = float(args.principal)
        monthly = float(args.payment)
        interest = float(args.interest)
    except ValueError:
        stop_me()
    interest_rate = nominal_interest(interest)
    value = month_number(interest_rate, monthly, principle)
    result = math.ceil(round(value, 2))
    if result == 1 or result % 12 == 1:
        m = "month"
    else:
        m = "months"
    if result / 12 == 1:
        y = "year"
    else:
        y = "years"
    if result < 12:
        print(f"It will take {result} {m} to repay the loan!")
    elif result % 12 == 0:
        print(f"It will take {math.floor(result / 12)} {y} to repay the loan!")
    else:
        print(f"It will take {math.floor(result / 12)} {y} and {result % 12} {m} to repay the loan!")
    overpayment(result, monthly, principle)



def payment():

    try:
        principle = float(args.principal)
        periods = float(args.period)
        interest = float(args.interest)
    except ValueError:
        stop_me()

    interest_rate = nominal_interest(interest)
    result = math.ceil(ordinary_monthly(interest_rate, principle, periods))

    print(f"Your monthly payment = {result}!")
    overpayment(periods, result, principle)


def ordinary_monthly(interest_rate, principle, periods):
    x = (1 + interest_rate) ** periods
    result = principle * ((interest_rate * x) / (x - 1))
    return result

def loan():

    try:
        monthly = float(args.payment)
        periods = float(args.period)
        interest = float(args.interest)
    except ValueError:
        stop_me()

    interest_rate = nominal_interest(interest)
    value = int(loan_principle(interest_rate, monthly, periods))

    print(f"Your loan principal = {value}!")
    overpayment(periods, monthly, value)


def loan_principle(interest_rate, monthly, periods):
    x = (1 + interest_rate) ** periods
    result = monthly / ((interest_rate * x) / (x - 1))
    return result



def nominal_interest(interest):
    result = (interest / 100) / 12
    return result

def month_number(interest_rate, monthly, principle):
    x = (monthly / (monthly - interest_rate * principle))
    if x < 0:
        print("Inccrease your monthly payment to pay the loan in this universe!")
        sys.exit()
    result = math.log(x, 1 + interest_rate)
    return result

def diff_calc(args):
    try:
        principle = float(args.principal)
        periods = float(args.period)
        interest = float(args.interest)
    except ValueError:
        stop_me()
    interest_rate = nominal_interest(interest)
    x = 1
    total_payment = 0
    while x <= periods:
        diff_payment = principle / periods + interest_rate * (principle - ((principle * (x - 1)) / periods))
        print(f"Month {x}: payment is {math.ceil(diff_payment)}")
        x = x + 1
        total_payment = total_payment + math.ceil(diff_payment)
    print("")
    overpayment = int(total_payment - principle)
    print(f"Overpayment = {overpayment}")


def check_type(args):
    if args.principal and args.period and args.interest and not args.payment:
        return "a"
    elif args.principal and args.payment and args.interest and not args.period:
        return "n"
    elif args.payment and args.period and args.interest and not args.principal:
        return "p"
    else:
        stop_me()

def run_calc(answer):
    if answer == "n":
        month()
    if answer == "a":
        payment()
    if answer == "p":
        loan()


def check_validity(args):
    if args.type:
        if args.type == "diff":
            if args.principal and args.period and args.interest and not args.payment:
                diff_calc(args)
            else:
                stop_me()
        elif args.type == "annuity":
            answer = check_type(args)
            run_calc(answer)
    else:
        stop_me()

check_validity(args)
