'''
SG
May 11th 2023
python 3.10.10
pyinstaller 5.1
requests 2.28.1
bs4 4.11.1
tk 8.6.12
playsound 1.2.2
json ???
re ???

'''

import re
import requests
import bs4
import time
import webbrowser
import json
from tkinter import *
from playsound import playsound

# submit button function
def submit(event=None):
    link=link_entry.get()
    price=price_entry.get()
    asker.link=link
    asker.destroy()

# opening link button function
def open_link():
    webbrowser.open(asker.link)

# a default popup window for every alert
def popup_window(current_value):
    popup=Tk()
    popup.title("")
    popup.geometry('400x200')
    price_drop_label=Label(popup, text="Price has dropped for the desired product!",font=("Arial", 13))
    price_drop_label.pack(pady=2)
    current_price_label=Label(popup, text=f"Current price: {current_value}",font=("Arial",13))
    current_price_label.pack(pady=2)
    button=Button(popup, text="Okay",font=("Arial", 13),command=popup.destroy)
    button.pack(pady=2)
    open_button = Button(popup, text="Open Link", font=("Arial", 13),command=open_link)
    open_button.pack(pady=2)
    popup.lift()
    popup.attributes('-topmost', True)
    popup.after_idle(popup.attributes, '-topmost', False)
    popup.mainloop()

# sound and window function
def sound_and_window():
    playsound("whatever.mp3")
    popup_window(current_value)

# function to only enter digits in price module
def validate_price_entry(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False

# creating asking window
asker=Tk()
asker.title("Input Example")
asker.geometry("200x200")

link_value=StringVar()
price_value=IntVar()

# creating label and textbox for link and price
link_label=Label(asker, text="Link: \n")
link_label.pack()
link_entry=Entry(asker, width=20, textvariable=link_value)
link_entry.pack()
price_label=Label(asker, text="Price: \n")
price_label.pack()
price_entry=Entry(asker, width=20, textvariable=price_value, validate="key", validatecommand=(asker.register(validate_price_entry), "%P"))
price_entry.pack()

# creating submit button
submit_button=Button(asker, text="Submit", command=submit)
submit_button.pack()

asker.bind('<Return>', submit)
asker.mainloop()

# Main loop
while True:
    time.sleep(3)
    try:
        result=requests.get(link_value.get())
        soup=bs4.BeautifulSoup(result.text,"lxml")

        if 'prime' in link_value.get():
            select_price_tag=soup.select("script",type="text/javascript")[34]
            current_value=int(re.search(r'\d+',select_price_tag.text).group())
            if current_value<=price_value.get():
                sound_and_window()
                break
            else:
                continue

        elif 'mdcomputers' in link_value.get():
            current_value=int(float(soup.select_one("#price-special").get('content')))
            if current_value<=price_value.get():
                sound_and_window()
                break
            else:
                continue

        elif 'vedant' in link_value.get():
            script_tag=soup.select('script', type='application/ld+json')[-2]
            json_data=json.loads(script_tag.contents[0])
            current_value=int(float(json_data['offers']['price']))
            if current_value<=price_value.get():
                sound_and_window()
                break
            else:
                continue
    except:
        print('an error occured')
    finally:
        break