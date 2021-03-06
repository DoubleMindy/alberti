__author__ = 'Timokhin Ilya'
__license__ = 'SCS-152, HSE MIEM 2017'
import sys
import math
import random
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit,
                             QApplication, QCheckBox, QComboBox, QTextEdit)
from PyQt5.QtGui import QFont

def  rotation(a, pos):
    return a[-pos:] + a[:-pos]

def get_random_key(alpha):
    k = []
    alpha_copy = alpha
    for letters in range(0, len(alpha_copy)):
        rand_letter = alpha_copy[random.randint(0, len(alpha_copy)-1)]
        k.append(rand_letter)
        alpha_copy.remove(rand_letter)
    return k    
        

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
    while(alpha[key.index(text[0])] != text[0]):
                key = rotation(key, 1)
    if decode == False:
        return cicle_rotation(text, alpha, key, decode = False)
    else:
        return cicle_rotation(text, alpha, key)
    
def Alberti_second(alpha, key, text, decode):
    if decode == False:
        key = rotation(key, abs(len(alpha)-key.index(text[0])))   
    else:
        key = rotation(key, math.ceil(len(alpha)/2)) 
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
                cipher.append(random_state_letters[x].upper())
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
        self.combo.activated[str].connect(self.onActive)

        self.tip_for_key = QLabel('What is key?', self)
        self.tip_for_key.move(30, 55)
        self.tip_for_key.setToolTip("Сюда (через пробел) вводится содержимое внутреннего <b>диска Альберти</b>")
        self.tip_for_key.setStyleSheet("QLabel {color:blue}")

        self.rand = QPushButton('Generate key', self)
        self.rand.setGeometry(320, 50, 100, 20)                  

        self.rand.clicked.connect(self.genKey)
        
        self.cb = QCheckBox('Decode text', self)
        self.cb.move(30, 250)

        lblk = QLabel('Enter key: ', self)
        lblk.move(30, 10)

        default_info =  "<b> Первая буква открытого текста совмещается с собой на внешнем диске.<br> \
Далее происходит поворот внутреннего диска на 1 букву по часовой стрелке, <br> ищется соответствие второй буквы \
на внешнем диске,  заменяется на букву <br> с внутреннего диска и т.д.</b>"
        self.bigtip = QLabel(default_info, self)
        self.bigtip.move(10, 520)
        self.bigtip.setFont(QFont('Calibri', 10))

        self.k = QLineEdit(self)
        self.k.setGeometry(30, 30, 400, 22)

        lbltx = QLabel('Enter text (Open Text or Cipher Text): ', self)
        lbltx.move(30, 70)
        
        self.txt = QLineEdit(self)
        self.txt.setGeometry(30, 90, 400, 42)

        lblres = QLabel('Result is: ', self)
        lblres.move(30, 150)

        lblinfo = QLabel('ИНФОРМАЦИЯ О ДАННОМ РЕЖИМЕ: ', self)
        lblinfo.move(100, 500)
        lblinfo.setFont(QFont('Times New Roman', 12))
        
        self.res = QLineEdit(self)
        self.res.setGeometry(30, 170, 400, 52)

        self.btn = QPushButton('Code it!', self)
        self.btn.setGeometry(30, 295, 250, 42)
        self.btn.setStyleSheet("QPushButton { background-color: red }"
                      "QPushButton:pressed { background-color: blue }" )
        lbltx = QLabel('Enter indicator (for 3-rd mode): ', self)
        lbltx.move(30, 340)

        self.indic = QLineEdit(self)
        self.indic.setGeometry(30, 360, 30, 20)

        lblper = QLabel('Enter period (for 4-th mode): ', self)
        lblper.move(30, 380)

        self.p = QLineEdit(self)
        self.p.setGeometry(30, 400, 30, 20)
        
        lblpas = QLabel('Enter password (for 5-th mode): ', self)
        lblpas.move(30, 420)

        self.pas = QLineEdit(self)
        self.pas.setGeometry(30, 440, 150, 20)

        self.lang = QComboBox(self)
        self.lang.addItems(["Русский", "English"])
        self.lang.setGeometry(100, 270, 90, 22)
        
        self.btn.clicked.connect(self.showDialog)
        
        self.setGeometry(300, 300, 500, 600)
        self.setWindowTitle('Alberti Cipher')
        self.show()

    def onActive(self):
        if self.combo.currentText() == "Mode 1":
            info = "<b> Первая буква открытого текста совмещается с собой на внешнем диске.<br> \
Далее происходит поворот внутреннего диска на 1 букву по часовой стрелке, <br> ищется соответствие второй буквы \
на внешнем диске,  заменяется на  букву <br> с внутреннего диска и т.д.</b>"
        if self.combo.currentText() == "Mode 2":
            info = " <b>Первая буква сообщения на внутреннем диске устанавливается напротив <br> буквы А на внешнем. \
Далее её соответствие ищется на внешнем диске, затем <br> после каждого зашифрования 1 символа ключ \
поворачивается <br> на 1 символ \n по часовой стрелке и т.д.</b>"
        if self.combo.currentText() == "Mode 3":
            info = "<b>Выбирается индикатор, устанавливаемый напротив первой буквы алфавита. <br> После \
зашифрования каждой буквы внутренний диск поворачивается <br> на 1 символ по часовой стрелке</b>"
        if self.combo.currentText() == "Mode 4":
            info = "<b>Выбирается произвольная буква на внутреннем диске, она устанавливается <br> \
напротив буквы А на внешнем диске. Эта буква записывается как заглавная. <br>Следующие <i>p</i> букв (<i>p</i> - период) \
шифруются без движения внутреннего диска. <br> Это действие повторяется, каждый раз устанавливается новая случайная буква.</b>"
        if self.combo.currentText() == "Mode 5":
            info = "<b>Выбирается пароль, первая буква которого совмещается с буквой А внешнего <br> диска. \
           Далее производится шифрование первой буквы  открытого <br> текста, затем с буквой А совмещается \
           вторая буква  пароля и шифруется вторая <br> буква открытого текста и т.д.</b>"
        self.bigtip.setText(info)
        self.bigtip.adjustSize()
            
    def genKey(self):
        if self.lang.currentText() == "Русский":
            alf = ['А','Б','В','Г','Д','Е','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ю','Я']
        else:
            alf = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']        
        self.k.setText(' '.join(get_random_key(alf)))
        
    def showDialog(self):

        if self.lang.currentText() == "Русский":
            alf = ['А','Б','В','Г','Д','Е','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ю','Я']
        else:
            alf = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            
        j = self.k.text().upper().split(' ')
        checker = [i for i in self.k.text().upper().split(' ') if i in alf]
        if ((len(alf) == len(j)) and (len(set(j)) == len(j)) and (len(self.txt.text()) > 0)):
            if self.cb.isChecked() == True:
                
                if self.combo.currentText() == "Mode 1": 
                    self.res.setText(str(Alberti_first(alf, j, self.txt.text().upper(), decode = True)))
                    
                if self.combo.currentText() == "Mode 2": 
                    self.res.setText(str(Alberti_second(alf, j, self.txt.text().upper(), decode = True)))
                    
                if self.combo.currentText() == "Mode 3":
                    try:
                        self.res.setText(str(Alberti_third(alf, j, self.txt.text().upper(), self.indic.text().upper(), decode = True)))
                    except (ValueError, AttributeError):
                        self.res.setText('Invalid indicator!')   
                    
                if self.combo.currentText() == "Mode 4":
                    decode = True
                    s = self.k.text().split(' ')
                    link = 0
                    self.res.setText(str(Alberti_fourth(alf, s, self.txt.text(), decode, link)))
                    
                if self.combo.currentText() == "Mode 5":
                    try:
                        self.res.setText(str(Alberti_fifth(alf, j, self.txt.text().upper(), self.pas.text().upper(), decode = True)))
                    except:
                        self.res.setText('Invalid password!)')                                        
            else:
                
                if self.combo.currentText() == "Mode 1": 
                    self.res.setText(str(Alberti_first(alf, j, self.txt.text().upper(), decode = False)))
                    
                if self.combo.currentText() == "Mode 2": 
                    self.res.setText(str(Alberti_second(alf, j, self.txt.text().upper(), decode = False)))
                    
                if self.combo.currentText() == "Mode 3":
                    try:
                        self.res.setText(str(Alberti_third(alf, j, self.txt.text().upper(), self.indic.text().upper(), decode = False)))
                    except (ValueError, AttributeError):
                        self.res.setText('Invalid indicator!')
                        
                    
                if self.combo.currentText() == "Mode 4":
                    decode = False
                    try:
                        self.res.setText(str(Alberti_fourth(alf, j, self.txt.text().upper(), decode, int(self.p.text()))))
                    except (ValueError, AttributeError):
                        self.res.setText('Invalid period!')
                    
                if self.combo.currentText() == "Mode 5":
                    try:
                        self.res.setText(str(Alberti_fifth(alf, j, self.txt.text().upper(), self.pas.text().upper(), decode = False)))
                    except:
                        self.res.setText('Invalid password!)')
        else:
            self.res.setText('Invalid key or text!')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Disk()
    sys.exit(app.exec_())
