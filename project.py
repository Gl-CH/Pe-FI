import sys
import tkinter as tk
from re import match as regex_match
from tkinter import messagebox
from datetime import datetime as time




class Account:
    def log_it(func):
        def wrapper(*args,**kwargs):
            func(*args,**kwargs)
            with open("transaction_history.txt","a") as file:
                file.write(f"{str(func.__qualname__).split(".")[1].title()} at {str(time.now())}\n")
        return wrapper
    
    def __init__(self) -> None:
        try:
            with open("old_bank_statement.txt","r") as file:
                self._balance = int(file.read())
        except:
            with open("old_bank_statement.txt","w") as file:
                self._balance = 0
                file.write("0")

    @property
    def balance(self):
        return self._balance


    @balance.setter
    def balance(self,amount):
        if amount >= 0:
            self._balance = amount
    
    @log_it
    def deposit(self,amount):
        if amount.isdigit():
            self._balance += int(amount) 
            Popup(f"Done! Balance is {self.balance}","Balance")
        else:
            Popup("Invalid Amount")

    @log_it
    def widthdraw(self,amount):
        if amount.isdigit():
            if int(amount) <= self._balance:
                self._balance -= int(amount)
                Popup(f"Done! Balance is {self.balance}","Balance")
            else:
                Popup("Insufficent Funds")
        else:
            Popup("Invalid Amount")


class Window:
    def __init__(self,name,size) -> None:
        self._name = name
        self._size = size
        self._window = tk.Tk()
        self._window.title(self._name)
        self._window.geometry(self._size)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        if name.isalpha():
            self._name = name

    @property
    def size(self):
        return self._size
        
    @size.setter
    def size(self,size):
        if regex_match(r"^\d{1,3}-\d{1,3}x\d{1,3}-\d{1,3}$",size):
            self._size = size

    def add_label(self,text:str,font:tuple):
        tk.Label(self._window,text = text ,font = font,).pack()

    def add_button(self,text:str,font:tuple,command):
        button = tk.Button(self._window,text = text,font = font, command= command)
        button.pack(pady= 20)

    def add_textbox(self):
         text_box = tk.Entry(self._window)
         text_box.pack()
         return text_box

    def __str__(self) -> str:
        return str(self.balance)
    
    def mainloop(self):
        self._window.mainloop()

class Popup:
    def __init__(self,text,title = "window") -> None:
        messagebox.showinfo(title,str(text))

account = Account()

def main():   
    window = Window("pefi","240x480")
    window.add_label("Welcome to Pefi",('Roboto',18))
    window.add_button("Check Balance",('Roboto',18),lambda:Popup(f"Balance is {account.balance}"))
    window.add_button("Deposit",('Roboto',18),deposit_window)
    window.add_button("Widthdraw",('Roboto',18),widthdraw_window)
    window.add_button("Close",('Roboto',18),close_window)
    window.mainloop()

def widthdraw_window():
    widthdraw_window = Window("Widthdraw","240x480")
    widthdraw_window.add_label("Widthdraw how much",('Roboto',8))
    text_box = widthdraw_window.add_textbox()
    widthdraw_window.add_button("Enter",('Roboto',18),lambda:account.widthdraw(text_box.get()))
    widthdraw_window.mainloop()


def deposit_window():
    deposit_window = Window("Deposit","240x480")
    deposit_window.add_label("Deposit how much",('Roboto',8))
    text_box = deposit_window.add_textbox()
    deposit_window.add_button("Enter",('Roboto',18),lambda:account.deposit(text_box.get()))
    deposit_window.mainloop()

def close_window():
    with open("old_bank_statement.txt","w") as file:
        file.write(str(account.balance))
    sys.exit(0)

if __name__ == "__main__":
    main()