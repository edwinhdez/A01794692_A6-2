import unittest
import os
import json
import sys
# Añadir el directorio padre de ReservationSytem al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ReservationSytem.src.reservation_system import Hotel, Reservation, Customer, DATA_FOLDER

class TestHotel(unittest.TestCase):
    def setUp(self):
        self.hotel = Hotel("Test Hotel", "Test Location", [101, 102, 103])
        self.customer = Customer("Test Customer", "test@example.com")
        self.reservation = self.hotel.make_reservation(self.customer, 101, "2025-03-01", "2025-03-05")

    def tearDown(self):
        # Eliminar archivos JSON creados durante las pruebas
        try:
            os.remove(os.path.join(DATA_FOLDER, 'Test Hotel.json'))
            os.remove(os.path.join(DATA_FOLDER, 'Test Customer.json'))
        except FileNotFoundError:
            pass

    def test_make_reservation(self):
        self.assertIsNotNone(self.reservation)
        self.assertEqual(self.reservation.customer.name, "Test Customer")
        self.assertEqual(self.reservation.room_number, 101)

    def test_make_reservation_room_already_reserved(self):
        # Intentar hacer una reserva en una habitación ya reservada
        reservation = self.hotel.make_reservation(self.customer, 101, "2025-03-02", "2025-03-06")
        self.assertIsNone(reservation)

    def test_is_room_reserved(self):
        self.assertTrue(self.hotel.is_room_reserved(101, "2025-03-01", "2025-03-05"))
        self.assertFalse(self.hotel.is_room_reserved(102, "2025-03-01", "2025-03-05"))

    def test_cancel_reservation(self):
        self.hotel.cancel_reservation(self.reservation)
        self.assertFalse(self.hotel.is_room_reserved(101, "2025-03-01", "2025-03-05"))

    def test_save_to_file(self):
        self.hotel.save_to_file()
        self.assertTrue(os.path.exists(os.path.join(DATA_FOLDER, 'Test Hotel.json')))

    def test_load_from_file(self):
        self.hotel.save_to_file()
        loaded_hotel = Hotel.load_from_file("Test Hotel")
        self.assertIsNotNone(loaded_hotel)
        self.assertEqual(loaded_hotel.name, "Test Hotel")

    def test_display_info(self):
        self.hotel.display_info()

    def test_modify_info(self):
        self.hotel.modify_info(name="Updated Hotel", location="Updated Location", rooms=[201, 202])
        self.assertEqual(self.hotel.name, "Updated Hotel")
        self.assertEqual(self.hotel.location, "Updated Location")
        self.assertEqual(self.hotel.rooms, [201, 202])

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("Test Customer", "test@example.com")

    def tearDown(self):
        # Eliminar archivos JSON creados durante las pruebas
        try:
            os.remove(os.path.join(DATA_FOLDER, 'Test Customer.json'))
        except FileNotFoundError:
            pass

    def test_save_to_file(self):
        self.customer.save_to_file()
        self.assertTrue(os.path.exists(os.path.join(DATA_FOLDER, 'Test Customer.json')))

    def test_load_from_file(self):
        self.customer.save_to_file()
        loaded_customer = Customer.load_from_file("Test Customer")
        self.assertIsNotNone(loaded_customer)
        self.assertEqual(loaded_customer.name, "Test Customer")

    def test_modify_info(self):
        self.customer.modify_info(name="Updated Customer", email="updated@example.com")
        self.assertEqual(self.customer.name, "Updated Customer")
        self.assertEqual(self.customer.email, "updated@example.com")

    def test_display_info(self):
        self.customer.display_info()

class TestReservation(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("Test Customer", "test@example.com")
        self.reservation = Reservation(self.customer, 101, "2025-03-01", "2025-03-05")

    def test_to_dict(self):
        res_dict = self.reservation.to_dict()
        self.assertEqual(res_dict['customer']['name'], "Test Customer")
        self.assertEqual(res_dict['room_number'], 101)

    def test_from_dict(self):
        res_dict = self.reservation.to_dict()
        new_reservation = Reservation.from_dict(res_dict)
        self.assertEqual(new_reservation.customer.name, "Test Customer")
        self.assertEqual(new_reservation.room_number, 101)

if __name__ == '__main__':
    unittest.main()