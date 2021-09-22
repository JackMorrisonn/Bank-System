import mysql.connector
from passwordHash import *
from datetime import datetime, date

def init():
	db = mysql.connector.connect(
		host = "127.0.0.1",
		user = "root",
		passwd = "rootpass",
		database = "bankSystem"
		)
	return db

db = init()

#Initial Setup of Tables from Design Diagram
def setup():
	mycursor.execute("CREATE TABLE Client (client_id int PRIMARY KEY AUTO_INCREMENT, f_name VARCHAR(50), l_name VARCHAR(50), ph_no int, client_add VARCHAR(50), password VARCHAR(50))")
	mycursor.execute("CREATE TABLE Account (account_num int PRIMARY KEY AUTO_INCREMENT, client_id int, FOREIGN KEY (client_id) REFERENCES Client(client_id), account_type VARCHAR(10), balance int)")
	mycursor.execute("CREATE TABLE Card(card_num int PRIMARY KEY, account_num int, FOREIGN KEY (account_num) REFERENCES Account(account_num), pin int, expire_date DATE)")
	mycursor.execute("CREATE TABLE Transaction(transact_num int PRIMARY KEY AUTO_INCREMENT, client_id int, FOREIGN KEY (client_id)  REFERENCES Client(client_id), target_num int, amount int, transact_type VARCHAR(50), transact_date DATE)")


####################################################

#Database Entering Functions

####################################################


def newClient(f_name, l_name, ph_no, client_add, password):
	db = init()
	mycursor = db.cursor(buffered = True)
	try:
		password = bytes(password, 'utf-8')
		hashedPass = hashPass(password)
		clientInsertQuery = """INSERT INTO Client (f_name, l_name, ph_no, client_add, password) VALUES (%s, %s, %s, %s, %s)"""
		clientDataToInsert = (f_name, l_name, ph_no, client_add, hashedPass)
		mycursor.execute(clientInsertQuery, clientDataToInsert)
		db.commit()
	except:
		print("There was an error inserting data")
	else:
		print("New Client Inserted")
		db.close()

def newAccount(client_id, account_type, balance):
	db = init()
	mycursor = db.cursor(buffered = True)
	try:
		accountInsertQuery = """INSERT INTO Account (client_id, account_type, balance) VALUES (%s, %s, %s)"""
		accountDataToInsert = (client_id, account_type, balance)
		mycursor.execute(accountInsertQuery, accountDataToInsert)
		db.commit()
	except:
		print("There was an error inserting data")
	else:
		print("New Account Inserted")
		db.close()

def newCard(card_num, account_num, pin, expire_date):
	db = init()
	mycursor = db.cursor(buffered = True)
	try:
		cardInsertQuery = """INSERT INTO Card (card_num, account_num, pin, expire_date) VALUES (%s, %s, %s, %s)"""
		cardDataToInsert = (card_num, account_num, pin, expire_date)
		mycursor.execute(cardInsertQuery, cardDataToInsert)
		db.commit()
	except:
		print("There was an error inserting data")
	else:
		print("New Card Inserted")
	db.close()

def newTransaction(client_id, target_num, amount, transact_type,transact_date, transact_account):
	db = init()
	mycursor = db.cursor(buffered = True)
	try:
		transactInsertQuery = """INSERT INTO Transaction (client_id, target_num, amount, transact_type, transact_date, account_type) VALUES (%s, %s, %s, %s, %s, %s)"""
		transactDataToInsert = (client_id, target_num, amount, transact_type, transact_date, transact_account)
		mycursor.execute(transactInsertQuery, transactDataToInsert)
		db.commit()
	except:
		print("There was an error inserting data")
	else:
		print("New Transaction Inserted")
	db.close()





mycursor = db.cursor(buffered = True)

today = date.today()
expireyear = datetime.today().year+2
expiredate = today.replace(year = expireyear)
formatExpire = expiredate.strftime('%Y-%m-%d')


mycursor.execute("SELECT * FROM Card")
for x in mycursor:
	print(x)

mycursor.close()
db.close()
