from pathlib import Path
import sys
import pandas as pd
import tkinter as tk
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, font


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Stefan\Desktop\tkinter designer\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#################Funkcije za program######################
def change_text(output_label, new_text):
    canvas.itemconfig(output_label, text=new_text)


def pronadji_proizvod():
    button_2.config(text="Izmeni cenu")
    barcode = entry_1.get()

    # Pravljenje datafile
    df = pd.read_excel(file_path, header=None, dtype=str)

    # Izbacuje vrste sa NaN vrednostima u barkode i naziv kolonama
    df = df.dropna(subset=[barcode_column, name_column])

    if barcode in df[barcode_column].astype(str).values:
        product_name = df.loc[df[barcode_column].astype(str) == barcode, name_column].values[0]
        old_price = df.loc[df[barcode_column].astype(str) == barcode, price_column].values[0]

        change_text(output_label, f"Stara cena: {product_name} ({barcode}): {old_price}")

    else:
        change_text(output_label, f"Proizvod nije pronadjen")

def updateCena():
    barkod = entry_1.get()
    new_price = entry_3.get()

    df = pd.read_excel(file_path, header=None, dtype=str)

    # Ažuriraj cenu samo ako je nova cena uneta
    if new_price:
        # Ažuriraj DataFrame, ne briši redove sa NaN vrednostima
        mask = df[barcode_column].notna() & df[name_column].notna()
        mask &= df[barcode_column].astype(str) == barkod
        df.loc[mask, price_column] = float(new_price)
        df.to_excel(file_path, index=False, header=False)

        # Obriši podatke u entry boxevima nakon izvršenja ažuriranja cene
        entry_1.delete(0, tk.END)
        entry_3.delete(0, tk.END)
        entry_2.delete(0, tk.END)

        # Vrati fokus na prvi entry point
        window.after(10, lambda: entry_1.focus_set())
        button_2.config(text="Promenjena")
    else:
        entry_1.delete(0, tk.END)
        entry_2.delete(0, tk.END)
        entry_3.delete(0, tk.END)
        button_2.config(text="Nije uneta")
        # Ako nova cena nije uneta, vrati fokus na prvi entry point
        window.after(10, lambda: entry_1.focus_set())
    change_text(output_label, "")
    change_text(predlozena_cena, "")

#pitaj za lokaciju fajla
def ask_for_file_location():
    #popup
    popup = tk.Tk()
    custom_font = font.Font(family="Helvetica", size=12)
    popup.title("Select File")
    popup.geometry("200x80")
    popup.minsize(200, 80)

    #inacijalizacija max velicine prozora
    max_width = 200
    max_height = 80
    popup.maxsize(max_width, max_height)

    def enforce_max_size(event):
        if popup.winfo_width() > max_width or popup.winfo_height() > max_height:
            popup.geometry(f"{min(popup.winfo_width(), max_width)}x{min(popup.winfo_height(), max_height)}")

    popup.bind("<Configure>", enforce_max_size)

    #tekst i dugme
    label = tk.Label(popup, text="Please select the file path", font=custom_font)
    label.pack()

    def ok_button_clicked():
        popup.destroy()

    ok_button = tk.Button(popup, text="OK", command=ok_button_clicked, font=custom_font)
    ok_button.pack()

    popup.mainloop()

    #otvori fajl dijalog nakon sto je popup zatvoren
    file_path = filedialog.askopenfilename(title="Select File")
    return file_path

############# komande za fokusiranje sledecih widgeta ###############
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

def activate_button(event=None):
    pronadji_proizvod()
    event.widget.tk_focusNext().focus()
    return "break"

def activate_button2(event=None):
    updateCena()
    event.widget.tk_focusNext().focus()
############################
    
def calculate_and_display_price():
    pdv_price_entry = entry_2.get()

    entry_3.focus_set()

    if pdv_price_entry:
        try:
            pdv_price = float(pdv_price_entry)
            suggested_price = pdv_price * 1.3
            change_text(predlozena_cena, f"Predlozena cena: {suggested_price:.2f}")
            entry_3.focus_set()
        except ValueError:
            change_text(predlozena_cena, "Unesite validnu cenu sa PDV-om")
    else:
        change_text(predlozena_cena, "Cena sa PDV-om nije uneta")

#excel konstante
file_path = ask_for_file_location()
barcode_column = 6
name_column = 0
price_column = 1
##########################################################
##########################################################
##########################################################
if file_path:
    window = Tk()

    window.geometry("846x599")
    window.configure(bg = "#5A92B1")


    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 599,
        width = 846,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        846.0,
        84.0,
        fill="#92B48F",
        outline="")

    canvas.create_text(
        23.0,
        13.0,
        anchor="nw",
        text="ZAPONETTI",
        fill="#000000",
        font=("InriaSans Regular", 48 * -1)
    )

    canvas.create_rectangle(
        0.0,
        83.0,
        847.0,
        599.0,
        fill="#5A92B1",
        outline="")

    canvas.create_rectangle(
        321.0,
        514.0,
        527.0,
        564.0,
        fill="#5A92B1",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        213.0,
        256.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        213.0,
        476.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        423.0,
        330.0,
        image=image_image_3
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        564.5,
        134.0,
        image=entry_image_1
    )

    entry_1 = Entry(
        bd=0,
        bg="#C7D8E2",
        fg="#000716",
        highlightthickness=0,
        font=("MontserratRoman Medium", 24 * -1)
    )
    entry_1.place(
        x=390.0,
        y=107.0,
        width=349.0,
        height=48.0
    )

    entry_1.focus_set() ###

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        564.5,
        257.0,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#C8D9E2",
        fg="#000716",
        highlightthickness=0,
        font=("MontserratRoman Medium", 24 * -1)
    )
    entry_2.place(
        x=390.0,
        y=230.0,
        width=349.0,
        height=48.0
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        564.5,
        476.0,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#C8D9E2",
        fg="#000716",
        highlightthickness=0,
        font=("MontserratRoman Medium", 24 * -1)
    )
    entry_3.place(
        x=390.0,
        y=449.0,
        width=349.0,
        height=48.0
    )

    canvas.create_rectangle(
        -3.0,
        80.0,
        845.9999043936405,
        84.09585479894764,
        fill="#000000",
        outline="")

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        213.0,
        134.0,
        image=image_image_4
    )

    canvas.create_text(
        122.0,
        119.0,
        anchor="nw",
        text="Uneti Barcode:",
        fill="#000000",
        font=("MontserratRoman Medium", 24 * -1)
    )

    output_label = canvas.create_text(
        425.0,
        330.0,
        anchor="center",
        text="",
        fill="#000000",
        font=("MontserratRoman Medium", 18 * -1)
    )

    canvas.create_text(
        122.0,
        119.0,
        anchor="nw",
        text="",
        fill="#000000",
        font=("MontserratRoman Medium", 24 * -1)
    )

    canvas.create_text(
        135.0,
        461.0,
        anchor="nw",
        text="Nova cena:",
        fill="#000000",
        font=("MontserratRoman Medium", 24 * -1)
    )

    canvas.create_text(
        110.0,
        242.0,
        anchor="nw",
        text="Cena sa PDV-om:",
        fill="#000000",
        font=("MontserratRoman Medium", 24 * -1)
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        793.0,
        42.0,
        image=image_image_5
    )

    canvas.create_rectangle(
        320.0,
        172.0,
        526.0,
        222.0,
        fill="#5A92B1",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: pronadji_proizvod(), ###
        relief="flat"
    )
    button_1.place(
        x=317.0,
        y=168.0,
        width=214.0,
        height=60.0
    )

    entry_1.bind("<Return>", lambda event: (pronadji_proizvod(), window.after(10, lambda: entry_2.focus_set()))) ####
    entry_2.bind("<Return>", lambda event: calculate_and_display_price()) ###


    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: updateCena(), ###
        relief="flat"
    )
    button_2.place(
        x=309.0,
        y=512.0,
        width=226.0,
        height=63.0
    )


    entry_3.bind("<Return>", activate_button2) ### 

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        423.0,
        396.0,
        image=image_image_6
    )

    predlozena_cena = canvas.create_text(
        415.0,
        395.0,
        anchor="center",
        text="",
        fill="#000000",
        font=("MontserratRoman Medium", 18 * -1)
    )
    window.resizable(False, False)
    window.mainloop()
else:
    sys.exit()