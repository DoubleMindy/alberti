__author__ = 'Timokhin Ilya'
__license__ = 'SCS-152, HSE MIEM 2017'
import sys
import math
import random
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit,
    QInputDialog, QApplication, QCheckBox, QComboBox)

def  rotation(a, pos):
    return a[-pos:] + a[:-pos]

def rotate_to_A(alpha, key, x):
    while(alpha.index(alpha[key.index(x)]) != 0):
                   key = rotation(key, 1)
    return key               

def cicle_rotation(text, alpha, new_key, decode = True):
    cipher = []
    for letter in text:
        if letter not in new_key:
            cipher.append(letter)
        else:
            if decode == False:
                cipher.append(new_key[alpha.index(letter)])
                new_key = rotation(new_key, 1)
            else:
                cipher.append(alpha[new_key.index(letter)])
                new_key = rotation(new_key, 1)    
    return ''.join(cipher)

def Alberti_first(alpha, key, text, decode):
    key = rotation(key, abs(alpha.index(text[0]) - key.index(text[0])))
    if decode == False:
        return cicle_rotation(text, alpha, key, decode = False)
    else:
        return cicle_rotation(text, alpha, key)
    
def Alberti_second(alpha, key, text, decode):
    if decode == False:
        key = rotation(key, len(alpha)-key.index(text[0]))   
    else:
        key = rotation(key, 10)
        while(alpha.index(alpha[key.index(alpha[key.index(text[0])])]) != 0):
                   key = rotation(key, 1)
    if decode == False:
        return cicle_rotation(text, alpha, key, decode = False)
    else:
        return cicle_rotation(text, alpha, key)

def Alberti_third(alpha, key, text, ind, decode):
    key = rotation(key, abs(key.index(ind)) - alpha.index(alpha[0]))
    if decode == False:
        return cicle_rotation(text, alpha, key, decode = False)
    else:
        return cicle_rotation(text, alpha, key)

def Alberti_fourth(alpha, key, text, decode, period):
    cipher = []
    if decode == True:
        for letter in text:
            if letter.isupper() == True:
                key = rotate_to_A(alpha, key, letter)
            else:
                cipher.append(alpha[key.index(letter.upper())])

    if decode == False:
        random_state_letters = []
        x = 0
        for i in range(0, len(text)//period+1):
            random_state_letters.append(alpha[random.randint(0, len(alpha)-1)])
        for letter in range(0, 1+len(text)+ len(text)//(period)):
            if letter%(period+1) == 0:
                cipher.append(random_state_letters[x])
                key = rotate_to_A(alpha, key, random_state_letters[x])
                x += 1
            else:
                cipher.append(key[alpha.index(text[letter-x])].lower())
    return ''.join(cipher)

def Alberti_fifth(alpha, key, text, password, decode = True):
    cipher = []
    spaces = [x for x in range(0, len(text)-1) if text[x] not in key]
    no_spaces = [x for x in text if x in key]
    password = list((password*math.ceil(len(no_spaces)/len(password))))
    
    for i in range(0, len(password)-len(no_spaces)):
        password.pop()
        
    for i in spaces:
        password.insert(i, text[i])
        
    for letter in range(0, len(text)):
        if password[letter] not in key:
            cipher.append(password[letter])
        else:    
            key = rotate_to_A(alpha, key, password[letter])
            if decode == False:  
                cipher.append(key[alpha.index(text[letter])])
            else:
                cipher.append(alpha[key.index(text[letter])])
    return ''.join(cipher)

class Disk(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.combo = QComboBox(self)
        self.combo.addItems(["Mode 1", "Mode 2",
                        "Mode 3", "Mode 4", "Mode 5"])
        self.combo.move(30, 270)
        
        self.cb = QCheckBox('Decode text', self)
        self.cb.move(30, 250)

        lblk = QLabel('Enter key: ', self)
        lblk.move(30, 10)

        self.k = QLineEdit(self)
        self.k.setGeometry(30, 30, 400, 22)

        lbltx = QLabel('Enter text (Open Text or Cipher Text): ', self)
        lbltx.move(30, 70)
        
        self.txt = QLineEdit(self)
        self.txt.setGeometry(30, 90, 400, 42)

        lblres = QLabel('Result is: ', self)
        lblres.move(30, 150)
        
        self.res = QLineEdit(self)
        self.res.setGeometry(30, 170, 400, 52)

        self.btn = QPushButton('DO', self)
        self.btn.move(30, 300)

        lbltx = QLabel('Enter indicator (for 3-rd mode): ', self)
        lbltx.move(30, 340)

        self.indic = QLineEdit(self)
        self.indic.setGeometry(30, 360, 30, 20)

        lblper = QLabel('Enter period (for 4-th mode): ', self)
        lblper.move(30, 380)

        self.p = QLineEdit(self)
        self.p.setGeometry(30, 400, 30, 20)
        
        lblpas = QLabel('Enter period (for 5-th mode): ', self)
        lblpas.move(30, 420)

        self.pas = QLineEdit(self)
        self.pas.setGeometry(30, 440, 150, 20)
        
        self.btn.clicked.connect(self.showDialog)
        
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Alberti cipher')
        self.show()


    def showDialog(self):
        alf = ['А','Б','В','Г','Д','Е','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ю','Я']
        j = self.k.text().upper().split(' ')
        checker = [i for i in self.k.text().upper().split(' ') if i in alf]
        if ((len(alf) == len(j)) and (len(set(j)) == len(j)) and (len(checker) == len(j)) and (len(self.txt.text()) > 0)):
            if self.cb.isChecked() == True:
                
                if self.combo.currentText() == "Mode 1": 
                    self.res.setText(str(Alberti_first(alf, j, self.txt.text().upper(), decode = True)))
                    
                if self.combo.currentText() == "Mode 2": 
                    self.res.setText(str(Alberti_second(alf, j, self.txt.text().upper(), decode = True)))
                    
                if self.combo.currentText() == "Mode 3":                   
                    self.res.setText(str(Alberti_third(alf, j, self.txt.text().upper(), self.indic.text().upper(), decode = True)))
                    
                if self.combo.currentText() == "Mode 4":
                    decode = True
                    s = self.k.text().split(' ')
                    self.res.setText(str(Alberti_fourth(alf, j, self.txt.text(), decode, self.p.text())))
                    
                if self.combo.currentText() == "Mode 5":
                    self.res.setText(str(Alberti_fifth(alf, j, self.txt.text().upper(), self.pas.text().upper(), decode = True)))
                    
            else:
                
                if self.combo.currentText() == "Mode 1": 
                    self.res.setText(str(Alberti_first(alf, j, self.txt.text().upper(), decode = False)))
                    
                if self.combo.currentText() == "Mode 2": 
                    self.res.setText(str(Alberti_second(alf, j, self.txt.text().upper(), decode = False)))
                    
                if self.combo.currentText() == "Mode 3": 
                    self.res.setText(str(Alberti_third(alf, j, self.txt.text().upper(), self.indic.text().upper(), decode = False)))
                    
                if self.combo.currentText() == "Mode 4":
                    decode = False
                    s = self.k.text().split(' ')
                    self.res.setText(str(Alberti_fourth(alf, j, self.txt.text(), decode, int(self.p.text()))))
                    
                if self.combo.currentText() == "Mode 5":
                    self.res.setText(str(Alberti_fifth(alf, j, self.txt.text().upper(), self.pas.text().upper(), decode = False)))
        else:
            self.res.setText('Invalid input!')    
        


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Disk()
    sys.exit(app.exec_())
