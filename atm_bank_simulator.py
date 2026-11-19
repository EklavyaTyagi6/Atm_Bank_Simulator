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