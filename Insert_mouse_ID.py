import gspread
import pandas as pd
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from google.colab import auth
from IPython.display import display, Javascript

# Function to create input boxes and submit button using JS
def create_input_boxes():
    display(Javascript('''
    // Create input elements
    function createInput(id, placeholder) {
        var input = document.createElement("input");
        input.id = id;
        input.placeholder = placeholder;
        input.style.margin = "10px";
        input.style.padding = "12px";
        input.style.fontSize = "16px";
        input.style.width = "250px";
        input.style.height = "40px";
        return input;
    }

    var input1 = createInput("dateofsurgery", "Enter Date of surgery");
    var input2 = createInput("animalWeight", "Enter Weight before surgery (g)");
    var input3 = createInput("mousebirth", "Mouse date of birth ");
    
    // Submit button
    var button = document.createElement("button");
    button.innerHTML = "Submit";
    button.style.margin = "10px";
    button.style.padding = "12px 20px";
    button.style.fontSize = "16px";
    button.style.backgroundColor = "#4CAF50";
    button.style.color = "white";
    button.style.border = "none";
    button.style.borderRadius = "8px";
    button.style.cursor = "pointer";

    // Create a container for the input fields and arrange them in 3 columns
    var inputContainer = document.createElement("div");
    inputContainer.style.display = "grid";
    inputContainer.style.gridTemplateColumns = "1fr 1fr 1fr"; // 3 columns
    inputContainer.style.gridGap = "10px";
    inputContainer.style.marginTop = "20px";

    // Append inputs to the container in the desired order (3 columns)
    inputContainer.appendChild(input1); // dateofsurgery
    inputContainer.appendChild(input2); // animalWeight
    inputContainer.appendChild(input3); // mousebirth

    // Add the container and buttons to the page
    var container = document.createElement("div");
    container.className = "custom-inputs";
    container.style.display = "flex";
    container.style.flexDirection = "column";
    container.style.alignItems = "center";
    container.style.marginTop = "20px";

    container.appendChild(inputContainer);
    container.appendChild(button);
    document.body.appendChild(container);

    // Button click actions for Submit
    button.onclick = function() {
        var val1 = document.getElementById("dateofsurgery").value;
        var val2 = document.getElementById("animalWeight").value;
        var val3 = document.getElementById("mousebirth").value;
        google.colab.kernel.invokeFunction("notebook.update_data", [val1, val2, val3], {});
    }
    '''))

# Python callback to update the sheet
def update_data(val1, val2, val3):
    try:
        from datetime import datetime

        # Mount Google Drive and authenticate
        drive.mount('/content/drive')
        auth.authenticate_user()
        creds, _ = default()
        gc = gspread.authorize(creds)

        # Open the Google Sheet
        file_id = '17t6CB6Nze274z1od3cmfdKnHZ2OMLdFFay7yMQ_Ofi0'
        worksheet = gc.open_by_key(file_id).sheet1
        head_parameter = pd.DataFrame(worksheet.get_all_records())

        # Transpose: field names become columns, mice become rows
        head_parameter = head_parameter.set_index(head_parameter.columns[0]).T

        # Clean ellipsis issues
        head_parameter = head_parameter.applymap(lambda x: pd.NA if isinstance(x, type(...)) else x)
        head_parameter.replace("...", pd.NA, inplace=True)

        # Insert new data for this mouse
        head_parameter.loc[new_mouse_id, "Date of surgery"] = val1
        head_parameter.loc[new_mouse_id, "Weight before surgery (g)"] = val2
        head_parameter.loc[new_mouse_id, "Mouse date of birth"] = val3

        # Step 1: Parse all date strings into datetime
        head_parameter["Date of surgery"] = pd.to_datetime(head_parameter["Date of surgery"], errors="coerce")
        head_parameter["Mouse date of birth"] = pd.to_datetime(head_parameter["Mouse date of birth"], errors="coerce")
        
        # Step 2: Calculate mouse age in days
        head_parameter["Mouse age (days)"] = (
            head_parameter["Date of surgery"] - head_parameter["Mouse date of birth"]
        ).dt.days
        
        # Step 3: Now safely format the datetimes into strings (for clean display in sheet)
        head_parameter["Date of surgery"] = head_parameter["Date of surgery"].apply(
            lambda x: x.strftime("%m/%d/%Y") if pd.notnull(x) else ""
        )
        head_parameter["Mouse date of birth"] = head_parameter["Mouse date of birth"].apply(
            lambda x: x.strftime("%m/%d/%Y") if pd.notnull(x) else ""
        )

        # Transpose back to original layout
        head_parameter = head_parameter.T.reset_index()

        # Write back to the sheet
        worksheet.clear()
        set_with_dataframe(worksheet, head_parameter)

        print("✅ Values updated successfully in the sheet.")

    except Exception as e:
        print(f"❌ Error while updating the sheet: {e}")
        
# Register the callback function
from google.colab import output
output.register_callback('notebook.update_data', update_data)

# Step 1: Ask for Mouse ID first
new_mouse_id = str(input("Mouse ID: "))

# Step 2: Initialize the input boxes and the callback after Mouse ID is entered
create_input_boxes()
