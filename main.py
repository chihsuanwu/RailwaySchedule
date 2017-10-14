import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        tk.mainloop()



    def create_widgets(self):
        self.station = tk.Listbox(self)
        self.station.pack(anchor='nw')

        self.new_station = tk.Label(self, text='新增車站')
        self.new_station.pack(side=tk.LEFT, anchor='nw')
        self.station_entry = tk.Entry(self)
        self.station_entry.pack(side=tk.LEFT, anchor='nw')
        self.new_station_button = tk.Button(self, text='確定', command=self.__new_station)
        self.new_station_button.pack(side=tk.LEFT, anchor='nw')

    def __new_station(self):
        self.station.insert(tk.END, self.station_entry.get())
        self.station_entry.delete(0, tk.END)


def main():
    app = App()

if __name__ == '__main__':
    main()

