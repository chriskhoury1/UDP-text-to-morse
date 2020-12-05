from socket import *
import os
import socket

class UDPclient:
    def __init__(self, port=13000):  # constructor of class UDPclient, with parameter port which defaults to 13000
        self.port = port

    def send(self, serverName='Chris', msg='message.txt', serverPort=16000):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating the socket at the sending client side
        clientSocket.bind(('', self.port))  # binding it to the address of client
        file1 = open(msg, "r")  # opening the txt file with read privileges
        msg = file1.readlines()[0]  # extracting the words from the txt file using .readlines() which returns a list
        # containing each line from the txt file, but we just need the first one
        msg += ' (from '+str(self.port)+')'  # add a simple indicator at the end to know which client sent the message
        morse_msg = ''
        morse = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                 'Y': '-.--', 'Z': '--..', 'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
                 'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.',
                 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-', 'v': '...-',
                 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..', '1': '.----', '2': '..---', '3': '...--', '4':
                     '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
                 ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'}
        # dictionary for morse values to alphanumeric
        for i in msg:  # converting to morse by iterating over the sentence
            if i == ' ':
                morse_msg += '   '  # if there is a space, we add three spaces signifying the difference between words
            if i not in morse:  # avoids errors so that the program does not stop here
                continue
            else:
                morse_msg += morse[i]  # add the letter to the morse message
                morse_msg += " "  # adding a space between each letter

        clientSocket.sendto(morse_msg.encode(), (serverName, serverPort)) # use the sendto function (only in UDP) to
        # send the encoded morse msg (using .encode()) and the address of the server
        clientSocket.close()  # closing the socket we opened
        file1.close()  # closing the txt file we opened

    def receive(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating the socket at the receiving client side
        clientSocket.bind(('', self.port))  # binding the socket to the address of the receiving client
        Morse1 = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
                  '....': 'h',
                  '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p',
                  '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
                  '-.--': 'y', '--..': 'z', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
                  '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0', '--..--': ', ',
                  '.-.-.-': '.', '..--..': '?', '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')'}

        morse_msg, serverAddress = clientSocket.recvfrom(2048)  # receive the message from the server using recvfrom
        # only in UDP) and store the address of the server in serverAddress
        recoveredMsg = ''
        morse_msg = morse_msg.decode()  # decoding the message which was sent encoded for transmission purposes
        sentence = morse_msg.split('   ')  # use the split function to split where we have three spaces ie the difference between words
        for word in sentence:  # iterate over the words
            for letter in word.split(' '):  # iterate over the letters in the words using the split function again to seperate the letters
                if letter != '':  # avoiding empty chars
                    recoveredMsg += Morse1[letter]  #look for the corresponding morse representation in the dictionary and replace it with the letter
            recoveredMsg += ' '  # add a space after each set of letters making a word to get the original sentence

        for i in range(1, 100): # here we check if there is another file already created
            if not os.path.exists('./recoveredFile.txt'): # if there is no file, we create one
                file2 = open(r"recoveredFile.txt", "w")  # we use the open function with 'w' or write privileges
                file2.write(recoveredMsg)  # write the converted message on the new txt file
                break
            elif not os.path.exists('./recoveredFile('+str(i)+').txt'): # and we keep on incrementing if the last number of file was taken
                file2 = open('recoveredFile('+str(i)+').txt', "w")
                file2.write(recoveredMsg)
                break  # break so that the full loop doesn't occur (so that we don't create 100 files)
        clientSocket.close()  # close the opened socket
        file2.close()  # close the opened file we used to write the output on
