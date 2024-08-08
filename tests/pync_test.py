import pync
import time
import os

from pync import Notifier

i = 0
while True:
    i = i + 1
    pync.notify(
        'Reminder - Drink Water, Sir', 
        title='Qbot', 
        open='https://ufund-me.github.io/',
        # appIcon='https://raw.githubusercontent.com/UFund-Me/Qbot/main/qbot/gui/imgs/UFund.png',
        # appIcon='https://ufund-me.github.io/img/UFund.png',
        # appIcon='https://ufund-me.github.io/img/logo.ico',
        appIcon='./qbot/gui/imgs/logo.ico'
    )
    Notifier.notify(
        "Notification from %s" % __file__,
        title='pync Notification',
        open='https://github.com/SeTeM/pync',
        appIcon='https://ufund-me.github.io/img/UFund.png'
    )
    os.system("afplay ./qbot/asserts/statics/sounds/bell.wav")
    time.sleep(2)

    # Notifier.notify(
    #     "Notification from %s" % __file__,
    #     title='pync Notification',
    #     open='https://github.com/SeTeM/pync',
    #     appIcon='https://ufund-me.github.io/img/UFund.png'
    # )

    print("new loop ", i)
    time.sleep(3)
