import gspread
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import base64
from io import BytesIO
import seaborn as sns
import glob
import os
import gdown
from google.colab import files
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from google.colab import auth
from IPython.display import display, Javascript
from IPython.display import display, Image
from IPython.display import HTML

# Mount Google Drive and authenticate
drive.mount('/content/drive')
auth.authenticate_user()  # Authenticate manually to avoid errors
creds, _ = default()
gc = gspread.authorize(creds)

# Open the Google Sheet
file_id = '17t6CB6Nze274z1od3cmfdKnHZ2OMLdFFay7yMQ_Ofi0'  # Use the correct Google Sheet ID here
sh = gc.open_by_key(file_id)  # Open the Google Sheet with the file_id
worksheet = gc.open_by_key(file_id).sheet1
head_parameter = pd.DataFrame(worksheet.get_all_records())  # Fetch all records from the sheet

# mouse ID
global mouse_id, num_mice
mice = np.array(head_parameter.columns[60:])
num_mice = len(mice) # count the number of mice
mouse_id = mice[-1]

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

    var input1 = createInput("xL1000", "Enter xL1000");
    var input2 = createInput("xL1500", "Enter xL1500");
    var input3 = createInput("xL2000", "Enter xL2000");
    var input4 = createInput("xL2500", "Enter xL2500");
    var input5 = createInput("xL3000", "Enter xL3000");
    var input6 = createInput("xL3500", "Enter xL3500");
    var input7 = createInput("xL4000", "Enter xL4000");
    var input8 = createInput("xL4500", "Enter xL4500");
    var input9 = createInput("xR1000", "Enter xR1000");
    var input10 = createInput("xR1500", "Enter xR1500");
    var input11 = createInput("xR2000", "Enter xR2000");
    var input12 = createInput("xR2500", "Enter xR2500");
    var input13 = createInput("xR3000", "Enter xR3000");
    var input14 = createInput("xR3500", "Enter xR3500");
    var input15 = createInput("xR4000", "Enter xR4000");
    var input16 = createInput("xR4500", "Enter xR4500");
    var input17 = createInput("zL1000", "Enter zL1000");
    var input18 = createInput("zL1500", "Enter zL1500");
    var input19 = createInput("zL2000", "Enter zL2000");
    var input20 = createInput("zL2500", "Enter zL2500");
    var input21 = createInput("zL3000", "Enter zL3000");
    var input22 = createInput("zL3500", "Enter zL3500");
    var input23 = createInput("zL4000", "Enter zL4000");
    var input24 = createInput("zL4500", "Enter zL4500");
    var input25 = createInput("zR1000", "Enter zR1000");
    var input26 = createInput("zR1500", "Enter zR1500");
    var input27 = createInput("zR2000", "Enter zR2000");
    var input28 = createInput("zR2500", "Enter zR2500");
    var input29 = createInput("zR3000", "Enter zR3000");
    var input30 = createInput("zR3500", "Enter zR3500");
    var input31 = createInput("zR4000", "Enter zR4000");
    var input32 = createInput("zR4500", "Enter zR4500");

    // correction result box
    var resultBox = document.createElement("textarea");
    resultBox.id = "resultBox";
    resultBox.style.margin = "10px";
    resultBox.style.padding = "12px";
    resultBox.style.fontSize = "16px";
    resultBox.style.width = "500px";
    resultBox.style.height = "200px";
    resultBox.style.display = "block";  // Ensure it's visible by default
    resultBox.readOnly = true;

    // Plot result box (for embedding the plot)
    var plotBox1 = document.createElement("div");
    plotBox1.id = "plotBox1";
    plotBox1.style.margin = "10px";
    plotBox1.style.height = "1600px";  // Adjusted height for better image display
    plotBox1.style.width = "80%";
    plotBox1.style.display = "flex";
    plotBox1.style.justifyContent = "center";
    plotBox1.style.alignItems = "center";
    plotBox1.style.backgroundColor = "#ffe0e0";  // Light red-pink for Plot 1

    var plotBox2 = document.createElement("div");
    plotBox2.id = "plotBox2";
    plotBox2.style.margin = "10px";
    plotBox2.style.height = "1500px";  // Adjusted height for better image display
    plotBox2.style.width = "80%";
    plotBox2.style.display = "flex";
    plotBox2.style.justifyContent = "center";
    plotBox2.style.alignItems = "center";
    plotBox2.style.backgroundColor = "#e0f7ff";  // Light blue for Plot 2

    var plotBox3 = document.createElement("div");
    plotBox3.id = "plotBox3";
    plotBox3.style.margin = "10px";
    plotBox3.style.height = "1500px";  // Adjusted height for better image display
    plotBox3.style.width = "80%";
    plotBox3.style.display = "flex";
    plotBox3.style.justifyContent = "center";
    plotBox3.style.alignItems = "center";
    plotBox3.style.backgroundColor = "#e9ffe0";  // Light green for Plot 3
    
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

    // Finish correction and write into the sheet button
    var finishButton = document.createElement("button");
    finishButton.innerHTML = "Finish Correction and write into the sheet";
    finishButton.style.margin = "10px";
    finishButton.style.padding = "12px 20px";
    finishButton.style.fontSize = "16px";
    finishButton.style.backgroundColor = "#FF5733";
    finishButton.style.color = "white";
    finishButton.style.border = "none";
    finishButton.style.borderRadius = "8px";
    finishButton.style.cursor = "pointer";

    // Create a container for the input fields and arrange them in 8 columns
    var inputContainer = document.createElement("div");
    inputContainer.style.display = "grid";
    inputContainer.style.gridTemplateColumns = "1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr"; // 8 columns
    inputContainer.style.gridGap = "10px";
    inputContainer.style.marginTop = "20px";

    // Append inputs to the container in the desired order (8 columns)
    inputContainer.appendChild(input1); // xL1000
    inputContainer.appendChild(input2); // xL1500
    inputContainer.appendChild(input3); // xL2000
    inputContainer.appendChild(input4); // xL2500
    inputContainer.appendChild(input5); // xL3000
    inputContainer.appendChild(input6); // xL3500
    inputContainer.appendChild(input7); // xL4000
    inputContainer.appendChild(input8); // xL4500
    inputContainer.appendChild(input9); // xR1000
    inputContainer.appendChild(input10); // xR1500
    inputContainer.appendChild(input11); // xR2000
    inputContainer.appendChild(input12); // xR2500
    inputContainer.appendChild(input13); // xR3000
    inputContainer.appendChild(input14); // xR3500
    inputContainer.appendChild(input15); // xR4000
    inputContainer.appendChild(input16); // xR4500
    inputContainer.appendChild(input17); // zL1000
    inputContainer.appendChild(input18); // zL1500
    inputContainer.appendChild(input19); // zL2000
    inputContainer.appendChild(input20); // zL2500
    inputContainer.appendChild(input21); // zL3000
    inputContainer.appendChild(input22); // zL3500
    inputContainer.appendChild(input23); // zL4000
    inputContainer.appendChild(input24); // zL4500
    inputContainer.appendChild(input25); // zR1000
    inputContainer.appendChild(input26); // zR1500
    inputContainer.appendChild(input27); // zR2000
    inputContainer.appendChild(input28); // zR2500
    inputContainer.appendChild(input29); // zR3000
    inputContainer.appendChild(input30); // zR3500
    inputContainer.appendChild(input31); // zR4000
    inputContainer.appendChild(input32); // zR4500

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
    container.appendChild(plotBox1);
    container.appendChild(plotBox2);
    container.appendChild(plotBox3);
    document.body.appendChild(container);

    // Button click actions for Submit and Finish correction
    button.onclick = function() {
        var val1 = document.getElementById("xL1000").value;
        var val2 = document.getElementById("xL1500").value;
        var val3 = document.getElementById("xL2000").value;
        var val4 = document.getElementById("xL2500").value;
        var val5 = document.getElementById("xL3000").value;
        var val6 = document.getElementById("xL3500").value;
        var val7 = document.getElementById("xL4000").value;
        var val8 = document.getElementById("xL4500").value;
        var val9 = document.getElementById("xR1000").value;
        var val10 = document.getElementById("xR1500").value;
        var val11 = document.getElementById("xR2000").value;
        var val12 = document.getElementById("xR2500").value;
        var val13 = document.getElementById("xR3000").value;
        var val14 = document.getElementById("xR3500").value;
        var val15 = document.getElementById("xR4000").value;
        var val16 = document.getElementById("xR4500").value;
        var val17 = document.getElementById("zL1000").value;
        var val18 = document.getElementById("zL1500").value;
        var val19 = document.getElementById("zL2000").value;
        var val20 = document.getElementById("zL2500").value;
        var val21 = document.getElementById("zL3000").value;
        var val22 = document.getElementById("zL3500").value;
        var val23 = document.getElementById("zL4000").value;
        var val24 = document.getElementById("zL4500").value;
        var val25 = document.getElementById("zR1000").value;
        var val26 = document.getElementById("zR1500").value;
        var val27 = document.getElementById("zR2000").value;
        var val28 = document.getElementById("zR2500").value;
        var val29 = document.getElementById("zR3000").value;
        var val30 = document.getElementById("zR3500").value;
        var val31 = document.getElementById("zR4000").value;
        var val32 = document.getElementById("zR4500").value;
        console.log("Submitting data to Python:", [val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12, val13, val14, val15, val16, val17, val18, val19, val20, val21, val22, val23, val24, val25, val26, val27, val28, val29, val30, val31, val32]);
        google.colab.kernel.invokeFunction("notebook.update_correction_result", [val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12, val13, val14, val15, val16, val17, val18, val19, val20, val21, val22, val23, val24, val25, val26, val27, val28, val29, val30, val31, val32], {});
    }

        finishButton.onclick = function() {
          google.colab.kernel.invokeFunction("notebook.finish_correction", [], {});
        }
    '''))
    
def output_result(result, append=True):
    js_code = f'''
    var resultBox = document.getElementById("resultBox");
    resultBox.style.display = "block";
    {"resultBox.value += `\\n\\n" + `" + result + "`;" if append else "resultBox.value = `" + result + "`;"} 
    '''
    display(Javascript(js_code))

def midline_correction(xL_values, xR_values):
    meanL = abs(np.mean(xL_values))
    meanR = abs(np.mean(xR_values))
    midline = abs(meanL-meanR) / 2  # Calculate the midline by averaging differences and dividing by 2
    if meanL - meanR < 0:
        midline = midline * -1
    return midline

# Python callback to compute corrections and update Google Sheets
def CorrectionCalculation(xR1000, xR3000, zR1000, zR3000, xL1000, xL3000, zL1000, zL3000):
    try:
        # Convert all values to float
        
        xR1000 = float(xR1000)
        xR3000 = float(xR3000)
        zR1000 = float(zR1000)
        zR3000 = float(zR3000)
        xL1000 = float(xL1000)
        xL3000 = float(xL3000)
        zL1000 = float(zL1000)
        zL3000 = float(zL3000)
        
        # Theta Calculations
        Theta_L = round(-math.atan((xL3000 - xL1000) / 2000) * 180 /  math.pi, 4)
        Theta_R = round(math.atan((xR3000 - xR1000) / 2000) * 180 / math.pi, 4)
        
        YawCorrection = round((Theta_R - Theta_L) / 2, 3)
        
        # Offsets and Ratios
        Zoffset1000 = zL1000 - zR1000
        Zoffset3000 = zL3000 - zR3000
        Xoffset1000 = xR1000 - xL1000
        Xoffset3000 = xR3000 - xL3000
        Ratio1000 = Zoffset1000 / Xoffset1000
        Ratio3000 = Zoffset3000 / Xoffset3000
        
        # Angle Calculations
        Angle1000 = round(math.atan(Ratio1000) * 180 /math.pi, 2)
        Angle3000 = round(math.atan(Ratio3000) * 180 /math.pi, 2)
        RollCorrection = round((Angle1000 + Angle3000) / 2, 2)
        
        if YawCorrection > 0:
            Yawdirection = 'clockwise'
        elif YawCorrection < 0:
            Yawdirection = 'counterclockwise'
        
        if RollCorrection > 0:
            Rolldirection = 'counterclockwise'
        elif RollCorrection < 0:
            Rolldirection = 'clockwise'
        
        # Compose result
        result = (
            f"Yaw correction: {abs(YawCorrection)}°, {Yawdirection}\\n\\n"
            f"Roll correction: {abs(RollCorrection)}°, {Rolldirection}\\n\\n"
        )

        # Return results
        return YawCorrection, RollCorrection, result

    except ValueError:
        result = "Please enter valid numerical values."
        return None, None, result
    
# Python callback to update the sheet and calculate the midline
def update_correction_result(val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12, val13, val14, val15, val16, val17, val18, val19, val20, val21, val22, val23, val24, val25, val26, val27, val28, val29, val30, val31, val32):
    # Fetch the head_parameter DataFrame from Google Sheets
    worksheet = gc.open_by_key(file_id).sheet1
    head_parameter = pd.DataFrame(worksheet.get_all_records())  # Fetch all records from the sheet
    
    # Overwrite the values in the sheet
    head_parameter.iloc[9, -1] = val1
    head_parameter.iloc[10, -1] = val2
    head_parameter.iloc[11, -1] = val3
    head_parameter.iloc[12, -1] = val4
    head_parameter.iloc[13, -1] = val5
    head_parameter.iloc[14, -1] = val6
    head_parameter.iloc[15, -1] = val7
    head_parameter.iloc[16, -1] = val8
    head_parameter.iloc[17, -1] = val9
    head_parameter.iloc[18, -1] = val10
    head_parameter.iloc[19, -1] = val11
    head_parameter.iloc[20, -1] = val12
    head_parameter.iloc[21, -1] = val13
    head_parameter.iloc[22, -1] = val14
    head_parameter.iloc[23, -1] = val15
    head_parameter.iloc[24, -1] = val16
    head_parameter.iloc[25, -1] = val17
    head_parameter.iloc[26, -1] = val18
    head_parameter.iloc[27, -1] = val19
    head_parameter.iloc[28, -1] = val20
    head_parameter.iloc[29, -1] = val21
    head_parameter.iloc[30, -1] = val22
    head_parameter.iloc[31, -1] = val23
    head_parameter.iloc[32, -1] = val24
    head_parameter.iloc[33, -1] = val25
    head_parameter.iloc[34, -1] = val26
    head_parameter.iloc[35, -1] = val27
    head_parameter.iloc[36, -1] = val28
    head_parameter.iloc[37, -1] = val29
    head_parameter.iloc[38, -1] = val30
    head_parameter.iloc[39, -1] = val31
    head_parameter.iloc[40, -1] = val32
    
    xL_values = [float(x) for x in list(head_parameter.iloc[9:12,-1])]
    xR_values = [float(x) for x in list(head_parameter.iloc[17:20,-1])]
    midline = midline_correction(xL_values,xR_values)
    
    # Display result in result box
    if midline > 0:
        result_m = (f"Calculated midline: \\n {abs(midline):.3f} To the left")
    else:
        result_m = (f"Calculated midline: \\n {abs(midline):.3f} To the right")
    
    YawCorrection, RollCorrection, result_yr = CorrectionCalculation(val9, val13, val25, val29, val1, val5, val17, val21)
    
    head_parameter.iloc[53, -1] = midline
    head_parameter.iloc[54, -1] = YawCorrection
    head_parameter.iloc[55, -1] = RollCorrection
    
    # Write the updated DataFrame back to the sheet
    worksheet.clear()  # Optional: Use with caution, can clear the entire sheet
    set_with_dataframe(worksheet, head_parameter)  # Update the sheet
    output_result(result_m)
    output_result(result_yr)
    
# Functions
# Function to determine if the value is in the range mean ± STD
def isInside(value,mean,std):
    if value <= mean + 2*std and value >= mean - 2*std:
        return True # Value is inside the range
    else:
        return False # Value is outside the range


# Function for histogram
# raw_data: list like or pandas DataFrame, with only on dimension. Can tolerant nan or str in the data (drop it automatically)
# name: name of the histogram.
# row: row of the subplot
# col: column of the subplot
# unit: unit of the histogram
# mousedata: individual mouse data, with one value only

def HistoSubplot(raw_data,name,row,col,unit,mousedata,**kwargs):
    # Data processing
    raw_data = pd.DataFrame(raw_data)
    raw_data.columns = [0]
    data = raw_data.dropna() # drop NaN values
    data_mean = data.mean()[0]
    data_std = data.std()[0]

    # if 'bins' exist in the input, set the binwidth to the bins input
    # else: set the binwidth to STD/2
    if 'bins' in kwargs:
        binwidth = kwargs['bins']
    else:
        binwidth = data_std/2 # binsize
    bins = np.arange(data.min()[0], data.max()[0] + binwidth, binwidth)

    y, x, _ = axs[row,col].hist(data, color = 'black',bins = bins, rwidth = 0.8) # obtain x and y of the histogram
    mouseY = 1.1*max(y) # calculate max height of the histogram

    # plotting histogram for [i,j] panel
    axs[row,col].axvline(data_mean,lw = 2,color = 'black', ls = '--') # mean
    for n in [1,-1]:
        axs[row,col].axvline(data_mean + n*data_std ,lw = 1,color = 'black', ls = '--') # 1 std
        axs[row,col].axvline(data_mean + 2*n*data_std ,lw = 1,color = 'black', ls = 'dotted') # 2 std
    axs[row,col].set_xlabel(name + f' ({unit})')
    axs[row,col].set_ylabel('Number of mice')
    axs[row,col].set_xlim(data_mean-4*data_std,data_mean+4*data_std)
    axs[row,col].set_ylim(0,mouseY*1.1)

    if isInside(mousedata,data_mean,data_std):
        axs[row,col].scatter(mousedata, mouseY, color = 'red', marker = '*', s = 100)
    elif np.isnan(mousedata):
        axs[row,col].set_title("Does not exist!", fontweight="bold")
    else:
        axs[row,col].scatter(mousedata, mouseY, facecolors='none',edgecolor = 'blue', marker = 'o', s = 100)
        axs[row,col].scatter(mousedata, mouseY, color = 'blue' ,marker = '.', s = 50)
        axs[row,col].set_title("PARAMETER OUT OF BOUNDS!", fontweight="bold")

# Functions of linear regression
from sklearn.linear_model import LinearRegression

def clear_data(raw_data):
    raw_data = raw_data.dropna() # drop NaN values
    data = [x for x in raw_data if type(x) != str] # create a list with miniloop and select items that are not string
    return data

def linear_regression_plot_axs(x,y,linespace,i,j,**kwargs):
    x = np.array(x).reshape(-1,1)
    model = LinearRegression()
    model.fit(x,y)
    slope = model.coef_[0]
    intercept = model.intercept_
    x0 = linespace
    y0 = x0*slope + intercept
    if 'color' in kwargs:
        color = kwargs['color']
        alpha = 1
    else:
        color = 'grey'
        alpha = 0.3
    if 'lw' in kwargs:
        lw = kwargs['lw']
    else:
        lw = 1
    axs[i,j].plot(x0,y0,lw=lw,color=color,alpha = alpha)
    return [slope,intercept]

def linear_regression(x,y):
    x = np.array(x).reshape(-1,1)
    model = LinearRegression()
    model.fit(x,y)
    slope = model.coef_[0]
    intercept = model.intercept_
    return [slope,intercept]

def display_inline_image(base64_img, target_id):
    display(HTML(f"""
        <script>
        setTimeout(function() {{
            const img = document.createElement('img');
            img.src = "data:image/png;base64,{base64_img}";
            img.style.maxWidth = "100%";
            img.style.height = "auto";
            const container = document.getElementById('{target_id}');
            if (container) {{
                container.innerHTML = '';
                container.appendChild(img);
            }} else {{
                console.error("Container {target_id} not found.");
            }}
        }}, 100);  // Delay to ensure DOM is ready
        </script>
    """))
    
# Figure 1
def update_figure_1(head_parameter,mouseData1,mouseData2,mouseData3,midline):
    
    mouseXLR = [np.array([d.values[0] for d in mouseData2]), np.array([d.values[1] for d in mouseData2])]
    mouseZLR = [np.array([d.values[0] for d in mouseData3]), np.array([d.values[1] for d in mouseData3])]
    yPositions = np.arange(1000, 4501, 500)
    
     # All previous MetaData
    leftRidge = head_parameter.iloc[9:17,60:]
    rightRidge = head_parameter.iloc[17:25,60:]
    leftRidgeZ = head_parameter.iloc[25:33,60:]
    rightRidgeZ = head_parameter.iloc[33:41,60:]

    animalWeight = head_parameter.iloc[0,60:].values
    LeftEarBarInitial = head_parameter.iloc[3,60:].values
    RightEarBarInitial = head_parameter.iloc[4,60:].values
    NoseDVposition = head_parameter.iloc[8,60:].values
    RCSlambdaDistance = head_parameter.iloc[7,60:].values

    meanL = leftRidge.mean(axis=1).values.astype(float)
    stdL = leftRidge.std(axis=1).values.astype(float)
    meanR = rightRidge.mean(axis=1).values.astype(float)
    stdR = rightRidge.std(axis=1).values.astype(float)
    meanLz = leftRidgeZ.mean(axis=1).values.astype(float)
    stdLz = leftRidgeZ.std(axis=1).values.astype(float)
    meanRz = rightRidgeZ.mean(axis=1).values.astype(float)
    stdRz = rightRidgeZ.std(axis=1).values.astype(float)

    global axs, fig1

    fig1, axs = plt.subplots(3,5,figsize = (22,18))
    for i in range(3):
        for j in range(5):
            axs[i,j].spines['top'].set_visible(False)
            axs[i,j].spines['right'].set_visible(False)

    # Left - Right Ridge x/z-Positions for specific mouse
    # axs[1].plot(leftRidge, yPositions, color = 'grey', linestyle = '-.', linewidth = 0.1, alpha = 0.5)
    axs[0,0].plot(meanL, yPositions, color = 'red', linestyle = '-', linewidth = 2)
    axs[0,0].plot(mouseXLR[0], yPositions, color = 'black', linestyle = '-', linewidth = 2)
    axs[0,0].fill_betweenx(yPositions,meanL+stdL,meanL-stdL, color = 'grey', alpha = 0.4, linestyle = '--') # fill between x0 to x1 at y, std = 1
    axs[0,0].fill_betweenx(yPositions,meanL+2*stdL,meanL-2*stdL, color = 'grey', alpha = 0.3, linestyle = 'dotted') # fill between x0 to x1 at y, std = 2
    axs[0,0].scatter(mouseXLR[0], yPositions, color = 'black', marker = 'o', s = 25, zorder=100)
    axs[0,0].set_xlabel('L lateral displacement (µm)')
    axs[0,0].set_ylabel('A/P position (µm)')
    axs[0,0].set_xlim([5000,2500])
    axs[0,0].set_ylim([1000-100,4500+100])

    # axs[1].plot(rightRidge, yPositions, color = 'grey', linestyle = '-.', linewidth = 0.1, alpha = 0.5)
    axs[0,1].plot(meanR, yPositions, color = 'red', linestyle = '-', linewidth = 2)
    axs[0,1].plot(mouseXLR[1], yPositions, color = 'black', linestyle = '-', linewidth = 2)
    axs[0,1].fill_betweenx(yPositions,meanR+stdR,meanR-stdR, color = 'grey', alpha = 0.4, linestyle = '--') # fill between x0 to x1 at y, std = 1
    axs[0,1].fill_betweenx(yPositions,meanR+2*stdR,meanR-2*stdR, color = 'grey', alpha = 0.3, linestyle = 'dotted') # fill between x0 to x1 at y, std = 2
    axs[0,1].scatter(mouseXLR[1], yPositions, color = 'black', marker = 'o', s = 25, zorder=100)
    axs[0,1].set_xlabel('R lateral displacement (µm)')
    axs[0,1].set_ylabel('A/P position (µm)')
    axs[0,1].set_xlim([-2500,-5000])
    axs[0,1].set_ylim([1000-100,4500+100])

    # axs[5].plot(leftRidgeZ, yPositions, color = 'grey', linestyle = '--', linewidth = 0.1, alpha = 0.5)
    axs[1,0].plot(meanLz, yPositions, color = 'red', linestyle = '-', linewidth = 2)
    axs[1,0].plot(mouseZLR[0], yPositions, color = 'black', linestyle = '-', linewidth = 2)
    axs[1,0].fill_betweenx(yPositions,meanLz+stdLz,meanLz-stdLz, color = 'grey', alpha = 0.4, linestyle = '--') # fill between x0 to x1 at y, std = 1
    axs[1,0].fill_betweenx(yPositions,meanLz+2*stdLz,meanLz-2*stdLz, color = 'grey', alpha = 0.3, linestyle = 'dotted') # fill between x0 to x1 at y, std = 2
    axs[1,0].scatter(mouseZLR[0], yPositions, color = 'black', marker = 'o', s = 25, zorder=100)
    axs[1,0].set_xlabel('L vertical displacement (µm)')
    axs[1,0].set_ylabel('A/P position (µm)')
    axs[1,0].set_xlim([1600,400])
    axs[1,0].set_ylim([1000-100,4500+100])

    # axs[6].plot(rightRidgeZ, yPositions, color = 'grey', linestyle = '-.', linewidth = 0.1, alpha = 0.5)
    axs[1,1].plot(meanRz, yPositions, color = 'red', linestyle = '-', linewidth = 2)
    axs[1,1].plot(mouseZLR[1], yPositions, color = 'black', linestyle = '-', linewidth = 2)
    axs[1,1].fill_betweenx(yPositions,meanRz+stdRz,meanRz-stdRz, color = 'grey', alpha = 0.4, linestyle = '--') # fill between x0 to x1 at y, std = 1
    axs[1,1].fill_betweenx(yPositions,meanRz+2*stdRz,meanRz-2*stdRz, color = 'grey', alpha = 0.3, linestyle = 'dotted') # fill between x0 to x1 at y, std = 2
    axs[1,1].scatter(mouseZLR[1], yPositions, color = 'black', marker = 'o', s = 25, zorder=100)
    axs[1,1].set_xlabel('R vertical displacement (µm)')
    axs[1,1].set_ylabel('A/P position (µm)')
    axs[1,1].set_xlim([400,1600])
    axs[1,1].set_ylim([1000-100,4500+100])

    # Specific Mouse Regression
    # row 0, col 2
    linespace = np.arange(2500,5000,100)
    axs[0,2].plot(leftRidge, rightRidge, color = 'gray', linestyle = '-')
    axs[0,2].scatter(mouseXLR[0], mouseXLR[1], color = 'black', s=25, marker = 's',zorder = 100)
    axs[0,2].plot(linespace, -linespace, color = 'black', linestyle = ':', alpha = 0.5)
    linear_regression_plot_axs(mouseXLR[0], mouseXLR[1], linespace,0,2, color = 'red',lw = 2)
    axs[0,2].set_title(f'Regression for current mouse', size = 10)
    axs[0,2].set_xlabel('L lateral displacement (µm)')
    axs[0,2].set_ylabel('R lateral displacement (µm)')

    # row 1, col 2
    linespace = np.arange(400,1500,100)
    axs[1,2].plot(leftRidgeZ, rightRidgeZ, color = 'gray', linestyle = '-')
    axs[1,2].scatter(mouseZLR[0], mouseZLR[1], color = 'black', s=25, marker = 's',zorder = 100)
    axs[1,2].plot(linespace, linespace, color = 'black', linestyle = ':', alpha = 0.5)
    linear_regression_plot_axs(mouseZLR[0], mouseZLR[1], linespace,1,2, color = 'red',lw = 2)
    axs[1,2].set_title(f'Regression for current mouse', size = 10)
    axs[1,2].set_xlabel('L vertical displacement (µm)')
    axs[1,2].set_ylabel('R vertical displacement (µm)')
    mouseLRregression = [linear_regression(mouseXLR[0],mouseXLR[1]),linear_regression(mouseZLR[0],mouseZLR[1])]
    # Calculate lateral linear regression
    linespace = np.linspace(3000, 5000, 100)
    XAllintercept = []
    XAllslope = []
    for i in range(num_mice):
        positionsL = clear_data(leftRidge.iloc[:,i])
        positionsR = clear_data(rightRidge.iloc[:,i])
        if len(positionsL) > 1 and len(positionsR) > 1:
            slope, intercept = linear_regression(positionsL,positionsR)
            XAllslope.append(slope)
            XAllintercept.append(intercept)
        else:
            XAllslope.append(np.nan)
            XAllintercept.append(np.nan)

    HistoSubplot(XAllslope,'',0,3,'',mouseLRregression[0][0])
    axs[0,3].set_xlabel('Slopes')
    axs[0,3].set_title('Slope of L-R lateral displacement')

    HistoSubplot(XAllintercept,'',0,4,'',mouseLRregression[0][1])
    axs[0,4].set_xlabel('Intercepts')
    axs[0,4].set_title('Intercept of L-R lateral displacement')

    # Calculate vertical linear regression
    linespace = np.linspace(500, 1500, 100)
    ZAllintercept = []
    ZAllslope = []
    for i in range(num_mice):
        positionsLz = clear_data(leftRidgeZ.iloc[:,i])
        positionsRz = clear_data(rightRidgeZ.iloc[:,i])
        if len(positionsLz) > 1 and len(positionsRz) > 1:
            slope, intercept = linear_regression(positionsLz,positionsRz)
            ZAllslope.append(slope)
            ZAllintercept.append(intercept)
        else:
            ZAllslope.append(np.nan)
            ZAllintercept.append(np.nan)
    
    HistoSubplot(ZAllslope,'',1,3,'',mouseLRregression[1][0])
    axs[1,3].set_xlabel('Slopes')
    axs[1,3].set_title('Slope of L-R vertical displacement')
    
    HistoSubplot(ZAllintercept,'',1,4,'',mouseLRregression[1][1])
    axs[1,4].set_xlabel('Intercepts')
    axs[1,4].set_title('Intercept of L-R vertical displacement')
    
    # histograms of all values
    HistoSubplot(animalWeight,'Animal Weight',2,0,'g',mouseData1.iloc[0])
    HistoSubplot(LeftEarBarInitial,'Left ear bar',2,1,'mm',mouseData1.iloc[1])
    HistoSubplot(RightEarBarInitial,'Right ear bar',2,2,'mm',mouseData1.iloc[2])
    HistoSubplot(NoseDVposition,'Pitch angle (º)',2,3,'˚',mouseData1.iloc[3])
    HistoSubplot(RCSlambdaDistance,'RCS - lambda distance',2,4,'µm',mouseData1.iloc[4])

    # load midline from doc
    if midline > 0:
      midline_direction = 'To the left'
    else:
      midline_direction = 'To the right'
    
    fig1.suptitle(f'Data for mouse {mouse_id}', fontweight="bold", y = 1)
    fig1.text(0.5, 0.985, f"Calculated midline: {abs(midline):.1f} µm → {midline_direction}", 
              fontsize=10, ha='center', color='darkred', fontweight='bold')
    plt.tight_layout()

    # Convert plot to image and display in result box
    img_buf = BytesIO()
    fig1.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
    display_inline_image(img_base64, "plotBox1")

# Figure 2, histograms showing the L-R x-positions
def update_figure_2(head_parameter,mouseData2):
    
    yPositions = np.arange(1000, 4501, 500)
     # All previous MetaData
    leftRidge = head_parameter.iloc[9:17,60:]
    leftRidge.columns = head_parameter.iloc[0,60:]
    rightRidge = head_parameter.iloc[17:25,60:]
    rightRidge.columns = head_parameter.iloc[0,60:]
    
    animalWeight = head_parameter.iloc[0,60:].values
    LeftEarBarInitial = head_parameter.iloc[3,60:].values
    RightEarBarInitial = head_parameter.iloc[4,60:].values
    NoseDVposition = head_parameter.iloc[8,60:].values
    RCSlambdaDistance = head_parameter.iloc[7,60:].values
    
    meanL = leftRidge.mean(axis=1).values.astype(float)
    stdL = leftRidge.std(axis=1).values.astype(float)
    meanR = rightRidge.mean(axis=1).values.astype(float)
    stdR = rightRidge.std(axis=1).values.astype(float)
    
    # collecting master data from file
    MasterListData = [leftRidge.reset_index(drop = True),rightRidge.reset_index(drop = True)]
    MasterListName = [['LEFT displacement at y=1000 µm PRCS','RIGHT displacement at y=1000 µm PRCS'],
                      ['LEFT displacement at y=1500 µm PRCS','RIGHT displacement at y=1500 µm PRCS'],
                      ['LEFT displacement at y=2000 µm PRCS','RIGHT displacement at y=2000 µm PRCS'],
                      ['LEFT displacement at y=2500 µm PRCS','RIGHT displacement at y=2500 µm PRCS'],
                      ['LEFT displacement at y=3000 µm PRCS','RIGHT displacement at y=3000 µm PRCS'],
                      ['LEFT displacement at y=3500 µm PRCS','RIGHT displacement at y=3500 µm PRCS'],
                      ['LEFT displacement at y=4000 µm PRCS','RIGHT displacement at y=4000 µm PRCS'],
                      ['LEFT displacement at y=4500 µm PRCS','RIGHT displacement at y=4500 µm PRCS']]
    MasterListUnit = [['µm','µm'],['µm','µm'],['µm','µm'],['µm','µm'],['µm','µm'],['µm','µm'],['µm','µm'],['µm','µm']]
    
    # setting a global xlim
    xlim = [[5000,2500],[-2500,-5000]]
    bins = 50
    
    # plotting using HistoSubplot function
    # row = 8 (j), col = 2 (i)
    global axs, fig2
    fig2,axs = plt.subplots(8,2,figsize = (12,12))
    for i in range(2):
        for j in range(8):
            HistoSubplot(MasterListData[i].loc[j,:],MasterListName[j][i],j,i,MasterListUnit[j][i],mouseData2[j].iloc[i],bins = bins)
            axs[j,i].set_xlim(xlim[i])
    plt.figtext(0.265,0.97,f'Left side lateral displacement (µm) for mouse {mouse_id} (red asterisk)', va="center", ha="center", size=9, fontweight="bold")
    plt.figtext(0.755,0.97,f'Right side lateral displacement (µm) for mouse {mouse_id} (red asterisk)', va="center", ha="center", size=9, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Convert plot to image and display in result box
    img_buf = BytesIO()
    fig2.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

    display_inline_image(img_base64, "plotBox2")

# Figure 3, histograms showing the L-R z-positions
def update_figure_3(head_parameter,mouseData3):
  
    yPositions = np.arange(1000, 4501, 500)
    
     # All previous MetaData
    leftRidgeZ = head_parameter.iloc[25:33,60:]
    rightRidgeZ = head_parameter.iloc[33:41,60:]
    
    animalWeight = head_parameter.iloc[0,60:].values
    LeftEarBarInitial = head_parameter.iloc[3,60:].values
    RightEarBarInitial = head_parameter.iloc[4,60:].values
    NoseDVposition = head_parameter.iloc[8,60:].values
    RCSlambdaDistance = head_parameter.iloc[7,60:].values
    
    meanLz = leftRidgeZ.mean(axis=1).values.astype(float)
    stdLz = leftRidgeZ.std(axis=1).values.astype(float)
    meanRz = rightRidgeZ.mean(axis=1).values.astype(float)
    stdRz = rightRidgeZ.std(axis=1).values.astype(float)

    # collecting master data from file
    MasterListData = [leftRidgeZ.reset_index(drop = True),rightRidgeZ.reset_index(drop = True)]
    MasterListName = [['LEFT Z-displacement at y=1000 µm PRCS','RIGHT Z-displacement at y=1000 µm PRCS'],
                      ['LEFT Z-displacement at y=1500 µm PRCS','RIGHT Z-displacement at y=1500 µm PRCS'],
                      ['LEFT Z-displacement at y=2000 µm PRCS','RIGHT Z-displacement at y=2000 µm PRCS'],
                      ['LEFT Z-displacement at y=2500 µm PRCS','RIGHT Z-displacement at y=2500 µm PRCS'],
                      ['LEFT Z-displacement at y=3000 µm PRCS','RIGHT Z-displacement at y=3000 µm PRCS'],
                      ['LEFT Z-displacement at y=3500 µm PRCS','RIGHT Z-displacement at y=3500 µm PRCS'],
                      ['LEFT Z-displacement at y=4000 µm PRCS','RIGHT Z-displacement at y=4000 µm PRCS'],
                      ['LEFT Z-displacement at y=4500 µm PRCS','RIGHT Z-displacement at y=4500 µm PRCS']]
    MasterListUnit = [['µm','µm'],['µm','µm'],['µm','µm'],['µm','µm'],['µm','µm'],['µm','µm'],['µm','µm'],['µm','µm']]
    
    # setting a global xlim
    xlim = [[1600,400],[400,1600]]
    bins = 40
    
    # plotting using HistoSubplot function
    # row = 8 (j), col = 2 (i)
    global axs, fig3
    fig3,axs = plt.subplots(8,2,figsize = (12,12))
    for i in range(2):
        for j in range(8):
            HistoSubplot(MasterListData[i].loc[j,:],MasterListName[j][i],j,i,MasterListUnit[j][i],mouseData3[j].iloc[i],bins = bins)
            axs[j,i].set_xlim(xlim[i])
    plt.figtext(0.265,0.97,f'Left side z-lateral displacement (µm) for mouse {mouse_id} (red asterisk)', va="center", ha="center", size=9, fontweight="bold")
    plt.figtext(0.755,0.97,f'Right side z-lateral displacement (µm) for mouse {mouse_id} (red asterisk)', va="center", ha="center", size=9, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Convert plot to image and display in result box
    img_buf = BytesIO()
    fig3.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
    display_inline_image(img_base64, "plotBox3")

def finish_correction():
    worksheet = gc.open_by_key(file_id).sheet1
    head_parameter = pd.DataFrame(worksheet.get_all_records())
    head_parameter = head_parameter.replace('', np.nan)
    head_parameter = head_parameter.replace('lost', np.nan)

    xL_values = [float(x) for x in list(head_parameter.iloc[9:14,-1])]
    xR_values = [float(x) for x in list(head_parameter.iloc[17:22,-1])]
    
    midline = midline_correction(xL_values,xR_values)
    
    head_parameter.iloc[9:17, -1] -= midline
    head_parameter.iloc[9:17, -1] = head_parameter.iloc[9:17, -1].round(0).astype(int)
    head_parameter.iloc[17:25, -1] -= midline
    head_parameter.iloc[17:25, -1] = head_parameter.iloc[17:25, -1].round(0).astype(int)
    worksheet.clear()  # Optional: Use with caution, can clear the entire sheet
    set_with_dataframe(worksheet, head_parameter)  # Update the sheet


    mousefile = head_parameter[mouse_id]
    # Weight before surgery (g), Left ear bar (initial) (mm), Right ear bar (initial) (mm), Nose DV position, RCS-lambda distance (µm)
    mouseData1 = mousefile.iloc[[0,3,4,8,7]]
    # (XL, XR) (1000:4500:500)
    mouseData2 = [mousefile.iloc[[9,17]],mousefile.iloc[[10,18]],mousefile.iloc[[11,19]],mousefile.iloc[[12,20]],mousefile.iloc[[13,21]],mousefile.iloc[[14,22]],mousefile.iloc[[15,23]],mousefile.iloc[[16,24]]]
    # (ZL, ZR) (1000:4500:500)
    mouseData3 = [mousefile.iloc[[25,33]],mousefile.iloc[[26,34]],mousefile.iloc[[27,35]],mousefile.iloc[[28,36]],mousefile.iloc[[29,37]],mousefile.iloc[[30,38]],mousefile.iloc[[31,39]],mousefile.iloc[[32,40]]]

    print("Finished updating the sheet")
    
    print("Calling update_figure_1...")
    update_figure_1(head_parameter,mouseData1,mouseData2,mouseData3,midline)
    print("Calling update_figure_2...")
    update_figure_2(head_parameter,mouseData2)
    print("Calling update_figure_3...")
    update_figure_3(head_parameter,mouseData3)

# Register the callback function
from google.colab import output
output.register_callback('notebook.update_correction_result', update_correction_result)
output.register_callback('notebook.finish_correction', finish_correction)
# Initialize the input boxes and the callback
create_input_boxes()
