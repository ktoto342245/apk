from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.uix.effectwidget import EffectWidget, AdvancedEffectBase
from kivy.properties import NumericProperty, ListProperty
from random import random

# Устанавливаем размер окна для тестирования на ПК
Window.size = (360, 640)  # Размер экрана, как у смартфона

class HeartAnimation(Scatter):
    """Виджет для анимированных сердечек"""
    def __init__(self, **kwargs):
        super(HeartAnimation, self).__init__(**kwargs)
        self.size = (50, 50)
        self.add_widget(Image(source='heart.png', size=(50, 50)))

    def animate(self):
        # Анимация: сердечко поднимается и исчезает
        anim = Animation(y=self.y + 400, t='out_quad', duration=2) + Animation(opacity=0, duration=0.5)
        anim.start(self)
        anim.bind(on_complete=lambda *args: self.parent.remove_widget(self))

class LoveKittenWidget(FloatLayout):
    """Основной виджет приложения"""
    bg_color = ListProperty([0.9, 0.6, 0.8, 1])  # Фоновый цвет (розовый)

    def __init__(self, **kwargs):
        super(LoveKittenWidget, self).__init__(**kwargs)

        # Устанавливаем фон
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(size=Window.size, pos=self.pos)

        # Обновление фона при изменении размера окна
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Добавляем текст
        self.label = Label(
            text="[b]Я очень сильно люблю своего котёнка![/b]",
            font_size='24sp',
            color=(1, 0.5, 0.5, 1),  # Розовый цвет текста
            markup=True,
            size_hint=(0.9, 0.2),
            pos_hint={'center_x': 0.5, 'y': 0.8}
        )
        self.add_widget(self.label)

        # Добавляем изображение котёнка
        self.kitten = Image(
            source='kitten.png',  # Укажите путь к изображению котёнка
            size_hint=(0.6, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.kitten)

        # Добавляем кнопку
        self.button = Button(
            text='Показать любовь!',
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.1},
            background_color=(1, 0.4, 0.6, 1),  # Яркий розовый
            color=(1, 1, 1, 1)
        )
        self.button.bind(on_press=self.show_love)
        self.add_widget(self.button)

        # Эффект свечения для кнопки
        self.effect_widget = EffectWidget()
        self.effect_widget.add_widget(self.button)
        self.add_widget(self.effect_widget)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def show_love(self, instance):
        """Показывает анимацию сердечек и меняет фон"""
        # Меняем цвет фона с анимацией
        new_color = [random(), random(), random(), 1]
        Animation(bg_color=new_color, duration=1).start(self)

        # Создаём несколько сердечек
        for _ in range(5):
            heart = HeartAnimation(
                pos=(self.center_x - 25 + random() * 50, self.y + 100)
            )
            self.add_widget(heart)
            Clock.schedule_once(lambda dt, h=heart: h.animate(), 0.1 * _)

class LoveKittenApp(App):
    def build(self):
        return LoveKittenWidget()

if __name__ == '__main__':
    LoveKittenApp().run()
