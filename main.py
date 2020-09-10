import os
import csv
import time
import threading
from threading import Thread
import sys
import socket
import serial
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
from pandas.plotting import register_matplotlib_converters
import cv2 as cv

register_matplotlib_converters()  # modifica convertorii globali
style.use("ggplot")  # un stil de plotare


class server(Thread):  # threadul pentru server
    def run(self):
        TCP_IP = "127.0.0.1"  # adresa IP pentru IPv4 localhost
        TCP_PORT = 5005       # numarul portului pentru tcp pe care se asculta
        Buffer_size = 20      # dimensiunea buffer-ului, in mod normal trebuia sa fie 1024 dar vrem sa fie rapid

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # construim un socket care are doi parametrii, primul
                                                               # AF_INET care reprezinta familia acestuia iar cel
                                                               # de-al doilea reprezinta conexiunea orientata prin
                                                               # protocolul TCP
        s.bind((TCP_IP, TCP_PORT))  # leaga socket-ul la adresa
        s.listen(1)  # defineste lungimea cozii backlog-ului care ar da maximul de clineti disponibili

        connect, addres = s.accept() # accepta conexiuni din afara cerute de client
        print("Connenction adress: ", addres)
        while 1:
            data = connect.recv(Buffer_size)  # se pregateste de a primi date prin protocolul de transfer de fisiere
            if not data:  # daca nu primim ne oprim
                break
            print("Received data: ", data)
            connect.send(data)  # echo
        connect.close()  # inchide conexiunea cu baza de date si elibereaza resursele


class client(Thread):
    def run(self):
        TCP_IP = "127.0.0.1"  # adresa IP pentru IPv4 localhost
        TCP_PORT = 5005       # numarul portului pentru tcp pe care se asculta
        Buffer_size = 1024    # dimensiunea buffer-ului
        message = "Respect"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # construim un socket care are doi parametrii, primul
                                                               # AF_INET care reprezinta familia acestuia iar cel
                                                               # de-al doilea reprezinta conexiunea orientata prin
                                                               # protocolul TCP
        s.connect((TCP_IP, TCP_PORT))  # leaga socket-ul la adresa
        s.send(str.encode(message))  # trebuie sa fie bytes data type
        data = s.recv(Buffer_size)   # primeste data de la socket in bytes data type
        s.close()  # inchide socket-ul

        print("received data:", data)


class conexiuneArduino(Thread):
    def get_data(self):
        if self.connect() == 1:  # daca se poate conecta prin functia connect
            while True:
                while self.port.inWaiting() == 0:  # cat timp portul asteapta
                    print(",,,", )
                    time.sleep(0.2)
                    continue
                recv = self.port.readline()  # citeste pe port pana la timpout
                print(recv)
                time.sleep(2)

    def connect(self):  # Connect to serial port of Arduino, returns 1 for ok connect
        self.serial = "COM6"  # serial portul de la aduino
        self.baud = 9600  # baudrate
        try:
            self.port = serial.Serial(self.serial, self.baud, timeout=3)  # deschide serial portul
            time.sleep(5)
            print("Connected...")
            return 1
        except Exception as e:  # Exceptie in cazul in care nu se poate deschide serial portul
            print("Error connecting to arduino:\t", e)
            return 0

    def run(self):
        self.get_data() # ruleaza functia get_data in thread-ul 3
        # Thread.__init__(self)


class grafice(Thread):
    def run(self):
        # if threading.current_thread() is threading.main_thread(): #plotarea nu mergea pe thread-ul principal si
        # asta verifica daca mere

        s = open("C:/Users/FetCatz/Desktop/pisici/date_temperatura.csv", mode="r", encoding="utf-8-sig").read()
        open("C:/Users/FetCatz/Desktop/pisici/date_temperatura.csv", mode="w", encoding="utf-8").write(s)

        temperatura1, temperatura2, temperatura3, data = np.loadtxt( # deschide text, dintr-un fisier text
            "C:/Users/FetCatz/Desktop/pisici/date_temperatura.csv",
            dtype=str,  # default float
            unpack=True, # default False
            delimiter=",")

        t1 = [float(i) for i in temperatura1]  # list comprehension care face o lista cu valori float
        t2 = [float(i) for i in temperatura2]  # list comprehension care face o lista cu valori float
        t3 = [float(i) for i in temperatura3]  # list comprehension care face o lista cu valori float
        fig0 = plt.figure()  # intai creez figura si dupa o umplu cu date si o afisez
        plt.plot(data, t1, "r", data, t2, "b", data, t3, "g")  # plotarea graficului

        plt.title("Temperatura in functie de timp")  # titlul graficuli
        plt.ylabel("Temperatura")  # abscisa y
        plt.xlabel("Timp")  # abscisa x

        line1, = plt.plot([], color="r", label="Temperatura 1")  # prima coloana pentru temperatura
        line2, = plt.plot([], color="b", label="Temperatura 2")  # a doua coloana pentru temperatura
        line3, = plt.plot([], color="g", label="Temperatura 3")  # a treia coloana pentru temperatura
        plt.legend(handles=[line1, line2, line3], loc=1, prop={"size": 9})  # legenda graficului
        plt.xticks(rotation="vertical", fontsize=8) # pozitionarea verticala pe abscisa x

        if os.path.exists("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "temperatura.png") is True:  # verifica
            os.remove("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "temperatura.png")  # daca exista deja
                                                                                              # imaginea si o strerge
        fig0.savefig("temperatura.png")  # creaza un domeniu pentru imagine
        img0 = cv.imread("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "temperatura.png")  # calea imaginii
        cv.imshow("image0", img0)  # afisarea imaginii
        cv.waitKey(1)  # afiseaza imaginea timp de o secunda
        plt.close(fig0)  # inchide domeniul pentru imagine
        # am procedat asa deoarece plt.show() nu putea sa functioneze cum trebuie in intermediul thread-ului
        # Pentru Umiditate

        umiditate1, umiditate2, umiditate3, data2 = np.loadtxt("C:/Users/FetCatz/Desktop/pisici/date_umiditate.csv",
                                                               dtype=str,
                                                               unpack=True,
                                                               delimiter=",")

        u1 = [float(i) for i in umiditate1]  # list comprehension care face o lista cu valori float
        u2 = [float(i) for i in umiditate2]  # list comprehension care face o lista cu valori float
        u3 = [float(i) for i in umiditate3]  # list comprehension care face o lista cu valori float
        fig1 = plt.figure()
        plt.plot(data2, u1, "r", data2, u2, "b", data2, u3, "g")

        plt.title("Umiditate  in functie de timp")
        plt.ylabel("Umiditate")
        plt.xlabel("Timp")

        line1, = plt.plot([], color="r", label="Umiditatea 1")
        line2, = plt.plot([], color="b", label="Umiditatea 2")
        line3, = plt.plot([], color="g", label="Umiditatea 3")
        plt.legend(handles=[line1, line2, line3], loc=4, prop={"size": 13})
        plt.xticks(rotation="vertical", fontsize=8)

        if os.path.exists("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "umiditate.png") is True:
            os.remove("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "umiditate.png")

        fig1.savefig("umiditate.png")
        img1 = cv.imread("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "umiditate.png")
        cv.imshow("Figure 1", img1)
        cv.waitKey(1)
        plt.close(fig1)

        # Pentru Viteza

        viteza, data3 = np.loadtxt("C:/Users/FetCatz/Desktop/pisici/date_viteza.csv",
                                   dtype=str,
                                   unpack=True,
                                   delimiter=",")

        v = [float(i) for i in viteza]  # list comprehension care face o lista cu valori float
        fig2 = plt.figure()
        plt.plot(data3, v)

        plt.title("Viteza in functie de timp")
        plt.ylabel("Viteza")
        plt.xlabel("Timp")

        line1, = plt.plot([], color="r", label="Viteza")
        plt.legend(handles=[line1], loc=1, prop={"size": 15})
        plt.xticks(rotation="vertical", fontsize=8)

        if os.path.exists("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "viteza.png") is True:
            os.remove("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "viteza.png")

        fig2.savefig("viteza.png")
        img2 = cv.imread("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "viteza.png")
        cv.imshow("image2", img2)
        cv.waitKey(1)
        plt.close(fig2)

        # Pentru prezenta

        prezenta1, prezenta2, data4 = np.loadtxt("C:/Users/FetCatz/Desktop/pisici/date_prezenta.csv",
                                                 dtype=str,
                                                 unpack=True,
                                                 delimiter=",")

        # p1 = [float(i) for i in prezenta1]
        # p2 = [float(i) for i in prezenta2]
        fig3 = plt.figure()
        plt.plot(data4, prezenta1, "r", data4, prezenta2, "b")

        plt.title("Prezenta  in functie de timp")
        plt.ylabel("Prezenta")
        plt.xlabel("Timp")

        line1, = plt.plot([], color="r", label="Prezenta1")
        line2, = plt.plot([], color="b", label="Prezenta2")
        plt.legend(handles=[line1, line2], loc=5, prop={"size": 15})
        plt.xticks(rotation="vertical", fontsize=8)
        if os.path.exists("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "prezenta.png") is True:
            os.remove("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "prezenta.png")

        fig3.savefig("prezenta.png")
        img3 = cv.imread("C:/Users/FetCatz/PycharmProjects/Depresie" + "/" + "prezenta.png")
        cv.imshow("image3", img3)
        cv.waitKey(1)
        plt.close(fig3)

    # Thread.__init__(self)


class thread_checker(Thread):
    print("Starting thread checker...")

    def run(self):
        a_old = []
        a = []
        a = threading.enumerate()  # returneaza o lista cu toate threadurile care sunt in viata
        if a_old != a:
            print("Current threads are: \n")
            for i in threading.enumerate():  # pentru element in lista de thread-uri in viata
                print("\t", i)  # printeaza thread-ul
            time.sleep(2)
            a_old = a


if __name__ == '__main__':  # verifica daca ne aflam in main

    server = server()
    server.start()  # porneste thread-ul server

    client = client()
    client.start()  # porneste thread-ul client

    arduino = conexiuneArduino()
    arduino.start()  # porneste thread-ul arduino

    grafice = grafice()
    grafice.start()  # porneste thread-ul grafice

    threader = thread_checker()
    threader.start()  # porneste thread-ul server
