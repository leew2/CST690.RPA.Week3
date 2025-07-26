import pandas as pd
import time as time
import smtplib
import logging
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from faker import Faker
from pathlib import Path

def main():
    # Set up logging
    logging.basicConfig(filename="inventory_log.txt", level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    # Define the path to the CSV file
    csv_path = Path("data/inventory_raw.csv")
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)
    print("Loaded inventory data:")

    cont = True
    # Main loop for user interaction
    while cont:
        print("\nChoose an action:")
        print("0. Exit")
        print("1. Identify duplicates")
        print("2. Remove duplicates")
        print("3. Check inventory (OnHandQty < ReorderPoint)")
        print("4. Show inventory data")
        print("5. Save changes")

        choice = input("User:").strip()
        if choice == "0" or choice.lower() in ["exit", "end"]:
            cont = False
        elif choice == "1":
            logging.info("User choose to identify duplicates.")
            start = time.time()
            df = identify_duplicates(df)
            end = time.time()
            print(f"Time taken to identify duplicates: {end - start:.2f} seconds")
        elif choice == "2":
            logging.info("User choose to remove duplicates.")
            start = time.time()
            df = remove_duplicates(df)
            end = time.time()
            print(f"Time taken to remove duplicates: {end - start:.2f} seconds")
        elif choice == "3":
            logging.info("User choose to check inventory.")
            start = time.time()
            checking_inventory(df)
            end = time.time()
            print(f"Time taken to check/restock inventory: {end - start:.2f} seconds")
        elif choice == "4":
            logging.info("User requested to show inventory data.")
            print(df)
        elif choice == "5":
            logging.info("User requested to save changes.")
            df.to_csv("data/inventory_raw_new.csv", index=False)
            print("Changes saved to 'data/inventory_raw_new.csv'")
        else:
            print("Invalid choice. Please try again.")

def checking_inventory(df):
    # Log that checking_inventory was called
    logging.info("Checking inventory for low stock items.")
    # Check if OnHandQty is less than ReorderPoint
    if "OnHandQty" not in df.columns or "ReorderPoint" not in df.columns:
        print("Required columns 'OnHandQty' or 'ReorderPoint' not found in the data.")
        logging.warning("Required columns 'OnHandQty' or 'ReorderPoint' not found in the data.")
        return
    low_stock = df[df["OnHandQty"] < df["ReorderPoint"]]
    amount = low_stock.shape[0]
    logging.info(f"Found {amount} items with OnHandQty less than ReorderPoint.")
    if not low_stock.empty:
        print("\nItems with OnHandQty less than ReorderPoint:")
        print(low_stock)
        # Automatically email the low stock report
        send_low_stock_email(low_stock)

        choice = input("Do you want to restock these items? (yes/no): ").strip().lower()
        logging.info(f"User restock prompt input: {choice}")
        if choice == "yes" or choice == "y":
            print("Restocking items") # Adding ReorderPoint to OnHandQty to Restock
            mask = df["OnHandQty"] < df["ReorderPoint"]
            df.loc[mask, "OnHandQty"] = df.loc[mask, "OnHandQty"] + df.loc[mask, "ReorderPoint"]
            print(df[mask])
            print(f"Restocked {amount} items from {df.shape[0]} total rows.")
            logging.info(f"Restocked {amount} items.")
        elif choice == "no":
            print("No items will be restocked.")
            logging.info("User choose not to restock.")
        else:
            logging.info("User gave invalid input for restock prompt.")

    else:
        print("\nAll items are sufficiently stocked.")
        logging.info("All items are sufficiently stocked.")

def send_low_stock_email(low_stock_df):
    # Prompt user for email details
    sender = "email@example.com"
    password = "password"
    recipient = "email@example.com"
    subject = "Low Stock Inventory Report"
    body = f"Low stock items (OnHandQty < ReorderPoint):\n\n{low_stock_df.to_string(index=False)}"

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Low stock report sent to {recipient}.")
        logging.info(f"Low stock report sent to {recipient}.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        logging.error(f"Failed to send email: {e}")

def remove_duplicates(df):
    # Remove duplicate rows
    df_no_duplicates = df.drop_duplicates()
    print("\nData after removing duplicates:")
    return df_no_duplicates

def identify_duplicates(df):
    # Log that identify_duplicates was called
    logging.info("identify_duplicates called.")
    # Identify duplicate rows
    duplicates = df[df.duplicated()]
    amount = duplicates.shape[0]
    total = df.shape[0]
    logging.info(f"Found {amount} duplicate rows out of {total} total rows.")
    if not duplicates.empty:
        print("\nDuplicate rows found:")
        print(duplicates)
        choice = input("Do you want to remove duplicates? (yes/no): ").strip().lower()
        logging.info(f"User duplicate removal prompt input: {choice}")
        if choice == "yes" or choice == "y":
            print(f"Removing {amount} duplicates from {total} total rows...")
            logging.info(f"Removing {amount} duplicates from {total} total rows.")
            return remove_duplicates(df)
        elif choice == "no" or choice == "n":
            print(f"Keeping {amount} duplicates.")
            logging.info(f"Keeping {amount} duplicates.")
            return df
        else:
            print(f"Invalid choice. Keeping {amount} duplicates.")
            logging.info(f"Invalid input. Keeping {amount} duplicates.")
            return df
    else:
        print("\nNo duplicate rows found.")
        logging.info("No duplicate rows found.")


if __name__ == "__main__":
    start = time.time()
    logging.info("------------- Script execution Started -------------")
    main()
    logging.info("------------- Script execution Ended -------------")
    end = time.time()
    print(f"Total time taken: {end - start:.2f} seconds")

