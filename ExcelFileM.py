import pandas as pd
from faker import Faker
from pathlib import Path


def main():
    # Define the path to the CSV file
    csv_path = Path("data/inventory_raw.csv")
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    print("Loaded inventory data:")
    print(df)
    cont = True
    # Switch-like menu for user action
    while cont:
        print("\nChoose an action:")
        print("1. Identify duplicates")
        print("2. Remove duplicates")
        print("3. Check inventory (OnHandQty < ReorderPoint)")
        print("4. Exit")
        print("5. Show inventory data")
        print("6. Save changes")
        choice = input("User:").strip()
        
        if choice == "0" or choice.lower() in ["exit", "end"]:
            cont = False
        elif choice == "1":
            df = identify_duplicates(df)
        elif choice == "2":
            df = remove_duplicates(df)
        elif choice == "3":
            checking_inventory(df)
            print("Exiting the program.")
        elif choice == "4":
            print(df)
        elif choice == "5":
            df.to_csv("data/inventory_raw_new.csv", index=False)
            print("Changes saved.")
        else:
            print("Invalid choice. Please try again.")

def checking_inventory(df):
    # Check if OnHandQty is less than ReorderPoint
    if "OnHandQty" not in df.columns or "ReorderPoint" not in df.columns:
        print("Required columns 'OnHandQty' or 'ReorderPoint' not found in the data.")
        return
    low_stock = df[df["OnHandQty"] < df["ReorderPoint"]]
    if not low_stock.empty:
        print("\nItems with OnHandQty less than ReorderPoint:")
        print(low_stock)
        choice = input("Do you want to restock these items? (yes/no): ").strip().lower()
        if choice == "yes":
            print("Restocking items by adding ReorderPoint to OnHandQty...")
            mask = df["OnHandQty"] < df["ReorderPoint"]
            df.loc[mask, "OnHandQty"] = df.loc[mask, "OnHandQty"] + df.loc[mask, "ReorderPoint"]
            print("Restocked items:")
            print(df[mask])
        elif choice == "no":
            print("No items will be restocked.")
    else:
        print("\nAll items are sufficiently stocked.")

def remove_duplicates(df):
    # Remove duplicate rows
    df_no_duplicates = df.drop_duplicates()
    print("\nData after removing duplicates:")
    return df_no_duplicates

def identify_duplicates(df):
    # Identify duplicate rows
    duplicates = df[df.duplicated()]
    if not duplicates.empty:
        print("\nDuplicate rows found:")
        print(duplicates)
        choice = input("Do you want to remove duplicates? (yes/no): ").strip().lower()
        if choice == "yes":
            print("Removing duplicates...")
            return remove_duplicates(df)
        elif choice == "no":
            print("Keeping duplicates as is.")
            return df
        else:
            print("Invalid choice. Keeping duplicates as is.")
            return df
    else:
        print("\nNo duplicate rows found.")


if __name__ == "__main__":
    main()

