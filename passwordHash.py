import bcrypt


def hashPass(passToHash):
	hashedPass = bcrypt.hashpw(passToHash, bcrypt.gensalt())
	return hashedPass

def checkPass(password, hashedPass):
	return bcrypt.checkpw(password, hashedPass)
	

