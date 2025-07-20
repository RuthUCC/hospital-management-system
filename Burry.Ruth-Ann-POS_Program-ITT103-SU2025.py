
from datetime import datetime    #Imports datetime module to help with date formatting and error handling

#Creat our first class (super class)
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    # function or method to display attributes of the person class
    def display(self):
        print(f"Name: {self.name}".upper(),
              f"\nAge: {self.age}",
              f"\nGender: {self.gender}".upper())

#Second class
class Patient(Person):
    id_counter = 1

    def __init__(self, name, age, gender):
        super().__init__(name, age, gender)
        self.patient_id = f"PAT{Patient.id_counter:04d}"  #formatted string used to generate patient id
        Patient.id_counter += 1
        self.appointment_list = []

    #Function or method to display details or attributes of a patient
    def display_profile(self):
        print(f"\n*****Patient Profile*****",
              f"\nPatient ID: {self.patient_id}")
        self.display()

#Our third class
class Doctor(Person):
    id_counter = 1

    def __init__(self, name, age, gender, specialty, schedule):
        super().__init__(name, age, gender)
        self.doctor_id = f"DOC{Doctor.id_counter:04d}"  #Formatted string is used to generate doctor id
        Doctor.id_counter += 1
        self.specialty = specialty

        self.schedule = []   #stores doctor's schedule as a list
        for entry in schedule:   #We use a for loop to gp through each entry in doctor's schedule
            if isinstance(entry, str):  #checks to see if entry is a string
                parts = entry.strip().split(" ")  #strips any spaces from start and end of string entry and splits it into list of two parts
                if len(parts) == 2:
                    self.schedule.append((parts[0], parts[1]))  #Adds the two parts of the split string to the doctor's schedule

    #Function or method to display doctor's schedule
    def display_schedule(self):
        formatted_schedule = [f"{date} {time}" for (date, time) in self.schedule]
        print(f"\n*****Doctor Schedule*****",
              f"\nDoctor ID: {self.doctor_id}")
        self.display()
        print(f"\nSpecialty: {self.specialty}".upper(),
              f"\nAvailable Times: {', '.join(formatted_schedule)}")

    #Function or method to display doctor's availability
    def is_available(self, date, time):
        return (date, time) in self.schedule

#Creating our 4th class
class Appointment:
    id_counter = 1

    def __init__(self, patient, doctor, date, time):
        self.appointment_id = f"APP{Appointment.id_counter:04d}"  #Creates appointment id as formatted string
        Appointment.id_counter += 1
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = "Confirmed"

    #Function or method to confirm an appointment
    def confirm(self):
        self.status = "confirmed"
        print(f"Appointment {self.appointment_id} has been confirmed for {self.date} at {self.time}.",
              f"\nPatient: {self.patient}",
              f"\nDoctor: {self.doctor}",
              f"\nStatus: {self.status}")

    #Function or method to cancel an appointment
    def cancel(self):
        self.status = "cancelled"
        print(f"Appointment {self.appointment_id} has been {self.status}.")

#Creating our fifth and biggest class
class HospitalSystem:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.appointments = {}

    #Function or method to add or register patient
    def add_patient(self, name, age, gender):
        patient = Patient(name, age, gender)
        self.patients[patient.patient_id] = patient
        print(f"Patient has been registered with ID: {patient.patient_id}")

    #Function or method to add a doctor
    def add_doctor(self, name, age, gender, specialty, schedule):
        doctor = Doctor(name, age, gender, specialty, schedule)
        self.doctors[doctor.doctor_id] = doctor
        print(f"Doctor has been added with ID: {doctor.doctor_id}")

    #Function or method to book an appointment
    def book_appointment(self, patient_id, doctor_id, date, time):
        try:
            patient = self.patients[patient_id]
            doctor = self.doctors[doctor_id]

            #Check for double booking
            for appointment in self.appointments.values():
                if (appointment.doctor.doctor_id == doctor_id and
                        appointment.date == date and appointment.time == time and
                        appointment.status == "Confirmed"):
                    raise Exception("Doctor already has an appointment at this time.")

            #Use the is_available() method from the Doctor class to print message if doctor is not available
            if not doctor.is_available(date, time):
                raise Exception("Doctor is not available at this date and time.")

            appointment = Appointment(patient, doctor, date, time)
            self.appointments[appointment.appointment_id] = appointment
            patient.appointment_list.append(appointment)  #Adds appointment to patient history
            print(f"Appointment booked successfully with ID: {appointment.appointment_id}")

        except KeyError:
            print("Invalid patient or doctor ID.") #Happens if the user types an ID that doesn't exist in the dictionary.
        except Exception as e:     #Catches any other error and stores the error message as 'e'
            print(f"Error booking appointment: {e}")

    #Function or method to cancel an appointment
    def cancel_appointment(self, appointment_id):
        try:
            appointment = self.appointments[appointment_id]
            appointment.cancel()
        except KeyError:   #Handles an error of the appointment id entered by user is not found
            print("Appointment ID not found.")

    #Function or method to generate bill
    def generate_bill(self, appointment_id):
        try:
            appointment = self.appointments[appointment_id]
            if appointment.status != "Confirmed":
                print("No bill can be generated for a cancelled appointment.")
                return

            print("\n========== PRINCESS MARGARET HOSPITAL ==========")
            print(f"Appointment ID: {appointment.appointment_id}")
            print(f"Patient Name : {appointment.patient.name}")
            print(f"Doctor       : {appointment.doctor.name}")
            print(f"Specialty    : {appointment.doctor.specialty}")
            print(f"Date         : {appointment.date}")
            print(f"Time         : {appointment.time}")
            print("\n--- Charges ---")
            consultation_fee = 3000
            print(f"Consultation Fee: JMD ${consultation_fee}")
            try:
                additional_fee = float(input("Enter additional service fees: JMD "))
            except ValueError:
                print("Invalid amount entered. Additional fees set to $0.")
                additional_fee = 0
            total = consultation_fee + additional_fee
            print(f"Total Amount Due: JMD ${total}")
            print("==================================\n")
        except KeyError:  # Handles keyerror if a matching key is not found within dictionary
            print("Appointment not found.")

#Helper function to validate age input from user
def validateage():
    while True:
        age = input("Enter age: ").strip()
        try:
            age = int(age)
            if age <= 0:
                print("Age must be a positive number.")
            else:
                return age
        except ValueError:
            print("Invalid input. Please enter a number.")

#Helper function that validates name input from user
def get_valid_name():
        while True:
            name = input("Enter name: ").strip()
            if name == "":
                print("Name cannot be empty.")
            elif name.replace(" ", "").isalpha():
                return name
            else:
                print("Name should only contain letters.")

#Helper function that validates gender input from user
def get_valid_gender():
        valid_genders = ["male", "female", "other"]

        while True:
            gender = input("Enter gender (Male/Female/Other): ").strip().lower()

            if gender in valid_genders:
                return gender.capitalize()    #Returns capitalized version of gender input if valid
            else:
                print("Invalid input. Please enter 'Male', 'Female', or 'Other'.")

#Helper function that validates date input from user with the aid of the imported datetime module
def get_valid_date():
    while True:
        date_input = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            valid_date = datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

#Helper function that validates time input from user with the aid of the datetime module imported
def get_valid_time():
    while True:
        time_input = input("Enter time (HH:MM, 24-hour format): ").strip()
        try:
            datetime.strptime(time_input, "%H:%M")
            return time_input
        except ValueError:
            print("Invalid time format. Please use HH:MM (e.g., 14:30).")


#Function that displays the menu options to the user and processes their selection
def main_menu():
    hospital = HospitalSystem()

    while True:
        print("""\nWELCOME TO THE HOSPITAL MANAGEMENT SYSTEM.
        \nWhat would you like to do today?
        \n1. Register New Patient
        \n2. Add New Doctor
        \n3. View Patient Profile
        \n4. View Doctor Schedule
        \n5. Book Appointment
        \n6. Cancel Appointment
        \n7. Generate Bill
        \n8. Exit""")

        choice = input("Select an option (1–8): ")

        if choice == "1":
            name = get_valid_name()
            age = validateage()
            gender = get_valid_gender()
            hospital.add_patient(name, age, gender)

        elif choice == "2":
            name = get_valid_name()
            age = validateage()
            gender = get_valid_gender()
            specialty = input("Enter doctor's specialty: ")
            schedule_input = input("Enter available schedule (comma-separated date and time e.g. 2025-07-18 10:00,2025-07-18 11:00): ")
            schedule = [entry.strip() for entry in schedule_input.split(",")]
            hospital.add_doctor(name, age, gender, specialty, schedule)

        elif choice == "3":
            pid = input("Enter patient ID (e.g. PAT0001): ")
            if pid in hospital.patients:
                hospital.patients[pid].display_profile()  # checks to esnure patient id is in hospital system
            else:
                print("Patient not found.")

        elif choice == "4":
            did = input("Enter doctor ID (e.g. DOC0001): ")
            if did in hospital.doctors:  # checks to ensure doctor id is in hospital system
                hospital.doctors[did].display_schedule()
            else:
                print("Doctor not found.")

        elif choice == "5":
            pid = input("Enter patient ID: ")
            did = input("Enter doctor ID: ")
            date = get_valid_date()
            time = get_valid_time()
            hospital.book_appointment(pid, did, date, time)

        elif choice == "6":
            aid = input("Enter appointment ID to cancel (e.g. APP0001): ")
            hospital.cancel_appointment(aid)

        elif choice == "7":
            aid = input("Enter appointment ID to generate bill (e.g. A001): ")
            hospital.generate_bill(aid)

        elif choice == "8":
            print("Thanks for coming. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


# This next line will call on the main_menu() function to run our program
main_menu()