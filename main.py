from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MeuApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.label = Label(text="App Criada no Termux 🚀", font_size=20)
        botao = Button(text='Clique Aqui', font_size=24, background_color=(0.1, 0.5, 0.8, 1))
        botao.bind(on_press=self.mudar_texto)

        layout.add_widget(self.label)
        layout.add_widget(botao)
        return layout

    def mudar_texto(self, instance):
        self.label.text = "Compilado com Sucesso na Nuvem! 🔥"

if __name__ == '__main__':
    MeuApp().run()
