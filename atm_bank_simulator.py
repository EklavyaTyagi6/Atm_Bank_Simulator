VALID_NOTES = (2000, 500, 200, 100)
DATA_FILE = "accounts_py.txt"


def get_valid_int(prompt):
    while True:
        user_text = input(prompt).strip()
        try:
            return int(user_text)
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_valid_digits(prompt, required_length):
    while True:
        user_text = input(prompt).strip()
        if len(user_text) == required_length and user_text.isdigit():
            return user_text
        print(f"Invalid input. Please enter exactly {required_length} digits.")


def load_accounts(filename):
    accounts = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            current_acc = None

            for raw_line in file:
                line = raw_line.strip()
                if not line or line == "----------":
                    continue

                if ":" in line:
                    label, value = [part.strip() for part in line.split(":", 1)]

                    if label == "Account Number":
                        current_acc = value
                        accounts[current_acc] = {
                            "name": "",
                            "pin": "",
                            "balance": 0,
                            "blocked": False,
                            "transactions": [],
                        }
                    elif current_acc is not None:
                        if label == "Name":
                            accounts[current_acc]["name"] = value
                        elif label == "PIN":
                            accounts[current_acc]["pin"] = value
                        elif label == "Balance":
                            accounts[current_acc]["balance"] = int(float(value))
                        elif label == "Blocked":
                            accounts[current_acc]["blocked"] = value.lower() == "true"
                        elif label == "Transaction":
                            try:
                                txn_parts = value.split("|")
                                t_type = txn_parts[0].strip()
                                amt_part = txn_parts[1].split(":", 1)[1].strip()
                                t_amount = int(float(amt_part))
                                accounts[current_acc]["transactions"].append((t_type, t_amount))
                            except (IndexError, ValueError):
                                continue
    except FileNotFoundError:
        pass

    if not accounts:
        accounts = {
            "123456789100": {
                "name": "Manish Kumar",
                "pin": "1234",
                "balance": 6000,
                "blocked": False,
                "transactions": [("Deposit", 5000), ("Deposit", 1000)],
            },
            "123456789101": {
                "name": "Ashish Kumar",
                "pin": "5678",
                "balance": 10000,
                "blocked": False,
                "transactions": [("Deposit", 10000)],
            },
        }
        save_accounts(filename, accounts)

    return accounts


def save_accounts(filename, accounts):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for acc_num, info in accounts.items():
                file.write(f"Account Number: {acc_num}\n")
                file.write(f"Name: {info['name']}\n")
                file.write(f"PIN: {info['pin']}\n")
                file.write(f"Balance: {info['balance']}\n")
                if info.get("blocked", False):
                    file.write("Blocked: True\n")

                net_txn_change = sum(
                    amt if t_type == "Deposit" else -amt
                    for t_type, amt in info["transactions"]
                )
                running_bal = info["balance"] - net_txn_change

                for t_type, t_amount in info["transactions"]:
                    if t_type == "Deposit":
                        running_bal += t_amount
                    elif t_type == "Withdrawal":
                        running_bal -= t_amount
                    file.write(
                        f"Transaction: {t_type} | Amount: {t_amount} | Balance After: {running_bal}\n"
                    )

                file.write("----------\n")
    except OSError as error:
        print(f"Could not save data to file: {error}")


def ask_continue_or_exit():
    while True:
        print("1. Continue (Re-enter Account Number)")
        print("2. Exit")
        option = get_valid_int("Choose an option (1 or 2): ")
        if option == 1:
            return True
        if option == 2:
            print("Thank you for using the ATM. Goodbye!")
            return False
        print("Invalid choice. Please select 1 or 2.")


def verify_login(accounts):
    while True:
        account_num = get_valid_digits("Enter your 12-digit Account Number: ", 12)
        if account_num not in accounts:
            print("Account not found.")
            if not ask_continue_or_exit():
                return None
            continue

        if accounts[account_num].get("blocked", False):
            print("This card is blocked due to multiple failed PIN attempts.")
            if not ask_continue_or_exit():
                return None
            continue

        attempts = 0
        reenter_account = False

        while attempts < 3:
            pin = get_valid_digits("Enter your 4-digit PIN: ", 4)
            if accounts[account_num]["pin"] == pin:
                print(f"Login successful! Welcome, {accounts[account_num]['name']}")
                return account_num

            attempts += 1
            remaining = 3 - attempts
            print(f"Incorrect PIN. Attempts remaining: {remaining}")

            if remaining == 0:
                accounts[account_num]["blocked"] = True
                save_accounts(DATA_FILE, accounts)
                print("Maximum login attempts reached. Your card is blocked!")
                return None

            while True:
                print("1. Try PIN again")
                print("2. Continue (Re-enter Account Number)")
                print("3. Exit")
                next_step = get_valid_int("Choose an option (1-3): ")
                if next_step == 1:
                    break
                if next_step == 2:
                    reenter_account = True
                    break
                if next_step == 3:
                    print("Thank you for using the ATM. Goodbye!")
                    return None
                print("Invalid choice. Please select from 1 to 3.")

            if reenter_account:
                break


def deposit_money(balance, amount):
    return balance + amount


def withdraw_money(balance, amount):
    if amount > balance:
        return -1
    return balance - amount


def dispense_notes(amount):
    notes_dispensed = {}
    for note in VALID_NOTES:
        count, amount = divmod(amount, note)
        if count > 0:
            notes_dispensed[note] = count

    print("Notes dispensed:")
    for note, count in notes_dispensed.items():
        print(f"Rs. {note} x {count}")


def calc_compound_interest(principal, rate, years):
    if years <= 0:
        return principal
    return principal * ((1 + rate / 100) ** years)


def show_mini_statement(transactions):
    print("\n--- Mini Statement ---")
    recent = transactions[-5:]
    if not recent:
        print("No transactions found.")
    else:
        for t_type, t_amount in recent:
            print(f"{t_type}: Rs. {t_amount}")
    print("----------------------")


def main():
    accounts = load_accounts(DATA_FILE)

    print("Welcome to the ATM Simulator")
    current_acc = verify_login(accounts)

    if current_acc is None:
        return

    while True:
        print("\n--- ATM Menu ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Mini Statement")
        print("5. Calculate Expected Interest")
        print("6. Exit")

        choice = get_valid_int("Select an option (1-6): ")

        if choice == 1:
            print(f"Current Balance: Rs. {accounts[current_acc]['balance']}")

        elif choice == 2:
            amt = get_valid_int("Enter amount to deposit (multiples of 100): ")
            if amt > 0 and amt % 5 == 0:
                accounts[current_acc]["balance"] = deposit_money(
                    accounts[current_acc]["balance"], amt
                )
                accounts[current_acc]["transactions"].append(("Deposit", amt))
                save_accounts(DATA_FILE, accounts)
                print("Deposit successful.")
            else:
                print("Invalid amount. Must be greater than 0 and a multiple of 100.")

        elif choice == 3:
            amt = get_valid_int("Enter amount to withdraw (multiples of 100): ")
            if amt > 0 and amt % 5 == 0:
                new_balance = withdraw_money(accounts[current_acc]["balance"], amt)
                if new_balance == -1:
                    print("Insufficient balance!")
                else:
                    accounts[current_acc]["balance"] = new_balance
                    accounts[current_acc]["transactions"].append(("Withdrawal", amt))
                    dispense_notes(amt)
                    save_accounts(DATA_FILE, accounts)
                    print("Withdrawal successful.")
            else:
                print("Invalid amount. Must be greater than 0 and a multiple of 100.")

        elif choice == 4:
            show_mini_statement(accounts[current_acc]["transactions"])

        elif choice == 5:
            years = get_valid_int("Enter number of years to forecast: ")
            if years > 0:
                future_val = calc_compound_interest(
                    accounts[current_acc]["balance"], 5.0, years
                )
                print(
                    f"Expected Balance after {years} years at 5.0%: Rs. {round(future_val, 2)}"
                )
            else:
                print("Years must be greater than zero.")

        elif choice == 6:
            save_accounts(DATA_FILE, accounts)
            print("Thank you for using the ATM!")
            break

        else:
            print("Invalid choice. Please select from 1 to 6.")


if __name__ == "__main__":
    main()