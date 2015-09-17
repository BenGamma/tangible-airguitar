import kivy
kivy.require('1.0.8')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from glob import glob
from plyer import gyroscope
from os.path import dirname, join

class AirGuitarBackground(BoxLayout):
	pass 

class AirGuitarApp(App):

	# Catch sorted audio files names
	audio_files = sorted(glob(join(dirname(__file__), '*.wav')))	
	sound = ObjectProperty(None, allownone=True)
	file_to_read_index = 0
	volume_for_moove = 0
	last_gyr_val3 = 0

	def build(self):
		try:
			gyroscope.enable()
			Clock.schedule_interval(self.on_moove, 1.0/5) #5 calls per second 1.0/5
		except:
			print 'failed to enable gyroscope'
		return AirGuitarBackground()

	def on_moove(self, dt):
		try:
			# Get value from gyroscope
			axe3_value = gyroscope.orientation[2]
			# If phone is shaked
			if self.diff_gyr_value(self.last_gyr_val3, axe3_value) >= 2:
				# Get value of shake to set volume
				volume_for_moove = (self.diff_gyr_value(self.last_gyr_val3, axe3_value))/10
				# If there is no sound
				if self.sound is None:
					# Play it
					self.play_sample(volume_for_moove)
				# Elif a sound has been played and is in stop state
				elif self.sound.status == 'stop':
					# Clean memory
					self.release_audio()
		except:
			print 'Cannot read gyroscope'

	def diff_gyr_value(self, last_val, new_val):
		if last_val == new_val:
			return 0
		else:
			return abs(last_val - new_val)
		self.last_gyr_val3 = new_val

	def release_audio(self):
		if self.sound:
			self.sound.stop()
			self.sound.unload()
			self.sound = None		

	def play_sample(self, volume):
		# If actual index is equal to the length of the audio file tuple
		if self.file_to_read_index == len(self.audio_files):
			# We've read all the file, start again from index 0
			self.file_to_read_index = 0
		# Play sound	
		self.sound = SoundLoader.load(self.audio_files[self.file_to_read_index])
		self.sound.volume = volume
		self.sound.play()
		# Increment index
		self.file_to_read_index = self.file_to_read_index + 1

if __name__ == '__main__':
	AirGuitarApp().run()
