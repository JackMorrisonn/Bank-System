import mysql.connector
from bankSystem import newTransaction
from datetime import datetime

def init():
	db = mysql.connector.connect(
		host = "127.0.0.1",
		user = "root",
		passwd = "rootpass",
		database = "bankSystem"
		)
	return db
	
def balanceCheck(clientId, amount, accountType):
	db = init()
	transactioncursor = db.cursor(buffered = True)
	balance_query = """SELECT balance from Account WHERE client_id = %s AND account_type = %s"""
	balanceQValues = (clientId, accountType)
	transactioncursor.execute(balance_query, balanceQValues)
	balance = transactioncursor.fetchone()
	clientBalance = int(balance[0])
	transactioncursor.close()
	db.close()
	if clientBalance - amount > 0:
		return True
	else:
		return False

def withdraw(clientId, amount, accountType):
	db = init()
	transactioncursor = db.cursor(buffered = True)
	withdraw_query = """UPDATE Account SET balance = balance - %s WHERE client_id = %s AND account_type = %s"""
	withdrawValues = (amount, clientId, accountType)

	transactioncursor.execute(withdraw_query, withdrawValues)
	db.commit()
	transactioncursor.close()
	db.close()
	


def deposit(targetId, amount, accountType):
	db = init()
	transactioncursor = db.cursor(buffered = True)
	deposit_query = """UPDATE Account SET balance = balance + %s WHERE client_id = %s AND account_type = %s"""
	depositValues = (amount, targetId, accountType)

	transactioncursor.execute(deposit_query, depositValues)
	db.commit()
	transactioncursor.close()
	db.close()

def createTransaction(clientId, targetId, clientAccountType, targetAccountType, amount):
	if balanceCheck(clientId, amount, clientAccountType):
		try:
			withdraw(clientId, amount, clientAccountType)
			deposit(targetId, amount, targetAccountType)
			date = datetime.today().strftime('%Y-%m-%d')
			newTransaction(clientId, targetId, amount, 'withdraw', date, clientAccountType)
			newTransaction(targetId, clientId, amount, 'deposit', date, targetAccountType)
		except:
			return False
		else:
			return True
	else:
		return False

def getTransactHistory(clientId, accountType):
	db = init()
	transactHistory = []
	transaction = []
	transactioncursor = db.cursor(buffered = True)
	transaction_query = """SELECT amount, transact_type, transact_date, target_num FROM Transaction WHERE client_id = %s AND account_type = %s"""
	transactionInfo = (clientId, accountType)
	try:
		transactioncursor.execute(transaction_query, transactionInfo)
		for x in transactioncursor:
			transaction = []
			amount, transactType, transactDate, targetId = x
			transaction.append(amount)
			transaction.append(transactType)
			transaction.append(transactDate.strftime('%d/%m/%Y'))
			transaction.append(targetId)
			transactHistory.append(transaction)
	except:
		print("Invalid Data")
	else:
		return transactHistory

db = init()
db.close()

