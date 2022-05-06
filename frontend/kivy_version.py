from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from searcher import find_content
from kivy.uix.label import Label
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from searcher import task


class Container(GridLayout, Screen):

    def open_kivy_video(self, link):
        """
        Отдельно по по ссылкам строит плейеры к обрезанным видео.
        """
        player = VideoPlayer(
            source=link,
            options={'eos': 'loop'}, size_hint_y=None, height=500)
        player.volume = 1
        return player

    def go_study(self):
        """
        Строит слои на старнице через цикл
        Слой названия примера
        Слой определения слова
        Слой субтитра
        Слой видеоролика
        """
        self.grid.bind(minimum_height=self.grid.setter('height'))
        content = find_content.get_content(self.input.text)
        video_subtitles_dict = find_content.get_video(content)
        definition_word = Label(text=f'Definition: {find_content.get_definition(self.input.text)}',
                                     color=(0.2, 0.6, 0.6, 1))
        self.grid.add_widget(definition_word)

        for element in video_subtitles_dict:

            label = Label(text=video_subtitles_dict[element][1], size_hint_y=None, height=40,
                          color=(0.2, 0.6, 0.6, 1))

            intro = Label(text=f'Video № {element}', color=(0, 0, 0, 1), size_hint_y=None, height=40)

            self.grid.add_widget(intro)
            self.grid.add_widget(self.open_kivy_video(video_subtitles_dict[element][0]))
            self.grid.add_widget(label)

    def go_task(self):
        """
        переход к странице с заданиями
        """
        self.manager.transition.direction = 'left'
        self.manager.current = 'task'


class Task(Screen):
    def __init__(self, **kwargs):
        """
        Строит старницу с заданиями
        слой объяснения задания
        Слой самого задания
        """
        super().__init__(**kwargs)
        self.condition = Label(text='build the right sentences')
        self.task_grid.add_widget(self.condition)
        for counter, element in enumerate(task.build_correct_sentence_task('english')):
            self.lyrics = Label(text=f'№ {counter+1}:\n {element}', size_hint_y=None, height=40,
                                color=(0.2, 0.6, 0.6, 1), size_hint=(1.0, 1.0), halign="left", valign="middle")
            self.lyrics.bind(size=self.lyrics.setter('text_size'))
            self.task_grid.add_widget(self.lyrics)

    def go_main(self, *args):
        """
        возврат на главную страницу
        """
        self.manager.transition.direction = 'right'
        self.manager.current = 'container'

    def checker_task(self):
        """
        проверка задания
        """
        self.label_answer_task.text = task.checker('english', self.text_answer.text)


class WebApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Container(name='container'))
        sm.add_widget(Task(name='task'))
        return sm


if __name__ == '__main__':
    WebApp().run()
