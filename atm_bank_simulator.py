# Set of valid note denominations
VALID_NOTES = {2000, 500, 200, 100}


# Handles PIN login with a maximum of three attempts.
def verify_login(accounts):

    account_num = input("Enter your Account Number: ").strip()
    if account_num not in accounts:
        print("Account not found.")
        return None

    attempts = 0
    while attempts < 3:
        pin = input("Enter your PIN: ").strip()
        if accounts[account_num]['pin'] == pin:
            print("Login successful!")
            return account_num
        else:
            print("Incorrect PIN.")
            attempts += 1
            print(f"Attempts remaining: {3 - attempts}")

    print("Maximum login attempts reached.")
    return None

# Adds the deposit amount to the balance.

def deposit_money(balance, amount):
    return balance + amount

# Adds the withdraw amount to the balance

def withdraw_money(balance, amount):
    """
    Deducts the withdrawal amount from the balance if sufficient.
    Returns -1 if balance is insufficient.
    """
    if amount > balance:
        return -1
    return balance - amount

# Add dispence function

def dispense_notes(amount):
    """
    Splits the withdrawal amount into notes using a nested loop.
    """
    # Tuple holding fixed note denominations
    denominations = (2000, 500, 200, 100)
    notes_dispensed = {}
    
    # For loop with an inner while loop
    for note in denominations:
        if note in VALID_NOTES:
            count = 0
            while amount >= note:
                amount -= note
                count += 1
            if count > 0:
                notes_dispensed[note] = count
    print("Notes dispensed:")
    for note, count in notes_dispensed.items():
        print(f"Rs. {note} x {count}")           

def calc_compound_interest(principal, rate, years):
    """
    Recursive function to calculate compound interest.
    """
    if years <= 0:
        return principal
    else:
        new_principal = principal + (principal * (rate / 100))
        return calc_compound_interest(new_principal, rate, years - 1)

def show_mini_statement(transactions):
    """
    Shows a mini statement of the last five transactions.
    """
    print("\n--- Mini Statement ---")
    recent = transactions[-5:]
    for t_type, t_amount in recent:
        print(f"{t_type}: Rs. {t_amount}")
    print("----------------------")
    
def main():
    # Dictionary containing the main data (replacing the file system)
    accounts = {
        '1001': {'pin': '1234', 'balance': 5000.0, 'transactions': [('Deposit', 5000.0)]},
        '1002': {'pin': '5678', 'balance': 10000.0, 'transactions': [('Deposit', 10000.0)]}
    }

    print("Welcome to the ATM Simulator")
    current_acc = verify_login(accounts)
    
    if not current_acc:
        return

    while True:
        print("\n--- ATM Menu ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Mini Statement")
        print("5. Calculate Expected Interest")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            print(f"Current Balance: Rs. {accounts[current_acc]['balance']}")

        elif choice == '2':
            amt_input = input("Enter amount to deposit: ").replace('.', '', 1)
            if amt_input.isdigit():
                amt = float(input("Confirm amount: "))
                if amt > 0:
                    accounts[current_acc]['balance'] = deposit_money(accounts[current_acc]['balance'], amt)
                    accounts[current_acc]['transactions'].append(('Deposit', amt))
                    print("Deposit successful.")
                else:
                    print("Amount must be greater than zero.")
            else:
                print("Invalid number.")

        elif choice == '3':
                    amt_input = input("Enter amount to withdraw (multiples of 100): ")
                    if amt_input.isdigit():
                        amt = float(amt_input)
                        if amt > 0 and amt % 100 == 0:
                            new_balance = withdraw_money(accounts[current_acc]['balance'], amt)
                            if new_balance == -1:
                                print("Insufficient balance!")
                            else:
                                accounts[current_acc]['balance'] = new_balance
                                accounts[current_acc]['transactions'].append(('Withdrawal', amt))
                                dispense_notes(amt)
                                print("Withdrawal successful.")
                        else:
                            print("Invalid amount. Must be a multiple of 100.")
                    else:
                        print("Invalid number.")

        elif choice == '4':
            show_mini_statement(accounts[current_acc]['transactions'])
            
        elif choice == '5':
            years_input = input("Enter number of years to forecast: ")
            if years_input.isdigit():
                years = int(years_input)
                future_val = calc_compound_interest(accounts[current_acc]['balance'], 5.0, years)
                print(f"Expected Balance after {years} years at 5.0%: Rs. {round(future_val, 2)}")
            else:
                print("Invalid number of years.")
        
        elif choice == '6':
            print("Thank you for using the ATM!")
            break

        else:
            print("Invalid choice. Please select from 1 to 6.")