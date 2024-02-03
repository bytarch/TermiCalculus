import logging
import numpy as np
from sympy import symbols, sqrt, cbrt, integrate, diff, solve
import sqlite3

# Configure logging to write to a file
logging.basicConfig(filename='logs.spp', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a connection and cursor for the SQLite database
conn = sqlite3.connect('calculus_database.db')
cursor = conn.cursor()

# Create a table to store calculations
cursor.execute('''
    CREATE TABLE IF NOT EXISTS calculations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operation TEXT,
        input_text TEXT,
        result TEXT
    )
''')
conn.commit()

def save_calculation(operation, input_text, result):
    cursor.execute('INSERT INTO calculations (operation, input_text, result) VALUES (?, ?, ?)', (operation, input_text, result))
    conn.commit()

def display_previous_calculations():
    cursor.execute('SELECT * FROM calculations')
    calculations = cursor.fetchall()

    print("\nPrevious Calculations:")
    for calc in calculations:
        print(f"ID: {calc[0]}, Operation: {calc[1]}, Input: {calc[2]}, Result: {calc[3]}")

def calculate_derivative(coefficients, x):
    poly = sum(c * x**i for i, c in enumerate(coefficients))
    derivative = diff(poly, x)
    return derivative

def calculate_integral(coefficients, a, b):
    x = symbols('x')
    poly = sum(c * x**i for i, c in enumerate(coefficients))
    integral = integrate(poly, (x, a, b))
    return integral

def solve_polynomial(coefficients, initial_guess):
    x = symbols('x')
    poly = sum(c * x**i for i, c in enumerate(coefficients))
    derivative = diff(poly, x)
    root = solve(poly, x, initial_guess)
    return root[0] if root else None

def main():
    coefficients = []

    while True:
        print("\nChoose operation:")
        print("1. Differentiation of Polynomial")
        print("2. Integration of Polynomial")
        print("3. Solve Polynomial Equation")
        print("4. Square Root")
        print("5. Cube Root")
        print("6. Perfect Square Check")
        print("7. View Previous Calculations")
        print("8. Quit")

        choice = input("Enter choice (1-8): ")

        if choice == '1':
            coefficients = list(map(float, input("Enter the coefficients of the polynomial (highest order to constant term, separated by spaces): ").split()))
            x = float(input("Enter value of x for differentiation: "))
            result = calculate_derivative(coefficients, x)
            save_calculation("Differentiation", f"Coefficients: {coefficients}, x: {x}", result)
            print(f"Derivative at x = {x} is: {result}")
            logging.info(f"Differentiation: Coefficients={coefficients}, x={x}, Result={result}")

        elif choice == '2':
            coefficients = list(map(float, input("Enter the coefficients of the polynomial (highest order to constant term, separated by spaces): ").split()))
            a = float(input("Enter lower limit (a) for integration: "))
            b = float(input("Enter upper limit (b) for integration: "))
            result = calculate_integral(coefficients, a, b)
            save_calculation("Integration", f"Coefficients: {coefficients}, Lower limit: {a}, Upper limit: {b}", result)
            print(f"Integral from {a} to {b} is: {result}")
            logging.info(f"Integration: Coefficients={coefficients}, Lower limit={a}, Upper limit={b}, Result={result}")

        elif choice == '3':
            coefficients = list(map(float, input("Enter the coefficients of the polynomial (highest order to constant term, separated by spaces): ").split()))
            initial_guess = float(input("Enter initial guess for solving polynomial equation: "))
            result = solve_polynomial(coefficients, initial_guess)
            save_calculation("Polynomial Solving", f"Coefficients: {coefficients}, Initial guess: {initial_guess}", result)
            if result is not None:
                print(f"Root of the polynomial equation is: {result}")
            else:
                print("Unable to find a root.")
            logging.info(f"Polynomial Solving: Coefficients={coefficients}, Initial guess={initial_guess}, Result={result}")

        elif choice == '4':
            number = float(input("Enter a number for square root: "))
            result = sqrt(number)
            save_calculation("Square Root", f"Number: {number}", result)
            print(f"Square root of {number} is: {result}")
            logging.info(f"Square Root: Number={number}, Result={result}")

        elif choice == '5':
            number = float(input("Enter a number for cube root: "))
            result = cbrt(number)
            save_calculation("Cube Root", f"Number: {number}", result)
            print(f"Cube root of {number} is: {result}")
            logging.info(f"Cube Root: Number={number}, Result={result}")

        elif choice == '6':
            number = float(input("Enter a number for perfect square check: "))
            result = "Perfect Square" if np.sqrt(number).is_integer() else "Not a Perfect Square"
            save_calculation("Perfect Square Check", f"Number: {number}", result)
            print(result)
            logging.info(f"Perfect Square Check: Number={number}, Result={result}")

        elif choice == '7':
            display_previous_calculations()

        elif choice == '8':
            print("Exiting the program. Goodbye!")
            logging.info("Program exit")
            break

        else:
            print("Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    main()

# Close the database connection when the program exits
conn.close()
