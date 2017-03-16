# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import base64
from io import BytesIO
from PIL import Image

from objc_util import NSBundle, ObjCClass, uiimage_to_png
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

	def close(self, _=None):
		self._uic.stop()
		self._player.endGeneratingPlaybackNotifications()
		self._nc.removeAllObservers()
		del self._npc
		del self._uic
		del self._nc
		del self._player

	def init_params(self, query):
		self.thumb_size = int(query['thumb_size'][0])
		self.updatePlaybackState();
		self.setNowPlayingSongArtwork()

	def updatePlaybackState(self, _=None):
		self._uic.eval_js(
			'updatePlaybackState("' + self._npc.state.name + '");'
		)

	def togglePlayPause(self, _=None):
		self._npc.play_pause()

	def setNowPlayingSongArtwork(self, _=None):
		img = self._npc.now_playing.artwork(brep=False)
		if not img.size[0] == img.size[1]:
			smaller = min(img.size[0], img.size[1])
			img = img.crop((
				int((img.size[0] - smaller) / 2.0),
				int((img.size[1] - smaller) / 2.0),
				int((img.size[0] + smaller) / 2.0),
				int((img.size[1] + smaller) / 2.0)
			))
		img.thumbnail((self.thumb_size, self.thumb_size), Image.ANTIALIAS)
		buf = BytesIO()
		img.save(buf, format='PNG')
		self._uic.eval_js(
			'setNowPlayingSongArtwork("%s");'
			%  base64.b64encode(buf.getvalue()).decode('ascii')
		)

	def cmdProc(self, cmd, query):
		print('%s: %s' % (cmd, query))
		try:
			getattr(self, cmd)(query)
		except:
			print('Unknown Command')
			raise
		if not cmd == 'close':
			self._uic.eval_js(
				'pick_cmd();'
			)
		
