'''
SG
May 4th 2023
python 3.10.10
pyinstaller 5.1
requests 2.28.1
bs4 4.11.1
tk 8.6.12
playsound 1.2.2

'''
# primeABGB

import requests
import bs4
import time
import webbrowser
from tkinter import *
from playsound import playsound

# submit button function
def submit(event=None):
    link=link_entry.get()
    price=price_entry.get()
    asker.link=link
    asker.destroy()

# close window for okay button
def close_window():
    popup.destroy()
    
# opening link button function
def open_link():
    webbrowser.open(asker.link)
    
# creating window
asker=Tk()
asker.title("Input Example")
asker.geometry("200x200")

link_value=StringVar()
price_value=IntVar()

# creating label and textbox for link
link_label=Label(asker, text="Link: \n")
link_label.pack()
link_entry=Entry(asker, width=20, textvariable=link_value)
link_entry.pack()

# creating label and textbox for price
price_label=Label(asker, text="Price: \n")
price_label.pack()
price_entry=Entry(asker, width=20, textvariable=price_value)
price_entry.pack()

# creating submit button
submit_button=Button(asker, text="Submit", command=submit)
submit_button.pack()

asker.bind('<Return>', submit)
asker.mainloop()

#Prime loop
if 'prime' in link_value.get():
    while True:
        time.sleep(3)
        result=requests.get(link_value.get())
        soup=bs4.BeautifulSoup(result.text,"lxml")
        if int(soup.select("script",type="text/javascript")[34].text[16:21])<=price_value.get():
            playsound("C:\\Users\\thepu\\Downloads\\whatever.mp3")
            popup=Tk()
            popup.title("")
            popup.geometry('400x200')
            price_drop_label=Label(popup, text="Price has dropped for the desired product!",font=("Arial", 13))
            price_drop_label.pack(pady=2)
            current_price_label=Label(popup, text=f"Current price: {int(soup.select('script',type='text/javascript')[34].text[16:21])}",font=("Arial", 13))
            current_price_label.pack(pady=2)
            button=Button(popup, text="Okay",font=("Arial", 13),command=close_window)
            button.pack(pady=2)
            open_button = Button(popup, text="Open Link", font=("Arial", 13),command=open_link)
            open_button.pack(pady=2)
            popup.lift()
            popup.attributes('-topmost', True)
            popup.after_idle(popup.attributes, '-topmost', False)
            popup.mainloop()
            break
        else:
            continue
        
# MDC loop   
elif 'mdcomputers' in link_value.get():
    while True:
        time.sleep(3)
        result=requests.get(link_value.get())
        soup=bs4.BeautifulSoup(result.text,"lxml")
        if int(float(soup.select_one("#price-special").get('content')))<=price_value.get():
            playsound("C:\\Users\\thepu\\Downloads\\whatever.mp3")
            popup=Tk()
            popup.title("")
            popup.geometry('400x200')
            price_drop_label=Label(popup, text="Price has dropped for the desired product!",font=("Arial", 13))
            price_drop_label.pack(pady=2)
            current_price_label=Label(popup, text=f"Current price: {soup.select_one('#price-special').get('content')}",font=("Arial",13))
            current_price_label.pack(pady=2)
            button=Button(popup, text="Okay",font=("Arial", 13),command=close_window)
            button.pack(pady=2)
            open_button = Button(popup, text="Open Link", font=("Arial", 13),command=open_link)
            open_button.pack(pady=2)
            popup.lift()
            popup.attributes('-topmost', True)
            popup.after_idle(popup.attributes, '-topmost', False)
            popup.mainloop()
            break
        else:
            continue