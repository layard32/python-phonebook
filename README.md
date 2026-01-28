# Phonebook

Minimalistic phonebook app made entirely in Python. 

## Features

* It implements basic actions (create, modify and delete contacts) and simple persistence of the contacts via .txt files inside a folder called "Informazioni" (the folder is created in the same folder where the app is).
* Built using `tkinter` and `ttkbootstrap` for theming.
* Simple input validation included in the GUI.
* Simple login screen handles access to the application. The credentials are hard-coded (**admin** for username and **password** for password).

## How to run the application

In order to test the application, you have two options:
1. Run from source. Make sure to have the latest version of python (obviously) and `ttkbootstrap` installed (if you don't have, you can use `pip`): 
    ```bash
    pip install ttkboostrap
    python main.py
    ```

2. Build the executable. Make sure to have `pyinstaller` and run the following command:
    ```bash
    pip install pyinstaller
    pyinstaller --noconsole --onefile --name "Rubrica" --hidden-import="ttkbootstrap" main.py
    ```