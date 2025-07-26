# Inventory Management Python Scripts

This repository contains Python scripts for managing and generating inventory data using Pandas and Faker.

## Files

- **ExcelFileM.py**: Main script for inventory management operations, including duplicate detection, inventory checks, restocking, logging, and email notifications.
- **generate_fake_inventory.py**: (Not shown) Presumably generates fake inventory data using Faker and saves it as a CSV file.
- **data/inventory_raw.csv**: Example inventory data in CSV format.

## Features

- **Duplicate Detection & Removal**: Identify and optionally remove duplicate rows in your inventory data. All actions and user choices are logged to `inventory_log.txt`.
- **Inventory Check & Restock**: Check for items where `OnHandQty` is less than `ReorderPoint`. Optionally restock these items by adding the reorder amount. The number of low-stock items is logged.
- **Email Notification**: When low stock is detected, a report is automatically emailed (Gmail SMTP) to a specified recipient. Update sender/recipient credentials in the script as needed.
- **Logging**: All major actions, user choices, and results are logged to `inventory_log.txt` for auditing and troubleshooting.

## Requirements

- Python 3.7+
- pandas
- faker

Install dependencies with:

```
pip install pandas faker
```

## Usage
1. Run `generate_fake_inventory.py` to generate new inventory data.
2. Run the main script:
   ```
   python ExcelFileM.py
   ```

## Folder Structure

```
.
├── ExcelFileM.py
├── generate_fake_inventory.py
├── data/
│   └── inventory_raw.csv
├── inventory_log.txt
```

## Notes

- To enable email notifications, update the sender, password, and recipient in the `send_low_stock_email` function in `ExcelFileM.py`.
- Email does not work due to google(?) try your own
- All user actions and important events are logged in `inventory_log.txt`.

## License

This project is for educational purposes.
** Created With Copilot **