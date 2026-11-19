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