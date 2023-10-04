import random

# Function to create account
def create_account(users):
    name = input("Enter your name: ")
    deposit_amount = float(input("Enter deposit amount (must be more than 50): "))
    while deposit_amount < 50:
        print("Deposit amount must be more than 50.")
        deposit_amount = float(input("Enter deposit amount (must be more than 50): "))

    pin_code = input("Enter 4-digit pin code: ")
    while len(pin_code) != 4 or not pin_code.isdigit():
        print("Pin code must be 4 digits.")
        pin_code = input("Enter 4-digit pin code: ")

    id = random.randint(1000000000, 9999999999)
    username = name + str(random.randint(100, 999))
    while username in users:
        username = name + str(random.randint(100, 999))

    user = {
        'id': id,
        'name': name,
        'username': username,
        'pin_code': pin_code,
        'status': 'ACTIVE',
        'currency': 'PKR',
        'balance': deposit_amount,
        'statement': [f"Deposit: {deposit_amount} PKR"]
    }
    users[username] = user

    with open('users.txt', 'a') as file:
        file.write(f"{username}:{user}\n")

    print(f"Account created successfully. Your username is {username}.")

# Function to all other activities
def login(users):
    username = input("Enter your username or account number: ")
    if username not in users:
        print("User not found.")
        return

    user = users[username]
    pin_attempts = 0
    while pin_attempts < 3:
        pin = input("Enter your pin code: ")
        if pin == user['pin_code']:
            break
        else:
            pin_attempts += 1
            if pin_attempts < 3:
                print(f"Invalid pin code. {3 - pin_attempts} attempts remaining.")
            else:
                print("Invalid pin code. Account blocked.")
                user['status'] = 'BLOCKED'
                users[username] = user
                with open('users.txt', 'a') as file:
                    file.write(f"{username}:{user}\n")
                return

    while True:
        print("\nMenu:")
        print("1. Account Details")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Update Pin")
        print("5. Check Statement")
        print("6. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            print(f"Name: {user['name']}")
            print(f"Username: {user['username']}")
            print(f"Status: {user['status']}")
            print(f"Balance: {user['balance']} {user['currency']}")
        elif choice == '2':
            deposit_amount = float(input("Enter deposit amount: "))
            if deposit_amount >= 50:
                user['balance'] += deposit_amount
                user['statement'].append(f"Deposit: {deposit_amount} {user['currency']}")
                users[username] = user
                with open('users.txt', 'a') as file:
                    file.write(f"{username}:{user}\n")
                print("Deposit successful.")
                print(f"New Balance: {user['balance']} {user['currency']}")
            else:
                print("Deposit amount must be at least 50.")
        elif choice == '3':
            if user['status'] == 'BLOCKED':
                print("Blocked users cannot withdraw. Contact support to unblock your account.")
            else:
                withdraw_amount = float(input("Enter withdraw amount: "))
                tax = withdraw_amount * 0.01
                if withdraw_amount + tax <= user['balance']:
                    user['balance'] -= (withdraw_amount + tax)
                    user['statement'].append(f"Withdraw: {withdraw_amount} {user['currency']} (Tax: {tax} {user['currency']})")
                    users[username] = user
                    with open('users.txt', 'a') as file:
                        file.write(f"{username}:{user}\n")
                    print("Withdraw successful.")
                    print(f"New Balance: {user['balance']} {user['currency']}")
                else:
                    print("Insufficient balance for withdrawal.")
        elif choice == '4':
            old_pin = input("Enter your previous pin code: ")
            if old_pin == user['pin_code']:
                new_pin = input("Enter your new 4-digit pin code: ")
                while len(new_pin) != 4 or not new_pin.isdigit():
                    print("Pin code must be 4 digits.")
                    new_pin = input("Enter new 4-digit pin code: ")
                user['pin_code'] = new_pin
                users[username] = user
                with open('users.txt', 'a') as file:
                    file.write(f"{username}:{user}\n")
                print("Pin code updated successfully.")
            else:
                print("Invalid previous pin code.")
        elif choice == '5':
            with open(f"{username}_statement.txt", 'w') as file:
                for entry in user['statement']:
                    file.write(f"{entry}\n")
            print("Statement generated successfully.")
        elif choice == '6':
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

# Main screen loop to show main screen
users = {}
with open('users.txt', 'r') as file:
    for line in file:
        username, data = line.strip().split(':')
        users[username] = eval(data)

while True:
    print("\nMain Menu:")
    print("1. Create Account")
    print("2. Login")
    print("3. Terminate Program")
    choice = input("Enter your choice: ")

    if choice == '1':
        create_account(users)
    elif choice == '2':
        login(users)
    elif choice == '3':
        print("Terminating program.")
        break
    else:
        print("Invalid choice. Please choose a valid option.")
