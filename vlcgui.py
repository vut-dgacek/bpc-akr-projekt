import os
import sys
import platform
import pathlib
from PyQt5 import QtWidgets, QtGui, QtCore


# If platform is winblows use included binary
if platform.system() == "Windows":
	VLC_PATH = f'{pathlib.Path(__file__).resolve().parent}\\bin\\vlc-3.0.20'
	print(VLC_PATH)
	#os.environ['PATH']
	os.environ['PYTHON_VLC_MODULE_PATH'] = VLC_PATH


import vlc


class Player(QtWidgets.QMainWindow):
	def __init__(self, master=None):
		QtWidgets.QMainWindow.__init__(self, master)
		self.setWindowTitle("Media Player")

		# Basic media player instance
		self.instance = vlc.Instance()
		#self.instance = vlc.Instance("--verbose 2".split())	# Usefull for debugging
		self.mediaplayer = self.instance.media_player_new()
		# Add media
		self.media = self.instance.media_new(sys.argv[1])
		self.mediaplayer.set_media(self.media)
		self.media.parse()

		# Set UI
		self.widget = QtWidgets.QWidget(self)
		self.setCentralWidget(self.widget)
		self.videoframe = QtWidgets.QFrame()

		self.palette = self.videoframe.palette()
		self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
		self.videoframe.setPalette(self.palette)
		self.videoframe.setAutoFillBackground(True)

		self.positionslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
		self.positionslider.setToolTip("Position")
		self.positionslider.setMaximum(1000)
		self.positionslider.sliderMoved.connect(self.set_position)
		self.positionslider.sliderPressed.connect(self.set_position)

		self.hbuttonbox = QtWidgets.QHBoxLayout()
		self.playbutton = QtWidgets.QPushButton("Play")
		self.hbuttonbox.addWidget(self.playbutton)
		self.playbutton.clicked.connect(self.play_pause)

		self.stopbutton = QtWidgets.QPushButton("Stop")
		self.hbuttonbox.addWidget(self.stopbutton)
		self.stopbutton.clicked.connect(self.stop)

		self.hbuttonbox.addStretch(1)
		self.volumeslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
		self.volumeslider.setMaximum(100)
		self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
		self.volumeslider.setToolTip("Volume")
		self.hbuttonbox.addWidget(self.volumeslider)
		self.volumeslider.valueChanged.connect(self.set_volume)

		self.vboxlayout = QtWidgets.QVBoxLayout()
		self.vboxlayout.addWidget(self.videoframe)
		self.vboxlayout.addWidget(self.positionslider)
		self.vboxlayout.addLayout(self.hbuttonbox)

		self.widget.setLayout(self.vboxlayout)

		self.timer = QtCore.QTimer(self)
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.update_ui)

		# Additional vlc settings
		# Bind to videoframe
		if platform.system() == "Linux":  # for Linux using the X Server
			self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
		elif platform.system() == "Windows":  # for Windows
			self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
		# Set window title
		self.setWindowTitle(self.media.get_meta(0))

		# Set media state
		self.is_paused = False

	def play_pause(self):
		if self.mediaplayer.is_playing():
			self.mediaplayer.pause()
			self.playbutton.setText("Play")
			self.is_paused = True
			self.timer.stop()
		else:
			if self.mediaplayer.play() == -1:
				self.open_file()
				return

			self.mediaplayer.play()
			self.playbutton.setText("Pause")
			self.timer.start()
			self.is_paused = False

	def stop(self):
		self.mediaplayer.stop()
		self.playbutton.setText("Play")

	def set_volume(self, volume):
		self.mediaplayer.audio_set_volume(volume)

	def set_position(self):
		# Set the media position to where the slider was dragged
		self.timer.stop()
		pos = self.positionslider.value()
		self.mediaplayer.set_position(pos / 1000.0)
		self.timer.start()

	def update_ui(self):
		media_pos = int(self.mediaplayer.get_position() * 1000)
		self.positionslider.setValue(media_pos)

		# No need to call this function if nothing is played
		if not self.mediaplayer.is_playing():
			self.timer.stop()
			if not self.is_paused:
				self.stop()


def main():
	app = QtWidgets.QApplication(sys.argv)
	player = Player()
	player.show()
	player.resize(1280, 720)
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()

