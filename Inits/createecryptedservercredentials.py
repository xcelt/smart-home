'''Helper module to generate, encrypt and save hub credentials'''
'''NOTE: First run createcryptokeys.py to generate keys'''

import utils

server_user = "user1"
server_pass = "user1password"

credentials = {'user':server_user, 'pass':server_pass}

# public_key, private_key = utils.load_keys("../Secrets/pub.key","../Secrets/prv.key")
fer_key = utils.load_fernet_key("../Secrets/dev_enc.key")


if utils.encrypt_and_save_fernet(credentials, fer_key, "../Secrets/creds.bin"):
    print("Credentials created and saved to 'Secrets/creds.bin'")