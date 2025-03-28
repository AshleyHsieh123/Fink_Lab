import gspread
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

    // Plot result box (for embedding the plot)
    var plotBox = document.createElement("div");
    plotBox.id = "plotBox";
    plotBox.style.margin = "10px";
    plotBox.style.height = "600px";  // Adjusted height for better image display
    plotBox.style.width = "100%";    // Adjust width to take up available space
    
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
    container.appendChild(plotBox);
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

        xL_values = [float(x) for x in list(head_parameter.iloc[9:14,-1])]
        xR_values = [float(x) for x in list(head_parameter.iloc[17:22,-1])]
        midline = midline_correction(xL_values,xR_values)
        
        # Display result in result box
        if midline > 0:
            print(f"Calculated midline: {midline}", 'To the left')
        else:
            print(f"Calculated midline: {midline}", 'To the right')
        
        # Write the updated DataFrame back to the sheet
        worksheet.clear()  # Optional: Use with caution, can clear the entire sheet
        set_with_dataframe(worksheet, head_parameter)  # Update the sheet
        
    except Exception as e:
        print(f"Error in callback: {e}")

def finish_correction():
    worksheet = gc.open_by_key(file_id).sheet1
    head_parameter = pd.DataFrame(worksheet.get_all_records())
    xL_values = [float(x) for x in list(head_parameter.iloc[9:14,-1])]
    xR_values = [float(x) for x in list(head_parameter.iloc[17:22,-1])]
    
    midline = midline_correction(xL_values,xR_values)
    
    head_parameter.iloc[9:17, -1] += midline
    head_parameter.iloc[9:17, -1] = head_parameter.iloc[9:17, -1].round(0).astype(int)
    head_parameter.iloc[17:25, -1] += midline
    head_parameter.iloc[17:25, -1] = head_parameter.iloc[17:25, -1].round(0).astype(int)
    worksheet.clear()  # Optional: Use with caution, can clear the entire sheet
    set_with_dataframe(worksheet, head_parameter)  # Update the sheet

    mice = np.array(head_parameter.iloc[0,:])
    num_mice = len(mice[60:]) # count the number of mice

    mouse_index = np.where(mice == mouse_id)[0][0]  # Find the index of the mouse
    mousefile = head_parameter.iloc[0:53,mouse_index]
    mousefile.index = head_parameter.iloc[0:53,1].to_list()
    mouseData1 = [[mousefile['Weight before surgery (g)'],mousefile['Left ear bar (initial) (mm)'],mousefile['Right ear bar (initial) (mm)'],mousefile['Nose DV position º'],mousefile['RCS-lambda distance (µm)']]]
    mouseData2 = [[mousefile['At 1000PRCS, L positions of LEFT temporal ridge (µm)'],mousefile['At 1000PRCS, L positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 1500PRCS, L positions of LEFT temporal ridge (µm)'],mousefile['At 1500PRCS, L positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 2000PRCS, L positions of LEFT temporal ridge (µm)'],mousefile['At 2000PRCS, L positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 2500PRCS, L positions of LEFT temporal ridge (µm)'],mousefile['At 2500PRCS, L positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 3000PRCS, L positions of LEFT temporal ridge (µm)'],mousefile['At 3000PRCS, L positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 3500PRCS, L positions of LEFT temporal ridge (µm)'],mousefile['At 3500PRCS, L positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 4000PRCS, L positions of LEFT temporal ridge (µm)'],mousefile['At 4000PRCS, L positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 4500PRCS, L positions of LEFT temporal ridge (µm)'],mousefile['At 4500PRCS, L positions of RIGHT temporal ridge (µm)']]]
    mouseData3 = [[mousefile['At 1000PRCS, V positions of LEFT temporal ridge (µm)'],mousefile['At 1000PRCS, V positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 1500PRCS, V positions of LEFT temporal ridge (µm)'],mousefile['At 1500PRCS, V positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 2000PRCS, V positions of LEFT temporal ridge (µm)'],mousefile['At 2000PRCS, V positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 2500PRCS, V positions of LEFT temporal ridge (µm)'],mousefile['At 2500PRCS, V positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 3000PRCS, V positions of LEFT temporal ridge (µm)'],mousefile['At 3000PRCS, V positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 3500PRCS, V positions of LEFT temporal ridge (µm)'],mousefile['At 3500PRCS, V positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 4000PRCS, V positions of LEFT temporal ridge (µm)'],mousefile['At 4000PRCS, V positions of RIGHT temporal ridge (µm)']],
                  [mousefile['At 4500PRCS, V positions of LEFT temporal ridge (µm)'],mousefile['At 4500PRCS, V positions of RIGHT temporal ridge (µm)']]]

     # All previous MetaData

    leftRidge = head_parameter.iloc[9:17,60:]
    leftRidge.columns = head_parameter.iloc[0,60:]
    rightRidge = head_parameter.iloc[17:25,60:]
    rightRidge.columns = head_parameter.iloc[0,60:]
    leftRidgeZ = head_parameter.iloc[25:33,60:]
    leftRidgeZ.columns = head_parameter.iloc[0,60:]
    rightRidgeZ = head_parameter.iloc[33:41,60:]
    rightRidgeZ.columns = head_parameter.iloc[0,60:]

    animalWeight = head_parameter.iloc[0,60:]
    LeftEarBarInitial = head_parameter.iloc[3,60:]
    RightEarBarInitial = head_parameter.iloc[4,60:]
    NoseDVposition = head_parameter.iloc[8,60:]
    RCSlambdaDistance = head_parameter.iloc[7,60:]

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
        raw_data = pd.head_parameter(raw_data)
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
    
    # Calculated data
    
    mouseXLR = list(map(list, zip(*mouseData2)))
    mouseZLR = list(map(list, zip(*mouseData3)))
    
    yPositions = np.array([1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500])
    rightRidge = rightRidge.apply(pd.to_numeric, errors='coerce')  # Convert columns to numeric
    leftRidge = leftRidge.apply(pd.to_numeric, errors='coerce')
    rightRidgeZ = rightRidgeZ.apply(pd.to_numeric, errors='coerce')
    leftRidgeZ = leftRidgeZ.apply(pd.to_numeric, errors='coerce')
    
    meanR = np.nanmean(rightRidge, axis=1)
    stdR = np.nanstd(rightRidge, axis=1)
    meanL = np.nanmean(leftRidge, axis=1)
    stdL = np.nanstd(leftRidge, axis=1)
    minR, maxR = np.nanmin(rightRidge, axis=1), np.nanmax(rightRidge, axis=1)
    minL, maxL = np.nanmin(leftRidge, axis=1), np.nanmax(leftRidge, axis=1)
    
    meanRz = np.nanmean(rightRidgeZ, axis=1)
    stdRz = np.nanstd(rightRidgeZ, axis=1)
    meanLz = np.nanmean(leftRidgeZ, axis=1)
    stdLz = np.nanstd(leftRidgeZ, axis=1)
    minRz, maxRz = np.nanmin(rightRidgeZ, axis=1), np.nanmax(rightRidgeZ, axis=1)
    minLz, maxLz = np.nanmin(leftRidgeZ, axis=1), np.nanmax(leftRidgeZ, axis=1)
    
    # Figure 1
    
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
    HistoSubplot(animalWeight,'Animal Weight',2,0,'g',mouseData1[0][0])
    HistoSubplot(LeftEarBarInitial,'Left ear bar',2,1,'mm',mouseData1[0][1])
    HistoSubplot(RightEarBarInitial,'Right ear bar',2,2,'mm',mouseData1[0][2])
    HistoSubplot(NoseDVposition,'Nose DV position',2,3,'˚',mouseData1[0][3])
    HistoSubplot(RCSlambdaDistance,'RCS - lambda distance',2,4,'µm',mouseData1[0][4])
    
    fig1.suptitle(f'Data for mouse {mouse_id}', fontweight="bold", y = 1)
    plt.tight_layout()

    # Convert plot to image and display in result box
    img_buf = BytesIO()
    fig1.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

    display(Javascript(f'''
    var plotBox = document.getElementById("plotBox");
    plotBox.innerHTML = '<img src="data:image/png;base64,' + "{img_base64}" + '" />';
    '''))
    display(fig1)
    print('\n\n')
    
    # Figure 2, histograms showing the L-R x-positions
    
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
    fig2,axs = plt.subplots(8,2,figsize = (12,12))
    for i in range(2):
        for j in range(8):
            HistoSubplot(MasterListData[i].loc[j,:],MasterListName[j][i],j,i,MasterListUnit[j][i],mouseData2[j][i],bins = bins)
            axs[j,i].set_xlim(xlim[i])
    plt.figtext(0.265,1,f'Left side lateral displacement (µm) for mouse {mouse_id} (red asterisk)', va="center", ha="center", size=9, fontweight="bold")
    plt.figtext(0.755,1,f'Right side lateral displacement (µm) for mouse {mouse_id} (red asterisk)', va="center", ha="center", size=9, fontweight="bold")
    plt.tight_layout()
    
    # Convert plot to image and display in result box
    img_buf = BytesIO()
    fig2.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

    display(Javascript(f'''
    var plotBox = document.getElementById("plotBox");
    plotBox.innerHTML = '<img src="data:image/png;base64,' + "{img_base64}" + '" />';
    '''))
    display(fig2)
    print('\n\n')
    
    # Figure 3, histograms showing the L-R z-positions
    
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
    fig3,axs = plt.subplots(8,2,figsize = (12,12))
    for i in range(2):
        for j in range(8):
            HistoSubplot(MasterListData[i].loc[j,:],MasterListName[j][i],j,i,MasterListUnit[j][i],mouseData3[j][i],bins = bins)
            axs[j,i].set_xlim(xlim[i])
    plt.figtext(0.265,1,f'Left side z-lateral displacement (µm) for mouse {mouse_id} (red asterisk)', va="center", ha="center", size=9, fontweight="bold")
    plt.figtext(0.755,1,f'Right side z-lateral displacement (µm) for mouse {mouse_id} (red asterisk)', va="center", ha="center", size=9, fontweight="bold")
    plt.tight_layout()

    # Convert plot to image and display in result box
    img_buf = BytesIO()
    fig3.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

    display(Javascript(f'''
    var plotBox = document.getElementById("plotBox");
    plotBox.innerHTML = '<img src="data:image/png;base64,' + "{img_base64}" + '" />';
    '''))
    display(fig3)
    print('\n\n')

    
# Register the callback function
from google.colab import output
output.register_callback('notebook.update_correction_result', update_correction_result)
output.register_callback('notebook.finish_correction', finish_correction)

# Initialize the input boxes and the callback
create_input_boxes()
