from beid import scan_readers, read_infos, triggered_decorator
from pprint import pprint
from time import sleep

# retrieve a list of available readers
r = scan_readers()[0]

# declare a function that will be executed automatically when a card is removed/insterted
# funcion arguments should be :
# - action : which will be "inserted" or "removed" when the function will be called
# - card : which will be the card if inserted
# - reader : which will hold  the name of the reader to use 

@triggered_decorator
def basic_read(action, card, reader=r.name):
    if action=="inserted":
        i = read_infos(card)
        pprint(i)

sleep(5)

infos = read_infos(r, read_photo=True)
with open("photo.jpg", "wb") as f:
    f.write(infos['photo'])