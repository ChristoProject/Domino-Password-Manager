# Librerie richieste
import random
import pymongo
from pymongo import ReturnDocument
import string
from simplecrypt import encrypt, decrypt
import os
import certifi
from time import sleep

ca = certifi.where()

# Connessione a MongoDB
url = ''
client = pymongo.MongoClient(url, tlsCAFile=ca)
db = client[''] ##Nome del DB
collection = db[''] ##Nome della collection


menu = {
    '1': 'Genera nuove credenziali',
    '2': 'Inserisci nuove credenziali',
    '3': 'Aggiorna le credenziali',
    '4': 'Cerca le credenziali',
    '5': 'Elimina credenziali',
    '6': 'Chiudi'
}


def clear_screen():
    os.system('clear')


def print_menu():
    for key in menu.keys():
        print(key, ' - ', menu[key])


# Generatore di Password
def psw_gen():
    letter_low = string.ascii_lowercase
    letter_cap = string.ascii_uppercase
    numbers = string.digits
    punctuation = string.punctuation
    characters = str(letter_cap + letter_low + numbers + punctuation)
    new_psw = ''

    for c in range(24):
        new_psw += random.choice(characters)

    return new_psw


# Login
def login():
    secret_key = int() ##Inserisci il codice di sicurezza per fare il login
    inserted_key = int(input('Codice di sicurezza: '))
    if inserted_key == secret_key:
        print('Accesso Consentito')
    else:
        print('Codice di Sicurezza errato. Accesso Negato')
        login()


# Security
class Safe:
    def encrypt(self, p_txt):
        password = input('Encryption Key: ')
        c_txt = encrypt(password, p_txt)
        return c_txt

    def decrypt(self, c_txt):
        password = input('Decryption Key: ')
        p_txt = decrypt(password, c_txt)
        return p_txt


safety = Safe()


# Generatore di Credenziali
def credential_gen():
    add_username = input('Username: ')
    add_platform = input('Platform: ')

    psw_gen()
    psw = psw_gen()

    e_psw = safety.encrypt(psw)

    input_credentials = {
        'Username': add_username,
        'Platform': add_platform.lower(),
        'Password': e_psw
    }
    print('---------------')
    print('La tua password è: ', psw)
    print('---------------')

    save = input('Salvare le credenziali [S/N]: ')
    if save == 'S':
        collection.insert_one(input_credentials)
        print('---------------')
        print('Le tue credenziali sono state savate')
        print('---------------')
    else:
        clear_screen()


# Aggiunta manuale delle credenziali a DB
def credential_manual_add():
    add_username = input('Username: ')
    add_platform = input('Platform: ')
    add_psw = input('Password: ')

    e_psw = safety.encrypt(add_psw)

    input_manual = {
        'Username': add_username,
        'Platform': add_platform.lower(),
        'Password': e_psw
    }
    save = input('Salvare le credenziali [S/N]: ')
    if save == 'S':
        collection.insert_one(input_manual)
        print('---------------')
        print('Le tue credenziali sono state savate')
        print('---------------')
        sleep(3)
        clear_screen()
    else:
        clear_screen()
        credential_manual_add()


# Cercare le credenziali
def credential_finder():
    print('Per quale piattaforma vuoi trovare le credenziali ?')
    find_platform = input('Platform: ').lower()
    try:
        result = collection.find({'Platform': find_platform})
        for record in result:
            e_pass = (record['Password'])
            e_username = (record['Username'])
            d_result = safety.decrypt(e_pass)
            d_record = str(d_result)
            print('---------------')
            print('Username: ' + e_username)
            print('Password: ' + d_record[2:-1])
            print('---------------')
            sleep(3)
        prox = input('Vuoi cercare altro? [S/N]: ')
        if prox == 'S':
            clear_screen()
            credential_finder()
        else:
            clear_screen()
    except:
        print('Non ho trovato credenziali per questa piattaforma')
        credential_finder()


# Aggiornare le credenziali
def credential_update():
    print('Quale vuoi aggiornare ?')
    record_filter = input().lower()
    print('Inserisci la nuova password')
    record_update = input()
    check = input('Sei sicuro di voler aggiornare la password? [S/N]: ')
    if check == 'S':
        e_record_update = safety.encrypt(record_update)
        collection.find_one_and_update({'Platform': record_filter},
                                       {'$set': {'Password': e_record_update}},
                                       return_document=ReturnDocument.AFTER)
        print('---------------')
        print('Le credenziali sono state aggiornate')
        print('---------------')
        sleep(3)
        clear_screen()
    else:
        credential_update()


# Eliminare le credenziali
def credential_remove():
    print('Quale piattaforma vuoi eliminare ?')
    record_filter = input().lower()
    check = input('Sicuro di voler eliminare le credenziali? [S/N]')
    if check == 'S':
        collection.delete_one({'Platform': record_filter})
        print('---------------')
        print('Credenziali eliminate')
        print('---------------')
        sleep(3)
        clear_screen()
    else:
        credential_remove()


if __name__ == '__main__':

    login()

    while True:

        print_menu()
        print('---------------')
        option = input("Scegli un'opzione: ")
        print('---------------')

        if option == '1':
            credential_gen()
        elif option == '2':
            credential_manual_add()
        elif option == '3':
            credential_update()
        elif option == '4':
            credential_finder()
        elif option == '5':
            credential_remove()
        elif option == '6':
            break
        else:
            print('Inserisci una opzione valida')
