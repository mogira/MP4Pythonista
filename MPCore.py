# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from objc_util import NSBundle, ObjCClass
from objc_tools.music import NowPlayingController, PlaybackState

from NotificationController import NotificationController
from UIController import UIController


class MPCore:
	def __init__(self, ui_file_path):
		NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
		self._player = ObjCClass('MPMusicPlayerController').systemMusicPlayer()
		self._nc = NotificationController(self)
		self._uic = UIController(self, ui_file_path)
		self._npc = NowPlayingController()

	def start(self):
		self._nc.registerAllObservers()
		self._player.beginGeneratingPlaybackNotifications()
		self._uic.start()

	def close(self):
		self._uic.stop()
		self._player.endGeneratingPlaybackNotifications()
		self._nc.removeAllObservers()
		del self._npc
		del self._uic
		del self._nc
		del self._player

	def updatePlaybackState(self):
		ar = ['Stopped', 'Playing', 'Paused', 'Interrupted', 'SeekingForward', 'SeekingBackward']
		self._uic.eval_js(
			'updatePlaybackState("' + self._npc.state.name + '");'
		)

	def togglePlayPause(self):
		self._npc.play_pause()

	def cmdProc(self, cmd, query):
		print('%s: %s' % (cmd, query))
		if cmd == 'close':
			self.close()
		elif cmd == 'togglePlayPause':
			self.togglePlayPause()
		elif cmd == 'updatePlaybackState':
			self.updatePlaybackState()
		else:
			pass
		
