from flask import Flask,request,send_from_directory
import itertools
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def home():
    return send_from_directory('.', 'index.html')

@app.route("/decrypt")
@cross_origin()
def decrypt():
    plaintext = request.args.get('plaintext')
    ciphertext = request.args.get('ciphertext')
    print(plaintext)
    print(ciphertext)
    if not plaintext or not ciphertext:
        return "Incorrect params"
    for i in range(2,8):
        newArr = []
        # print(list(range(0,i)))
        iterations = list(itertools.permutations(list(range(0,i))))
        for j in iterations:
            newArr = columnarTransposition(plaintext,j,ciphertext)
            if newArr:
                return {'key': [x+1 for x in newArr]}
    return "Key not found!, only checking sets 2-7"
    
def columnarTransposition(msg, key, ciphertext):
    """
    Function to encrypt a message using columnar transposition using a specific key
    """
    msg = msg.replace(" ", "").lower()
    arr = []

    for letter in key:
        arr.append([letter])
    count = 0

    while len(msg) > 0:
        letter = msg[0]
        msg = msg[1:]
        arr[count].append(letter)

        count += 1
        if count >= len(key):
            count = 0

    arr.sort()
    cipher = ''

    for i in range(0, len(arr)):
        for j in range(1, len(arr[i])):
            cipher += arr[i][j]

    cipher = cipher.upper()
    ciphertext = ciphertext.upper()
    if cipher == ciphertext:
        return list(key)
    return False

if __name__ == "__main__":
    app.run(debug=True)