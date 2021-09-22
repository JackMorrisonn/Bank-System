import mysql.connector
from tkinter import *
from tkinter import ttk  
import tkinter.font as TkFont
from passwordHash import *
from transactionHandler import createTransaction, getTransactHistory



width = 960
height = 540

window = Tk()


bgcolour = "white"
fgcolour = "black"
alternatecolour = "firebrick3"
Abadi24 = TkFont.Font(family ="Abadi", size = 24)
Abadi16 = TkFont.Font(family ="Abadi", size = 16)
Abadi10 = TkFont.Font(family ="Abadi", size = 10)


#Login using enduser account
#Doesnt have any editing rights, can only use SELECT statement

#Init statement is called every page to have a live version of the database, rather than an image created at the start of the program
#Each connection is closed at the end of the program

def init():
	db = mysql.connector.connect(
		host = "127.0.0.1",
		user = "enduser",
		passwd = "password1234",
		database = "bankSystem"
	)
	return db

#Login Handler

def login():
	db = init()
	clientID = userEntry.get()
	password = passEntry.get()
	password = bytes(password, 'utf-8')
	logincursor = db.cursor(buffered = True)

	try:
		login_query = """SELECT password FROM Client WHERE client_id = %s"""
		logincursor.execute(login_query, (int(clientID),))
		passToCheck = logincursor.fetchone()
		for row in passToCheck:
			row = bytes(row, 'utf-8')
			isCorrect = checkPass(password, row)

	except:
		wrongData = Label(window, text = "Wrong ID/Pass", fg = "red", bg = bgcolour)
		wrongData.place(x = width/2, y = height/2 - 20, anchor = "center")
	else:
		if isCorrect:
			getData = """SELECT f_name, l_name FROM Client WHERE client_id = %s"""
			logincursor.execute(getData, (int(clientID),))
			userData = logincursor.fetchall()
			for row in userData:
				fName, lName = row
			logincursor.close()
			db.close()
			homeScreen(clientID, fName, lName)
		else:
			wrongData = Label(window, text = "Wrong ID/Pass", fg = "red", bg = bgcolour)
			wrongData.place(x = width/2, y = height/2 - 20, anchor = "center")
	

#Allows the program to get the current balance for the current account

def getBalance(clientId, accountType):
	db = init()
	balance_query = """SELECT balance FROM Account WHERE client_id = %s AND account_type = %s"""
	balanceData = (clientId, accountType)

	balancecursor = db.cursor(buffered = True)
	balancecursor.execute(balance_query, balanceData)
	balance = balancecursor.fetchone()

	for row in balance:
		clientBalance = row
	db.close()
	return clientBalance

#Initial check if the account is admin 

def isAdmin(clientId):
	db = init()
	admincursor = db.cursor(buffered = True)
	admin_query = """SELECT f_name, l_name FROM Client WHERE client_id = %s"""
	admindata = (int(clientId), )
	admincursor.execute(admin_query, admindata)
	adminInfo = admincursor.fetchall()
	for row in adminInfo:
		fname, lname = row
	admincursor.close()
	db.close()
	if fname == 'admin' and lname == 'admin':
		return True
	else:
		return False
	
####################################################

#GUI ELEMENTS

####################################################

def loginPage():
	clearScreen()
	topBanner = Frame(window, bg = fgcolour, height = 25, width = 960)
	topBanner.place(x = 0, y = 0)

	welcomeBanner = Frame(window, bg = alternatecolour, height = 75, width = 960)
	welcomeBanner.place(x = 0, y = 25)
	welcomeMessage = Label(welcomeBanner, text = "Login", fg = "white", bg = alternatecolour, font = Abadi24)
	welcomeMessage.place(x = 0, y = 25)

	window.title("Login")
	window.geometry("960x540")
	window.minsize(960, 540)
	window.maxsize(960, 540)
	window.configure(background = bgcolour)

	global userEntry
	global passEntry

	enterUser = Label(window, text = "Client ID", bg = bgcolour)
	enterUser.place(x = width/2, y = height/2, anchor = "center")
	userEntry = Entry(window, width = 40, bg = "white")
	userEntry.place(x = width/2, y = height/2 + 20, anchor = "center")


	enterPass = Label(window, text = "Password", bg = bgcolour)
	enterPass.place(x = width/2, y = height/2 + 40, anchor = "center")
	passEntry = Entry(window, width = 40, show = "*", bg = "white")
	passEntry.place(x = width/2, y = height/2 + 60, anchor = "center")

	loginButton = Button(window, text = "Login", width = 10, command = login)
	loginButton.place(x = width/2, y = height/2 + 100, anchor = "center")



def homeScreen(clientId, fName, lName):
	db = init()
	clearScreen()
	window.title("Home Screen")
	if isAdmin(clientId):
		adminPage()
		db.close()

	else:
		clientBalance = StringVar()
		clientBalance.set("Avaliable Balance: $" + str(getBalance(clientId, 'savings')))
		
		totalFrame = Frame(window, bg = alternatecolour, height = 400, width = 700)
		totalFrame.place(x = 0, y = 120)

		balanceFrame = Frame(totalFrame, bg = fgcolour, height = 40, width = 650)
		balanceFrame.place(x = 25, y = 5)
		balanceText = Label(balanceFrame, textvariable = clientBalance, fg = "white", bg = fgcolour, font = Abadi16)
		balanceText.place(x = 650, y = 5, anchor = "ne")

		def changeBalance(event):	
			clientBalance.set("Avaliable Balance: $" + str(getBalance(clientId, accountSelector.get())))
			balanceText = Label(balanceFrame, textvariable = clientBalance, fg = "white", bg = fgcolour, font = Abadi16)
			balanceText.place(x = 650, y = 5, anchor = "ne")

			transactionHist = getTransactHistory(clientId, accountSelector.get())
			if len(transactionHist) > 5:
				maxIndex = -5
			else:
				maxIndex = len(transactionHist) * -1
			for i in range(-1, maxIndex , -1):
				transaction = StringVar()
				if transactionHist[i][1] == "withdraw":
					transaction.set('$' + str(transactionHist[i][0]) + ' | ' + transactionHist[i][1] + ' | ' + transactionHist[i][2] +  ' | Paid into id: ' + str(transactionHist[i][3]))
				else:
					transaction.set('$' + str(transactionHist[i][0]) + ' | ' + transactionHist[i][1] + ' | ' + transactionHist[i][2] +  ' | Paid from id: ' + str(transactionHist[i][3]))
				transactionBox = Frame(transactionFrame, bg = fgcolour, height = 60, width = 650, highlightbackground= alternatecolour, highlightthickness=1)
				transactionBox.place(x = 0, y = 60 * ((i * -1) - 1))
				transactionLabel = Label(transactionBox, textvariable = transaction, fg = "white", bg = "black", font = Abadi10)
				transactionLabel.place(x = 15, y = 20)


		topBanner = Frame(window, bg = fgcolour, height = 25, width = 960)
		topBanner.place(x = 0, y = 0)

		welcomeMessage = StringVar()
		welcomeMessage.set("Welcome " + fName.capitalize() + " " + lName.capitalize())
		
		welcomeBanner = Frame(window, bg = alternatecolour, height = 75, width = 960)
		welcomeBanner.place(x = 0, y = 25)
		welcomeMessage = Label(welcomeBanner, textvariable = welcomeMessage, fg = "white", bg = alternatecolour, font = Abadi24)
		welcomeMessage.place(x = 0, y = 25)

		logoutButton = Button(welcomeBanner, text = "Logout", command = loginPage)
		logoutButton.place(x = 950, y = 45, anchor = "ne")

		transactionFrame = Frame(totalFrame, bg = bgcolour, height = 300, width = 650)
		transactionFrame.place(x = 25, y = 60)

		accounts = ['savings', 'credit']
		accountSelector = ttk.Combobox(balanceFrame, values = accounts, state = "readonly")
		accountSelector.current(0)
		accountSelector.bind("<<ComboboxSelected>>", changeBalance)
		accountSelector.place(x = 10, y = 8)

		transactionHist = getTransactHistory(clientId, accountSelector.get())
		if len(transactionHist) > 5:
			maxIndex = -5
		else:
			maxIndex = len(transactionHist) * -1
		for i in range(-1, maxIndex -1, -1):
			transaction = StringVar()
			if transactionHist[i][1] == "withdraw":
				transaction.set('$' + str(transactionHist[i][0]) + ' | ' + transactionHist[i][1] + ' | ' + transactionHist[i][2] +  ' | Paid into id: ' + str(transactionHist[i][3]))
			else:
				transaction.set('$' + str(transactionHist[i][0]) + ' | ' + transactionHist[i][1] + ' | ' + transactionHist[i][2] +  ' | Paid from id: ' + str(transactionHist[i][3]))
			transactionBox = Frame(transactionFrame, bg = fgcolour, height = 60, width = 650, highlightbackground= alternatecolour, highlightthickness=1)
			transactionBox.place(x = 0, y = 60 * ((i * -1) - 1))
			transactionLabel = Label(transactionBox, textvariable = transaction, fg = "white", bg = "black", font = Abadi10)
			transactionLabel.place(x = 15, y = 20)

		payButton = Button(totalFrame, text = "Pay Someone", command = lambda: [payScreen(clientId, fName, lName), db.close()])
		payButton.place(x = 25, y = 370)



def payScreen(clientId, fName, lName):
	db = init()
	clearScreen()
	window.title("Pay Someone")

	topBanner = Frame(window, bg = fgcolour, height = 25, width = 960)
	topBanner.place(x = 0, y = 0)

	welcomeBanner = Frame(window, bg = alternatecolour, height = 75, width = 960)
	welcomeBanner.place(x = 0, y = 25)
	welcomeMessage = Label(welcomeBanner, text = "Pay Someone", fg = "white", bg = alternatecolour, font = Abadi24)
	welcomeMessage.place(x = 0, y = 25)

	logoutButton = Button(welcomeBanner, text = "Logout", command = loginPage)
	logoutButton.place(x = 950, y = 45, anchor = "ne")

	homeButton = Button(welcomeBanner, text = "Home", command = lambda: [homeScreen(clientId, fName, lName), db.close()])
	homeButton.place(x = 900, y = 45, anchor = "ne")

	totalFrame = Frame(window, bg = alternatecolour, height = 400, width = 700)
	totalFrame.place(x = 0, y = 120)

	targetClient = Label(totalFrame, text = "Who do you wish to pay?", fg = "white", bg = alternatecolour, font = Abadi10)
	targetClient.place(x = 25, y = 20)
	targetEnter = Entry(totalFrame, width = 40, bg = "white")
	targetEnter.place(x = 25, y = 50)


	account = Label(totalFrame, text = "From which account?", fg = "white", bg = alternatecolour, font = Abadi10)
	account.place(x = 25, y = 80)
	accounts = ['savings', 'credit']
	accountSelector = ttk.Combobox(totalFrame, values = accounts, state = "readonly")
	accountSelector.current(0)
	accountSelector.place(x = 25, y = 110)

	targetAccount = Label(totalFrame, text = "To Which Account?", fg = "white", bg = alternatecolour, font = Abadi10)
	targetAccount.place(x = 25, y = 140)
	targetAccounts = ['savings', 'credit']
	targetAccountSelector = ttk.Combobox(totalFrame, values = accounts, state = "readonly")
	targetAccountSelector.current(0)
	targetAccountSelector.place(x = 25, y = 170)

	amountToPay = Label(totalFrame, text = "How much?", fg = "white", bg = alternatecolour, font = Abadi10)
	amountToPay.place(x = 25, y = 200)
	amountEnter = Entry(totalFrame, width = 40, bg = "white")
	amountEnter.place(x = 25, y = 230)
	
	payButton = Button(totalFrame, text = "Pay", command = lambda: newTransaction(clientId, targetEnter.get(), accountSelector.get(), targetAccountSelector.get(), int(amountEnter.get())) )
	payButton.place(x = 25, y = 260)

	def newTransaction(clientId, targetId, clientAccount, targetAccount, amount):
		resultWin = Tk()
		resultWin.title("Transaction")
		resultWin.geometry("192x108")
		resultWin.minsize(192, 108)
		resultWin.maxsize(192, 108)
		resultWin.configure(background = alternatecolour)

		topBanner = Frame(resultWin, bg = fgcolour, height = 15, width = 192)
		topBanner.place(x = 0, y = 0)

		w = 192/2
		h = 108/2

		if createTransaction(clientId, targetId, clientAccount, targetAccount, amount):
			validTransact = Label(resultWin, text = "Transaction successful!", fg = "black", bg = alternatecolour, font = Abadi10)
			validTransact.place(x = w, y = 30, anchor = "center")
		else:
			invalidTransact = Label(resultWin, text = "Transaction was invalid", fg = "red", bg = "white", font = Abadi10)
			invalidTransact.place(x = w, y = 30, anchor = "center")

		continueButton = Button(resultWin, text = "Continue", command = lambda: [payScreen(clientId, fName, lName), resultWin.destroy()])
		continueButton.place(x = w, y = 60, anchor = "center")


def adminPage():
	db = init()
	from bankSystem import newClient, newAccount

	clearScreen()
	window.title("Admin")
	topBanner = Frame(window, bg = fgcolour, height = 25, width = 960)
	topBanner.place(x = 0, y = 0)

	welcomeBanner = Frame(window, bg = alternatecolour, height = 75, width = 960)
	welcomeBanner.place(x = 0, y = 25)
	welcomeMessage = Label(welcomeBanner, text = "Admin", fg = "white", bg = alternatecolour, font = Abadi24)
	welcomeMessage.place(x = 0, y = 25)

	totalFrame = Frame(window, bg = alternatecolour, height = 400, width = 700)
	totalFrame.place(x = 0, y = 120)

	logoutButton = Button(welcomeBanner, text = "Logout", command = loginPage)
	logoutButton.place(x = 950, y = 45, anchor = "ne")
	
	fName = Label(totalFrame, text = "Enter new client given name", fg = "white", bg = alternatecolour, font = Abadi10)
	newUserFName = Entry(totalFrame, width = 40, bg = "white")
	fName.place(x = 25, y = 30)
	newUserFName.place(x = 25, y = 60)

	lName = Label(totalFrame, text = "Enter new client family name", fg = "white", bg = alternatecolour, font = Abadi10)
	newUserLName = Entry(totalFrame, width = 40, bg = "white")
	lName.place(x = 25, y = 90)
	newUserLName.place(x = 25, y = 120)

	phNo = Label(totalFrame, text = "Enter new client phone number", fg = "white", bg = alternatecolour, font = Abadi10)
	newUserPhNo = Entry(totalFrame, width = 40, bg = "white")
	phNo.place(x = 25, y = 150)
	newUserPhNo.place(x = 25, y = 180)

	add = Label(totalFrame, text = "Enter new client address", fg = "white", bg = alternatecolour, font = Abadi10)
	newUserAdd = Entry(totalFrame, width = 40, bg = "white")
	add.place(x = 25, y = 210)
	newUserAdd.place(x = 25, y = 240)

	passW = Label(totalFrame, text = "Enter new client password", fg = "white", bg = alternatecolour, font = Abadi10)
	newUserPass = Entry(totalFrame, width = 40, bg = "white")
	passW.place(x = 25, y = 270)
	newUserPass.place(x = 25, y = 300)

	newUser = Button(totalFrame, text = "Create new User", command = lambda: enterNewClient(newUserFName.get(), newUserLName.get(), newUserPhNo.get(), newUserAdd.get(), newUserPass.get()))
	newUser.place(x = 25, y = 330)

	def enterNewAccount():
		clientcursor = db.cursor(buffered = True)
		clientId_query = """SELECT client_id FROM Client WHERE client_id = (SELECT max(client_id) FROM Client)"""
		clientcursor.execute(clientId_query)
		latestClient = clientcursor.fetchone()
		for row in latestClient:
			latestId = row

		newAccount(int(latestId) + 1, 'savings', 0)
		newAccount(int(latestId) + 1, 'credit', 0)


	def enterNewClient(fName, lName, phNo, add, passW):
		blankData = False
		newClientData = [fName, lName, phNo, add, passW]
		for i in range(len(newClientData)):
			if newClientData[i] == "":
				blankData = True
				break

		resultWin = Tk()
		resultWin.title("New Client")
		resultWin.geometry("192x108")
		resultWin.minsize(192, 108)
		resultWin.maxsize(192, 108)
		resultWin.configure(background = alternatecolour)

		w = 192/2
		h = 108/2
		topBanner = Frame(resultWin, bg = fgcolour, height = 15, width = 192)
		topBanner.place(x = 0, y = 0)

		if blankData == False:
			clientcursor = db.cursor(buffered = True)
			newClient(fName, lName, int(phNo), add, passW)
			validClient = Label(resultWin, text = "Client was created", fg = "white", bg = alternatecolour, font = Abadi10)
			validClient.place(x = w, y = 30, anchor = "center")
			enterNewAccount()

		else:
			invalidClient = Label(resultWin, text = "Some data was invalid", fg = "red", bg = "white", font = Abadi10)
			invalidClient.place(x = w, y = 30, anchor = "center")

		continueButton = Button(resultWin, text = "Continue", command = lambda: [adminPage(), resultWin.destroy()])
		continueButton.place(x = w, y = 60, anchor = "center")


def clearScreen():
	widgetLst = window.winfo_children()
	for item in widgetLst:
		item.destroy()



loginPage()
window.mainloop()
