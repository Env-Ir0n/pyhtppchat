import gnupg
import json

def generate_key(email, passphrase=None):
    # Initialize the GnuPG object
    gpg = gnupg.GPG()

    # Generate a key pair
    input_data = gpg.gen_key_input(
        name_email=email,
        passphrase=passphrase
    )

    key = gpg.gen_key(input_data)

    # Export the public key
    public_key = gpg.export_keys(key.fingerprint)
    
    # Export the private key
    private_key = gpg.export_keys(key.fingerprint, secret=True, passphrase=passphrase)

    with open('private.asc','w') as f:
        f.write(private_key)
    
    with open('public.asc','w') as f:
        f.write(public_key)
    
    global servername
    servername = input('Name for server (nickname only, not address): ')
    
    openserver = input('Set server as open?[Y/n]')
    
    if openserver == 'Y':
        global openserve
        openserve = True
        global passwrd
        passwrd = None
    else:
        global passwrd
        openserve = False
        global passwrd
        passwrd = input('Server password: ')

with open('server.json','w') as f:
    e = open('private.asc')
    data = {"basic":{"servername":servername}, "auth":{"keys":{"ADMIN":e.read()}, "open?":openserve, "pass":passwrd }}
    e.close()
    f.write(json.dumps(data))

email = input('Email address (For encryption purposes*)')
try:
    password = input('Encryption passphrase | ^C to skip')
except KeyboardInterrupt:
    print('No passphrase')

print('Run "runhttpchat" to start the server')