# 5/20/23 Looking to create a program to open files and use voice to read player files and coaches profiles
# I would like to keep the menu interactive and try to plot out player stats in a graph for effeciency.  
# Due to issues at home my research was delayed to accomodate the family needs.  I spent roughly 2 hours on this project 
# and it is not as polished as I would like. Using speech recognition to write to a file and read from a file, I would like to add this as a player can be registered on the fly
# I would like to use AI to create a file based on the information provided. 

import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import messagebox
import time



# Initialize speech recognition and text to speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Base class representing a person in our application
class Person:
    def __init__(self, name):
        self.name = name
        
# Derived class representing a player inherited from a person with new attribute of jersey and position
class Player(Person):
    def __init__(self, name, jersey_number, position):
        super().__init__(name)
        self.jersey_number = jersey_number
        self.position = position

    def print_info(self):
        return f"Player {self.name} wears jersey number {self.jersey_number} and plays as a {self.position}."

# Derived class representing a coach inherited from a person with attribute of speciality
class Coach(Person):
    def __init__(self, name, specialty_skill):
        super().__init__(name)
        self.specialty_skill = specialty_skill

    def print_info(self):
        return f"Coach {self.name} specializes in {self.specialty_skill}."


# Derived class representing a parent inherited from person with an attribute of having a child in the program.
class Parent(Person):
    def __init__(self, name, child_name):
        super().__init__(name)
        self.child_name = child_name

    def print_info(self):
        return f"{self.name} is the parent of {self.child_name}."
    
# This is the portion to capture the audio message to add a player, coach or parent
def voice_input(prompt=None):
    if prompt:
        engine.say(prompt)
        engine.runAndWait()
        time.sleep(1)  # Add wait time for user to prepare to speak

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, I didn't catch that. Please try again.")
            return None
        except sr.RequestError:
            messagebox.showerror("Error", "There was an issue with the request. Please try again.")
            return None

def create_member():
    name = voice_input("Please say the name.")
    if not name:  # If voice input failed
        return

    if type_selected.get() == "Player":
        jersey_number = voice_input("Please say the jersey number.")
        if not jersey_number:  # If voice input failed
            return
        position = voice_input("Please say the position.")
        if not position:  # If voice input failed
            return
        player = Player(name, jersey_number, position)
        write_to_file(player.print_info())
    elif type_selected.get() == "Coach":
        specialty_skill = voice_input("Please say the specialty skill.")
        if not specialty_skill:  # If voice input failed
            return
        coach = Coach(name, specialty_skill)
        write_to_file(coach.print_info())
    elif type_selected.get() == "Parent":
        child_name = voice_input("Please say the child's name.")
        if not child_name:  # If voice input failed
            return
        parent = Parent(name, child_name)
        write_to_file(parent.print_info())
    messagebox.showinfo("Success", f"{type_selected.get()} Created Successfully")

root = tk.Tk()
root.title("East Bay Soldiers")

type_selected = tk.StringVar()

player_button = tk.Radiobutton(root, text="Player", variable=type_selected, value="Player")
player_button.pack()

coach_button = tk.Radiobutton(root, text="Coach", variable=type_selected, value="Coach")
coach_button.pack()

parent_button = tk.Radiobutton(root, text="Parent", variable=type_selected, value="Parent")
parent_button.pack()

create_button = tk.Button(root, text="Create A Member ", command=create_member)
create_button.pack()

root.mainloop()

def write_to_file(data, file_name='registration.txt'):
    with open(file_name, 'a') as file:
        file.write(data + "\n")

def readFile(filename='registration.txt'):
    with open(filename, 'r') as file:
        return file.read()


def menu():
    # Define dictionary for menu options
    options = {1: "Create Player ", 
               2: "Create Coach ", 
               3: "Create Parent ", 
               4: "Exit"}

    # Define list to keep track of all instances so to be able to add them to file and recall them if necessary. 
    people = []

    # Define tuple for player positions this allows the user to not deviate from the desired choices.  
    positions = ('Point Guard', 'Shooting Guard', 'Small Forward', 'Power Forward', 'Center')

    while True:
        for key, value in options.items():
            print(f"{key}: {value}")

        try:
            user_input = int(input("Select an option: "))

            if user_input not in options:
                print("Invalid input, try again.")
                continue

            if user_input == 1:
                name = input("Enter name for Player: ")
                jersey_number = int(input("Enter jersey number for the player: "))
                print("Enter position for the player: Choose from ", positions)
                position = input()
                while position not in positions:
                    print("Invalid position. Please choose from ", positions)
                    position = input()
                player = Player(name, jersey_number, position)
                people.append(player)
                write_to_file(player.print_info())

            elif user_input == 2:
                name = input("Enter name for Coach: ")
                specialty_skill = input("Enter specialty skill for the coach: ")
                coach = Coach(name, specialty_skill)
                people.append(coach)
                write_to_file(coach.print_info())

            elif user_input == 3:
                name = input("Enter name for Parent: ")
                child_name = input("Enter child's name for the parent: ")
                parent = Parent(name, child_name)
                people.append(parent)
                write_to_file(parent.print_info())

            elif user_input == 4:
                print("Exiting program...")
                break

        except ValueError:
            print("Invalid input, you must enter a number for the jersey number.")

if __name__ == "__main__":
    menu()


