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
