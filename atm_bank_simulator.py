"""
ATM and Bank Account Simulator

A command-line ATM simulator supporting PIN-based login with card blocking,
balance inquiry, deposits, withdrawals with currency note dispensing,
mini statements, compound interest forecasting, and file-based persistence.
"""

# Available ATM currency denominations in descending order (for greedy note dispensing)
VALID_NOTES = (2000, 500, 200, 100)

# Text file used to load and persist account details and transaction history
DATA_FILE = "accounts_py.txt"


def get_valid_int(prompt):
    """Prompt the user repeatedly until a valid whole number (integer) is entered."""
    while True:
        user_text = input(prompt).strip()
        try:
            return int(user_text)
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_valid_digits(prompt, required_length):
    """Prompt the user until a numeric string of exact length `required_length` is entered."""
    while True:
        user_text = input(prompt).strip()
        if len(user_text) == required_length and user_text.isdigit():
            return user_text
        print(f"Invalid input. Please enter exactly {required_length} digits.")


def load_accounts(filename):
    """Load accounts and transaction history from `filename`.

    If the file does not exist or contains no accounts, default sample accounts
    are created and saved to `filename`.
    """
    accounts = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            current_acc = None

            for raw_line in file:
                line = raw_line.strip()
                # Skip blank lines and account separator lines
                if not line or line == "----------":
                    continue

                if ":" in line:
                    # Split only on the first colon so values containing colons stay intact
                    label, value = [part.strip() for part in line.split(":", 1)]

                    if label == "Account Number":
                        # Start a new account record
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
                            # Parse format: "<Type> | Amount: <amount> | Balance After: <bal>"
                            try:
                                txn_parts = value.split("|")
                                t_type = txn_parts[0].strip()
                                amt_part = txn_parts[1].split(":", 1)[1].strip()
                                t_amount = int(float(amt_part))
                                accounts[current_acc]["transactions"].append((t_type, t_amount))
                            except (IndexError, ValueError):
                                # Skip malformed transaction lines without crashing
                                continue
    except FileNotFoundError:
        pass

    # Initialize default accounts if no data was loaded
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
    """Write all account records and running transaction balances to `filename`."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for acc_num, info in accounts.items():
                file.write(f"Account Number: {acc_num}\n")
                file.write(f"Name: {info['name']}\n")
                file.write(f"PIN: {info['pin']}\n")
                file.write(f"Balance: {info['balance']}\n")
                if info.get("blocked", False):
                    file.write("Blocked: True\n")

                # Compute the starting balance prior to recorded transactions
                net_txn_change = sum(
                    amt if t_type == "Deposit" else (-amt if t_type == "Withdrawal" else 0)
                    for t_type, amt in info["transactions"]
                )
                running_bal = info["balance"] - net_txn_change

                # Write each transaction along with the running balance after it
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
    """Ask the user whether to re-enter an account number or exit the ATM."""
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
    """Authenticate a user by 12-digit account number and 4-digit PIN.

    Blocks the card and saves the updated status after 3 consecutive failed PIN attempts.
    Returns the authenticated account number, or None if the user exits or is blocked.
    """
    while True:
        account_num = get_valid_digits("Enter your 12-digit Account Number: ", 12)
        if account_num not in accounts:
            print("Account not found.")
            if not ask_continue_or_exit():
                return None
            continue

        # Prevent login if the card is already blocked
        if accounts[account_num].get("blocked", False):
            print("This card is blocked due to multiple failed PIN attempts.")
            if not ask_continue_or_exit():
                return None
            continue

        attempts = 0
        reenter_account = False

        # Allow up to 3 PIN attempts
        while attempts < 3:
            pin = get_valid_digits("Enter your 4-digit PIN: ", 4)
            if accounts[account_num]["pin"] == pin:
                print(f"Login successful! Welcome, {accounts[account_num]['name']}")
                return account_num

            attempts += 1
            remaining = 3 - attempts
            print(f"Incorrect PIN. Attempts remaining: {remaining}")

            # Block the card once all 3 attempts are exhausted
            if remaining == 0:
                accounts[account_num]["blocked"] = True
                save_accounts(DATA_FILE, accounts)
                print("Maximum login attempts reached. Your card is blocked!")
                return None

            # Give the user options after a wrong PIN
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
    """Return the updated balance after adding `amount`."""
    return balance + amount


def withdraw_money(balance, amount):
    """Return the updated balance after subtracting `amount`, or -1 if funds are insufficient."""
    if amount > balance:
        return -1
    return balance - amount


def dispense_notes(amount):
    """Break `amount` into the fewest ATM currency notes and display the breakdown."""
    notes_dispensed = {}
    for note in VALID_NOTES:
        count, amount = divmod(amount, note)
        if count > 0:
            notes_dispensed[note] = count

    print("Notes dispensed:")
    for note, count in notes_dispensed.items():
        print(f"Rs. {note} x {count}")


def calc_compound_interest(principal, rate, years):
    """Calculate the compound amount after `years` at an annual interest `rate` (%)."""
    if years <= 0:
        return principal
    return principal * ((1 + rate / 100) ** years)


def show_mini_statement(transactions):
    """Display the 5 most recent transactions for the logged-in account."""
    print("\n--- Mini Statement ---")
    recent = transactions[-5:]
    if not recent:
        print("No transactions found.")
    else:
        for t_type, t_amount in recent:
            print(f"{t_type}: Rs. {t_amount}")
    print("----------------------")


def main():
    """Run the main ATM simulator workflow: load accounts, log in, and serve menu actions."""
    accounts = load_accounts(DATA_FILE)

    print("Welcome to the ATM Simulator")
    current_acc = verify_login(accounts)

    # Exit if login failed, was blocked, or user chose to quit
    if current_acc is None:
        return

    # Main ATM menu loop
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
            # Display current account balance
            print(f"Current Balance: Rs. {accounts[current_acc]['balance']}")

        elif choice == 2:
            # Deposit money (must be positive and a multiple of 100)
            amt = get_valid_int("Enter amount to deposit (multiples of 100): ")
            if amt > 0 and amt % 100 == 0:
                accounts[current_acc]["balance"] = deposit_money(
                    accounts[current_acc]["balance"], amt
                )
                accounts[current_acc]["transactions"].append(("Deposit", amt))
                save_accounts(DATA_FILE, accounts)
                print("Deposit successful.")
            else:
                print("Invalid amount. Must be greater than 0 and a multiple of 100.")

        elif choice == 3:
            # Withdraw money (must be positive, a multiple of 100, and within balance)
            amt = get_valid_int("Enter amount to withdraw (multiples of 100): ")
            if amt > 0 and amt % 100 == 0:
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
            # Show the last 5 transactions
            show_mini_statement(accounts[current_acc]["transactions"])

        elif choice == 5:
            # Forecast compound interest at a fixed 5.0% annual rate
            years = get_valid_int("Enter number of years to forecast: ")
            if years > 0:
                future_val = calc_compound_interest(
                    accounts[current_acc]["balance"], 5.0, years
                )
                print(
                    f"Expected Balance after {years} years at 5.0%: Rs. {future_val:.2f}"
                )
            else:
                print("Invalid number. Please enter a positive number of years.")

        elif choice == 6:
            # Exit the ATM session
            print("Thank you for using the ATM!")
            break

        else:
            print("Invalid choice. Please select from 1 to 6.")


if __name__ == "__main__":
    main()
