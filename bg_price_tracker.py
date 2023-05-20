'''
SG
May 20th 2023
python 3.10.10
compiled using pyinstaller 5.1

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
    playsound("whatever.mp3")
    popup=Tk()
    popup.title("")
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 200) // 2
    popup.geometry(f'400x200+{x}+{y}')
    popup.resizable(False,False)
    price_drop_label=Label(popup, text="Price has dropped for the desired product!", font=("Arial", 13))
    price_drop_label.pack(pady=2)
    current_price_label=Label(popup, text=f"Current price: {current_value}", font=("Arial",13))
    current_price_label.pack(pady=2)
    button=Button(popup, text="Okay", font=("Arial", 13), command=popup.destroy)
    button.pack(pady=2)
    open_button = Button(popup, text="Open Link", font=("Arial", 13), command=open_link)
    open_button.pack(pady=2)
    popup.lift()
    popup.attributes('-topmost', True)
    popup.after_idle(popup.attributes, '-topmost', False)
    popup.mainloop()
    
def error_window_func():
    error_window=Tk()
    error_window.title("Error!")
    screen_width = error_window.winfo_screenwidth()
    screen_height = error_window.winfo_screenheight()
    x = (screen_width - 200) // 2
    y = (screen_height - 100) // 2
    error_window.geometry(f'200x100+{x}+{y}')
    error_window.resizable(False,False)
    error_label=Label(error_window,text="Please enter a valid link!",font=("Arial", 13))
    error_label.pack(pady=12)
    try_again_button=Button(error_window,text="Try Again", font=("Arial", 13), command=asker.mainloop)
    try_again_button.pack(pady=2) 
    error_window.mainloop()

# function to only enter digits in price module
def validate_price_entry(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False       

# creating asking window
asker=Tk()
asker.title("")
screen_width = asker.winfo_screenwidth()
screen_height = asker.winfo_screenheight()
x = (screen_width - 200) // 2
y = (screen_height - 155) // 2
asker.geometry(f"200x155+{x}+{y}")
asker.resizable(False,False)

link_value=StringVar()
price_value=IntVar()

# creating label and textbox for link and price
link_label=Label(asker, text="Link:", font=("Arial", 13))
link_label.pack(pady=2)
link_entry=Entry(asker, width=20, textvariable=link_value, font=("Arial", 13))
link_entry.pack(pady=2)
price_label=Label(asker, text="Price:", font=("Arial", 13))
price_label.pack(pady=2)
price_entry=Entry(asker, width=20, textvariable=price_value, font=("Arial", 13), validate="key", validatecommand=(asker.register(validate_price_entry), "%P"))
price_entry.pack(pady=2)

# creating submit button
submit_button=Button(asker, text="Submit", command=submit, font=("Arial",13))
submit_button.pack(pady=2)

asker.bind('<Return>', submit)
asker.lift()
asker.attributes('-topmost', True)
asker.after_idle(asker.attributes, '-topmost', False)
asker.mainloop()

# Main loop
while True:
    try:
        result=requests.get(link_value.get())
        soup=bs4.BeautifulSoup(result.text,"lxml")
        
        # Prime logic
        if 'prime' in link_value.get():
            price_tag_list=soup.select("script",type="rocketlazyloadscript")
            for tag in price_tag_list:
                if '"price":' in tag.text:
                    price_match=re.search(r'"price":(\d+)',tag.text)
                    current_value=int(price_match.group(1))
                    break
                else:
                    continue
            if current_value<=price_value.get():
                popup_window(current_value)
                break
            else:
                time.sleep(600)
                continue

        # MDComputers logic
        elif 'mdcomputers' in link_value.get():
            current_value=int(float(soup.select_one("#price-special").get('content')))
            if current_value<=price_value.get():
                popup_window(current_value)
                break
            else:
                time.sleep(600)
                continue

        # Vedant logic
        elif 'vedant' in link_value.get():
            script_tag=soup.select('script', type='application/ld+json')[-2]
            json_data=json.loads(script_tag.contents[0])
            current_value=int(float(json_data['offers']['price']))
            if current_value<=price_value.get():
                popup_window(current_value)
                break
            else:
                time.sleep(600)
                continue
    except:
        error_window_func()
    finally:
        break
    
'''
old primeABGB crawler code:
    replaced May 13th 2023:
    select_price_tag=soup.select("script",type="text/javascript")[34]
    current_value=int(re.search(r'\d+',select_price_tag.text).group())

'''