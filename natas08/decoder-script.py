import base64

print('enter the encoded secret:')
secret = input()
secret = bytes.fromhex(secret)
secret = secret[::-1]
secret = base64.decodebytes(secret)

print("Decoded secret:", secret.decode('utf-8', errors='replace'))
