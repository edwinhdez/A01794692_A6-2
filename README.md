# Reservation System

Este proyecto implementa un sistema de reservas para hoteles utilizando clases abstractas en Python. El sistema permite crear hoteles, clientes y reservas, y maneja la persistencia de datos utilizando archivos JSON.

## Estructura del Proyecto

El proyecto contiene las siguientes clases principales:

### Clases Abstractas

1. **AbstractHotel**
    - `make_reservation(self, customer, room_number, check_in, check_out)`
    - `is_room_reserved(self, room_number, check_in, check_out)`
    - `cancel_reservation(self, reservation)`
    - `save_to_file(self)`
    - `load_from_file(name)`
    - `display_info(self)`
    - `modify_info(self, name=None, location=None, rooms=None)`

2. **AbstractReservation**
    - `to_dict(self)`
    - `from_dict(data)`

3. **AbstractCustomer**
    - `save_to_file(self)`
    - `load_from_file(name)`
    - `display_info(self)`
    - `modify_info(self, name=None, email=None)`
    - `to_dict(self)`
    - `from_dict(data)`

### Clases Concretas

1. **Hotel (hereda de AbstractHotel)**
    - `__init__(self, name, location, rooms)`
    - `make_reservation(self, customer, room_number, check_in, check_out)`
    - `is_room_reserved(self, room_number, check_in, check_out)`
    - `cancel_reservation(self, reservation)`
    - `save_to_file(self)`
    - `load_from_file(name)`
    - `display_info(self)`
    - `modify_info(self, name=None, location=None, rooms=None)`

2. **Reservation (hereda de AbstractReservation)**
    - `__init__(self, customer, room_number, check_in, check_out)`
    - `to_dict(self)`
    - `from_dict(data)`

3. **Customer (hereda de AbstractCustomer)**
    - `__init__(self, name, email)`
    - `save_to_file(self)`
    - `load_from_file(name)`
    - `display_info(self)`
    - `modify_info(self, name=None, email=None)`
    - `to_dict(self)`
    - `from_dict(data)`

## Uso del Sistema

### Crear un Hotel

```python
hotel = Hotel("Grand Hotel", "New York", [101, 102, 103, 104, 105])
hotel.save_to_file()
```

### Cargar un Hotel
```python
loaded_hotel = Hotel.load_from_file("Grand Hotel")
if loaded_hotel:
    loaded_hotel.display_info()
```

### Crear un Cliente
```python
customer = Customer("John Doe", "john.doe@example.com")
customer.save_to_file()
```

### Cargar un Cliente
```python
loaded_customer = Customer.load_from_file("John Doe")
if loaded_customer:
    loaded_customer.display_info()
```

### Hacer una Reserva
```python
reservation = loaded_hotel.make_reservation(loaded_customer, 101, "2025-03-01", "2025-03-05")
if reservation:
    print(f"Reservation successful for {reservation.customer.name} in room {reservation.room_number}")
else:
    print("Reservation failed")
```

### Hacer una Reserva
```python
loaded_hotel.cancel_reservation(reservation)
print("Reservation cancelled")
```

## Estructura de Archivos
- `**reservation_system.py:** Contiene la implementación de las clases abstractas y concretas para el sistema de reservas.`

data/: Carpeta donde se almacenan los archivos JSON con la información de los hoteles y clientes.
Requisitos
Python 3.x
Biblioteca json
Biblioteca abc