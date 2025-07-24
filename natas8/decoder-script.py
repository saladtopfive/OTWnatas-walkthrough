import base64

print('enter the encoded secret:')
secret = input()
secret = bytes.fromhex(secret)
print(secret)
secret = secret[::-1]
secret = base64.decodebytes(secret)

print("decoded secret: ", secret ,"(b' YOUR DECODED SECRET ')")

