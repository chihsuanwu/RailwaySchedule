import tkinter as tk
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.__read_data()
        self.__create_widgets()
        tk.mainloop()

    def __read_data(self):
        with open('station.json') as data_file:
            self.data = json.load(data_file)

    def __create_widgets(self):
        self.scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self, xscrollcommand=self.scrollbar.set,
                                scrollregion=(0, 0, self.data['stations'] * 200, 0))
        self.__draw_graph(self.canvas)
        self.scrollbar.configure(command=self.canvas.xview)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def __draw_graph(self, canvas):
        stations = 0
        line = [1, 1]
        for data in self.data['data']:
            data_type = data['type']
            if data_type == 'rail':
                line = data['line']
                continue

            stations += 1
            x_pos = 200 * stations - 100
            y_pos = 150
            # Draw station name.
            canvas.create_text(x_pos, 50, text=data['name'])

            main_line = sum(line)
            for x in range(main_line):
                dy_pos = y_pos - (main_line - 1) * 8 + x * 16
                if data_type == 'terminal':
                    if stations == 1:
                        canvas.create_line(x_pos - 50, dy_pos, x_pos + 100, dy_pos)
                    else:
                        canvas.create_line(x_pos - 100, dy_pos, x_pos + 50, dy_pos)
                else:
                    canvas.create_line(x_pos - 100, dy_pos, x_pos + 100, dy_pos)

            if data_type == 'terminal':
                stop = data['stop']
                for x in range(stop):
                    dy_pos = y_pos - (main_line - 1) * 8 + x * 16 - (stop - 2) // 2 * 16
                    canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos, fill='blue')
                    if stations == 1:
                        canvas.create_line(x_pos - 50, dy_pos - 4, x_pos - 50, dy_pos + 4)
                    else:
                        canvas.create_line(x_pos + 50, dy_pos - 4, x_pos + 50, dy_pos + 4)
            else:
                stop = data['stop']
                pass_line = data['pass']
                for x in range(pass_line[0]):
                    dy_pos = y_pos - (main_line - 1) * 8 + (line[1] + x) * 16
                    canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos, fill='red')
                for x in range(pass_line[1]):
                    dy_pos = y_pos - (main_line - 1) * 8 + (line[1] - 1 - x) * 16
                    canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos, fill='red')

                for x in range(stop[0]):
                    dy_pos = y_pos - (main_line - 1) * 8 + (line[1] + pass_line[0] + x) * 16
                    canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos, fill='blue')
                for x in range(stop[1]):
                    dy_pos = y_pos - (main_line - 1) * 8 + (line[1] - 1 - pass_line[1] - x) * 16
                    canvas.create_line(x_pos - 50, dy_pos, x_pos + 50, dy_pos, fill='blue')



def main():
    app = App()

if __name__ == '__main__':
    main()

