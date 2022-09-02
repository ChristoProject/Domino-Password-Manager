# Domino | Password Manager
Domino is a simple CLI password Vault.
It uses a MongoDB online free server to gather all your information.

# Safety
The safety of the instrument has two levels:
- Security code to LogIn the app
- Cryptography of the password before saving in the DB

# How to Use
Before you can use the tool you have to set the DB Connection and the Security Code for the LogIn:

## DB Connection:

> url = ' *here you paste the url to connect to you DB* '

> pymongo.MongoClient(url, tlsCAFile=ca)

> db = client[' *here you put the name of you DB* ']

> collection = db[' *here you put the name of the collection inside the DB* ']

## Security Code:
In the "login()" function (line 55) you have to put you personal LogIn Code:

> secret_key = int( *write your code here* )

# Cryptography
This is provided via a deedicated class and functions.
**Your key will not be saved** so remember it.
