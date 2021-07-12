from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import requests
import json
import datetime

# Buat objek
root = Tk()

varHari = StringVar()
varWaktu = StringVar()
varCuaca = StringVar()
varTemperatur = StringVar()
varGambar = StringVar()


def getHaridanWaktu():
    current_time = datetime.datetime.now()
    today = datetime.date.today()
    d1 = today.strftime("%d/%B/%Y")
    d2 = current_time.strftime("%H:%M:%S")
    varHari.set(f"Date:{d1}")
    varWaktu.set(f"Time: {d2}")

def set_label():
    currentTime = datetime.datetime.now().strftime("%H:%M:%S")
    labelWaktu['text'] = f"Time: {currentTime}"
    root.after(1, set_label)

def deteksiCuaca():
    global logo_img
    if (entryKota.get() == ""):
        messagebox.showwarning(title="Peringatan !", message="Harap masukan field terlebih dahulu !", )
    else:
        API = 'cfd198344a432f772a50d09103dfba35'
        url = f"http://api.openweathermap.org/data/2.5/weather?q={entryKota.get()}&appid={API}"
        try:
            response = requests.get(url)
            r = response.text
            with open("cuaca.json", 'w') as file:
                file.write(r)
            with open("cuaca.json", 'r') as file:
                d = json.load(file)
                cuaca = dict(d['weather'][0])['main']
                suhu = float(d['main']['temp']) - 273.15
                if cuaca == 'Haze':
                    cuaca1 = 'Berkabut'
                    logo_img = PhotoImage(file="images/kabut.png")
                    my_canvas.create_image(180 - 50 / 2, 40, image=logo_img)
                elif cuaca == 'Rain':
                    cuaca1 = 'Hujan'
                    logo_img = PhotoImage(file="images/hujan.png")
                    my_canvas.create_image(180 - 50 / 2, 40, image=logo_img)
                elif cuaca == 'Clear':
                    cuaca1 = 'Cerah'
                    logo_img = PhotoImage(file="images/cerah.png")
                    my_canvas.create_image(180 - 50 / 2, 40, image=logo_img)
                elif cuaca == 'Clouds':
                    cuaca1 = 'Berawan'
                    logo_img = PhotoImage(file="images/berawan.png")
                    my_canvas.create_image(180 - 50 / 2, 40, image=logo_img)
                else:
                    cuaca1 = cuaca

                varCuaca.set(cuaca1)
                varTemperatur.set(f"{suhu: .2f} Celsius")

        except KeyError:
            messagebox.showwarning(title="Peringatan !", message="Tidak ada kota tersebut !",)
        except requests.exceptions.ConnectionError as errc:
            messagebox.showerror(title="Error Connection !", message=errc, )
        except requests.exceptions.Timeout as errt:
            messagebox.showerror(title="Error Timeout !", message=errt, )
        except requests.exceptions.RequestException as err:
            messagebox.showerror(title="Error Requests !", message=err, )
        except Exception as e:
            messagebox.showerror(title="Error !", message=e, )


# Atur window
lebar = 390
tinggi = 450
setTengahX = (root.winfo_screenwidth() - lebar) // 2
setTengahY = (root.winfo_screenheight() - tinggi) // 2

root.geometry("%ix%i+%i+%i" % (lebar, tinggi, setTengahX, setTengahY))
root.resizable(False, False)
root.wm_title("Aplikasi Cuaca GUI")

# Buat objek frame
frameSaya = Frame(root,width=300, height=200)
frameSaya.grid(row=0,column=0, padx=0, pady=0)
frameSaya.config(background = "#fff")


# Buat tabel pada grid 0,0
labelHeader = Label(frameSaya, text="Aplikasi Cuaca \n Oleh Fathurrahman Rifqi Azzami - 1918101504 - II RPLK",background="#fff")
labelHeader.grid(row=0, column=0, padx=45, pady=30)

frameDua =  Frame(root, width=300, height=300)
frameDua.grid(row=1, column=0, padx=10, pady=40)

getHaridanWaktu()
labelHari = Label(frameDua, textvariable=varHari,font='arial 8 bold')
labelHari.grid(row=0, column=0,sticky="w")

labelWaktu = Label(frameDua, text="", font='arial 8 bold')
labelWaktu.grid(row=0, column=1,sticky="e")
set_label()


labelLength =  Label(frameDua, text="Input Kota / Negara")
labelLength.grid(row=1, column=0, pady=10,sticky="w")

entryKota =  ttk.Entry(frameDua, width=30)
entryKota.grid(row=1, column=1,pady=10)

buttonSaya =  ttk.Button(frameDua, text="Deteksi Cuaca", width=46, command=deteksiCuaca)
buttonSaya.grid(row=2, column=0, sticky="w", padx=0, pady=7, ipadx=10 , columnspan=2)

labelCuaca =  Label(frameDua, text="Cuaca")
labelCuaca.grid(row=3, column=0, pady=10,sticky="w")

labelGetCuaca = Label(frameDua, textvariable=varCuaca, font='arial 8 bold')
labelGetCuaca.grid(row=3, column=1,sticky="e")

labelTemperatur =  Label(frameDua, text="Temperatur")
labelTemperatur.grid(row=4, column=0, pady=7,sticky="w")

labelGetTemperatur = Label(frameDua, textvariable=varTemperatur, font='arial 8 bold')
labelGetTemperatur.grid(row=4, column=1,sticky="e")

my_canvas = Canvas(frameDua,bg="#fff",width=300,height=80)
my_canvas.grid(row=5, column=0,columnspan=2,pady=10)

root.mainloop()

