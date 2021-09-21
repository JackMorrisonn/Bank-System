# Bank-System

### Database ERD

<img src="https://github.com/JackMorrisonn/Bank-System/blob/main/BankSystemDatabaseDesign.png" alt="Database ERD" width="800"/>

---

### About the project

This project was created to expand my understanding of MySQL as well as how to utilise MySQL and databases using Python. The GUI for this project was created using Tkinter which despite its simplicity is very versitile for creating simple desktop applications. This project interacts with a MySQL database that holds all the data and is accessed using SQL statements through cursors in Python.

Each Client has an account which stores their client id, their first and last names as well as their address, phone number and a password. This password is hashed and salted using the bcrypt library for Python, and this hashed password is what is stored in the database. It is able to be decrypted using the function `
checkPass() ` in the bcrypt library. This way even if someone had access to the database they couldn't access user accounts. Each client, when created, is automatically given a credit and savings account, which stores their client id and the account id, as well as the type of account (either 'savings' or credit') as well as its current balance. Each account then has a card associated with it, with a pin and expire date.

Each account also has a history of transactions. Two transaction records are created automatically whenever a transaction occurs, one for the account that is being withdrawn from and one for the account that is being deposited into.

---

### Functionality

When the program is launched, the user is greeted with a login screen which will ask for an ID and a password. Currently, there exists an admin account and two user test accounts.

| User ID    | Password   | Type       |
|------------|:----------:|-----------:|
| 4000       | root       | Admin      |
| 4001       | pass1      | User       |
| 4002       | pass2      | User       |

### Login Page

<img src="https://github.com/JackMorrisonn/Bank-System/blob/main/sampleimages/LoginPage.PNG" alt="Login Page" width="800"/>

When the program is launched, this is the screen that will appear every time. The user is able to enter a user ID as well as a password, which are listed above.

### Home Page

<img src="https://github.com/JackMorrisonn/Bank-System/blob/main/sampleimages/UserHomepage.PNG" alt="Home Page" width="800"/>

Once the user has logged in, if they are a normal user they are greeted with a home page. This home page lists the 5 most recent transactions from the account as well as a button that allows people to pay into other accounts.

### Admin Page

<img src="https://github.com/JackMorrisonn/Bank-System/blob/main/sampleimages/AdminPortal.PNG" alt="Admin Page" width="800"/>

If the user enters the admin account ID and password they are instead directed to this page which allows the admin to add new users to the database.

### Pay Page

<img src="https://github.com/JackMorrisonn/Bank-System/blob/main/sampleimages/PayPage.PNG" alt="Pay Page" width="800"/>

When the "Pay Someone" button is pressed, it will take the user to the Pay Someone page. This allows the user to pay someone from a selected account into another account of any user by entering their ID and selecting which account to deposit into. Pressing the pay button will open up another small window either indicating that the payment was a success or a failure.
