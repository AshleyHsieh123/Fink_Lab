import gspread
import pandas as pd
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from google.colab import auth

# Mount Google Drive and authenticate
drive.mount('/content/drive')
auth.authenticate_user()  # Authenticate manually to avoid errors
# Get authenticated credentials
creds, _ = default()
gc = gspread.authorize(creds)

file_id = '17t6CB6Nze274z1od3cmfdKnHZ2OMLdFFay7yMQ_Ofi0'  # Use the correct Google Sheet ID here
sh = gc.open_by_key(file_id)  # Open the Google Sheet with the file_id
worksheet = sh.get_worksheet(0)  # Select the first sheet

head_parameter = pd.DataFrame(worksheet.get_all_records())  # Fetch all records from the sheet
new_mouse_id = str(input("Mouse ID: "))
 # Calculate the column letter for the new column (e.g., "Z" for the 26th column)
new_column_index = len(head_parameter.columns)  # Index of the newly added column
head_parameter[new_mouse_id] = ""

worksheet.clear()
set_with_dataframe(worksheet, head_parameter)

def get_column_letter(col_idx):
        letter = ''
        while col_idx >= 0:
            letter = chr(col_idx % 26 + 65) + letter
            col_idx = col_idx // 26 - 1
        return letter

column_letter = chr(65 + new_column_index - 1)  # Convert column index to letter (A=65 in ASCII)

  # Apply formatting for the new Mouse ID column header (e.g., bold)
worksheet.format(f'{column_letter}1', {'textFormat': {'bold': True}})


print(f"Mouse ID column '{new_mouse_id}' added to the sheet.")
