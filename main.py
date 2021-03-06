import tkinter as tk
import json
import random

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.__read_data()
        self.schedule = Schedule(self.station_data)
        self.__create_widgets()
        tk.mainloop()

    def __read_data(self):
        with open('station.json') as data_file:
            self.station_data = json.load(data_file)

    def __create_widgets(self):
        self.scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self, xscrollcommand=self.scrollbar.set,
                                scrollregion=(0, 0, self.station_data['stations'] * 200, 0))
        self.__draw_graph(self.canvas)
        self.scrollbar.configure(command=self.canvas.xview)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def __draw_graph(self, canvas):
        stations = 0
        line = [1, 1]
        for data in self.station_data['data']:
            if data['type'] == 'rail':
                line = data['line']
                self.__draw_rail(canvas, data, stations)
            else:
                stations += 1
                self.__draw_station(canvas, data, line, stations)

    def __draw_station(self, canvas, data, line, index):
        x_pos = 200 * index - 100
        y_pos = 150
        # Draw station name.
        canvas.create_text(x_pos, 40, text=data['name'])
        if data['type'] == 'terminal':
            canvas.create_text(x_pos, 55, text='terminal')
        else:
            canvas.create_text(x_pos, 55, text='stop time: ' + str(data['stop_time']))
            canvas.create_text(x_pos, 70, text='pass time: ' + str(data['pass_time']))

        main_line = sum(line)

        if data['type'] == 'terminal':
            stop = data['stop']
            # All line in terminal is stop line.
            for x in range(stop):
                dy_pos = y_pos - (main_line - 1) * 8 + x * 16 - (stop - 2) // 2 * 16
                canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos, fill='blue')
                # Draw terminal mark.
                if index == 1:
                    canvas.create_line(x_pos - 50, dy_pos - 4, x_pos - 50, dy_pos + 4)
                else:
                    canvas.create_line(x_pos + 50, dy_pos - 4, x_pos + 50, dy_pos + 4)
        else:
            stop = data['stop']
            pass_line = data['pass']
            # Draw pass line.
            for x in range(pass_line[0]):
                dy_pos = y_pos - (main_line - 1) * 8 + (line[1] + x) * 16
                canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos, fill='red')
            for x in range(pass_line[1]):
                dy_pos = y_pos - (main_line - 1) * 8 + (line[1] - 1 - x) * 16
                canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos, fill='red')
            # Draw stop line.
            for x in range(stop[0]):
                dy_pos = y_pos - (main_line - 1) * 8 + (line[1] + pass_line[0] + x) * 16
                canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos, fill='blue')
            for x in range(stop[1]):
                dy_pos = y_pos - (main_line - 1) * 8 + (line[1] - 1 - pass_line[1] - x) * 16
                canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos, fill='blue')

    def __draw_rail(self, canvas, data, index):
        x_pos = 200 * index
        y_pos = 150
        # Draw station name.
        canvas.create_text(x_pos, 70, text='time: ' + str(data['time']))
        main_line = sum(data['line'])
        for x in range(main_line):
            dy_pos = y_pos - (main_line - 1) * 8 + x * 16
            canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos)


class Schedule(object):
    def __init__(self, station_data):
        self.station_data = station_data
        with open('train.json') as data_file:
            self.train_data = json.load(data_file)
        with open('input.json') as data_file:
            self.input_data = json.load(data_file)

        self.schedule = {}
        self.station_array = []
        self.cycle = self.input_data['cycle']
        for station in station_data['data']:
            if station['type'] == 'rail':
                continue
            self.schedule.update({station['name']: [None] * self.cycle})
            self.station_array.append(station['name'])

        self.__encode_data()
        self.create_scheduel()

    def __encode_data(self):
        self.schedule_data = []
        for key, value in self.input_data['train'].items():
            train_data = self.train_data[value['type']]

            previous = train_data[0]
            index = 1
            from_stop = True
            first = True
            for station in self.station_array:
                # Find the first station.
                if first:
                    if station == previous:
                        first = False
                    continue

                to_stop = False
                if station == train_data[index]:
                    to_stop = True
                    index += 1

                # Store data.
                code = {
                    'no': key,
                    'from': previous,
                    'from_stop': from_stop,
                    'to': station,
                    'to_stop': to_stop
                }
                self.schedule_data.append(code)
                print(code)

                # Update data to next station.
                previous = station
                from_stop = to_stop



    def create_scheduel(self):
        interval = self.station_data['departure_arrival_interval']
        for data in self.schedule_data:
            station_from = data['from']
            station_to = data['to']
            for time, value in enumerate(self.schedule[station_from]):
                if value == None:
                    self.schedule[station_from][time] = data['no']






def main():
    app = App()

if __name__ == '__main__':
    main()

