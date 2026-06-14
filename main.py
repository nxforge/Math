from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from random import *
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout
import os
import shop

if not os.path.isdir("data"):
    os.mkdir("data")

class MathApp(App):
    def build(self):
        self.game_over_shown = True
        self.moneys = 0
        self.score = 1
        self.window = BoxLayout(orientation="vertical")
        
        
        self.loading = Image(source="image/loading.png", allow_stretch=True)
        self.window.add_widget(self.loading)
        
        
        self.main = BoxLayout(orientation="vertical")
        
        self.image_screen = Image(source="image/math.png", allow_stretch=True, size_hint=(1, 0.8))
        self.main.add_widget(self.image_screen)
        
        self.money = BoxLayout(orientation="horizontal", size_hint=(1, 0.5))
        self.main.add_widget(self.money)
        
        self.money_icon = Image(source="image/money.png", allow_stretch=True)
        self.money.add_widget(self.money_icon)
        
        self.money_score = Label(text="", font_size=100)
        self.money.add_widget(self.money_score)
        if os.path.exists("data/money.app"):
            self.money_score.text = open("data/money.app", "r").read()
        else:
            self.money_score.text = "100"
        
        self.main.add_widget(Widget(size_hint=(1, 0.5)))
        
        self.button_play = Button(text="Играть", background_normal="image/play.png", background_down="image/down.png", size_hint=(0.9, 0.3), pos_hint={"center_x": 0.5}, font_size=50, on_press=self.down_button_play)
        self.main.add_widget(self.button_play)
        
        self.button_store = Button(text="Магазин", background_normal="image/store.png", background_down="image/down.png", size_hint=(0.9, 0.3), pos_hint={"center_x": 0.5}, font_size=50, on_press=self.down_button_store)
        self.main.add_widget(self.button_store)
        
        self.main.add_widget(Widget(size_hint=(1, 0.5)))
        
        Clock.schedule_once(self.show_main, 5)
        
        
        self.game = BoxLayout(orientation="vertical")
        
        self.game_menu = BoxLayout(orientation="horizontal", size_hint=(1, 0.25))
        self.game.add_widget(self.game_menu)
        
        self.hearts = 3
        self.ihearts = Image(source="image/3_heart.png", allow_stretch=True)
        self.game_menu.add_widget(self.ihearts)
        
        self.time = Label(text="10", color=(0, 0, 1, 1), font_size=80)
        self.game_menu.add_widget(self.time)
        
        self.game_menu.add_widget(Widget())
        
        self.game.add_widget(Widget(size_hint=(1, 0.3)))
        
        self.example = Label(text="", font_size=100, size_hint=(1, 0.3))
        self.game.add_widget(self.example)
        
        self.game.add_widget(Label(text="=", font_size=100, size_hint=(1, 0.3)))
        
        self.choice = BoxLayout(orientation="horizontal", size_hint=(1, 0.3))
        self.game.add_widget(self.choice)
        
        self.a_answer = Button(text="", font_size=100, background_color=(0, 0, 0, 1), on_press=self.answer)
        self.choice.add_widget(self.a_answer)
        
        self.b_answer = Button(text="", font_size=100, background_color=(0, 0, 0, 1), on_press=self.answer)
        self.choice.add_widget(self.b_answer)
        
        self.c_answer = Button(text="", font_size=100, background_color=(0, 0, 0, 1), on_press=self.answer)
        self.choice.add_widget(self.c_answer)
        
        self.game.add_widget(Widget(size_hint=(1, 0.5)))
        
        self.game_over = ModalView(size_hint=(0.8, 0.8), auto_dismiss=False, background_color=(0, 0, 0, 0))
        self.game_over_layout = BoxLayout(orientation="vertical")
        self.game_over.add_widget(self.game_over_layout)
        
        self.game_over_layout.add_widget(Button(background_normal="image/back.png", background_down="image/back.png", size_hint=(None, None), size=(100, 100), on_press=self.back))

        self.game_over_layout.add_widget(Label(text="GAME OVER", font_size=100, color=(1, 0, 0, 1)))
        
        self.game_over_text = Label(color=(1, 1, 0, 1), font_size=50)
        self.game_over_layout.add_widget(self.game_over_text)
        
        self.game_over_layout.add_widget(Widget())
        
        self.game_over_play = Button(text="Играть", background_normal="image/play.png", background_down="image/down.png", size_hint=(1, 0.5), font_size=50, pos_hint={"center_x": 0.5}, on_press=self.functions_game)
        self.game_over_layout.add_widget(self.game_over_play)
        
        Clock.schedule_interval(lambda event: self.edit_time(""), 1)
        
        self.shop = BoxLayout(orientation="vertical")
        
        self.shop_title = BoxLayout(orientation="horizontal", size_hint=(1, 0.25))
        self.shop.add_widget(self.shop_title)
        
        self.shop_title.add_widget(Button(background_normal="image/back.png", background_down="image/back.png", pos_hint={"center_y": 0.5}, on_press=self.back, size_hint=(None, None), size=(100, 100)))
        
        self.shop_title.add_widget(Label(text="Магазин", font_size="30sp"))
        
        self.shop_product = Label(text="Знаки", font_size="50sp", size_hint=(0.3, 1), pos_hint={"center_x": 0.5})
        self.shop.add_widget(self.shop_product)

        self.signs = GridLayout(cols=2, rows=2, size_hint=(1, 1))
        self.shop.add_widget(self.signs)

        self.plus_layout = BoxLayout(orientation="vertical", on_release=lambda event: self.buy("plus", self.plus_money))
        self.plus = Image(source="image/plus.png", allow_stretch=True)
        self.plus_layout.add_widget(self.plus)
        self.plus_money = Label(text="100", font_size=40)
        self.plus_layout.add_widget(self.plus_money)
        self.signs.add_widget(self.plus_layout)

        self.minus_layout = BoxLayout(orientation="vertical", on_press=lambda event: self.buy("minus", self.minus_money))
        self.minus = Image(source="image/minus.png", allow_stretch=True)
        self.minus_layout.add_widget(self.minus)
        self.minus_money = Label(text="200", font_size=40)
        self.minus_layout.add_widget(self.minus_money)
        self.signs.add_widget(self.minus_layout)

        self.multiply_layout = BoxLayout(orientation="vertical", on_press=lambda event: self.buy("multiply", self.multiply_money))
        self.multiply = Image(source="image/multiply.png", allow_stretch=True)
        self.multiply_layout.add_widget(self.multiply)
        self.multiply_money = Label(text="300", font_size=40)
        self.multiply_layout.add_widget(self.multiply_money)
        self.signs.add_widget(self.multiply_layout)

        self.divide_layout = BoxLayout(orientation="vertical", on_press=lambda event: self.buy("divide", self.divide_money))
        self.divide = Image(source="image/divide.png", allow_stretch=True)
        self.divide_layout.add_widget(self.divide)
        self.divide_money = Label(text="400", font_size=40)
        self.divide_layout.add_widget(self.divide_money)
        self.signs.add_widget(self.divide_layout)
        
        return self.window
    
    
    def show_main(self, show):
        self.window.remove_widget(self.loading)
        Clock.schedule_once(lambda event: self.window.add_widget(self.main), 1)
        self.music = SoundLoader.load("sound/music.mp3")
        self.music.loop = True
        self.music.valume = 1.0
        self.music.play()
        
        
    def back(self, show):
        self.window.remove_widget(self.game)
        self.window.remove_widget(self.shop)
        self.window.add_widget(self.main)
        self.game_over.dismiss()
        self.button_play.size_hint = (0.9, 0.3)
        self.button_play.font_size = 50
        self.button_store.size_hint = (0.9, 0.3)
        self.button_store.font_size = 50
        Animation(volume=1.0, duration=0.5).start(self.music)
    
    
    def down_button_play(self, button):
        Animation(size_hint=(0, 0), duration=0.5).start(self.button_play)
        Animation(font_size=0, duration=0.5).start(self.button_play)
        Clock.schedule_once(lambda event: self.window.remove_widget(self.main), 0.4)
        Clock.schedule_once(lambda event: self.window.add_widget(self.game), 0.5)
        self.functions_game("")
        Animation(volume=0.2, duration=0.5).start(self.music)


    def buy(self, button, text):
        file = open("shop.py", "r").read()
        edit = file.replace(f"{button} = False", f"{button} = True")
        text.text = "Купленно"
        open("shop.py", "w").write(edit)
    
    
    def down_button_store(self, button):
        Animation(size_hint=(0, 0), duration=0.5).start(self.button_store)
        Animation(font_size=0, duration=0.5).start(self.button_store)
        Clock.schedule_once(lambda event: self.window.remove_widget(self.main), 0.4)
        Clock.schedule_once(lambda event: self.window.add_widget(self.shop), 0.5)
        Animation(volume=1.0, duration=0.5).start(self.music)
        self.button_store.size_hint = (0.9, 0.3)
        self.button_store.font_size = 50
        
        
    def functions_game(self, button):
        self.time.text = "11"
        self.new_example()
        self.game_over_shown = False
        self.moneys = 0
        self.game_over.dismiss()
        self.ihearts.source = "image/3_heart.png"
        self.hearts = 3
    
    
    def edit_time(self, clock):
        if clock == "true":
            time = int(self.time.text)
            time += 2
            time = str(time)
            self.time.text = time
        else:
            time = int(self.time.text)
            time -= 1
            if time < 0:
                time = 0
                self.game_over_show()
            elif time <= 5:
                Animation(color=(1, 0, 0, 1), duration=0.5).start(self.time)
                Clock.schedule_once(lambda event: Animation(color=(0, 0, 0, 1), duration=0.5).start(self.time), 0.5)
            else:
                Animation(color=(0, 0, 1, 1), duration=0.5).start(self.time)
            time = str(time)
            self.time.text = time
        
        
    def answer(self, button):
        answer_user = int(button.text)
        if self.answer_example == answer_user:
            self.score += 1
            self.edit_time("true")
            self.moneys += 1
            self.new_example()
        else:
            button.background_color = (1, 0, 0, 1)
            self.hearts -= 1
            self.ihearts.source = "image/{}_heart.png".format(self.hearts)
            if self.hearts == 0:
                self.game_over_show()
            else:
                if self.moneys > 2:
                    self.moneys = self.moneys // 2
            Clock.schedule_once(lambda event: Animation(background_color=(0, 0, 0, 1), duration=0.5).start(button), 0.5)
            SoundLoader.load("sound/error.mp3").play()
            
            
    def new_example(self):
        one = randint(1, self.score)
        two = randint(1, self.score)
        self.answer_example = one + two
        self.example.text = "{}+{}".format(one, two)
        self.a_answer.text = "{}".format(randint(1, self.answer_example + 10))
        self.b_answer.text = "{}".format(randint(1, self.answer_example + 10))
        self.c_answer.text = "{}".format(randint(1, self.answer_example + 10))
        answers = [self.a_answer, self.b_answer, self.c_answer]
        for a in answers:
            if int(a.text) == self.answer_example:
                break
        else:
            b = choice(answers)
            b.text = str(self.answer_example)
            
            
    def game_over_show(self):
        if self.game_over_shown == False:
            self.game_over.open()
            self.game_over_shown = True
            self.time.text = "0"
            money_score = int(self.money_score.text) + self.moneys * 2
            self.money_score.text = str(money_score)
            self.game_over_text.text = "Ты получаешь {} монет".format(self.moneys * 2)
            open("data/money.app", "w").write(self.money_score.text)


if __name__ == "__main__":
    MathApp().run()
