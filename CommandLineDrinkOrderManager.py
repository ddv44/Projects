import mysql.connector
from mysql.connector import Error

#Function to create a database connection
def create_con(hostname, username, userpw, dbname):
    connection = None
    success = False
    try:
        connection = mysql.connector.connect(
            host = hostname,
            user = username,
            password = userpw,
            database = dbname
        )
        success = True
    except Error as e:   #catch error
        print(f'The error {e} occured')
    return connection, success
    #If the connection is sucessful, set success flag to True

#Function to print the list of drinks available
def print_drinks(cursor):
    try:
        #SQL query to select all columns from the DRINKS table
        sql = 'SELECT *, id, drinkname, price FROM DRINKS'
        #Execute the SQL query
        cursor.execute(sql)
        #Fetch all rows from the result set
        drinks = cursor.fetchall()
        #Iterate through each row and print the drink details
        for drink in drinks:
            print(f"{drink[0]} - {drink[1]}: ${drink[2]}")
    except Error as e:
        #Print error message if fetching drinks fails
        print(f'Error fetching drinks: {e}')

# Function to get information about a specific drink
def get_drink_info(cursor,drink_ID):
    try:
        # SQL query to select description and color of the drink with the given ID
        cursor.execute("SELECT description, color FROM DRINKS WHERE id = %s", (drink_ID,))
        #Fetch the first row from the result set
        drink_info = cursor.fetchone()
        #Check if drink_info is not None
        if drink_info:
            print(f'Description: {drink_info[0]}')
            print(f'Color: {drink_info[1]}')
        else:
            #Print message if drink is not found
            print("Drink not found")
        
    except Error as e:
        print(f'Error fetching drink information: {e}')

#Main function
def main():

    conn, success = create_con('cis3368spring1.c3y48ko4g3p8.us-east-1.rds.amazonaws.com', 'admin', 'ktdv7180TT', 'DRINKS_MENU')
    
    if success:
        cursor = conn.cursor()
        # Initialize an empty list to store the order
        order = []
        # Print the list of available drinks
        print_drinks(cursor)
        
        while True:
             # Prompt the user to choose an action (start an order or get information about a drink)
            action = input("Do you want to start an order (A) or get information about a drink (B)? ").upper()
            if action == 'B':
                 # If user chooses to get information about a drink, prompt for the drink ID
                drink_ID = input("Enter the number/ID of the drink you want info on: ")
                 # Call the get_drink_info function to fetch and print drink information
                get_drink_info(cursor, drink_ID)
                
            elif action == 'A':
                while True:
                    # If user chooses to start an order, prompt for the drink ID to add to the order
                    drink_ID = input("Enter the number/ID of the drink you want to add to your order: ")
                    if drink_ID == "":
                        break
                    try:
                        # Convert the input to an integer (drink ID)
                        drink_ID = int(drink_ID)
                        # Execute SQL query to fetch the price of the drink with the given ID
                        cursor.execute("SELECT price FROM DRINKS WHERE id = %s", (drink_ID,))
                        # Fetch the price of the drink
                        price = cursor.fetchone()
                        if price:
                             # If price is fetched successfully, add the drink ID to the order list
                            order.append(drink_ID)
                            print(f'Added {drink_ID} to the order')

                            # Ask if the user wants to add another drink
                            add_another = input("Do you want to add another drink to your order? (Y/N): ").upper()
                            if add_another == 'Y':
                                 # Continue adding drinks if user chooses 'Y'
                                continue
                            elif add_another == 'N':
                                # Break out of the loop if user chooses 'N'
                                break
                            else:
                                print("Invalid input, please enter 'Y' or 'N'")
                        else:
                            print('Invalid drink number, please select a valid drink(number/ID)')
                    except ValueError:
                        print("Invalid input. Please enter a number.")

                # Calculate total and print receipt
                total_amount = 0
                for drink_ID in order:
                    cursor.execute("SELECT price FROM DRINKS WHERE id = %s", (drink_ID,))
                    price = cursor.fetchone()
                    if price:
                        total_amount += price[0]

                print("Receipt:")
                for drink_ID in order:
                    cursor.execute("SELECT drinkname, price FROM DRINKS WHERE id = %s", (drink_ID,))
                    drink_info = cursor.fetchone()
                    if drink_info:
                        print(f"{drink_info[0]}: ${drink_info[1]}")
                print(f"Total: ${total_amount}")
                break

            else:
                print("Invalid input, enter either 'A' or 'B'")
                continue
                
    else:
        print('Connection failed')


if __name__ == "__main__":
    main()
