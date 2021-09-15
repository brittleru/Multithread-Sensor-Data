# Multithread-Sensor-Data Arduino and TCP/IP (local host) connection and plotting sensor data CSV.

This is a project I had in university in the third year at the Java and Python Programming course. This course was taught by Conf. Dr. Ing. Victor Constantin.
</br></br>
After parsing and creating the CSV with the data from the sensors in Java, I had to plot that data in different windows for each type of data (one graph for temperature, one for humidity, one for presence and one for velocity). The plotting had to be on a different thread. Here I had a problem with plotting and I had to show images instead. I used OpenCV for it and so I checked if there exists an image already and deleted it if so, after that I created a domain for the image, show it for one second and close the domain. I did this because <code>plt.show()</code> could not work properly through the thread.
</br></br>
For bonus points there were two more tasks, one to connect to the microcontroller and send the data on a separate thread and another one to connect with TCP/IP port at the Python application in a separate thread. To do that so I created a class "conexiuneArduino(Thread)" which had the functions "get_data()", "connect()" and "run()", the connect function returned 1 if it could connect to Arduino, else if it couldn't open the serial port it would return 0, the function get_data would sleep for 0.2 seconds if the port was waiting and would read on the port until timeout otherwise, the run function would run the function get_data on a separate thread. For the TCP/IP connectivity I created two classes "server(Thread)" and "client(Thread)". The server class would be on the IPv4 IP address localhost <code>127.0.0.1</code>, listening on the TCP port 5005 and a buffer size of 20 (we want it to be fast, in normal case it should be 1024), the client class tries to connect to the server, encode the data (in this case it's a string "Respect") and send it to the server. I also have a class "thread_checker(Thread)" which is looking for alive threads.

## Here are the results:

### The graph for the temperature values:
![tepmerature graph](https://github.com/brittleru/Multithread-Sensor-Data/blob/master/images/temperatura.png?raw=true)

### The graph for the humidity values:
![humidity graph](https://github.com/brittleru/Multithread-Sensor-Data/blob/master/images/umiditate.png?raw=true)

### The graph for the velocity value:
![velocity graph](https://github.com/brittleru/Multithread-Sensor-Data/blob/master/images/viteza.png?raw=true)

### The graph for the presence values:
![presence graph](https://github.com/brittleru/Multithread-Sensor-Data/blob/master/images/prezenta.png?raw=true)

### Screenshot for Python-Arduino connection:
![arduino connection](https://github.com/brittleru/Multithread-Sensor-Data/blob/master/images/adru_results.png?raw=true)

### Screenshot from the Python console:
![python console](https://github.com/brittleru/Multithread-Sensor-Data/blob/master/images/results.png?raw=true)
