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
head_parameter[new_mouse_id] = ""

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

    var input1 = createInput("dateofsurgery", "Enter zR1000");
    var input2 = createInput("animalWeight", "Enter Weight before surgery (g)");
    var input3 = createInput("mousebirth", "Mouse date of birth ");
    var input6 = createInput("mouseage", "Enter Mouse age (days)");
    var input5 = createInput("LeftEarBarInitial", "Enter Left ear bar (initial) (mm)");
    var input6 = createInput("RightEarBarInitial", "Enter Right ear bar (initial) (mm)");

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
    inputContainer.appendChild(input1); // dateofsurgery
    inputContainer.appendChild(input2); // animalWeight
    inputContainer.appendChild(input3); // mousebirth
    inputContainer.appendChild(input4); // mouseage
    inputContainer.appendChild(input5); // LeftEarBarInitial
    inputContainer.appendChild(input6); // RightEarBarInitial

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
        var val4 = document.getElementById("mouseage").value;
        var val5 = document.getElementById("LeftEarBarInitial").value;
        var val6 = document.getElementById("RightEarBarInitial").value;
        google.colab.kernel.invokeFunction("notebook.update_correction_result", [val1, val2, val3, val4, val5, val6], {});
    }
    '''))

# Python callback to update the sheet and calculate the midline
def update_data(val1, val2, val3, val4, val5, val6):
    # Debugging: Print the values received
    print(f"Received values from JavaScript: {val1}, {val2}, {val3}, {val4}, {val5}, {val6}")

    try:
        # Fetch the head_parameter DataFrame from Google Sheets
        worksheet = gc.open_by_key(file_id).sheet1
        head_parameter = pd.DataFrame(worksheet.get_all_records())  # Fetch all records from the sheet

        # Overwrite the values in the sheet
        head_parameter.iloc[49, -1] = val1
        head_parameter.iloc[0, -1] = val2
        head_parameter.iloc[50, -1] = val3
        head_parameter.iloc[48, -1] = val4
        head_parameter.iloc[3, -1] = val5
        head_parameter.iloc[4, -1] = val6
      
# Register the callbacks for updating corrections and finishing the process
output.register_callback('notebook.update_data', update_data)

# Initialize the input boxes and the callback
create_input_boxes()

worksheet.clear()
set_with_dataframe(worksheet, head_parameter)
