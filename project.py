import sys
import sqlite3
import customtkinter as ctk
import pytweening as tweener
from datetime import datetime as time


ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.custom_font =("Lato",20,'normal')
        self.button_height = 60
        self.button_width = 180
        self.title("Pe-FI")
        self.account = Account()

        # Create buttons
        self.button_frame = ctk.CTkFrame(self,corner_radius= 12,width= 250,height=300,border_width=0.5,fg_color="#1E1E1E")
        self.balance_button = ctk.CTkButton(self.button_frame, text="Balance",corner_radius= 6,font=self.custom_font,height=self.button_height,width=self.button_width,command = self.balance_command)
        self.withdraw_button = ctk.CTkButton(self.button_frame, text="Withdraw",corner_radius= 6,font=self.custom_font,height=self.button_height,width=self.button_width,command = self.widthdraw_command)
        self.deposit_button = ctk.CTkButton(self.button_frame, text="Deposit",corner_radius=6,font= self.custom_font,height=self.button_height,width=self.button_width,command=self.deposit_command)
        self.greeting = ctk.CTkLabel(self,text="Welcome to Pe-FI",font = ("Ariel",32,'bold'),fg_color="transparent", bg_color="transparent")
        
        # Place buttons using pack
        self.balance_button.pack(pady = 10,anchor ="center")
        self.withdraw_button.pack(pady = 7,anchor = "center")
        self.deposit_button.pack(pady = 10,anchor = "center")
        self.button_frame.place(relx=0, rely=0.18, relwidth=0.5, relheight=1)
        self.greeting.grid(row=0, column=0, columnspan=3, pady=5, sticky="NSEW")

    def balance_command(self):
        self.input_frame = ctk.CTkFrame(self,corner_radius= 12,width= 250,height=300,border_width=0.45,fg_color="#1E1E1E")
        self.input_frame.place(relx= 0.51, rely=0.18, relwidth=0.5, relheight=1)
        balance_text = ctk.CTkLabel(self.input_frame,text="Your Balance is",font = ("Ariel",24,'bold'),anchor= "center")
        balance_num = ctk.CTkLabel(self.input_frame,text="$"+str(self.account.balance),font = ("Ariel",38,'bold'),anchor= "center")
        recent_transactions_label = ctk.CTkLabel(self.input_frame,text="Recent Transactions",font = ("Ariel",18,'bold'),fg_color="transparent", bg_color="transparent")
        output = ""
        for entries in self.account.recent_transactions(5):
            transaction_type  ={"deposit":"Deposited","widthdraw":"Widthdrew"}
            output += f"{transaction_type.get(entries[0])} {entries[1]}\n"
        transactions = ctk.CTkLabel(self.input_frame,text= output,font = ("Ariel",10,'bold'),fg_color="transparent", bg_color="transparent")
        balance_text.pack(pady = 3)
        balance_num.pack(pady=5)
        recent_transactions_label.pack(pady=5)
        transactions.pack(pady = 5)
                
    
    def deposit_command(self):
        self.deposit_frame = ctk.CTkFrame(self,corner_radius= 12,width= 250,height=300,border_width=0.45,fg_color="#1E1E1E")
        self.deposit_frame.place(relx= 0.51, rely=0.18, relwidth=0.5, relheight=1)
        deposit_text = ctk.CTkLabel(self.deposit_frame,text="Deposit How Much",font = ("Ariel",14,'bold'),anchor= "w",padx = 1)
        deposit_textbox = ctk.CTkEntry(self.deposit_frame)
        enter_button = ctk.CTkButton(self.deposit_frame,text = "enter",command = lambda:deposit(deposit_textbox.get()))
        deposit_text.pack(pady=5,)
        deposit_textbox.pack(pady=5)
        enter_button.pack(pady =5)
        def deposit(amount):
            deposit_textbox.delete(0, 'end')
            status = self.account.deposit(amount)
            status_text = ctk.CTkLabel(self.deposit_frame,text= status,font = ("Ariel",14,'bold'),anchor= "w",padx = 1)
            status_text.pack(pady =5)
            self.after(1000,lambda:status_text.destroy())

    def widthdraw_command(self):
        self.widthdraw_frame = ctk.CTkFrame(self,corner_radius= 12,width= 250,height=300,border_width=0.45,fg_color="#1E1E1E")
        self.widthdraw_frame.place(relx= 0.51, rely=0.18, relwidth=0.5, relheight=1)
        widthdraw_text = ctk.CTkLabel(self.widthdraw_frame,text="Widthdraw how much?",font = ("Ariel",14,'bold'),anchor= "center")
        widthdraw_textbox = ctk.CTkEntry(self.widthdraw_frame,)
        enter_button = ctk.CTkButton(self.widthdraw_frame,text = "enter",command = lambda:widthdraw(widthdraw_textbox.get()))
        widthdraw_text.pack(pady =5)
        widthdraw_textbox.pack(pady =5)
        enter_button.pack(pady =5)
        def widthdraw(amount):
            widthdraw_textbox.delete(0, 'end')
            status = self.account.widthdraw(amount)
            status_text = ctk.CTkLabel(self.widthdraw_frame,text= status,font = ("Ariel",14,'bold'),anchor= "w",padx = 1)
            status_text.pack(pady =5)
            self.after(1000,lambda:status_text.destroy())

class Account:
    def __init__(self) -> None:
        self.database = sqlite3.connect("/home/tinu/Workspace/Python/Pe-FI/database.db")
        self.cursor = self.database.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS account (id INTEGER PRIMARY KEY AUTOINCREMENT,transaction_type TEXT NOT NULL,amount INT NOT NULL,balance INT NOT NULL);")
        self.cursor.execute("SELECT balance FROM account ORDER BY id DESC LIMIT 1;")
        result = self.cursor.fetchone()
        if result == None:
            self.cursor.execute( "INSERT INTO account (transaction_type, amount, balance) VALUES ('deposit', 0, 0);")
            self.database.commit()
            self.cursor.execute("SELECT balance FROM account ORDER BY id DESC LIMIT 1;")
            self.balance = self.cursor.fetchone()[0]
        else:
            self.balance = result[0]
           
    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self,amount):
        if amount >= 0:
            self._balance = amount
    
    def deposit(self,amount):
        if amount.isdigit():
            self.balance += int(amount)
            self.cursor.execute( "INSERT INTO account (transaction_type, amount, balance) VALUES ('deposit', ?, ?);",(amount,self.balance))
            self.database.commit()
            return "Sucessful"
        else:
            return "Invalid Input"

    def widthdraw(self,amount):
        if amount.isdigit():
            if int(amount) <= self._balance:
                self.balance -= int(amount)
                self.cursor.execute( "INSERT INTO account (transaction_type, amount, balance) VALUES ('widthdraw', ?, ?);",(amount,self.balance))
                self.database.commit()
                return "Sucessful"
            else:
                return "Insufficent Funds"
        else:
            return "Invalid Input"

    def recent_transactions(self,no_of_transactions):
        self.cursor.execute("SELECT transaction_type,amount FROM account ORDER BY id DESC LIMIT ?;",(no_of_transactions,))
        return self.cursor.fetchall()

def main():   
    app = App()
    app.grid_columnconfigure(1, weight=1)
    app.mainloop()

if __name__ == "__main__":
    main()