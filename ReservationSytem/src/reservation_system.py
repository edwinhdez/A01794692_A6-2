"""
Este módulo define las clases y métodos para gestionar un sistema de reservas de hotel.
"""

import json
import os
from abc import ABC, abstractmethod

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_FOLDER, exist_ok=True)


class AbstractHotel(ABC):
    """
    Clase abstracta para definir la interfaz de un hotel.
    """

    @abstractmethod
    def make_reservation(self, customer, room_number, check_in, check_out):
        """
        Realiza una reserva en el hotel.
        """
        pass

    @abstractmethod
    def is_room_reserved(self, room_number, check_in, check_out):
        """
        Verifica si una habitación está reservada en un rango de fechas.
        """
        pass

    @abstractmethod
    def cancel_reservation(self, reservation):
        """
        Cancela una reserva en el hotel.
        """
        pass

    @abstractmethod
    def save_to_file(self):
        """
        Guarda la información del hotel en un archivo.
        """
        pass

    @staticmethod
    @abstractmethod
    def load_from_file(name):
        """
        Carga la información del hotel desde un archivo.
        """
        pass

    @abstractmethod
    def display_info(self):
        """
        Muestra la información del hotel.
        """
        pass

    @abstractmethod
    def modify_info(self, name=None, location=None, rooms=None):
        """
        Modifica la información del hotel.
        """
        pass


class Hotel(AbstractHotel):
    """
    Clase que representa un hotel.
    """

    def __init__(self, name, location, rooms):
        self.name = name
        self.location = location
        self.rooms = rooms
        self.reservations = []

    def make_reservation(self, customer, room_number, check_in, check_out):
        if room_number in self.rooms and not self.is_room_reserved(
            room_number, check_in, check_out
        ):
            reservation = Reservation(customer, room_number, check_in, check_out)
            self.reservations.append(reservation)
            self.save_to_file()
            return reservation
        return None

    def is_room_reserved(self, room_number, check_in, check_out):
        for reservation in self.reservations:
            if (
                reservation.room_number == room_number
                and not (check_out <= reservation.check_in or check_in >= reservation.check_out)
            ):
                return True
        return False

    def cancel_reservation(self, reservation):
        if reservation in self.reservations:
            self.reservations.remove(reservation)
            self.save_to_file()

    def save_to_file(self):
        data = {
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms,
            "reservations": [res.to_dict() for res in self.reservations],
        }
        with open(os.path.join(DATA_FOLDER, f"{self.name}.json"), "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_from_file(name):
        try:
            with open(os.path.join(DATA_FOLDER, f"{name}.json"), "r", encoding="utf-8") as file:
                data = json.load(file)
                hotel = Hotel(data["name"], data["location"], data["rooms"])
                hotel.reservations = [
                    Reservation.from_dict(res) for res in data["reservations"]
                ]
                return hotel
        except FileNotFoundError:
            print(f"Error: File '{name}.json' not found.")
        except json.JSONDecodeError:
            print(f"Error: File '{name}.json' contains invalid JSON.")
        except KeyError as e:
            print(f"Error: Missing key {e} in file '{name}.json'.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

    def display_info(self):
        print(f"Hotel Name: {self.name}")
        print(f"Location: {self.location}")
        print(f"Rooms: {self.rooms}")
        print(f"Reservations: {len(self.reservations)}")

    def modify_info(self, name=None, location=None, rooms=None):
        if name:
            self.name = name
        if location:
            self.location = location
        if rooms:
            self.rooms = rooms
        self.save_to_file()


class AbstractReservation(ABC):
    """
    Clase abstracta para definir la interfaz de una reserva.
    """

    @abstractmethod
    def to_dict(self):
        """
        Convierte la reserva a un diccionario.
        """
        pass

    @staticmethod
    @abstractmethod
    def from_dict(data):
        """
        Crea una reserva a partir de un diccionario.
        """
        pass


class Reservation(AbstractReservation):
    """
    Clase que representa una reserva.
    """

    def __init__(self, customer, room_number, check_in, check_out):
        self.customer = customer
        self.room_number = room_number
        self.check_in = check_in
        self.check_out = check_out

    def to_dict(self):
        return {
            "customer": self.customer.to_dict(),
            "room_number": self.room_number,
            "check_in": self.check_in,
            "check_out": self.check_out,
        }

    @staticmethod
    def from_dict(data):
        customer = Customer.from_dict(data["customer"])
        return Reservation(customer, data["room_number"], data["check_in"], data["check_out"])


class AbstractCustomer(ABC):
    """
    Clase abstracta para definir la interfaz de un cliente.
    """

    @abstractmethod
    def save_to_file(self):
        """
        Guarda la información del cliente en un archivo.
        """
        pass

    @staticmethod
    @abstractmethod
    def load_from_file(name):
        """
        Carga la información del cliente desde un archivo.
        """
        pass

    @abstractmethod
    def display_info(self):
        """
        Muestra la información del cliente.
        """
        pass

    @abstractmethod
    def modify_info(self, name=None, email=None):
        """
        Modifica la información del cliente.
        """
        pass

    @abstractmethod
    def to_dict(self):
        """
        Convierte el cliente a un diccionario.
        """
        pass

    @staticmethod
    @abstractmethod
    def from_dict(data):
        """
        Crea un cliente a partir de un diccionario.
        """
        pass


class Customer(AbstractCustomer):
    """
    Clase que representa un cliente.
    """

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def save_to_file(self):
        data = {"name": self.name, "email": self.email}
        with open(os.path.join(DATA_FOLDER, f"{self.name}.json"), "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_from_file(name):
        try:
            with open(os.path.join(DATA_FOLDER, f"{name}.json"), "r", encoding="utf-8") as file:
                data = json.load(file)
                return Customer(data["name"], data["email"])
        except FileNotFoundError:
            print(f"Error: File '{name}.json' not found.")
        except json.JSONDecodeError:
            print(f"Error: File '{name}.json' contains invalid JSON.")
        except KeyError as e:
            print(f"Error: Missing key {e} in file '{name}.json'.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

    def display_info(self):
        print(f"Customer Name: {self.name}")
        print(f"Email: {self.email}")

    def modify_info(self, name=None, email=None):
        if name:
            self.name = name
        if email:
            self.email = email
        self.save_to_file()

    def to_dict(self):
        return {"name": self.name, "email": self.email}

    @staticmethod
    def from_dict(data):
        return Customer(data["name"], data["email"])


# En accion
if __name__ == "__main__":
    # Crear un hotel
    hotel = Hotel("Grand Hotel", "New York", [101, 102, 103, 104, 105])
    hotel.save_to_file()

    # Cargar un hotel
    loaded_hotel = Hotel.load_from_file("Grand Hotel")
    if loaded_hotel:
        loaded_hotel.display_info()

    # Crear un cliente
    customer = Customer("John Doe", "john.doe@example.com")
    customer.save_to_file()

    # Cargar un cliente
    loaded_customer = Customer.load_from_file("John Doe")
    if loaded_customer:
        loaded_customer.display_info()

    # Hacer una reserva
    reservation = loaded_hotel.make_reservation(
        loaded_customer, 101, "2025-03-01", "2025-03-05"
    )
    if reservation:
        print(
            f"Reservation successful for {reservation.customer.name} in room "
            f"{reservation.room_number}"
        )
    else:
        print("Reservation failed")

    # Cancelar una reserva
    loaded_hotel.cancel_reservation(reservation)
    print("Reservation cancelled")

# Añadir una nueva línea al final del archivo
