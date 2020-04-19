# credit calculator by @anthony vollmer
# this is done procedurally, not object oriented
import math
import sys
# common input messages. Message, data type (float, integer, string)
cim = {
    "principal": ("Enter the credit principal:", "f"),
    "payment": ("Enter monthly payment:", "f"),
    "interest": ("Enter credit interest:", "f"),
    "periods": ("Enter count of periods:", "i"),
    "main_menu": ('What do you want to calculate? type "n" - for count of months,\ntype "a" - for annuity monthly '
                  'payment,\ntype "p" - for credit principal,\ntype "d" - for differential payments:\n', "s")
}

# common output messages with variable holder.
com = {
    "time_repay": "You need {} to repay this credit!",
    "annuity_payment": "Your annuity payment = {}!",
    "principal": "Your credit principal = {}",
    "invalid_select": "{} is an invalid selection",
    "bad_params": "Incorrect parameters.",
    "years": "{} years",
    "years_and": "{} years and {} months",
    "months": "{} months",
    "wrong_type": "Invalid variable type",
    "over_payment": "Overpayment = {}",
    "months_by_month": "Month {}: paid out {}"
}

# dictionary of parameter values, some keys have tuples with index values of cmd_params
param_dict = {
    "cmd_params": ("type", "interest", "principal", "payment", "periods"),  # I would update to include types as well (int/float/string)
    "repayment_period": (2, 3, 1),
    "annuity": (2, 4, 1),
    "credit_principal": (4, 3, 1),
    "diff_payment": (2, 4, 1),
    "type": ("annuity", "diff"),
    "menu": ("n", "a", "p", "d")
}


def diff_payment(pr, per, i):
    i = nominal_interest(i)
    results = [math.ceil(pr / per + i * (pr - (pr * (m_ - 1)) / per)) for m_ in range(1, int(per) + 1)]
    return results


def nominal_interest(interest_):
    return interest_ / 1200


def repayment_period(pr, pay, i):
    i = nominal_interest(i)
    return math.ceil(math.log(pay / (pay - i * pr), 1 + i))


def credit_principal(per, pay, i):
    i = nominal_interest(i)
    return math.floor(pay / ((i * math.pow((1 + i), per)) / (pow((1 + i), per) - 1)))


def annuity(pr, per, i):
    i = nominal_interest(i)
    return pr * ((i * math.pow((1 + i), per)) / (pow((1 + i), per) - 1))


def month_output(months):
    """converts months to years and months"""
    if months % 12 == 0:
        return com['years'].format(months // 12)
    elif months / 12 > 1:
        return com["years_and"].format(months // 12, months % 12)
    elif months / 12 < 1:
        return com['months'].format(months)


def user_input_common(message, variable_type):
    """called for user input, displays message and returns data type requested."""
    if variable_type == "f":
        return float(input(message))
    elif variable_type == "i":
        return int(input(message))
    elif variable_type == "s":
        return input(message)
    else:
        repr(com["wrong_type"])
        return


def check_keys(args, m_item):
    if len(list(set(param_dict["cmd_params"][x_] for x_ in param_dict[m_item]).intersection(args.keys()))) == 3:
        return True
    else:
        return False


def menu(selection):
    """Each menu option expects list of user inputs. User input is taken with data type to return,
    function is called, output printed."""
    user_input = []
    total = 0.0
    if selection == param_dict["menu"][0]:
        for i in [param_dict["cmd_params"][x_] for x_ in param_dict["repayment_period"]]:
            user_input.append(user_input_common(cim[i][0], cim[i][1]))
        results = repayment_period(user_input[0], user_input[1], user_input[2])
        print(com["time_repay"].format(month_output(results)))
        print(com["over_payment"].format(round(results * user_input[1] - user_input[0]), None))
    elif selection == param_dict["menu"][1]:
        for i in [param_dict["cmd_params"][x_] for x_ in param_dict["annuity"]]:
            user_input.append(user_input_common(cim[i][0], cim[i][1]))
        print(com["annuity_payment"].format(math.ceil(annuity(user_input[0], user_input[1], user_input[2]))))
        print(com["over_payment"].format(round(math.ceil(annuity(user_input[0], user_input[1], user_input[2]))
                                               * user_input[1] - user_input[0], None)))
    elif selection == param_dict["menu"][2]:
        for i in [param_dict["cmd_params"][x_] for x_ in param_dict["credit_principal"]]:
            user_input.append(user_input_common(cim[i][0], cim[i][1]))
        results = math.ceil(credit_principal(user_input[0], user_input[1], user_input[2]))
        print(com["principal"].format(results))
        print(com["over_payment"].format(round(user_input[0] * user_input[1] - results), None))
    elif selection == param_dict["menu"][3]:
        for i in [param_dict["cmd_params"][x_] for x_ in param_dict["diff_payment"]]:
            user_input.append(user_input_common(cim[i][0], cim[i][1]))
        for index, amount in enumerate(diff_payment(user_input[0], user_input[1], user_input[2]), start=1):
            print(com["months_by_month"].format(index, amount))
            total += float(amount)
        print(com["over_payment"].format(round(total - user_input[0]), None))
    else:
        print(com["invalid_select"].format(selection))


def start():
    total = 0
    if len(sys.argv) > 1:
        args = dict(arg.lstrip('-').split('=') if "=" in arg else (arg.lstrip('-'), "") for arg in sys.argv[1:])
    else:
        args = sys.argv
        print(len(args))
    if len(args) == 1:  # If there aren't any arguments then use the menu
        # print(f"MENU {args} {len(args)} - {sys.argv} {len(sys.argv)}")  # if there aren't any params, use menu # troubleshooting
        menu(user_input_common(cim["main_menu"][0], cim["main_menu"][1]))  # troubleshooting code
    # Check to see if there are not 4 arguments other than they .py file and if there are negative values in dictionary
    elif (len(args) != 4
            or any(float(arg) < 0 for arg in args.values() if arg.lstrip('-+').isnumeric())
            or len(args.keys() & param_dict["cmd_params"]) < 4
            or "type" not in args
            or args["type"] not in param_dict["type"]
            or (args["type"] == param_dict["type"][1] and param_dict["cmd_params"][3] in args)):
        # print(f"{args} {len(args)} - {sys.argv} {len(sys.argv)} - {args.values()}") # troubleshooting code
        print(com["bad_params"])
    else:  # function using command line arguments as they appear to be valid
        if param_dict["type"][0] == args["type"] and check_keys(args, "repayment_period"):
            # results = repayment_period(*[args[params] for params in [param_dict["cmd_params"][x_] for x_ in param_dict["repayment_period"]]])
            results = int(round(repayment_period(float(args["principal"]), float(args["payment"]), float(args["interest"])), None))
            print(com["time_repay"].format(month_output(results)))
            print(com["over_payment"].format(round(results * float(args["payment"]) - float(args["principal"])), None))
        elif param_dict["type"][0] == args["type"] and check_keys(args, "annuity"):
            # params = list(map(float, [args[params] for params in [param_dict["cmd_params"][x_] for x_ in param_dict["annuity"]]]))
            results = math.ceil(annuity(float(args["principal"]), int(args["periods"]), float(args["interest"])))
            print(com["annuity_payment"].format(results))
            print(com["over_payment"].format(round(results * int(args["periods"]) - float(args["principal"]), None)))
        elif param_dict["type"][0] == args["type"] and check_keys(args, "credit_principal"):
            results = math.floor(credit_principal(int(args["periods"]), float(args["payment"]), float(args["interest"])))
            print(com["principal"].format(results))
            print(com["over_payment"].format(round(float(args["payment"]) * int(args["periods"]) - results), None))
        elif param_dict["type"][1] == args["type"] and check_keys(args, "annuity"):
            results = diff_payment(float(args["principal"]), int(args["periods"]), float(args["interest"]))
            for index, amount in enumerate(results, start=1):
                print(com["months_by_month"].format(index, amount))
                total += float(amount)
            print(com["over_payment"].format(round(total - float(args[param_dict["cmd_params"][param_dict["annuity"][0]]])), None))
        else:
            print(f'{com["bad_params"]} round 2')


if __name__ == '__main__':
    start()
