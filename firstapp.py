import kivy
kivy.require("1.10.1")

from kivy.app import App #base class of our app inherits from App class

from kivy.uix.label import Label  #For rendering text
from kivy.uix.gridlayout import GridLayout  # widgets
from kivy.uix.textinput import TextInput  #input text from user 
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import os

class ConnectPage(GridLayout):
	"""docstring for ConnectPage"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 2
		
		if os.path.isfile("prev_details.txt"):
			with open("prev_details.txt", "r") as f:
				d = f.read().split(",")
				prev_ip = d[0]
				prev_port = d[1]
				prev_username = d[2]
		else:
			prev_ip = ""
			prev_port = ""
			prev_username = ""

		self.add_widget(Label(text="IP:"))

		self.ip = TextInput(text=prev_ip,multiline=False)
		self.add_widget(self.ip)

		self.add_widget(Label(text="Port:"))

		self.port = TextInput(text=prev_port,multiline=False)
		self.add_widget(self.port)
		
		self.add_widget(Label(text="Username:"))

		self.username = TextInput(text=prev_username,multiline=False)
		self.add_widget(self.username)
		
		self.join = Button(text="Join")
		self.join.bind(on_press=self.join_button)
		self.add_widget(Label())
		self.add_widget(self.join)
		
	def join_button(self, instance):
		port = self.port.text
		ip = self.ip.text
		username = self.username.text
		with open("prev_details.txt", "w") as f:
			f.write(f"{ip},{port},{username}")

		info = f"Attempting to join {ip}:{port} as {username}"
		chat_app.info_page.update_info(info)
		chat_app.screen_manager.current = "Info"


class InfoPage(GridLayout):
	"""docstring for InfoPage"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 1
		self.message = Label(halign="center", valign="middle", font_size="30")
		self.message.bind(width=self.update_text_width)
		self.add_widget(self.message)

	def update_info(self, message):
		self.message.text = message

	def update_text_width(self, *_):
		self.message.text_size = (self.message.width*0.9, None)



class DemoApp(App):
	def build(self):
		self.screen_manager = ScreenManager()

		self.connect_page = ConnectPage()
		screen = Screen(name="Connect")
		screen.add_widget(self.connect_page)
		self.screen_manager.add_widget(screen)

		self.info_page = InfoPage()
		screen = Screen(name="Info")
		screen.add_widget(self.info_page)
		self.screen_manager.add_widget(screen)

		return self.screen_manager


if __name__ == '__main__':
	chat_app = DemoApp()
	chat_app.run()