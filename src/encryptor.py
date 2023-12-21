import gnupg

def encrypt(content,key):
    GPG = gnupg.GPG()
    final = GPG.encrypt(content,key)
    return final

def decrypt(content,key):
    GPG = gnupg.GPG()
    final = GPG.decrypt(content,key)
    return final
