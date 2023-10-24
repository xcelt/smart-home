from django.db import models


# simulated weather data
thermostat_data = {
    "Bedroom": "Comfy, 22C",
    "Living Room": "Too hot, 30C",
    "Kitchen": "Tepid, 18C",
    "Dining Room": "Chilly, 15C",
}


while True:
    print("waiting for a connection....")
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    # receive the requested city from the client
    requested_city = client_socket.recv(1024).decode()

    # lookup for weather information for the requested city
    if requested_city in weather_data:
        response = weather_data[requested_city]
    else:
        response = "The requested city is not in the database"

    # send the weather information to the client
    client_socket.send(response.encode())

    client_socket.close()