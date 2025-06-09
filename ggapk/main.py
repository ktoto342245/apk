from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty
from random import random
import os

# Устанавливаем размер окна для тестирования на ПК
Window.size = (360, 640)

class LoveKittenWidget(FloatLayout):
    gradient_color = ListProperty([1, 0.6, 0.8, 1])  # Начальный цвет фона
    kitten_scale = NumericProperty(1.0)  # Для анимации котёнка

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Градиентный фон
        with self.canvas.before:
            Color(*self.gradient_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Анимация фона (радужный эффект)
        Clock.schedule_interval(self.animate_background, 2)

        # Изображение котёнка
        self.kitten = Image(
            source='kitten.png',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        self.add_widget(self.kitten)

        # Свечение под котёнком
        with self.kitten.canvas.before:
            Color(1, 1, 1, 0.3)
            self.glow = Ellipse(size=(dp(200), dp(200)), pos=(self.kitten.x - dp(50), self.kitten.y - dp(50)))
            self.kitten.bind(pos=self._update_glow)

        # Анимация котёнка (пульсация)
        Clock.schedule_interval(self.animate_kitten, 1)

        # Текст
        self.label = Label(
            text="[b][color=ff99cc]Я очень люблю своего котёнка![/color][/b]",
            font_size=dp(30),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            markup=True,
            font_name='Roboto' if os.path.exists('Roboto.ttf') else 'default'
        )
        self.add_widget(self.label)

        # Анимация цвета текста
        Clock.schedule_interval(self.animate_label, 1.5)

        # Кнопка "Мяу!"
        self.button = Button(
            text='Мяу!',
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=(1, 0.4, 0.8, 1),
            font_size=dp(20)
        )
        self.button.bind(on_press=self.on_button_press)
        self.add_widget(self.button)

        # Анимированные сердечки
        self.hearts = []
        for _ in range(5):  # Создаём 5 сердечек
            heart = Image(
                source='heart.png',
                size_hint=(0.1, 0.1),
                pos_hint={'x': random(), 'y': random()},
                opacity=0
            )
            self.add_widget(heart)
            self.hearts.append(heart)
        Clock.schedule_interval(self.animate_hearts, 0.5)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_glow(self, instance, value):
        self.glow.pos = (instance.x - dp(50), instance.y - dp(50))

    def animate_background(self, dt):
        # Плавная смена цвета фона
        anim = Animation(gradient_color=[random(), random(), random(), 1], duration=2)
        anim.start(self)

    def animate_kitten(self, dt):
        # Пульсация котёнка
        anim = Animation(kitten_scale=1.1, duration=0.5) + Animation(kitten_scale=1.0, duration=0.5)
        anim.start(self)

    def animate_label(self, dt):
        # Смена цвета текста
        colors = ['ff99cc', '99ccff', 'cc99ff', 'ffcc99']
        self.label.text = f"[b][color={colors[int(dt % 4)]}]Я очень люблю своего котёнка![/color][/b]"

    def animate_hearts(self, dt):
        # Анимация сердечек
        for heart in self.hearts:
            anim = Animation(
                pos_hint={'x': random(), 'y': random()},
                opacity=1,
                duration=0.5
            ) + Animation(opacity=0, duration=0.5)
            anim.start(heart)

    def on_button_press(self, instance):
        # Эффект нажатия кнопки
        anim = Animation(size_hint=(0.35, 0.12), duration=0.1) + Animation(size_hint=(0.3, 0.1), duration=0.1)
        anim.start(self.button)
        # Опционально: добавьте звук (раскомментируйте, если есть meow.wav)
        # from kivy.core.audio import SoundLoader
        # sound = SoundLoader.load('meow.wav')
        # if sound:
        #     sound.play()

class LoveKittenApp(App):
    def build(self):
        return LoveKittenWidget()

if __name__ == '__main__':
    LoveKittenApp().run()
