import matplotlib
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd
import datetime
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

style.use("ggplot")
# Pentru Temperatura

#
# def decode(s):
#     for encoding in "utf-8-sig", "utf-16":
#         try:
#             return s.decode(encoding)
#         except UnicodeDecodeError:
#             continue
#     return s.decode("latin-1")
#
#
# fp = open("C:/Users/FetCatz/Desktop/pisici/date_temperatura.csv")
# s = fp.read()
# u = s.decode("utf-8-sig")
# s = u.encode("utf-8")

s = open("C:/Users/FetCatz/Desktop/pisici/date_temperatura.csv", mode = "r", encoding = "utf-8-sig").read()
open("C:/Users/FetCatz/Desktop/pisici/date_temperatura.csv", mode = "w", encoding = "utf-8").write(s)

temperatura1, temperatura2, temperatura3, data = np.loadtxt("C:/Users/FetCatz/Desktop/pisici/date_temperatura.csv",
                                                            dtype = str,  # default float
                                                            unpack = True,
                                                            delimiter = ",")

t1 = [float(i) for i in temperatura1]
t2 = [float(i) for i in temperatura2]
t3 = [float(i) for i in temperatura3]
plt.plot(data, t1, "r", data, t2, "b", data, t3, "g")

plt.title("Temperatura in functie de timp")
plt.ylabel("Temperatura")
plt.xlabel("Timp")

line1, = plt.plot([], color = "r", label = "Temperatura 1")
line2, = plt.plot([], color = "b", label = "Temperatura 2")
line3, = plt.plot([], color = "g", label = "Temperatura 3")
plt.legend(handles = [line1, line2, line3], loc = 1, prop = {"size": 9})
plt.xticks(rotation = "vertical", fontsize = 8)
plt.show()

# Pentru Umiditate

umiditate1, umiditate2, umiditate3, data2 = np.loadtxt("C:/Users/FetCatz/Desktop/pisici/date_umiditate.csv",
                                                       dtype = str,
                                                       unpack = True,
                                                       delimiter = ",")

u1 = [float(i) for i in umiditate1]
u2 = [float(i) for i in umiditate2]
u3 = [float(i) for i in umiditate3]
plt.plot(data2, u1, "r", data2, u2, "b", data2, u3, "g")

plt.title("Umiditate  in functie de timp")
plt.ylabel("Umiditate")
plt.xlabel("Timp")

line1, = plt.plot([], color = "r", label = "Umiditatea 1")
line2, = plt.plot([], color = "b", label = "Umiditatea 2")
line3, = plt.plot([], color = "g", label = "Umiditatea 3")
plt.legend(handles = [line1, line2, line3], loc = 4, prop = {"size": 13})
plt.xticks(rotation = "vertical", fontsize = 8)
plt.show()

# Pentru Viteza


viteza, data3 = np.loadtxt("C:/Users/FetCatz/Desktop/pisici/date_viteza.csv",
                           dtype = str,
                           unpack = True,
                           delimiter = ",")

v = [float(i) for i in viteza]
plt.plot(data3, v)

plt.title("Viteza in functie de timp")
plt.ylabel("Viteza")
plt.xlabel("Timp")

line1, = plt.plot([], color = "r", label = "Viteza")
plt.legend(handles = [line1], loc = 1, prop = {"size": 15})
plt.xticks(rotation = "vertical", fontsize = 8)
plt.show()

# Pentru prezenta

prezenta1, prezenta2, data4 = np.loadtxt("C:/Users/FetCatz/Desktop/pisici/date_prezenta.csv",
                                         dtype = str,
                                         unpack = True,
                                         delimiter = ",")

# p1 = [float(i) for i in prezenta1]
# p2 = [float(i) for i in prezenta2]
plt.plot(data4, prezenta1, "r", data4, prezenta2, "b")

plt.title("Prezenta  in functie de timp")
plt.ylabel("Prezenta")
plt.xlabel("Timp")

line1, = plt.plot([], color = "r", label = "Prezenta1")
line2, = plt.plot([], color = "b", label = "Prezenta2")
plt.legend(handles = [line1, line2], loc = 5, prop = {"size": 15})
plt.xticks(rotation = "vertical", fontsize = 8)
plt.show()
