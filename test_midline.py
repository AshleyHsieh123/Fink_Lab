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
creds, _ = default()
gc = gspread.authorize(creds)

# Open the Google Sheet
file_id = '17t6CB6Nze274z1od3cmfdKnHZ2OMLdFFay7yMQ_Ofi0'  # Use the correct Google Sheet ID here
sh = gc.open_by_key(file_id)  # Open the Google Sheet with the file_id
worksheet = sh.get_worksheet(0)  # Select the first sheet

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

    var input1 = createInput("xL1500", "Enter xL1500");
    var input2 = createInput("xL2000", "Enter xL2000");
    var input3 = createInput("xL2500", "Enter xL2500");
    var input4 = createInput("xR1500", "Enter xR1500");
    var input5 = createInput("xR2000", "Enter xR2000");
    var input6 = createInput("xR2500", "Enter xR2500");
    var input7 = createInput("zL1500", "Enter zL1500");
    var input8 = createInput("zL2000", "Enter zL2000");
    var input9 = createInput("zL2500", "Enter zL2500");
    var input10 = createInput("zR1500", "Enter zR1500");
    var input11 = createInput("zR2000", "Enter zR2000");
    var input12 = createInput("zR2500", "Enter zR2500");

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

    // Finish correction button
    var finishButton = document.createElement("button");
    finishButton.innerHTML = "Finish Correction";
    finishButton.style.margin = "10px";
    finishButton.style.padding = "12px 20px";
    finishButton.style.fontSize = "16px";
    finishButton.style.backgroundColor = "#FF5733";
    finishButton.style.color = "white";
    finishButton.style.border = "none";
    finishButton.style.borderRadius = "8px";
    finishButton.style.cursor = "pointer";

    // Result output box
    var resultBox = document.createElement("textarea");
    resultBox.id = "resultBox";
    resultBox.style.margin = "10px";
    resultBox.style.padding = "12px";
    resultBox.style.fontSize = "16px";
    resultBox.style.width = "250px";
    resultBox.style.height = "100px";
    resultBox.style.display = "block";  // Ensure it's visible by default
    resultBox.readOnly = true;

    // Create a container for the input fields and arrange them in 3 columns
    var inputContainer = document.createElement("div");
    inputContainer.style.display = "grid";
    inputContainer.style.gridTemplateColumns = "1fr 1fr 1fr"; // 3 columns
    inputContainer.style.gridGap = "10px";
    inputContainer.style.marginTop = "20px";

    // Append inputs to the container in the desired order (3 columns)
    inputContainer.appendChild(input1); // xL1500
    inputContainer.appendChild(input2); // xL2000
    inputContainer.appendChild(input3); // xL2500
    inputContainer.appendChild(input4); // xR1500
    inputContainer.appendChild(input5); // xR2000
    inputContainer.appendChild(input6); // xR2500
    inputContainer.appendChild(input7); // zL1500
    inputContainer.appendChild(input8); // zL2000
    inputContainer.appendChild(input9); // zL2500
    inputContainer.appendChild(input10); // zR1500
    inputContainer.appendChild(input11); // zR2000
    inputContainer.appendChild(input12); // zR2500

    // Add the container, buttons, and result box to the page
    var container = document.createElement("div");
    container.className = "custom-inputs";
    container.style.display = "flex";
    container.style.flexDirection = "column";
    container.style.alignItems = "center";
    container.style.marginTop = "20px";

    container.appendChild(inputContainer);
    container.appendChild(button);
    container.appendChild(finishButton);
    container.appendChild(resultBox);
    document.body.appendChild(container);

    // Button click actions for Submit and Finish correction
    button.onclick = function() {
        var val1 = document.getElementById("xL1500").value;
        var val2 = document.getElementById("xL2000").value;
        var val3 = document.getElementById("xL2500").value;
        var val4 = document.getElementById("xR1500").value;
        var val5 = document.getElementById("xR2000").value;
        var val6 = document.getElementById("xR2500").value;
        var val7 = document.getElementById("zL1500").value;
        var val8 = document.getElementById("zL2000").value;
        var val9 = document.getElementById("zL2500").value;
        var val10 = document.getElementById("zR1500").value;
        var val11 = document.getElementById("zR2000").value;
        var val12 = document.getElementById("zR2500").value;
        console.log("Submitting data to Python:", [val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12]);
        google.colab.kernel.invokeFunction("notebook.update_correction_result", [val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12], {});
    }

    finishButton.onclick = function() {
        var val1 = document.getElementById("xL1500").value;
        var val2 = document.getElementById("xL2000").value;
        var val3 = document.getElementById("xL2500").value;
        var val4 = document.getElementById("xR1500").value;
        var val5 = document.getElementById("xR2000").value;
        var val6 = document.getElementById("xR2500").value;
        var val7 = document.getElementById("zL1500").value;
        var val8 = document.getElementById("zL2000").value;
        var val9 = document.getElementById("zL2500").value;
        var val10 = document.getElementById("zR1500").value;
        var val11 = document.getElementById("zR2000").value;
        var val12 = document.getElementById("zR2500").value;
        google.colab.kernel.invokeFunction("notebook.finish_correction", [val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12], {});
    }
    '''))

    
# Python callback to update the sheet and calculate the midline
def update_correction_result(val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12):
    # Debugging: Print the values received
    print(f"Received values from JavaScript: {val1}, {val2}, {val3}, {val4}, {val5}, {val6}, {val7}, {val8}, {val9}, {val10}, {val11}, {val12}")

    try:
        # Fetch the head_parameter DataFrame from Google Sheets
        worksheet = gc.open_by_key(file_id).sheet1
        head_parameter = pd.DataFrame(worksheet.get_all_records())  # Fetch all records from the sheet

        # Overwrite the values in the sheet
        head_parameter.iloc[10, -1] = val1
        head_parameter.iloc[11, -1] = val2
        head_parameter.iloc[12, -1] = val3
        head_parameter.iloc[18, -1] = val4
        head_parameter.iloc[19, -1] = val5
        head_parameter.iloc[20, -1] = val6
        head_parameter.iloc[26, -1] = val7
        head_parameter.iloc[27, -1] = val8
        head_parameter.iloc[28, -1] = val9
        head_parameter.iloc[34, -1] = val10
        head_parameter.iloc[35, -1] = val11
        head_parameter.iloc[36, -1] = val12

        # Calculate the midline using xL and xR values at different points
        # Fetching xL1000, xR1000, xL3000, xR3000 from the sheet
        xL_values = [
            float(val1),  # xL1500
            float(val2),  # xL2000
            float(val3),  # xL2500
            float(head_parameter['xL1000'][0]),  # xL1000 from the sheet
            float(head_parameter['xL3000'][0])   # xL3000 from the sheet
        ]
        
        xR_values = [
            float(val4),  # xR1500
            float(val5),  # xR2000
            float(val6),  # xR2500
            float(head_parameter['xR1000'][0]),  # xR1000 from the sheet
            float(head_parameter['xR3000'][0])   # xR3000 from the sheet
        ]

        differences = []
        for xL, xR in zip(xL_values, xR_values):
            differences.append(xL + xR)  # Difference between corresponding xL and xR

        midline = sum(differences) / len(differences) / 2  # Calculate the midline by averaging differences and dividing by 2
        
        # Display result in result box
        print(f"Calculated midline: {midline}")
        
        # Write the updated DataFrame back to the sheet
        worksheet.clear()  # Optional: Use with caution, can clear the entire sheet
        set_with_dataframe(worksheet, head_parameter)  # Update the sheet

        print("Values have been updated successfully in the sheet.")
    except Exception as e:
        print(f"Error in callback: {e}")

# Register the callback function
from google.colab import output
output.register_callback('notebook.update_correction_result', update_correction_result)

# Initialize the input boxes and the callback
create_input_boxes()
