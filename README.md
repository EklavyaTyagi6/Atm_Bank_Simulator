# ATM and Bank Account Simulator

A Python command-line application that simulates everyday ATM and banking operations with PIN-based authentication, card blocking, currency note dispensing, mini statements, compound interest forecasting, and persistent text-file storage.

## Features

- **Secure Login & Card Blocking**: Verifies a 12-digit account number and 4-digit PIN, automatically blocking the card after 3 consecutive failed PIN attempts.
- **Check Balance**: Displays the current account balance in Indian Rupees (Rs.).
- **Deposit Money**: Accepts positive deposit amounts in multiples of Rs. 100 and updates the saved balance and transaction history.
- **Withdraw Money & Note Dispensing**: Validates withdrawal amounts (positive multiples of Rs. 100 within available balance) and dispenses the minimum number of notes using Rs. 2000, Rs. 500, Rs. 200, and Rs. 100 denominations.
- **Mini Statement**: Lists up to the 5 most recent transactions on the account.
- **Compound Interest Forecast**: Projects the future balance over a chosen number of years at a 5.0% annual compound interest rate.
- **Persistent File Storage**: Reads and saves account details, blocked status, and running transaction balances in `accounts_py.txt`.

## Project Structure

```text
Atm_Bank_Simulator/
├── atm_bank_simulator.py   # Main Python program with ATM logic and menu loop
├── accounts_py.txt         # Text-based account and transaction data file
└── README.md               # Project documentation
```

## Requirements

- Python 3.6 or higher (uses only the Python Standard Library; no external dependencies required).

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/EklavyaTyagi6/Atm_Bank_Simulator.git
   cd Atm_Bank_Simulator
   ```
2. Run the simulator:
   ```bash
   python atm_bank_simulator.py
   ```
   *(On macOS/Linux, use `python3 atm_bank_simulator.py` if `python` points to Python 2.)*

## Sample Accounts

The repository includes `accounts_py.txt` pre-populated with two demo accounts:

| Account Number | Account Holder | PIN | Starting Balance |
| :--- | :--- | :--- | :--- |
| `123456789100` | Manish Kumar | `1234` | Rs. 6000 |
| `123456789101` | Ashish Kumar | `5678` | Rs. 16900 |

## Menu Options

After logging in, select any of the following options:

1. **Check Balance** — Display your current account balance.
2. **Deposit** — Deposit cash in multiples of Rs. 100.
3. **Withdraw** — Withdraw cash in multiples of Rs. 100 and see the note breakdown.
4. **Mini Statement** — View your 5 most recent transactions.
5. **Calculate Expected Interest** — Forecast your future balance at 5.0% annual compound interest.
6. **Exit** — End the ATM session.

## Data Storage Format (`accounts_py.txt`)

Each account record is stored in plain text and separated by `----------`:

```text
Account Number: 123456789100
Name: Manish Kumar
PIN: 1234
Balance: 6000
Transaction: Deposit | Amount: 5000 | Balance After: 5000
Transaction: Deposit | Amount: 1000 | Balance After: 6000
----------
```

If `accounts_py.txt` is missing or empty, the program automatically creates it with default sample accounts on startup.
