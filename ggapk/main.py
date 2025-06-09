from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

# Устанавливаем размер окна для тестирования на ПК
Window.size = (360, 640)

class LoveKittenWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Создаём градиентный фон (розово-фиолетовый)
        with self.canvas.before:
            Color(1, 0.6, 0.8, 1)  # Начальный цвет
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Добавляем изображение котёнка
        self.kitten = Image(
            source='kitten.png',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        self.add_widget(self.kitten)

        # Добавляем текст
        self.label = Label(
            text="[b]Я очень люблю своего котёнка![/b]",
            font_size=dp(28),
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            markup=True
        )
        self.add_widget(self.label)

        # Добавляем анимированное сердечко
        self.heart = Image(
            source='heart.png',
            size_hint=(0.15, 0.15),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0
        )
        self.add_widget(self.heart)

        # Запускаем анимацию сердечка
        Clock.schedule_interval(self.animate_heart, 1.5)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def animate_heart(self, dt):
        # Анимация появления и исчезновения сердечка
        anim = Animation(opacity=1, duration=0.7) + Animation(opacity=0, duration=0.7)
        anim.start(self.heart)

class LoveKittenApp(App):
    def build(self):
        return LoveKittenWidget()

if __name__ == '__main__':
    LoveKittenApp().run()
