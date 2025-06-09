from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.properties import ListProperty
from random import random

# Set window size for testing (smartphone-like)
Window.size = (360, 640)

class HeartAnimation(Scatter):
    """Widget for animated hearts"""
    def __init__(self, **kwargs):
        super(HeartAnimation, self).__init__(**kwargs)
        self.size = (50, 50)
        # Use text-based heart instead of image
        self.add_widget(Label(text='♥', font_size='40sp', color=(1, 0, 0, 1)))

    def animate(self):
        # Animation: heart rises and fades out
        anim = Animation(y=self.y + 400, t='out_quad', duration=2) + Animation(opacity=0, duration=0.5)
        anim.start(self)
        anim.bind(on_complete=lambda *args: self.parent.remove_widget(self))

class LoveKittenWidget(FloatLayout):
    """Main app widget"""
    bg_color = ListProperty([0.9, 0.6, 0.8, 1])  # Initial pink background

    def __init__(self, **kwargs):
        super(LoveKittenWidget, self).__init__(**kwargs)

        # Create gradient background
        with self.canvas.before:
            Color(0.9, 0.6, 0.8, 1)  # Pink base
            self.rect = Rectangle(size=Window.size, pos=self.pos)
            Color(0.5, 0.8, 1, 1)  # Light blue gradient
            self.rect2 = Rectangle(size=(Window.size[0], Window.size[1] / 2), pos=self.pos)

        # Update background on size/position change
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add text
        self.label = Label(
            text="[b]Я очень сильно \nлюблю своего котёнка![/b]",
            font_size='24sp',
            color=(1, 0.2, 0.4, 1),  # Bright pink text
            markup=True,
            size_hint=(0.9, 0.2),
            pos_hint={'center_x': 0.5, 'y': 0.8}
        )
        self.add_widget(self.label)

        # Add kitten placeholder (text instead of image)
        self.kitten = Label(
            text='😺',  # Cat emoji (or replace with image later)
            font_size='100sp',
            color=(1, 0.5, 0.7, 1),
            size_hint=(0.6, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.kitten)

        # Add button
        self.button = Button(
            text='Показать любовь!',
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.1},
            background_color=(1, 0.4, 0.6, 1),  # Bright pink button
            color=(1, 1, 1, 1)
        )
        self.button.bind(on_press=self.show_love)
        self.add_widget(self.button)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect2.pos = self.pos
        self.rect2.size = (self.size[0], self.size[1] / 2)

    def show_love(self, instance):
        """Show heart animations and change background color"""
        # Animate background color
        new_color = [random(), random(), random(), 1]
        Animation(bg_color=new_color, duration=1).start(self)

        # Create multiple hearts
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
