import gspread
import pandas as pd
from google.colab import drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from google.colab import auth
from IPython.display import display, Javascript
import numpy as np

mice = np.array(file_id.iloc[9,:])
num_mice = len(mice[60:]) # count the number of mice

mouse_index = np.where(mice == mouse_id)[0][0]  # Find the index of the mouse
mousefile = file_id.iloc[9:57,mouse_index]
mousefile.index = file_id.iloc[9:57,1].to_list()
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

  leftRidge = file_id.iloc[9:17,60:]
  leftRidge.columns = file_id.iloc[0,60:]
  rightRidge = file_id.iloc[17:25,60:]
  rightRidge.columns = file_id.iloc[0,60:]
  leftRidgeZ = file_id.iloc[25:33,60:]
  leftRidgeZ.columns = file_id.iloc[0,60:]
  rightRidgeZ = file_id.iloc[33:41,60:]
  rightRidgeZ.columns = file_id.iloc[0,60:]

  animalWeight = file_id.iloc[0,60:]
  LeftEarBarInitial = file_id.iloc[3,60:]
  RightEarBarInitial = file_id.iloc[4,60:]
  NoseDVposition = file_id.iloc[8,60:]
  RCSlambdaDistance = file_id.iloc[7,60:]

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

plt.text(-5, 60, 'midline', fontsize = 22)

fig1.suptitle(f'Data for mouse {mouse_id}', fontweight="bold", y = 1)
plt.tight_layout()
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
display(fig3)
print('\n\n')

LRidgeAT1000PRCS = mousefile ['At 1000PRCS, L positions of LEFT temporal ridge (µm)']
LRidgeAT3000PRCS = mousefile ['At 3000PRCS, L positions of LEFT temporal ridge (µm)']
RRidgeAT1000PRCS = mousefile ['At 1000PRCS, L positions of RIGHT temporal ridge (µm)']
RRidgeAT3000PRCS = mousefile ['At 3000PRCS, L positions of RIGHT temporal ridge (µm)']

# A/P "Yaw" Correction (˚)
Theta_Lº = round(-math.atan(((LRidgeAT3000PRCS - LRidgeAT1000PRCS))/2000)*360/(2*3.14159),4)
Theta_Rº = round(math.atan(((RRidgeAT3000PRCS - RRidgeAT1000PRCS))/2000)*360/(2*3.14159), 4)
YawCorrectionº = round((Theta_Rº - Theta_Lº)/2, 3)
# D/V "Pitch" Correction (˚)
DVoffset = float(input('D/V offset (µm) = '))
RCSλDistance = float(mousefile['RCS-lambda distance (µm)'])
PitchCorrectionº = round(math.atan(DVoffset/RCSλDistance)*180/3.14159, 2)
# M/L "Roll" Correction (˚)
Zoffset1000 = mousefile ['At 1000PRCS, V positions of LEFT temporal ridge (µm)'] - mousefile ['At 1000PRCS, V positions of RIGHT temporal ridge (µm)']
Zoffset3000 = mousefile ['At 3000PRCS, V positions of LEFT temporal ridge (µm)'] - mousefile ['At 3000PRCS, V positions of RIGHT temporal ridge (µm)']
Xoffset1000 = -(LRidgeAT1000PRCS - RRidgeAT1000PRCS)
Xoffset3000 = -(LRidgeAT3000PRCS - RRidgeAT3000PRCS)
Ratio1000 = Zoffset1000/Xoffset1000
Ratio3000 = Zoffset3000/Xoffset3000
Angle1000º = round(math.atan(Ratio1000)*360/(2*3.14159), 2)
Angle3000º = round(math.atan(Ratio3000)*360/(2*3.14159), 2)
RollCorrectionº = round((Angle1000º + Angle3000º)/2, 2)
# Lateral shift Correction (µm)
LateralShift = -(LRidgeAT1000PRCS + RRidgeAT1000PRCS)/2

# print info onto the file
print(f'Mouse: {mouse_id}')
# important
if YawCorrectionº > 0:
    print(f"YawCorrectionº = {YawCorrectionº}", 'clockwise')
else:
    print(f"YawCorrectionº = {YawCorrectionº}", 'counterclockwise')
print(f"PitchCorrectionº = {PitchCorrectionº}")
if YawCorrectionº > 0:
    print(f"RollCorrectionº = {RollCorrectionº}", 'clockwise')
else:
    print(f"RollCorrectionº = {RollCorrectionº}", 'counterclockwise')
if LateralShift < 0:
    print(f"LateralShift (µm) = {LateralShift}", 'move to right')
else:
    print(f"LateralShift (µm) = {LateralShift}", 'move to left')
print('=============================================')
# less important
print(f"Theta_Lº = {Theta_Lº}")
print(f"Theta_Rº = {Theta_Rº}")
#print(f"DVoffset (µm) = {DVoffset}")
print(f"RCSλDistance (µm) = {RCSλDistance}")
print(f"Zoffset1000 (µm) = {Zoffset1000}")
print(f"Zoffset3000 (µm) = {Zoffset3000}")
print(f"Xoffset1000 (µm) = {Xoffset1000}")
print(f"Xoffset3000 (µm) = {Xoffset3000}")
print(f"Ratio1000 = {Ratio1000}")
print(f"Ratio3000 = {Ratio3000}")
print(F"Angle1000º = {Angle1000º}")
print(F"Angle3000º = {Angle3000º}")
