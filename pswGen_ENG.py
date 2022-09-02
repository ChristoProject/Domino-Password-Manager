# Required Packages
import random
import pymongo
from pymongo import ReturnDocument
import string
from simplecrypt import encrypt, decrypt
import os
import certifi
from time import sleep

ca = certifi.where()

# MongoDB Connect
url = ''
client = pymongo.MongoClient(url, tlsCAFile=ca)
db = client[''] ##Insert the db name
collection = db[''] ##Insert the collection name


menu = {
    '1': 'Generate new credentials',
    '2': 'Credential manual add',
    '3': 'Credentials update',
    '4': 'Credentials finder',
    '5': 'Credentials remove',
    '6': 'Close'
}


def clear_screen():
    os.system('clear')


def print_menu():
    for key in menu.keys():
        print(key, ' - ', menu[key])


# Password generator
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
    secret_key = int()  ##Insert the key you want to use for logging in
    inserted_key = int(input('Security Code: '))
    if inserted_key == secret_key:
        print('Access Granted')
    else:
        print('Wrong Security Code. Access Denied')
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


# Credentials Generator
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
    print('Your Password: ', psw)
    print('---------------')

    save = input('Save the credentials [Y/N]: ')
    if save == 'Y':
        collection.insert_one(input_credentials)
        print('---------------')
        print('Saved')
        print('---------------')
    else:
        clear_screen()


# Credentials manual add
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
    save = input('Save Credentials [Y/N]: ')
    if save == 'Y':
        collection.insert_one(input_manual)
        print('---------------')
        print('Saved')
        print('---------------')
        sleep(3)
        clear_screen()
    else:
        clear_screen()
        credential_manual_add()


# Credentials Finder
def credential_finder():
    print('For which platform ?')
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
        prox = input('Want to search other credentials ? [Y/N]: ')
        if prox == 'S':
            clear_screen()
            credential_finder()
        else:
            clear_screen()
    except:
        print('Couldn't find any credentials for this platform')
        credential_finder()


# Update Credentials
def credential_update():
    print('Which platform you want to update ?')
    record_filter = input().lower()
    print('Insert new password')
    record_update = input()
    check = input('Do you want to save the password? [Y/N]: ')
    if check == 'Y':
        e_record_update = safety.encrypt(record_update)
        collection.find_one_and_update({'Platform': record_filter},
                                       {'$set': {'Password': e_record_update}},
                                       return_document=ReturnDocument.AFTER)
        print('---------------')
        print('Credentials updated')
        print('---------------')
        sleep(3)
        clear_screen()
    else:
        credential_update()


# Remove Credentials
def credential_remove():
    print('Which platform you want to remove ?')
    record_filter = input().lower()
    check = input('You want to remove these credentials ? [Y/N]')
    if check == 'Y':
        collection.delete_one({'Platform': record_filter})
        print('---------------')
        print('Credenzials removed')
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
        option = input("Choose an option: ")
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
            print('Choose a valid option')
