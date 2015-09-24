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
	audio_files_notes = sorted(glob(join(dirname(__file__), '*_note.wav')))
	audio_files_chords = sorted(glob(join(dirname(__file__), '*_chord.wav')))

	sound = ObjectProperty(None, allownone=True)
	note_file_index = 0
	chord_file_index = 0
	volume = 1.0
	last_gyr_val3 = 0
	sound_type = None

	def build(self):
		try:
			# Enable gyroscope
			gyroscope.enable()
			# Set timer who check for movements
			Clock.schedule_interval(self.on_moove, 1.0/5) #5 calls per second 1.0/5
		except:
			print 'failed to enable gyroscope'
		return AirGuitarBackground()

	def on_moove(self, dt):
		try:
			# Get value from gyroscope
			axe3_value = gyroscope.orientation[2]
			# If phone is shaked
			difference = self.diff_gyr_value(self.last_gyr_val3, axe3_value)
			if (difference >= 1) and (difference <= 2):
				# If there is no sound
				if self.sound is None:
					# Play it
					self.sound_type = "note"
					self.play_sample(self.sound_type)
					# Increment index
					self.note_file_index = self.note_file_index + 1
				# Elif a sound has been played and is in stop state
				elif self.sound.status == 'stop':
					# Clean memory
					self.release_audio()
				elif self.sound.status == 'play':
					# Clean memory
					self.sound.stop()
					self.release_audio()
			elif difference > 3:
				# If there is no sound
				if self.sound is None:
					# Play it
					self.sound_type = "chord"
					self.play_sample(self.sound_type)
					# Increment index
					self.chord_file_index = self.chord_file_index + 1
				# Elif a sound has been played and is in stop state
				elif self.sound.status == 'stop':
					# Clean memory
					self.release_audio()
				elif self.sound.status == 'play':
					# Clean memory
					self.sound.stop()
					self.release_audio()
		except:
			print 'Cannot read gyroscope'

	def diff_gyr_value(self, last_val, new_val):
		# If last value is equal to new value
		if last_val == new_val:
			# No movements
			return 0
		else:
			# Else, return the difference between the two values
			return abs(last_val - new_val)
		# New value is now the last one
		self.last_gyr_val3 = new_val

	def release_audio(self):
		if self.sound:
			self.sound.stop()
			self.sound.unload()
			self.sound = None		

	def play_sample(self, sound_type):
		# If actual index is equal to the length of the audio file tuple
		if self.note_file_index == len(self.audio_files_notes):
			# We've read all the file, start again from index 0
			self.note_file_index = 0
		if self.chord_file_index == len(self.audio_files_chords):
			# We've read all the file, start again from index 0
			self.chord_file_index = 0
		if sound_type == "note":
			# Play sound
			self.sound = SoundLoader.load(self.audio_files_notes[self.note_file_index])
		if sound_type == "chord":
			# Play sound
			self.sound = SoundLoader.load(self.audio_files_chords[self.chord_file_index])
		self.sound.volume = self.volume
		self.sound.play()

if __name__ == '__main__':
	AirGuitarApp().run()
