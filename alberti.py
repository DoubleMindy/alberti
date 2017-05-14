__author__ = 'Timokhin Ilya'
__license__ = 'SCS-152, HSE MIEM 2017'

import random
import math


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

def Alberti_first(alpha, key, text, decode = True):
    key = rotation(key, abs(alpha.index(text[0]) - key.index(text[0])))
    if decode == False:
        return cicle_rotation(text, alpha, key, decode = False)
    else:
        return cicle_rotation(text, alpha, key)

def Alberti_second(alpha, key, text, decode = True):
    if decode == False:
        key = rotation(key, 32-key.index(text[0]))   
    else:
        key = rotation(key, 10)
        while(alpha.index(alpha[key.index(alpha[key.index(OT[0])])]) != 0):
                   key = rotation(key, 1)
    if decode == False:
        return cicle_rotation(text, alpha, key, decode = False)
    else:
        return cicle_rotation(text, alpha, key)
     
def Alberti_third(alpha, key, text, ind, decode = True):
    key = rotation(key, abs(key.index(ind)) - alpha.index(alpha[0]))
    if decode == False:
        return cicle_rotation(text, alpha, key, decode = False)
    else:
        return cicle_rotation(text, alpha, key)

def Alberti_fourth(alpha, key, text, decode = True, period = 0):
    cipher = []
    if decode == True:
        for letter in text:
            if letter.isupper() == True:
                key = rotate_to_A(alpha, key, letter)
            else:
                cipher.append(alpha[key.index(letter.upper())])

    if decode == False:
        random_state_letters = []
        j = 0
        for i in range(0, len(text)//period+1):
            random_state_letters.append(alpha[random.randint(0, len(alpha)-1)])
        for letter in range(0, 1+len(text)+ len(text)//(period)):
            if letter%(period+1) == 0:
                cipher.append(random_state_letters[j])
                key = rotate_to_A(alpha, key, random_state_letters[j])
                j += 1
            else:
                cipher.append(key[alpha.index(text[letter-j])].lower())
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
    
            
    

if __name__ == '__main__':
    
    alf = ['А','Б','В','Г','Д','Е','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ю','Я']
    k = input('Enter key (split it with spaces): ').split(' ')
    checker = [i for i in k if i in alf]
    
    if ((len(alf) == len(k)) and (len(set(k)) == len(k)) and (len(checker) == len(k))):
        mode = input('Input disk mode (1, 2, 3, 4, 5): ')
        decode = input('Do you decode text? (print \'Д\' if so, and \'Н\' if not): ')
        if decode == 'Д':
            if mode == '1':
                OT = list(input('Enter text: ').upper())
                print(Alberti_first(alf, k, OT))
            if mode == '2':
                OT = list(input('Enter text: ').upper())
                print(Alberti_second(alf, k, OT))
            if mode == '3':
                indicator = input('Enter indicator: ').upper()
                OT = list(input('Enter text: ').upper())
                print(Alberti_third(alf, k, OT, indicator))
            if mode == '4':
                OT = list(input('Enter text: '))
                print(Alberti_fourth(alf, k, OT))
            if mode == '5':
                pw = input('Enter password: ').upper()
                OT = list(input('Enter text: ').upper())
                decode = True
                print(Alberti_fifth(alf, k, OT, pw, decode)) 
        if decode == 'Н':
            if mode == '1':
                OT = list(input('Enter text: ').upper())
                print(Alberti_first(alf, k, OT, decode = False))
            if mode == '2':
                OT = list(input('Enter text: ').upper())    
                print(Alberti_second(alf, k, OT, decode = False))
            if mode == '3':
                indicator = input('Enter indicator: ').upper()
                OT = list(input('Enter text: ').upper())
                print(Alberti_third(alf, k, OT, indicator, decode = False))
            if mode == '4':
                p = int(input('Period: '))
                OT = list(input('Enter text (without spaces): ').upper())
                decode = False
                print(Alberti_fourth(alf, k, OT, decode, p))
            if mode == '5':
                pw = input('Enter password: ').upper()
                OT = list(input('Enter text: ').upper())
                print(Alberti_fifth(alf, k, OT, pw, decode = False))
    else:
        print('Try another key! ')
