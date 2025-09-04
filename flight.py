import tkinter as tk
from tkinter import messagebox, ttk

# Mock Data
flights = [
    {"Flight ID": "FL001", "Departure": "New York", "Arrival": "London", "Date": "2025-01-10", "Time": "10:00", "Seats Available": 10},
    {"Flight ID": "FL002", "Departure": "Paris", "Arrival": "Tokyo", "Date": "2025-01-15", "Time": "14:00", "Seats Available": 5},
    {"Flight ID": "FL003", "Departure": "Sydney", "Arrival": "Dubai", "Date": "2025-02-01", "Time": "22:30", "Seats Available": 8},
    {"Flight ID": "FL004", "Departure": "Berlin", "Arrival": "Rome", "Date": "2025-02-05", "Time": "09:15", "Seats Available": 12},
    {"Flight ID": "FL005", "Departure": "Mumbai", "Arrival": "Singapore", "Date": "2025-02-10", "Time": "06:45", "Seats Available": 7},
]

passengers = [
    {"Passenger ID": "P001", "Name": "Rahul Sharma", "Contact Details": "+91-9876543210"},
    {"Passenger ID": "P002", "Name": "Priya Nair", "Contact Details": "+91-9823456789"},
    {"Passenger ID": "P003", "Name": "Amitabh Joshi", "Contact Details": "+91-9123456780"},
    {"Passenger ID": "P004", "Name": "Sneha Iyer", "Contact Details": "+91-9988776655"},
    {"Passenger ID": "P005", "Name": "Vikram Singh", "Contact Details": "+91-9001122334"},
    {"Passenger ID": "P006", "Name": "Neha Kapoor", "Contact Details": "+91-9786543210"},
    {"Passenger ID": "P007", "Name": "Arjun Reddy", "Contact Details": "+91-9654321876"},
    {"Passenger ID": "P008", "Name": "Pooja Mehta", "Contact Details": "+91-9456123789"},
    {"Passenger ID": "P009", "Name": "Rohan Desai", "Contact Details": "+91-9543216780"},
    {"Passenger ID": "P010", "Name": "Ananya Banerjee", "Contact Details": "+91-9234567890"},
]

bookings = []

class FlightBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Booking System")
        self.root.geometry("900x700")

        self.create_gui()
        self.view_schedule()
        self.view_passengers()
        self.update_booking_list()

    def create_gui(self):
        # Flight Management
        flight_frame = tk.LabelFrame(self.root, text="Flight Management", padx=10, pady=10)
        flight_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(flight_frame, text="Search Flights:").grid(row=0, column=0, padx=5, pady=5)
        self.flight_search_var = tk.StringVar()
        tk.Entry(flight_frame, textvariable=self.flight_search_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(flight_frame, text="Search", command=self.search_flights).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(flight_frame, text="View All", command=self.view_schedule).grid(row=0, column=3, padx=5, pady=5)

        self.flight_tree = ttk.Treeview(flight_frame, columns=("Flight ID", "Departure", "Arrival", "Date", "Time", "Seats Available"), show="headings", height=6)
        for col in self.flight_tree["columns"]:
            self.flight_tree.heading(col, text=col)
            self.flight_tree.column(col, width=120)
        self.flight_tree.grid(row=1, column=0, columnspan=4, pady=5)
        self.flight_tree.bind("<<TreeviewSelect>>", self.select_flight)

        # Passenger Management
        passenger_frame = tk.LabelFrame(self.root, text="Passenger Management", padx=10, pady=10)
        passenger_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(passenger_frame, text="Search Passengers:").grid(row=0, column=0, padx=5, pady=5)
        self.passenger_search_var = tk.StringVar()
        tk.Entry(passenger_frame, textvariable=self.passenger_search_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(passenger_frame, text="Search", command=self.search_passengers).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(passenger_frame, text="View All", command=self.view_passengers).grid(row=0, column=3, padx=5, pady=5)

        self.passenger_tree = ttk.Treeview(passenger_frame, columns=("Passenger ID", "Name", "Contact Details"), show="headings", height=6)
        for col in self.passenger_tree["columns"]:
            self.passenger_tree.heading(col, text=col)
            self.passenger_tree.column(col, width=150)
        self.passenger_tree.grid(row=1, column=0, columnspan=4, pady=5)
        self.passenger_tree.bind("<<TreeviewSelect>>", self.select_passenger)

        # Booking Management
        booking_frame = tk.LabelFrame(self.root, text="Booking Management", padx=10, pady=10)
        booking_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(booking_frame, text="Flight ID:").grid(row=0, column=0, padx=5, pady=5)
        self.flight_id_var = tk.StringVar()
        tk.Entry(booking_frame, textvariable=self.flight_id_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(booking_frame, text="Passenger ID:").grid(row=1, column=0, padx=5, pady=5)
        self.passenger_id_var = tk.StringVar()
        tk.Entry(booking_frame, textvariable=self.passenger_id_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(booking_frame, text="Book Flight", command=self.book_flight).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(booking_frame, text="Cancel Booking", command=self.cancel_booking).grid(row=2, column=1, padx=5, pady=5)

        # Current Bookings
        booking_list_frame = tk.LabelFrame(self.root, text="Current Bookings", padx=10, pady=10)
        booking_list_frame.pack(fill="x", padx=10, pady=5)

        self.booking_tree = ttk.Treeview(booking_list_frame, columns=("Flight ID", "Passenger ID"), show="headings", height=6)
        for col in self.booking_tree["columns"]:
            self.booking_tree.heading(col, text=col)
            self.booking_tree.column(col, width=120)
        self.booking_tree.pack(fill="x")

    # --- Data Display Functions ---
    def view_schedule(self):
        self.flight_tree.delete(*self.flight_tree.get_children())
        for flight in flights:
            self.flight_tree.insert("", "end", values=tuple(flight.values()))

    def search_flights(self):
        query = self.flight_search_var.get().lower()
        self.flight_tree.delete(*self.flight_tree.get_children())
        for flight in flights:
            if any(query in str(value).lower() for value in flight.values()):
                self.flight_tree.insert("", "end", values=tuple(flight.values()))

    def view_passengers(self):
        self.passenger_tree.delete(*self.passenger_tree.get_children())
        for passenger in passengers:
            self.passenger_tree.insert("", "end", values=tuple(passenger.values()))

    def search_passengers(self):
        query = self.passenger_search_var.get().lower()
        self.passenger_tree.delete(*self.passenger_tree.get_children())
        for passenger in passengers:
            if any(query in str(value).lower() for value in passenger.values()):
                self.passenger_tree.insert("", "end", values=tuple(passenger.values()))

    def update_booking_list(self):
        self.booking_tree.delete(*self.booking_tree.get_children())
        for b in bookings:
            self.booking_tree.insert("", "end", values=(b["Flight ID"], b["Passenger ID"]))

    # --- Selection Functions ---
    def select_flight(self, event):
        selected = self.flight_tree.focus()
        if selected:
            values = self.flight_tree.item(selected, "values")
            self.flight_id_var.set(values[0])

    def select_passenger(self, event):
        selected = self.passenger_tree.focus()
        if selected:
            values = self.passenger_tree.item(selected, "values")
            self.passenger_id_var.set(values[0])

    # --- Booking Functions ---
    def book_flight(self):
        flight_id = self.flight_id_var.get()
        passenger_id = self.passenger_id_var.get()

        flight = next((f for f in flights if f["Flight ID"] == flight_id), None)
        passenger = next((p for p in passengers if p["Passenger ID"] == passenger_id), None)

        if not flight:
            messagebox.showerror("Error", "Invalid Flight ID")
            return
        if not passenger:
            messagebox.showerror("Error", "Invalid Passenger ID")
            return
        if flight["Seats Available"] <= 0:
            messagebox.showerror("Error", "No seats available")
            return
        if any(b["Flight ID"] == flight_id and b["Passenger ID"] == passenger_id for b in bookings):
            messagebox.showerror("Error", "Duplicate booking")
            return

        flight["Seats Available"] -= 1
        bookings.append({"Flight ID": flight_id, "Passenger ID": passenger_id})
        self.view_schedule()
        self.update_booking_list()
        messagebox.showinfo("Success", "Flight booked successfully")

    def cancel_booking(self):
        flight_id = self.flight_id_var.get()
        passenger_id = self.passenger_id_var.get()

        booking = next((b for b in bookings if b["Flight ID"] == flight_id and b["Passenger ID"] == passenger_id), None)
        if not booking:
            messagebox.showerror("Error", "No such booking found")
            return

        bookings.remove(booking)
        flight = next(f for f in flights if f["Flight ID"] == flight_id)
        flight["Seats Available"] += 1
        self.view_schedule()
        self.update_booking_list()
        messagebox.showinfo("Success", "Booking cancelled successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = FlightBookingSystem(root)
    root.mainloop()
