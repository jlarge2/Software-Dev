##Breezy Budget
##Author: Jennifer Large
##Last Modified: 12/14/23
##Budget App that takes input for each budget item, categorizes it, and then outputs totals together and separately, 
##both monthly and biweekly (so the user can have that amount directly deposited into the appropriate account, making budgeting a breeze)

##imports
import tkinter as tk
from tkinter import ttk

##class for user input entries
class Entry:
    def __init__(self, amount, category, description, occurrence):
        self.amount = amount
        self.category = category.lower() #converts all to lowercase
        self.description = description
        self.occurrence = occurrence

    amount: float #shows each attribute and its variable type
    category: str
    description: str
    occurrence: bool

def main():
    ##user can enter a series of [entry]s, stored in a list
    global entries #entries declared as global variable
    entries = [] #empty list
    tree = None #to make the tree work later (and allow me to add to it later)


    ### MAIN WINDOW
    window = tk.Tk()
    window.title("Breezy Budget")
    window.geometry("1000x800")
    bgImage = tk.PhotoImage(file = "https://github.com/jlarge2/Software-Dev/blob/main/bg.png") #adding a background photo
    bgLabel = tk.Label(window, image = bgImage) 
    bgLabel.place(relwidth = 1, relheight = 1, relx = 0, rely = 0)

    textLabel = tk.Label(window, text="Breezy Budget", justify="center", font="Centaur 22 bold") #this prints if the image doesn't load

    ##checks to see if the title image loaded
    try:
        titleImage = tk.PhotoImage(file = "https://github.com/jlarge2/Software-Dev/blob/main/breezytitle.png")
        imageLabel = tk.Label(window, image = titleImage) 
        imageLabel.place(x = 360, y = 35)

        textLabel.pack_forget()  #makes it so alt text doesn't show if the image loads

    except tk.TclError:
        textLabel.pack()  #shows the alt title text if the image doesn't load
    

    ### TOTALS WINDOW
    totalsFrame = ttk.Frame(window)
    totalsFrame.pack(pady = 10)

    def ShowEntryList(entries):
        nonlocal tree
        window.withdraw() #hides main window to "switch" windows
        listWindow = tk.Toplevel()
        listWindow.title("Budget Items")
        listWindow.geometry("800x450")
        bg2Image = tk.PhotoImage(file = "https://github.com/jlarge2/Software-Dev/blob/main/bg.png") #applying background image to this window too
        bg2Label = tk.Label(listWindow, image=bg2Image)
        bg2Label.image = bg2Image  #keeping a reference because otherwise it won't show up
        bg2Label.place(relwidth = 1, relheight = 1, relx = 0, rely = 0)

        #create columns to prevent chaos (trust me)
        tree = ttk.Treeview(listWindow)
        tree["columns"] = ("Amount", "Category", "Description", "Occurrence")
        tree.column("#0", width = 0, stretch = tk.NO) #hidden column

        #column headings
        tree.heading("Amount", text = "Amount", anchor = "center")
        tree.heading("Category", text = "Category", anchor = "center")
        tree.heading("Description", text = "Description", anchor = "center")
        tree.heading("Occurrence", text = "Recurring?", anchor = "center")

        #making the amounts justify right, and everything else to be centered
        tree.column("Amount", anchor = "e")
        tree.column("Category", anchor = "center")
        tree.column("Description", anchor = "center")
        tree.column("Occurrence", anchor = "center")

        for entry in entries:
            tree.insert("", tk.END, values=(entry.amount, entry.category, entry.description, "Yes" if entry.occurrence else "No")) #adds the items

        tree.pack(fill="both", expand=True) #finishes the tree

        ##calculates totals for items input by the user
        spendingMonthly = CalculateMonthlyTotal("spending")
        billsMonthly = CalculateMonthlyTotal("bills")
        savingsMonthly = CalculateMonthlyTotal("savings")

        spendingBiweekly = CalculateBiweeklyTotal("spending")
        billsBiweekly = CalculateBiweeklyTotal("bills")
        savingsBiweekly = CalculateBiweeklyTotal("savings")

        ##totals frame for organization
        totalsFrame = ttk.Frame(listWindow)
        totalsFrame.pack(expand = True)

        ##frame within that frame so it can be centered
        frameMonthly = ttk.Frame(totalsFrame)
        frameMonthly.pack(side = "left", padx = 10)

        ##labels for monthly in 2 columns
        ttk.Label(frameMonthly, text = "Monthly Totals", font = "Centaur 11 bold").grid(row = 0, column = 0, columnspan = 2)

        ttk.Label(frameMonthly, text = "Spending:").grid(row = 1, column = 0, sticky = 'e') #sticky makes it line up where I want it
        ttk.Label(frameMonthly, text = f"${spendingMonthly:.2f}").grid(row = 1, column = 1, sticky = 'w')

        ttk.Label(frameMonthly, text="Bills:").grid(row=2, column=0, sticky='e')
        ttk.Label(frameMonthly, text=f"${billsMonthly:.2f}").grid(row=2, column=1, sticky='w')

        ttk.Label(frameMonthly, text="Savings:").grid(row=3, column=0, sticky='e')
        ttk.Label(frameMonthly, text=f"${savingsMonthly:.2f}").grid(row=3, column=1, sticky='w')

        ##frame within the totals frame to center alongside monthly totals
        frameBiweekly = ttk.Frame(totalsFrame)
        frameBiweekly.pack(side = "left", padx = 10)

        ##biweekly totals in 2 columns
        ttk.Label(frameBiweekly, text = "Biweekly Totals", font = "Centaur 11 bold").grid(row = 0, column = 0, columnspan = 2)

        ttk.Label(frameBiweekly, text = "Spending:").grid(row = 1, column = 0, sticky = 'e')
        ttk.Label(frameBiweekly, text = f"${spendingBiweekly:.2f}").grid(row = 1, column = 1 , sticky = 'w')

        ttk.Label(frameBiweekly, text = "Bills:").grid(row = 2, column = 0, sticky = 'e')
        ttk.Label(frameBiweekly, text = f"${billsBiweekly:.2f}").grid(row = 2, column = 1, sticky = 'w')

        ttk.Label(frameBiweekly, text = "Savings:").grid(row = 3, column = 0, sticky = 'e')
        ttk.Label(frameBiweekly, text = f"${savingsBiweekly:.2f}").grid(row = 3, column = 1, sticky = 'w')

        ##button to return to main window
        ##checking if it loads image, uses alt text if not
        try:
            imgReturn = tk.PhotoImage(file = "https://github.com/jlarge2/Software-Dev/blob/main/backtoaddmore.png")
        except tk.TclError as e:
            print(f"Failed to load image: {e}")
            imgReturn = None  #so it knows to show up

        imgReturn.image = imgReturn  #keeping a reference because otherwise it won't show up because it thinks it's garbage

        altTextReturn = "Return to Add More" #giving it alt text

        ##actually putting the button in
        returnButton = ttk.Button(listWindow, style = 'Img.TButton', compound = "left", image = imgReturn)
        if imgReturn:
            returnButton.configure(command = lambda: ReturnToAddPage(listWindow))
        else:
            returnButton.configure(text = altTextReturn)
        returnButton.pack(pady = 20)

    ##button to return to main window
    def ReturnToAddPage(listWindow):
        window.deiconify() #show main window
        listWindow.destroy() #close listWindow
    
    ##creates new list with just entries of that category, loops through to add, then returns calculated total
    def CalculateByCategory(entries, category):
        total = sum(entry.amount for entry in entries if entry.category == category)
        return total

    ##calculates monthly total
    def CalculateMonthlyTotal(category):
        return CalculateByCategory(entries, category)
    
    ##calculates biweekly total
    def CalculateBiweeklyTotal(category):
        monthlyTotal = CalculateByCategory(entries, category)
        if monthlyTotal is not None:
            return monthlyTotal // 2 #assuming 2 pay periods per month, using 2/s because math wasn't mathing with 1
        return 0

    ##to close the app
    def ButtonExit():
        window.destroy()

    ##input frame to hold information
    inputFrame = ttk.Frame(master = window)
    inputFrame.pack(pady = 200)

    ##variables and their types
    AmountInt = tk.IntVar() #$amounts
    CategoryStr = tk.StringVar() #category: spending, bills, or savings
    DescriptionStr = tk.StringVar() #description: food? gas? house payment?
    #OccurrenceBool = tk.BooleanVar() #is it recurring or no? with radio button, no longer needed

    ##column 1, with labels for each variable above
    amountLabel = ttk.Label(master = inputFrame, text = "Enter Amount")
    amountLabel.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")

    dollarLabel = ttk.Label(master = inputFrame, text = "$") #adding a $ to the amount column
    dollarLabel.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "e")

    categoryLabel = ttk.Label(master = inputFrame, text = "Enter Category (Spending, Bills, or Savings)")
    categoryLabel.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")

    descriptionLabel = ttk.Label(master = inputFrame, text = "Enter Description")
    descriptionLabel.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "w")

    occurrenceLabel = ttk.Label(master = inputFrame, text = "Is this a recurring cost?")
    occurrenceLabel.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "w")

    ##column 2, with input fields/radio buttons for each variable above
    entryAmount = ttk.Entry(master = inputFrame, textvariable = AmountInt)
    entryAmount.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "e")
    entryAmount.delete(0, tk.END) #it kept showing up with a 0 in the field, this should clear it
    ##validation for amount
    def validateAmount():
        amount = AmountInt.get()
        if amount: float(amount) #checks if float
        else:
            AmountInt.set("Must put a valid number")
    entryAmount.bind("<FocusOut>", lambda e: validateAmount()) #amount validation on focus out
    ##validation for category
    entryCategory = ttk.Entry(master = inputFrame, textvariable = CategoryStr) 
    entryCategory.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "e")
    def validateCategory(): #validate/convert to lowercase
        category = CategoryStr.get().upper()
        if category in ["spending", "savings", "bills"]:  #check against these three categories
            CategoryStr.set(category) #make lowercase
        else:
            CategoryStr.set("Invalid category!") #clear field if not one of these three
    entryCategory.bind("<FocusOut>", lambda e: validateCategory()) #category validation on focus out
    ##regular entry for description
    entryDescription = ttk.Entry(master = inputFrame, textvariable = DescriptionStr)
    entryDescription.grid(row = 2, column = 1, padx=5, pady = 5, sticky = "e")
    ##creating a radio button
    occurrenceFrame = ttk.Frame(master = inputFrame)
    occurrenceFrame.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "w")
    ##recurring variable
    OccurrenceValue = tk.StringVar()
    ##radio button yes
    yesRadio = ttk.Radiobutton(occurrenceFrame, text = "Yes", variable = OccurrenceValue, value = "Yes")
    yesRadio.pack(side = "left", padx = 5)
    ##radio button no
    noRadio = ttk.Radiobutton(occurrenceFrame, text = "No", variable = OccurrenceValue, value = "No")
    noRadio.pack(side = "left", padx = 5)

    def AddToList(): 
        nonlocal tree  #to tie back to the other tree
        global entries  #to get all the entries

        #gets info
        amount = AmountInt.get() 
        category = CategoryStr.get()
        description = DescriptionStr.get()
        occurrence = OccurrenceValue.get() == "Yes"  #convert to boolean

        # adds to the list
        newEntry = Entry(amount, category, description, occurrence)
        entries.append(newEntry)

        # Recalculate totals after adding new entry
        recalculateTotals()

        entryAmount.delete(0, tk.END)
        entryCategory.delete(0, tk.END)
        entryDescription.delete(0, tk.END)
        OccurrenceValue.set("")

    def recalculateTotals():
        global entries  # To access the global entries list
        # totalSpending = CalculateByCategory(entries, "spending")
        # totalBills = CalculateByCategory(entries, "bills")
        # totalSavings = CalculateByCategory(entries, "savings")

    ##load images for buttons with alt text if it doesn't load
    try:
        imgAdd = tk.PhotoImage(file="https://github.com/jlarge2/Software-Dev/blob/main/addtolist.png")
        imgTotals = tk.PhotoImage(file="https://github.com/jlarge2/Software-Dev/blob/main/totals.png")
        imgExit = tk.PhotoImage(file="https://github.com/jlarge2/Software-Dev/blob/main/closeprogram.png")
    except tk.TclError as e:
        print(f"Failed to load images: {e}")
        imgAdd = imgTotals = imgExit = None  #if they don't load, it sets to no images

    ##alternative text for buttons
    altTextAdd = "Add"
    altTextTotals = "Totals"
    altTextExit = "Exit Program" 

    ##buttons with images or alternative text if images fail to load
    addButton = ttk.Button(master = inputFrame, style = 'Img.TButton', compound = "left", image = imgAdd)
    if imgAdd:
        addButton.configure(command = AddToList)
    else:
        addButton.configure(text = altTextAdd)
    addButton.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "we")

    showListButton = ttk.Button(master = inputFrame, style = 'Img.TButton', compound = "left", image = imgTotals)
    if imgTotals:
        showListButton.configure(command = lambda: ShowEntryList(entries))
    else:
        showListButton.configure(text = altTextTotals)
    showListButton.grid(row = 8, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "we")

    exitButton = ttk.Button(master = inputFrame, style = 'Img.TButton', compound = "left", image = imgExit)
    if imgExit:
        exitButton.configure(command = ButtonExit)
    else:
        exitButton.configure(text = altTextExit)
    exitButton.grid(row = 9, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "we")


    ##main loop
    window.mainloop()

main()
