import hashlib


username1, password1 = "MickeyMouse", hashlib.sha512("mousepassword".encode()).hexdigest()
username2, password2 = "John", hashlib.sha512("johnpas8712tsword".encode()).hexdigest()
username3, password3 = "Stimpy762", hashlib.sha512("stimpypas08162sword".encode()).hexdigest()
username4, password4 = "Mary_Lamb", hashlib.sha512("marypas3345(sword".encode()).hexdigest()

print(password4)



