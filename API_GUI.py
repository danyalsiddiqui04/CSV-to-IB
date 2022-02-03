# Made by Danyal Siddiqui, 2021
# Creating GUI for IB API application

import tkinter as tk  # used to create gui window and widgets
from tkinter import filedialog  # used for creating file dialog box
import threading
import IB_API as api
import json
import os

class GUI(tk.Frame):
    def __init__(self, master=None):
        # set program variables
        default_port = 7497
        default_filename = ""
        default_isFilledChecked = False
        default_filledLimit = 5
        default_isOrderChecked = False
        default_orderLimit = 10
        self.started = False
        # create options file if it doesn't exist
        with open("options.txt", "a"):
            pass
        # set options variables
        with open("options.txt", "r") as options:
            if os.stat("options.txt").st_size == 0:
                optionsDict = {}
            for line in options:
                optionsDict = json.loads(line)
            if optionsDict.get("port"):
                self.port = optionsDict.get("port")
            else:
                optionsDict["port"] = default_port
                self.port = optionsDict.get("port")
            if optionsDict.get("isFilledChecked"):
                self.isFilledChecked = optionsDict.get("isFilledChecked")
            else:
                optionsDict["isFilledChecked"] = default_isFilledChecked
                self.isFilledChecked = optionsDict.get("isFilledChecked")
            if optionsDict.get("filename"):
                self.filename = optionsDict.get("filename")
            else:
                optionsDict["filename"] = default_filename
                self.filename = optionsDict.get("filename")
            if optionsDict.get("filledLimit"):
                self.filledLimit = optionsDict.get("filledLimit")
            else:
                optionsDict["filledLimit"] = default_filledLimit
                self.filledLimit = optionsDict["filledLimit"]
            if optionsDict.get("isOrderChecked"):
                self.isOrderChecked = optionsDict.get("isOrderChecked")
            else:
                optionsDict["isOrderChecked"] = default_isOrderChecked
                self.isOrderChecked = optionsDict.get("isOrderChecked")
            if optionsDict.get("orderLimit"):
                self.orderLimit = optionsDict.get("orderLimit")
            else:
                optionsDict["orderLimit"] = default_orderLimit
                self.orderLimit = optionsDict.get("orderLimit")
            if self.port == 7497:
                self.portName = "TWS Paper"
            elif self.port == 7496:
                self.portName = "TWS Live"
            elif self.port == 4002:
                self.portName = "IBG Paper"
            elif self.port == 4001:
                self.portName = "IBG Live"
        super().__init__(master)
        self.master = master
        self.master.title("IB API")
        self.windowWidth = 600
        self.windowHeight = 400
        self.window_size = str(self.windowWidth)+"x"+str(self.windowHeight)
        self.master.geometry(self.window_size)
        self.grid()
        self.create_widgets()
        
    def on_closing(self):
        self.save()
        self.stop()
        root.destroy()

    def create_widgets(self):
        # create widget tk variables
        port = tk.StringVar()
        port.set(str(self.portName))
        isFilledChecked = tk.BooleanVar()
        isFilledChecked.set(self.isFilledChecked)
        self.restrictionCheck(isFilledChecked)
        filledLimit = tk.IntVar()
        filledLimit.set(self.filledLimit)
        isOrderChecked = tk.BooleanVar()
        isOrderChecked.set(self.isOrderChecked)
        self.restrictionCheck(isFilledChecked)
        orderLimit = tk.IntVar()
        orderLimit.set(self.orderLimit)
        
        # creating tk widgets
        self.tradingType_drop = tk.OptionMenu(root, port, "TWS Paper", "TWS Live", "IBG Paper", "IBG Live", command=self.portClick)
        self.filled_check = tk.Checkbutton(root, text="Number of filled orders", variable=isFilledChecked, onvalue=True, offvalue=False, command=lambda: self.restrictionCheck(isFilledChecked))
        self.orderLimit_check = tk.Checkbutton(root, text="Number of placed orders", variable=isOrderChecked, onvalue=True, offvalue=False, command=lambda: self.isOrderChecked_func(isOrderChecked))
        self.restrictionLabel = tk.Label(root, text="Set restrictions on:")
        self.tradingTypeLabel = tk.Label(root, text="Trading Type:")
        self.start_button = tk.Button(root, text="Start Upload to TWS", command=self.start)
        self.stop_button = tk.Button(root, text="Stop Program", command=self.stop)
        self.browse_button = tk.Button(root, text="Browse", command=self.browse)
        self.file_label = tk.Label(root, text=self.filename)
        self.filledLimit_entry = tk.Entry(root, text=filledLimit, width=4)
        self.orderLimit_entry = tk.Entry(root, text=orderLimit, width=4)
        
        # drawing to the screen
        self.tradingType_drop.grid(row=1, column=0, padx=10)
        self.restrictionLabel.place(x=160, y=10)
        self.filled_check.grid(row=1, column=1, padx=10)
        self.tradingTypeLabel.grid(row=0, column=0, padx=10)
        self.start_button.place(x=self.windowWidth-100, y=self.windowHeight-40)
        self.stop_button.place(x=self.windowWidth-190, y=self.windowHeight-40)
        self.browse_button.place(x=10, y=self.windowHeight-40)
        self.file_label.place(x=10, y=self.windowHeight-65)
        self.filledLimit_entry.grid(row=1, column=2)
        self.orderLimit_check.grid(row=2, column=1)
        self.orderLimit_entry.grid(row=2, column=2)
        
    def restrictionCheck(self, check):
        # check which API restrictions are active
        self.isFilledChecked = check.get()
        
    def isOrderChecked_func(self, check):
        self.isOrderChecked = check.get()
        
    def browse(self):
        # get filename of csv file to be used for API
        self.filename_old = self.filename
        self.filename = filedialog.askopenfilename(initialdir=r"C:\Users\Danyal\Desktop", title="Select A File", filetypes=(("csv files", "*.csv"),))
        if self.filename == "":
            self.filename = self.filename_old
        self.file_label = tk.Label(root, text=self.filename)
        self.file_label.place(x=10, y=self.windowHeight-65)
        
    def portClick(self, port):
        # get the port value
        if port == "TWS Paper":
            self.port = 7497
        elif port == "TWS Live":
            self.port = 7496
        elif port == "IBG Paper":
            self.port = 4002
        elif port == "IBG Live":
            self.port = 4001
    
    def stop(self):
        if self.started:
            stopSystem_thread = threading.Thread(target=api.stop, daemon=True)
            stopSystem_thread.start()
    
    def save(self):
        # saving program options to a file
        optionsDict = {}
        # save each option to dict
        optionsDict["port"] = self.port
        optionsDict["isFilledChecked"] = self.isFilledChecked
        optionsDict["filename"] = self.filename
        optionsDict["filledLimit"] = self.filledLimit_entry.get()
        optionsDict["isOrderChecked"] = self.isOrderChecked
        optionsDict["orderLimit"] = self.orderLimit_entry.get()
        # write the dictionary to a file
        options_json = json.dumps(optionsDict)
        options = open("options.txt", "w")
        options.write(str(options_json))
        
    def start(self):
        self.save()
        system_thread = threading.Thread(target=api.system, daemon=True)
        system_thread.start()
        self.started = True
        
root = tk.Tk()
gui = GUI(master=root)
root.protocol("WM_DELETE_WINDOW", gui.on_closing)
gui.mainloop()