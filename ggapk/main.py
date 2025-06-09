from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty, StringProperty
from kivy.metrics import dp
from kivy.core.window import Window

# Устанавливаем размер окна (для тестирования на ПК)
Window.size = (360, 640)

class LoveKittenWidget(FloatLayout):
    heart_opacity = NumericProperty(0)
    message = StringProperty("Я очень люблю своего котёнка!")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Создаём градиентный фон
        with self.canvas.before:
            Color(1, 0.5, 0.7, 1)  # Розовый цвет
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Добавляем изображение котёнка
        self.kitten = Image(source='kitten.png', size_hint=(0.6, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.add_widget(self.kitten)

        # Добавляем текст
        self.label = Label(
            text=self.message,
            font_size=dp(30),
            color=(1, 1, 1, 1),
            bold=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            markup=True,
            font_name='Roboto'  # Убедитесь, что шрифт доступен
        )
        self.add_widget(self.label)

        # Добавляем кнопку
        self.button = Button(
            text='Мяу!',
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
            background_color=(1, 0.4, 0.6, 1),
            font_size=dp(20)
        )
        self.button.bind(on_press=self.play_meow)
        self.add_widget(self.button)

        # Добавляем анимированное сердечко
        self.heart = Image(
            source='heart.png',
            size_hint=(0.2, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0
        )
        self.add_widget(self.heart)

        # Запускаем анимацию
        Clock.schedule_interval(self.animate_heart, 1)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def animate_heart(self, dt):
        # Анимация появления и исчезновения сердечка
        anim = Animation(heart_opacity=1, duration=0.5) + Animation(heart_opacity=0, duration=0.5)
        anim.start(self)

    def play_meow(self, instance):
        # Воспроизведение звука мяуканья (добавьте файл meow.wav в папку проекта)
        sound = SoundLoader.load('meow.wav')
        if sound:
            sound.play()

class LoveKittenApp(App):
    def build(self):
        return LoveKittenWidget()

if __name__ == '__main__':
    LoveKittenApp().run()
