from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import BooleanProperty

class LifeGrid(GridLayout):
    running = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(LifeGrid, self).__init__(**kwargs)
        self.cols = 10
        self.rows = 10
        self.life_grid = [[0 for x in range(self.cols)] for y in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                btn = Button(text='0', size_hint=(1,1))
                btn.bind(on_press=self.button_press)
                self.add_widget(btn)

        self.rows +=1
        Clock.schedule_interval(self.update_life, 1)  # update life every 1 second

        start_btn = Button(text='Start', size_hint=(1, 0.5))
        start_btn.bind(on_press=self.start_press)
        self.add_widget(start_btn)
        
    def button_press(self, instance):
        if instance.text == '0':
            instance.text = '1'
        else:
            instance.text = '0'

    def start_press(self, instance):
        if self.running:
            self.running = False
            instance.text = 'Start'
        else:
            self.running = True
            instance.text = 'Stop'
    
    def update_life(self, dt):
        if not self.running:
            return
        
        new_grid = [[0 for x in range(self.cols)] for y in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                if index >= len(self.children):
                    continue
                btn = self.children[row * self.cols + col]
                if btn.text == 'Stop':
                    continue
                life = int(btn.text)
                count = self.count_neighbors(row, col)
                if life == 1 and (count < 2 or count > 3):
                    new_grid[row][col] = 0
                    btn.background_color = (1, 0, 0, 1)  # dead cell, red
                elif life == 0 and count == 3:
                    new_grid[row][col] = 1
                    btn.background_color = (0, 1, 0, 1)  # alive cell, green
                else:
                    new_grid[row][col] = life
                    if life == 0:
                        btn.background_color = (1, 1, 1, 1)  # unchanged cell, white
                    else:
                        btn.background_color = (0, 0, 1, 1)
                    
        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                if index >= len(self.children):
                    continue
                btn = self.children[row * self.cols + col]
                if btn.text == 'Stop':
                    continue
                btn.text = str(new_grid[row][col])
        self.life_grid = new_grid
    
    def count_neighbors(self, row, col):
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                    continue
                if r * self.cols + c >= len(self.children):
                    continue
                button = self.children[r * self.cols + c]
                if button.text == 'Stop':
                    continue
                count += int(button.text)
        return count



class LifeApp(App):
    def build(self):
        return LifeGrid()

if __name__ == '__main__':
    LifeApp().run()
