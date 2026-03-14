import csv
from collections import deque, Counter
from heapq import heappush, heappop
from tabulate import tabulate
import os

class Patient:
    def __init__(self, pid, name, age, disease, severity):
        self.pid = pid
        self.name = name
        self.age = age
        self.disease = disease
        self.severity = severity  

    def __lt__(self, other):
        return self.severity > other.severity

class Hospital:
    def __init__(self):
        self.patients = {}  
        self.emergency_queue = [] 
        self.normal_queue = deque()

    def add_patient(self, pid, name, age, disease, severity):
        if pid in self.patients:
            print(f"\n Patient ID {pid} already exists!")
            return
        if not (1 <= severity <= 10):
            print("\n Severity must be 1-10.")
            return
        if age <= 0:
            print("\n Age must be positive.")
            return

        patient = Patient(pid, name, age, disease, severity)
        self.patients[pid] = patient

        if severity >= 8:
            heappush(self.emergency_queue, patient)
        else:
            self.normal_queue.append(patient)

        print(f"\n Patient {name} added successfully.")

    def search_patient(self, pid):
        return self.patients.get(pid, None)

    def delete_patient(self, pid):
        patient = self.patients.pop(pid, None)
        if not patient:
            print("\n Patient not found.")
            return

        try:
            self.emergency_queue.remove(patient)
            from heapq import heapify
            heapify(self.emergency_queue)
        except ValueError:
            pass
        try:
            self.normal_queue.remove(patient)
        except ValueError:
            pass

        print(f"\n Patient {patient.name} deleted successfully.")

    def display_patients(self):
        if not self.patients:
            print("\n No patients available.")
            return

        table = []
        for p in self.patients.values():
            table.append([p.pid, p.name, p.age, p.disease, p.severity])
        print("\n" + tabulate(table, headers=["ID", "Name", "Age", "Disease", "Severity"], tablefmt="fancy_grid"))

    def display_queues(self):
        if self.emergency_queue:
            print("\nEmergency Queue (Severity ≥8):")
            table = [[idx+1, p.name, p.disease, p.severity] for idx, p in enumerate(self.emergency_queue)]
            print(tabulate(table, headers=["No.", "Name", "Disease", "Severity"], tablefmt="fancy_grid"))
        else:
            print("\nNo emergency patients.")

        if self.normal_queue:
            print("\nNormal Queue (Severity <8):")
            table = [[idx+1, p.name, p.disease, p.severity] for idx, p in enumerate(self.normal_queue)]
            print(tabulate(table, headers=["No.", "Name", "Disease", "Severity"], tablefmt="fancy_grid"))
        else:
            print("\nNo normal patients.")

    def serve_emergency(self):
        if not self.emergency_queue:
            print("\n No emergency patients to serve.")
            return
        patient = heappop(self.emergency_queue)
        self.patients.pop(patient.pid, None)
        print(f"\n Serving Emergency Patient: {patient.name} (Disease: {patient.disease}, Severity: {patient.severity})")

    def serve_normal(self):
        if not self.normal_queue:
            print("\n No normal patients to serve.")
            return
        patient = self.normal_queue.popleft()
        self.patients.pop(patient.pid, None)
        print(f"\n Serving Normal Patient: {patient.name} (Disease: {patient.disease}, Severity: {patient.severity})")

    def save_to_csv(self, filename="patients.csv"):
        if os.path.exists(filename):
            os.rename(filename, filename+".bak")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Age", "Disease", "Severity"])
            for p in list(self.patients.values()) + list(self.emergency_queue) + list(self.normal_queue):
                writer.writerow([p.pid, p.name, p.age, p.disease, p.severity])
        print(f"\n Records saved to {filename}")

    def load_from_csv(self, filename="patients.csv"):
        try:
            with open(filename, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.add_patient(int(row["ID"]), row["Name"], int(row["Age"]), row["Disease"], int(row["Severity"]))
            print(f"\n Records loaded from {filename}")
        except FileNotFoundError:
            print("\n No existing file found. Starting fresh.")

    def show_stats(self):
        total = len(self.patients)
        emergency_pending = len(self.emergency_queue)
        normal_pending = len(self.normal_queue)
        disease_count = Counter([p.disease for p in self.patients.values()])
        print(f"\n Statistics: Total Patients: {total}, Emergency Pending: {emergency_pending}, Normal Pending: {normal_pending}")
        print("Most common diseases:", disease_count.most_common(5))

def main():
    hospital = Hospital()
    hospital.load_from_csv()

    while True:
        print("\n===== Hospital Management System =====")
        print("1. Add Patient")
        print("2. Search Patient by ID")
        print("3. Delete Patient by ID")
        print("4. Display All Patients")
        print("5. Display Queues")
        print("6. Serve Next Emergency Patient")
        print("7. Serve Next Normal Patient")
        print("8. Show Statistics")
        print("9. Save & Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            try:
                pid = int(input("Enter Patient ID: "))
                name = input("Enter Name: ")
                age = int(input("Enter Age: "))
                disease = input("Enter Disease: ")
                severity = int(input("Enter Severity (1-10): "))
                hospital.add_patient(pid, name, age, disease, severity)
            except ValueError:
                print(" Invalid input. Please enter numeric values where required.")

        elif choice == "2":
            pid = int(input("Enter Patient ID: "))
            patient = hospital.search_patient(pid)
            if patient:
                print(f"\n Found: {patient.pid} | {patient.name} | Age: {patient.age} | Disease: {patient.disease} | Severity: {patient.severity}")
            else:
                print("\n Patient not found.")

        elif choice == "3":
            pid = int(input("Enter Patient ID to delete: "))
            hospital.delete_patient(pid)

        elif choice == "4":
            hospital.display_patients()

        elif choice == "5":
            hospital.display_queues()

        elif choice == "6":
            hospital.serve_emergency()

        elif choice == "7":
            hospital.serve_normal()

        elif choice == "8":
            hospital.show_stats()

        elif choice == "9":
            hospital.save_to_csv()
            print("\n Exiting system. Goodbye!")
            break

        else:
            print("\n Invalid choice. Try again.")

if __name__ == "__main__":
    main()
