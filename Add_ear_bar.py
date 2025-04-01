import gspread
import pandas as pd
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from google.colab import auth
from IPython.display import display, Javascript

# Mount Google Drive and authenticate
drive.mount('/content/drive')
auth.authenticate_user()  # Authenticate manually to avoid errors
# Get authenticated credentials
creds, _ = default()
gc = gspread.authorize(creds)

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

    var input1 = createInput("LeftEarBarInitial", "Enter Left ear bar (initial) (mm)");
    var input2 = createInput("RightEarBarInitial", "Enter Right ear bar (initial) (mm)");

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

    // Create a container for the input fields and arrange them in 2 columns
    var inputContainer = document.createElement("div");
    inputContainer.style.display = "grid";
    inputContainer.style.gridTemplateColumns = "1fr 1fr"; // 2 columns
    inputContainer.style.gridGap = "10px";
    inputContainer.style.marginTop = "20px";

     // Append inputs to the container in the desired order (2 columns)
    inputContainer.appendChild(input1); // LeftEarBarInitial
    inputContainer.appendChild(input2); // RightEarBarInitial

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
        var val1 = document.getElementById("LeftEarBarInitial").value;
        var val2 = document.getElementById("RightEarBarInitial").value;
        google.colab.kernel.invokeFunction("notebook.update_data", [val1, val2, {});
    }
    '''))

# Python callback to update the sheet
def update_data(val1, val2):
    try:
        file_id = '17t6CB6Nze274z1od3cmfdKnHZ2OMLdFFay7yMQ_Ofi0'  # Use the correct Google Sheet ID here
        # Fetch the head_parameter DataFrame from Google Sheets
        worksheet = gc.open_by_key(file_id).sheet1
        head_parameter = pd.DataFrame(worksheet.get_all_records())  # Fetch all records from the sheet
        new_mouse_id = head_parameter.columns[-1]  # Assuming last column is new mouse ID

        # Overwrite the values in the sheet (you can change the rows and columns as needed)
        head_parameter.iloc[3, -1] = val1
        head_parameter.iloc[4, -1] = val2

        # Write the updated DataFrame back to the sheet
        worksheet.clear()  # Optional: Use with caution, can clear the entire sheet
        set_with_dataframe(worksheet, head_parameter)  # Update the sheet

        print("Values have been updated successfully in the sheet.")
    except Exception as e:
        # Print the error message if something goes wrong
        print(f"Error while updating the sheet: {e}")

# Register the callback function
from google.colab import output
output.register_callback('notebook.update_data', update_data)


# Initialize the input boxes and the callback after Mouse ID is entered
create_input_boxes()


