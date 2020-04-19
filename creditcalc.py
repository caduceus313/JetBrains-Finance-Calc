import math
cim = {
    "principal": ("Enter the credit principal:", "f"),
    "payment": ("Enter monthly payment:", "f"),
    "interest": ("Enter credit interest:", "f"),
    "period": ("Enter count of periods:", "i"),
    "main_menu": ('What do you want to calculate? type "n" - for count of months,\ntype "a" - for annuity monthly payment,\ntype "p" - for credit principal:\n', "s")
}


def nominal_interest(interest_):
    return interest_ / 1200


def repayment_period(pr, pay, i):
    i = nominal_interest(i)
    return math.ceil(math.log(pay / (pay - i * pr), 1 + i))


def credit_principal(pay, per, i):
    i = nominal_interest(i)
    return pay / ((i * math.pow((1 + i), per)) / (pow((1 + i), per) - 1))


def annuity(pr, per, i):
    i = nominal_interest(i)
    return pr * ((i * math.pow((1 + i), per)) / (pow((1 + i), per) - 1))


def month_output(months):
    if months % 12 == 0:
        return f"{months / 12} years"
    elif months / 12 > 1:
        return f"{months // 12} years and {months % 12} months"
    elif months / 12 < 1:
        return f"{months} months"


def user_input_common(message, variable_type):
    if variable_type == "f":
        return float(input(message))
    elif variable_type == "i":
        return int(input(message))
    elif variable_type == "s":
        return input(message)
    else:
        repr("Invalid variable type")
        return


def menu(selection):
    user_input = []
    if selection == "n":
        for i in ["principal", "payment", "interest"]:
            user_input.append(user_input_common(cim[i][0], cim[i][1]))
        print(f"You need {month_output(repayment_period(user_input[0], user_input[1], user_input[2]))} to repay this credit!")
    elif selection == "a":
        for i in ["principal", "period", "interest"]:
            user_input.append(user_input_common(cim[i][0], cim[i][1]))
        print(f"Your annuity payment = {math.ceil(annuity(user_input[0], user_input[1], user_input[2]))}!")
    elif selection == "p":
        for i in ["payment", "period", "interest"]:
            user_input.append(user_input_common(cim[i][0], cim[i][1]))
        print(f"Your credit principal = {math.ceil(credit_principal(user_input[0], user_input[1], user_input[2]))}")
    else:
        print(f"{selection} is an invalid selection")


menu(user_input_common(cim["main_menu"][0], cim["main_menu"][1]))



