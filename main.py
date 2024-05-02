from tkinter import *
from tkinter import messagebox
import random
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def create_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list1 = [random.choice(letters) for _ in range(nr_letters)]

    password_list2 = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list3 = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_list1 + password_list2 + password_list3

    random.shuffle(password_list)

    password = "".join(password_list)

    if password_input.get() == "":
        password_input.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_info():
    site = website_input.get()
    username = username_input.get()
    password = password_input.get()

    new_data = {
        site: {
            "username": username,
            "password": password
        }
    }

    if len(site) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Don't leave any fields empty")
    else:
        ok = messagebox.askokcancel(message=f"Do you want to save the given information:\n"
                                       f"site: {site}\n"
                                       f"username: {username}\n"
                                       f"password: {password}")

        if ok:

            try:
                # first we open the file by reading the current data and then updating it with the new_data
                with open("passwords.json", "r") as file:

                    data = json.load(file)
                    data.update(new_data)

                # and here we save the new data
                with open("passwords.json", "w") as file:

                    json.dump(data, file, indent=4)

            except FileNotFoundError:
                print("second time?")

                # in case we cant open the file , we create it by inserting the new_data anew
                with open("passwords.json", "w") as file:
                    json.dump(new_data, file, indent=4)

            finally:

                username_input.delete(0, END)
                website_input.delete(0, END)
                password_input.delete(0, END)

                messagebox.showinfo(title="", message="Successful")

# ---------------------------- READ DATA ------------------------------- #


def get_info():

    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No record")
    else:
        site = website_input.get()

        password_input.delete(0, END)
        username_input.delete(0, END)

        try:

            password_input.insert(0, data[site]["password"])
            username_input.insert(0, data[site]["username"])

        except KeyError:
            messagebox.showinfo(title="Error", message=f"No record for {site}")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password manager")
window.tk.call('tk', 'scaling', 1.4)
window.config(pady=30, padx=30)

pic = PhotoImage(file="logo.png")

canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=pic)
canvas.grid(column=1, row=0)

label1 = Label(text="Website:")
label1.grid(column=0, row=1)
label2 = Label(text="Email/Username:")
label2.grid(column=0, row=2)
label3 = Label(text="Password:")
label3.grid(column=0, row=3)

website_input = Entry(width=35)
website_input.grid(column=1, row=1, columnspan=2)
website_input.focus()
username_input = Entry(width=35)
username_input.grid(column=1, row=2, columnspan=2)
username_input.insert(0, "email@email.com")
password_input = Entry(width=23)
password_input.grid(column=1, row=3, sticky="W", padx=5)

search_button = Button(text="Search", command=get_info, width=20)
search_button.grid(column=3, row=1)

pass_button = Button(text="Generate Password", command=create_pass, width=20)
pass_button.grid(column=3, row=3)

add_button = Button(text="Add", width=36, command=save_info)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
