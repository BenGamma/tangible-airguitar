import kivy
kivy.require('1.0.8')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from glob import glob
from plyer import accelerometer
from os.path import dirname, join

class AirGuitarBackground(BoxLayout):
	pass 

class AirGuitarApp(App):

	# Catch audio files names
	audio_files = glob(join(dirname(__file__), '*.wav'))
	
	sound = ObjectProperty(None, allownone=True)
	volume = NumericProperty(1.0)
	file_to_read_index = 0

	def build(self):
		try:
			accelerometer.enable()
			Clock.schedule_interval(self.on_moove, 1.0/5) #5 calls per second 1.0/5
		except:
			print 'failed to enable accelerometer'
		return AirGuitarBackground()

	def on_moove(self, dt):
		try:
			# Get values from accelerometer
			x_value = accelerometer.acceleration[0]
			y_value = accelerometer.acceleration[1]
			z_value = accelerometer.acceleration[2]
			if z_value > 4 and z_value < 7:
				# If there is no sound
				if self.sound is None:
					# Play it
					self.play_sample()
				# Elif a sound has been played and is in stop state
				elif self.sound.status == 'stop':
					# Clean memory
					self.release_audio()
		except:
			print 'Cannot read accelerometer'

	def release_audio(self):
		if self.sound:
			self.sound.stop()
			self.sound.unload()
			self.sound = None		

	def play_sample(self):
		# If actual index is equal to the length of the audio file tuple
		if self.file_to_read_index == len(self.audio_files):
			# We've read all the file, start again from index 0
			self.file_to_read_index = 0
		# Play sound	
		self.sound = SoundLoader.load(self.audio_files[self.file_to_read_index])
		self.sound.volume = self.volume
		self.sound.play()
		# Increment index
		self.file_to_read_index = self.file_to_read_index + 1

if __name__ == '__main__':
	AirGuitarApp().run()
