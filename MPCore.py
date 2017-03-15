# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from objc_util import NSBundle, ObjCClass
from NotificationController import NotificationController
from UIController import UIController

class MPCore:
	def __init__(self, ui_file_path):
		NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
		self._player = ObjCClass('MPMusicPlayerController').systemMusicPlayer()
		self._nc = NotificationController(self)
		self._uic = UIController(self, ui_file_path)
	def start(self):
		self._nc.registerAllObservers()
		self._player.beginGeneratingPlaybackNotifications()
		self._uic.start()
	def close(self):
		self._uic.stop()
		self._player.endGeneratingPlaybackNotifications()
		self._nc.removeAllObservers()
	def updatePlaybackState(self, state=''):
		ar = ['Stopped', 'Playing', 'Paused', 'Interrupted', 'SeekingForward', 'SeekingBackward']
		if state=='':
			state = ar[self._player.playbackState()]
		self._uic.eval_js('updatePlaybackState("'+state+'");')
	def togglePlayPause(self):
		state = self._player.playbackState()
		if state==0 or state==2:
			self._player.play()
			self.updatePlaybackState(state='Playing')
		elif (state==1):
			self._player.pause()
			self.updatePlaybackState(state='Paused')
	def cmdProc(self, cmd, query):
		print('%s: %s' % (cmd, query))
		if cmd=='close':
			self.close()
		elif cmd=='togglePlayPause':
			self.togglePlayPause()
		elif cmd=='updatePlaybackState':
			self.updatePlaybackState()
		else:
			pass
		
