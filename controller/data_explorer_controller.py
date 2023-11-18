import os
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

import pandas as pd
from model.data_source import DataSource
from model.database import Database
from view.data_explorer_public_view import DataExplorerPublicView
from view.data_explorer_view import DataExplorerView
from view.data_explorer_public_view import DataExplorerPublicView
from controller.data_source_controller import DataSourceController
import PySimpleGUI as sg
import threading
from datetime import datetime

matplotlib.use('TkAgg')


class DataExplorerController:

    db = Database.getInstance()
    collection = db.get_collection("data_sources")

    def __init__(self, des, username):
        self.username = username
        self.des = des
        if self.username != self.des.username:
            self.view = DataExplorerPublicView(
                self.des.name, self.des.data, self.des.chat)
            self.is_owner = False
        else:
            self.view = DataExplorerView(
                self.des.name, self.des.data, self.des.chat, self.des.is_public)
            self.is_owner = True

    def run(self):

        def watch():
            self.watch_for_changes()

        thread = threading.Thread(target=watch, daemon=True)
        thread.start()

        if self.des.data:
            data_source = DataSource.find_by_name(self.des.data)
            print("DES Data:", type(data_source), data_source)
            if data_source:
                # Assuming data_source_data is a list of dictionaries
                data_source_data = pd.DataFrame(data_source.data)

                # Create a new matplotlib figure and a subplot
                fig, ax = plt.subplots()

                # Plot the data on the subplot
                self.plot_data(data_source_data, ax)

                # Add the plot to the sg.Canvas element
                canvas_elem = self.view.window['-CANVAS-']
                canvas = canvas_elem.TKCanvas

                # Add the toolbar to the sg.Canvas element
                toolbar_canvas_elem = self.view.window['-CANVAS_TOOLS-']
                toolbar_canvas = toolbar_canvas_elem.TKCanvas

                self.draw_figure(self.view.window, canvas, toolbar_canvas, fig)

        while True:
            event, values = self.view.read()
            print(event, values)
            match event:
                case sg.WIN_CLOSED:
                    # thread.join()
                    os._exit(0)

                case "Cancel":
                    break

                case "-PUBLIC-":
                    state = values["-PUBLIC-"]
                    print("State:", state)
                    self.des.toggle_public(state)

                case "Send":
                    text = values["-CHAT-"]

                    current_time = datetime.now().time()
                    current_time_str = current_time.strftime("%H:%M:%S")
                    message = f"{current_time_str} | {self.username}: {text}"

                    self.des.chat.append(message)
                    self.des.save()

                case "Manage Data Source":
                    data_source_controller = DataSourceController(self.des)
                    data_source_controller.run()

    def watch_for_changes(self):
        """
            Monitors changes in the data_explorer collection
            and refreshes the Data Explorer if a change is detected,
            also updates the DES view to reflect the changes.
        """
        with self.collection.watch() as stream:
            for change in stream:
                print(self.des._id, change["documentKey"]["_id"])
                if change["documentKey"]["_id"] == self.des._id:
                    print(self.des)
                    self.des.refresh()
                    print(self.des)
                    print("Operation Type:", change["operationType"])
                    match change["operationType"]:
                        case "delete":
                            self.view.close()
                            os._exit(0)

                        case "update":
                            print("Updated Fields:",
                                  change["updateDescription"]["updatedFields"])
                            if "is_public" in change["updateDescription"]["updatedFields"]:
                                if self.is_owner == False:
                                    # Kill the entire process
                                    self.view.close()
                                    os._exit(0)

                                else:
                                    self.des.is_public = change["updateDescription"]["updatedFields"]["is_public"]
                                    print("Public State:", self.des.is_public)
                                    self.view.public_state = self.des.is_public

                            if "chat" in change["updateDescription"]["updatedFields"]:
                                chat = ''
                                for message in self.des.chat:
                                    chat += message + '\n'
                                self.view.window["-OUTPUT-"].update(chat)

    def draw_figure(self, window, canvas, toolbar_canvas, figure):
        # if window['-CANVAS-'].Widget is not None:
        #     window['-CANVAS-'].Widget.pack_forget()
        # if window['-CANVAS_TOOLS-'].Widget is not None:
        #     window['-CANVAS_TOOLS-'].Widget.pack_forget()
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        toolbar = NavigationToolbar2Tk(figure_canvas_agg, toolbar_canvas)
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg, toolbar

    def plot_data(self, data, ax):
        # Clear the previous plot
        ax.clear()

        # Plot the data on the subplot
        data.plot(kind='line', ax=ax)
