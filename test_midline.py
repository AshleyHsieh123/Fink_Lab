import gspread
import pandas as pd
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from google.colab import auth
from IPython.display import display, Javascript
import numpy as np

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
        input.style.width = "200px";
        input.style.height = "32px";
        return input;
    }

    var input1 = createInput("xL1500", "Enter xL1500");
    var input2 = createInput("xL2000", "Enter xL2000");
    var input3 = createInput("xL2500", "Enter xL2500");
    var input4 = createInput("xL3500", "Enter xL3500");
    var input5 = createInput("xL4000", "Enter xL4000");
    var input6 = createInput("xL4500", "Enter xL4500");
    var input7 = createInput("xR1500", "Enter xR1500");
    var input8 = createInput("xR2000", "Enter xR2000");
    var input9 = createInput("xR2500", "Enter xR2500");
    var input10 = createInput("xR3500", "Enter xR3500");
    var input11 = createInput("xR4000", "Enter xR4000");
    var input12 = createInput("xR4500", "Enter xR4500");
    var input13 = createInput("zL1500", "Enter zL1500");
    var input14 = createInput("zL2000", "Enter zL2000");
    var input15 = createInput("zL2500", "Enter zL2500");
    var input16 = createInput("zL3500", "Enter zL3500");
    var input17 = createInput("zL4000", "Enter zL4000");
    var input18 = createInput("zL4500", "Enter zL4500");
    var input19 = createInput("zR1500", "Enter zR1500");
    var input20 = createInput("zR2000", "Enter zR2000");
    var input21 = createInput("zR2500", "Enter zR2500");
    var input22 = createInput("zR3500", "Enter zR3500");
    var input23 = createInput("zR4000", "Enter zR4000");
    var input24 = createInput("zR4500", "Enter zR4500");

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

    // Create a container for the input fields and arrange them in 6 columns
    var inputContainer = document.createElement("div");
    inputContainer.style.display = "grid";
    inputContainer.style.gridTemplateColumns = "1fr 1fr 1fr 1fr 1fr 1fr"; // 6 columns
    inputContainer.style.gridGap = "10px";
    inputContainer.style.marginTop = "20px";

    // Append inputs to the container in the desired order (6 columns)
    inputContainer.appendChild(input1); // xL1500
    inputContainer.appendChild(input2); // xL2000
    inputContainer.appendChild(input3); // xL2500
    inputContainer.appendChild(input4); // xL3500
    inputContainer.appendChild(input5); // xL4000
    inputContainer.appendChild(input6); // xL4500
    inputContainer.appendChild(input7); // xR1500
    inputContainer.appendChild(input8); // xR2000
    inputContainer.appendChild(input9); // xR2500
    inputContainer.appendChild(input10); // xR3500
    inputContainer.appendChild(input11); // xR4000
    inputContainer.appendChild(input12); // xR4500
    inputContainer.appendChild(input13); // zL1500
    inputContainer.appendChild(input14); // zL2000
    inputContainer.appendChild(input15); // zL2500
    inputContainer.appendChild(input16); // zL3500
    inputContainer.appendChild(input17); // zL4000
    inputContainer.appendChild(input18); // zL4500
    inputContainer.appendChild(input19); // zR1500
    inputContainer.appendChild(input20); // zR2000
    inputContainer.appendChild(input21); // zR2500
    inputContainer.appendChild(input22); // zR3500
    inputContainer.appendChild(input23); // zR4000
    inputContainer.appendChild(input24); // zR4500

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
    document.body.appendChild(container);

    // Button click actions for Submit and Finish correction
    button.onclick = function() {
        var val1 = document.getElementById("xL1500").value;
        var val2 = document.getElementById("xL2000").value;
        var val3 = document.getElementById("xL2500").value;
        var val4 = document.getElementById("xL3500").value;
        var val5 = document.getElementById("xL4000").value;
        var val6 = document.getElementById("xL4500").value;
        var val7 = document.getElementById("xR1500").value;
        var val8 = document.getElementById("xR2000").value;
        var val9 = document.getElementById("xR2500").value;
        var val10 = document.getElementById("xR3500").value;
        var val11 = document.getElementById("xR4000").value;
        var val12 = document.getElementById("xR4500").value;
        var val13 = document.getElementById("zL1500").value;
        var val14 = document.getElementById("zL2000").value;
        var val15 = document.getElementById("zL2500").value;
        var val16 = document.getElementById("zL3500").value;
        var val17 = document.getElementById("zL4000").value;
        var val18 = document.getElementById("zL4500").value;
        var val19 = document.getElementById("zR1500").value;
        var val20 = document.getElementById("zR2000").value;
        var val21 = document.getElementById("zR2500").value;
        var val22 = document.getElementById("zR3500").value;
        var val23 = document.getElementById("zR4000").value;
        var val24 = document.getElementById("zR4500").value;
        console.log("Submitting data to Python:", [val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12, val13, val14, val15, val16, val17, val18, val19, val20, val21, val22, val23, val24]);
        google.colab.kernel.invokeFunction("notebook.update_correction_result", [val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12, val13, val14, val15, val16, val17, val18, val19, val20, val21, val22, val23, val24], {});
    }

    finishButton.onclick = function() {
        google.colab.kernel.invokeFunction("notebook.finish_correction", [], {});
    }
    '''))

def midline_correction(xL_values, xR_values):
    differences = []
    for xL, xR in zip(xL_values, xR_values):
        differences.append(xL + xR)  # Difference between corresponding xL and xR
    midline = np.mean(differences) / 2  # Calculate the midline by averaging differences and dividing by 2
    return midline
    
# Python callback to update the sheet and calculate the midline
def update_correction_result(val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12, val13, val14, val15, val16, val17, val18, val19, val20, val21, val22, val23, val24):
    try:
        # Fetch the head_parameter DataFrame from Google Sheets
        worksheet = gc.open_by_key(file_id).sheet1
        head_parameter = pd.DataFrame(worksheet.get_all_records())  # Fetch all records from the sheet

        # Overwrite the values in the sheet
        head_parameter.iloc[10, -1] = val1
        head_parameter.iloc[11, -1] = val2
        head_parameter.iloc[12, -1] = val3
        head_parameter.iloc[14, -1] = val4
        head_parameter.iloc[15, -1] = val5
        head_parameter.iloc[16, -1] = val6
        head_parameter.iloc[18, -1] = val7
        head_parameter.iloc[19, -1] = val8
        head_parameter.iloc[20, -1] = val9
        head_parameter.iloc[22, -1] = val10
        head_parameter.iloc[23, -1] = val11
        head_parameter.iloc[24, -1] = val12
        head_parameter.iloc[26, -1] = val13
        head_parameter.iloc[27, -1] = val14
        head_parameter.iloc[28, -1] = val15
        head_parameter.iloc[30, -1] = val16
        head_parameter.iloc[31, -1] = val17
        head_parameter.iloc[32, -1] = val18
        head_parameter.iloc[34, -1] = val19
        head_parameter.iloc[35, -1] = val20
        head_parameter.iloc[36, -1] = val21
        head_parameter.iloc[38, -1] = val22
        head_parameter.iloc[39, -1] = val23
        head_parameter.iloc[40, -1] = val24

        xL_values = list(head_parameter.iloc[9:13,-1].values)
        xR_values = list(head_parameter.iloc[17:21,-1].values)
        
        midline = midline_correction(xL_values,xR_values)
        
        # Display result in result box
        if midline > 0:
            print(f"Calculated midline: {midline}", 'To the left')
        else:
            print(f"Calculated midline: {midline}", 'To the right')
        
        # Write the updated DataFrame back to the sheet
        worksheet.clear()  # Optional: Use with caution, can clear the entire sheet
        set_with_dataframe(worksheet, head_parameter)  # Update the sheet
        return midline
        
    except Exception as e:
        print(f"Error in callback: {e}")

def finish_correction():
    worksheet = gc.open_by_key(file_id).sheet1
    head_parameter = pd.DataFrame(worksheet.get_all_records())

    midline = midline_correction(list(head_parameter.iloc[9:13,-1]),list(head_parameter.iloc[17:21,-1]))
    head_parameter.iloc[9:16, -1] += midline
    head_parameter.iloc[17:24, -1] += midline
    worksheet.clear()  # Optional: Use with caution, can clear the entire sheet
    set_with_dataframe(worksheet, head_parameter)  # Update the sheet
    
# Register the callback function
from google.colab import output
output.register_callback('notebook.update_correction_result', update_correction_result)

# Initialize the input boxes and the callback
create_input_boxes()
