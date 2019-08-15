from tkinter import *
import tkinter as tk

import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# Create Window
root = Tk()

root.geometry("+100+100")

# Create left frame for meter labels
lframe = Frame(root, bg='wheat1')
lframe.grid(row=1, column=0)

# Create right frame for meter add/remove
rframe = Frame(root, bg='wheat1')
rframe.grid(row=1, column=1)

bframe = Frame(root, width=750, bg='wheat1')
bframe.grid(row=2, column=0, columnspan=2)

root.title('Meter Analysis')
root.configure(background='wheat1', padx=30, pady=30)

# Connect to DB
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Declare vars for option menus
variable = StringVar()
variable1 = StringVar()
variable3 = StringVar()

# Declare vars for top info label and entry box
global infoText
infoText = StringVar(root)
inputRead = IntVar()

# Declare vars for summary labels
hv1LabelText = StringVar()
hv1LabelTextYTD = StringVar()
hv1LabelTextM = StringVar()
hv1LabelTextAve = StringVar()
hv1LabelTextH = StringVar()
hv1LabelTextL = StringVar()

hv2LabelText = StringVar()
hv2LabelTextYTD = StringVar()
hv2LabelTextM = StringVar()
hv2LabelTextAve = StringVar()
hv2LabelTextH = StringVar()
hv2LabelTextL = StringVar()

bencoLabelText = StringVar()
bencoLabelTextYTD = StringVar()
bencoLabelTextM = StringVar()
bencoLabelTextAve = StringVar()
bencoLabelTextH = StringVar()
bencoLabelTextL = StringVar()

# Create three list boxes for each meter
lboxHV1 = Listbox(lframe, bg='khaki3')
lboxHV1.grid(row=2, column=0, padx=10, pady=10, sticky=W+E+N+S)

lboxHV2 = Listbox(lframe, bg='khaki3')
lboxHV2.grid(row=2, column=1, padx=10, pady=10, sticky=W+E+N+S)

lboxBenco = Listbox(lframe, bg='khaki3')
lboxBenco.grid(row=2, column=2, padx=10, pady=10, sticky=W+E+N+S)

# Information label at top
Label(root, textvariable=infoText, font=("Times", 14), bg='Wheat1').grid(row=0, column=0, padx=5, pady=5)


# Function to populate all fields on start
def meterYTD(*meters, year):
    tableName = ''
    for meter in meters:
        if meter == 'HV1':
            tableName = 'HV1Table'
            labName = hv1LabelTextYTD
            labName1 = hv1LabelTextAve
            labName2 = hv1LabelTextH
            labName3 = hv1LabelTextL
            lboxText = lboxHV1
        elif meter == 'HV2':
            tableName = 'HV2Table'
            labName = hv2LabelTextYTD
            labName1 = hv2LabelTextAve
            labName2 = hv2LabelTextH
            labName3 = hv2LabelTextL
            lboxText = lboxHV2
        elif meter == 'Benco':
            tableName = 'BencoTable'
            labName = bencoLabelTextYTD
            labName1 = bencoLabelTextAve
            labName2 = bencoLabelTextH
            labName3 = bencoLabelTextL
            lboxText = lboxBenco

        # Clear list boxes
        lboxText.delete(0, "end")

        # Sort DB by reads
        cursor = connection.cursor()
        sql = f"SELECT Year, Month, Read FROM {tableName} ORDER BY Read ASC"
        y = cursor.execute(sql)

        # Iterate DB and add row tuples to months list
        months = []
        for month in y:
            months.append(month)
        # Iterate each tuple and add read to total list
        total = []
        for i in months:
            if (year - 1) == (i[0]) and i[1] == 'December':
                total.append(i[2])
            if i[0] == year:
                total.append(i[2])

        # YTD Consumption
        if total==[]:
            labName.set("No data")
        else:
            h = max(total)
            l = min(total)

            # Display difference between high and low reads
            totalCons = h - l
            if totalCons == 0:
                labName.set("No data")
            else:
                labName.set(f"{totalCons} kWh")

        # Calculate consumption by subtracting two values and adding to list
        consumptionList = []
        for i in range(len(total) - 1):
            consumptionList.append(abs(total[i] - total[i+1]))

        # Average Monthly Read
        if len(consumptionList) <= 0:
            labName1.set("No data")
        else:
            labName1.set(f"{round(sum(consumptionList)/len(consumptionList), 1)} kWh")

        # Max and Min Monthly Consumption
        if len(consumptionList) <= 0:
            labName2.set("No data")
        else:
            labName2.set(f"{max(consumptionList)} kWh")
        if len(consumptionList) <= 0:
            labName3.set("No data")
        else:
            labName3.set(f"{min(consumptionList)} kWh")

        # Populate the listboxes with Y, M and consumption
        for i in range(len(consumptionList)):
            lboxText.insert("end", f"{year} {months[i+1][1]}: {consumptionList[i]} kWh")
        infoText.set("Welcome to the Meter Analyser")


# Function to get option menu values and return DB lists for the meter selected
def getLists():
    global month
    global meter
    global year
    global tableName
    month = variable3.get()
    meter = variable1.get()
    year = variable.get()

    # Declare which table based on the meter value selected
    if meter == 'HV_1_Meter':
        tableName = 'HV1Table'
    elif meter == 'HV_2_Meter':
        tableName = 'HV2Table'
    elif meter == 'Benco_Meter':
        tableName = 'BencoTable'
    else:
        refresh()
        infoText.set("No meter selected.")
        return

    # Check if M, Y, Meter values were given
    if bool(month) and bool(year) and bool(meter) and bool(tableName):
        cursor = connection.cursor()
        sql = f"SELECT Year, Month, Read FROM {tableName} ORDER BY Read ASC"
        y = cursor.execute(sql)
        months = []
        for monthi in y:
            months.append(monthi)

        # Create list from DB columns
        global mList
        global yList
        global rList
        yList = []
        mList = []
        rList = []
        # Lists to hold M, Y and Read data
        for i in months:
            mList.append(i[1])
            yList.append(i[0])
            rList.append(i[2])
    # If no M, Y or Meter values given
    else:
        return

    return mList, yList, rList, tableName, month, meter, year


# Function to add new meter read
def addMeterRead():
    getLists()
    # Check if getLists return anything
    if getLists() != None:
        global read
        read = inputRead.get()

        # Check if M or Y have been selected
        if (month == 'Select Month' or year == 'Select Year'):
            refresh()
            infoText.set("Missing month/year")
            return

        # Check if M and Y are in DB already
        elif (month in mList) and (int(year) in yList):
            refresh()
            infoText.set("Meter Read already in database.")
            return

        # Check if meter read is less than or equal to previous reads
        elif (read <= max(rList)):
            refresh()
            infoText.set("Reading lower than previous.")
            return

        # Run if new read is higher than previous and does not have M&Y same as previous
        else:
            try:
                sql = f"INSERT INTO {tableName}(Year, Month, Read) VALUES('{year}', '{month}', {read})"
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                infoText.set("Meter read added successfully.")
                refresh()
            except:
                refresh()
                infoText.set('Error accessing DB.')
    else:
        refresh()
        infoText.set("Missing input data.")


# Function to remove a meter read row in DB
def removeMeterRead():
    getLists()
    if getLists() != None:
        # Check if M&Y are in DB
        if (month in mList) and (int(year) in yList):
            sql = f"DELETE FROM {tableName} WHERE (Year={year} AND Month='{month}')"
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            infoText.set(f"Read for {month} - {year} deleted.")
            refresh()
        # If M or Y not in DB
        else:
            refresh()
            if month == 'Select Month' or year == 'Select Year':
                infoText.set(f"Month or year not selected.")
                return
            else:
                infoText.set(f"Reading for {month} and {year} not in DB.")
                return
    else:
        refresh()
        infoText.set("Missing meter data.")


# Function to reset option menus and rerun meterYTD function
def refresh():
    variable.set('Select Year')
    variable1.set('Select Meter')
    variable3.set('Select Month')
    inputRead.set(0)
    infoText.set('')
    meterYTD(*['HV1'], year=2019)
    meterYTD(*['HV2'], year=2019)
    meterYTD(*['Benco'], year=2019)


# Function to show graphs
def showGraph(meter):
    # Declare which table based on the meter value selected
    if meter == 'HV1':
        tableName = 'HV1Table'
    elif meter == 'HV2':
        tableName = 'HV2Table'
    elif meter == 'Benco':
        tableName = 'BencoTable'
    cursor = connection.cursor()
    sql = f"SELECT Year, Month, Read FROM {tableName} ORDER BY Read ASC"
    y = cursor.execute(sql)
    months = []
    for monthi in y:
        months.append(monthi)

    # Create list from DB columns
    mList = []
    rList19 = []
    rList18 = []
    rList17 = []

    # Lists to hold M, Y and Read data
    for i in months:
        if (2019 - 1) == (i[0]) and i[1] == 'December':
            rList19.append(i[2])
        if i[0] == 2019:
            rList19.append(i[2])

        if (2018 - 1) == (i[0]) and i[1] == 'December':
            rList18.append(i[2])
        if i[0] == 2018:
            rList18.append(i[2])

        if (2017 - 1) == (i[0]) and i[1] == 'December':
            rList17.append(i[2])
        if i[0] == 2017:
            rList17.append(i[2])

        mList.append(i[1])

    monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                 'November', 'December']

    consumptionList17 = []
    for i in range(len(rList17) - 1):
        consumptionList17.append(abs(rList17[i] - rList17[i+1]))

    consumptionList18 = []
    for i in range(len(rList18) - 1):
        consumptionList18.append(abs(rList18[i] - rList18[i+1]))

    consumptionList19 = []
    for i in range(len(rList19) - 1):
        consumptionList19.append(abs(rList19[i] - rList19[i+1]))

    # Plot the points using matplotlib
    f = Figure(figsize=(28, 7), dpi=50)
    a = f.add_subplot(111)
    t = monthList[:len(consumptionList18)]
    s = consumptionList18

    if meter == 'Benco':
        a.plot(monthList[3:len(consumptionList19)+3], consumptionList19)
    else:
        a.plot(monthList[:len(consumptionList17)], consumptionList17, label='2017')
        a.plot(monthList[:len(consumptionList18)], consumptionList18, label='2018')
        a.plot(monthList[:len(consumptionList19)], consumptionList19, label='2019')
    a.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    a.legend(loc='upper left', fontsize=16)

    a.set_title(f"{meter} Consumption", fontsize=18)
    a.set_xlabel('Months', fontsize=17)
    a.set_ylabel('Consumption (kWh)', fontsize=17)

    # a tk.DrawingArea
    canvas = FigureCanvasTkAgg(f, master=bframe)
    canvas.get_tk_widget().grid(row=0, columnspan=3)
    canvas._tkcanvas.grid(row=0, columnspan=3)


# Run main function for three meters
meterYTD(*['HV1'], year=2019)
meterYTD(*['HV2'], year=2019)
meterYTD(*['Benco'], year=2019)
showGraph('HV1')


Label(rframe, text="Please select Month, Year and Meter to enter a read",
      font=("Times", 14), bg='wheat1').grid(row=5, column=0, columnspan=2, padx=5, pady=5)


# Add read button
subButton = Button(rframe, text='Add Read', command=addMeterRead, font=("Arial", 12), highlightbackground="khaki3", fg="Black", highlightthickness=5)
subButton.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky=W+E)

# Remove button
delButton = Button(rframe, text='Delete Read', command=removeMeterRead, font=("Arial", 12), highlightbackground="khaki3", fg="Red", highlightthickness=5)
delButton.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky=W+E)

# Refresh button
refButton = Button(rframe, text='Refresh', command=refresh, font=("Arial", 12), highlightbackground="khaki3", fg="Black", highlightthickness=5)
refButton.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky=W+E)

# Add quit button
qButton = Button(rframe, text='Quit', command=root.destroy, font=("Arial", 12), highlightbackground="khaki3", fg="Red", highlightthickness=5)
qButton.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky=W+E)

# Drop down box to select month
monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
variable3.set("Select Month") # default value
mOption = OptionMenu(rframe, variable3, *monthList)
mOption.grid(row=6, column=0, padx=5, pady=5, sticky=W+E)
mOption.config(bg='wheat1')

# Drop down box to select year
yearList = [2017, 2018, 2019, 2020, 2021]
variable.set("Select Year") # default value
yOption = OptionMenu(rframe, variable, *yearList)
yOption.grid(row=6, column=1, padx=5, pady=5, sticky=W+E)
yOption.config(bg='wheat1')


# Drop down box to select meter
meterList = ['HV_1_Meter', 'HV_2_Meter', 'Benco_Meter']
variable1.set("Select Meter") # default value
metOption = OptionMenu(rframe, variable1, *meterList)
metOption.grid(row=7, column=0, padx=5, pady=5, sticky=W+E)
metOption.config(bg='wheat1')

# Entry box for user input
e = Entry(rframe, textvariable=inputRead)
e.grid(row=7, column=1, sticky=W+E)
e.config(bg='khaki3')

# HV1 Labels
hv1Label = LabelFrame(lframe, text="HV 1 Meter", bg='khaki3')
hv1Label.grid(row=1, column=0, sticky=E + W, padx=10, pady=10)

Label(hv1Label, text="YTD", font=("Arial", 14), bg='khaki3').grid(row=0, column=0, padx=5, pady=5)
Label(hv1Label, text="Monthly Average", font=("Arial", 14), bg='khaki3').grid(row=1, column=0, padx=5, pady=5)
Label(hv1Label, text="Monthly High", font=("Arial", 14), bg='khaki3').grid(row=2, column=0, padx=5, pady=5)
Label(hv1Label, text="Monthly Low", font=("Arial", 14), bg='khaki3').grid(row=3, column=0, padx=5, pady=5)

Label(hv1Label, textvariable=hv1LabelTextYTD, font=("Arial", 14), bg='khaki3').grid(row=0, column=1, padx=5, pady=5)
Label(hv1Label, textvariable=hv1LabelTextAve, font=("Arial", 14), bg='khaki3').grid(row=1, column=1, padx=5, pady=5)
Label(hv1Label, textvariable=hv1LabelTextH, font=("Arial", 14), bg='khaki3').grid(row=2, column=1, padx=5, pady=5)
Label(hv1Label, textvariable=hv1LabelTextL, font=("Arial", 14), bg='khaki3').grid(row=3, column=1, padx=5, pady=5)

# HV2 Labels
hv2Label = LabelFrame(lframe, text="HV 2 Meter", bg='khaki3')
hv2Label.grid(row=1, column=1, sticky=E + W, padx=10, pady=10)

Label(hv2Label, text="YTD", font=("Arial", 14), bg='khaki3').grid(row=0, column=0, padx=5, pady=5)
Label(hv2Label, text="Monthly Average", font=("Arial", 14), bg='khaki3').grid(row=1, column=0, padx=5, pady=5)
Label(hv2Label, text="Monthly High", font=("Arial", 14), bg='khaki3').grid(row=2, column=0, padx=5, pady=5)
Label(hv2Label, text="Monthly Low", font=("Arial", 14), bg='khaki3').grid(row=3, column=0, padx=5, pady=5)

Label(hv2Label, textvariable=hv2LabelText, font=("Arial", 14), bg='khaki3').grid(row=1, column=1, padx=5, pady=5)
Label(hv2Label, textvariable=hv2LabelTextYTD, font=("Arial", 14), bg='khaki3').grid(row=0, column=2, padx=5, pady=5)
Label(hv2Label, textvariable=hv2LabelTextAve, font=("Arial", 14), bg='khaki3').grid(row=1, column=2, padx=5, pady=5)
Label(hv2Label, textvariable=hv2LabelTextH, font=("Arial", 14), bg='khaki3').grid(row=2, column=2, padx=5, pady=5)
Label(hv2Label, textvariable=hv2LabelTextL, font=("Arial", 14), bg='khaki3').grid(row=3, column=2, padx=5, pady=5)

# Benco Labels
bencoLabel = LabelFrame(lframe, text="Benco Meter", bg='khaki3')
bencoLabel.grid(row=1, column=2, sticky=E + W, padx=10, pady=10)

Label(bencoLabel, text="YTD", font=("Arial", 14), bg='khaki3').grid(row=0, column=0, padx=5, pady=5)
Label(bencoLabel, text="Monthly Average", font=("Arial", 14), bg='khaki3').grid(row=1, column=0, padx=5, pady=5)
Label(bencoLabel, text="Monthly High", font=("Arial", 14), bg='khaki3').grid(row=2, column=0, padx=5, pady=5)
Label(bencoLabel, text="Monthly Low", font=("Arial", 14), bg='khaki3').grid(row=3, column=0, padx=5, pady=5)

Label(bencoLabel, textvariable=bencoLabelText, font=("Arial", 14), bg='khaki3').grid(row=1, column=2, padx=5, pady=5)
Label(bencoLabel, textvariable=bencoLabelTextYTD, font=("Arial", 14), bg='khaki3').grid(row=0, column=3, padx=5, pady=5)
Label(bencoLabel, textvariable=bencoLabelTextAve, font=("Arial", 14), bg='khaki3').grid(row=1, column=3, padx=5, pady=5)
Label(bencoLabel, textvariable=bencoLabelTextH, font=("Arial", 14), bg='khaki3').grid(row=2, column=3, padx=5, pady=5)
Label(bencoLabel, textvariable=bencoLabelTextL, font=("Arial", 14), bg='khaki3').grid(row=3, column=3, padx=5, pady=5)

# Graph button HV1
HV1Button = Button(bframe, text='HV-1 Graph', command=lambda: showGraph('HV1'), font=("Times", 14), highlightbackground="khaki3", fg="Black", highlightthickness=5)
HV1Button.grid(row=1, column=0, padx=5, pady=5, sticky=W+E)

# Graph button HV2
HV2Button = Button(bframe, text='HV-2 Graph', command=lambda: showGraph('HV2'), font=("Times", 14), highlightbackground="khaki3", fg="Black", highlightthickness=5)
HV2Button.grid(row=1, column=1, padx=5, pady=5, sticky=W+E)

# Graph button Benco
BencoButton = Button(bframe, text='Benco Graph', command=lambda: showGraph('Benco'), font=("Times", 14), highlightbackground="khaki3", fg="Black", highlightthickness=5)
BencoButton.grid(row=1, column=2, padx=5, pady=5, sticky=W+E)

# 2017 Button
p17Button = Button(lframe, bg="gray", text='2017 Data', command=lambda: meterYTD(*['HV1', 'HV2', 'Benco'], year=2017), font=("Times", 14), highlightbackground="khaki3", fg="Black", highlightthickness=5)
p17Button.grid(row=4, column=0, padx=5, pady=5, sticky=W+E)

# 2018 Button
p18Button = Button(lframe, text='2018 Data', command=lambda: meterYTD(*['HV1', 'HV2', 'Benco'], year=2018), font=("Times", 14), highlightbackground="khaki3", fg="Black", highlightthickness=5)
p18Button.grid(row=4, column=1, padx=5, pady=5, sticky=W+E)

# 2019 Button
p19Button = Button(lframe, text='2019 Data', command=lambda: meterYTD(*['HV1', 'HV2', 'Benco'], year=2019), font=("Times", 14), highlightbackground="khaki3", fg="Black", highlightthickness=5)
p19Button.grid(row=4, column=2, padx=5, pady=5, sticky=W+E)

root.mainloop()