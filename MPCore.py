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
		self.thumb_size = 0

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
		if not self._npc.now_playing == None:
			img = self._npc.now_playing.artwork(brep=False)
			if not img.size[0] == img.size[1]:
				smaller = min(img.size[0], img.size[1])
				img = img.crop((
					int((img.size[0] - smaller) / 2.0),
					int((img.size[1] - smaller) / 2.0),
					int((img.size[0] + smaller) / 2.0),
					int((img.size[1] + smaller) / 2.0)
				))
			img = img.resize((self.thumb_size, self.thumb_size), Image.ANTIALIAS)
		else:
			img = Image.new('RGB', (self.thumb_size, self.thumb_size), (0xFF, 0xFF, 0xFF))
		buf = BytesIO()
		img.save(buf, format='PNG')
		self._uic.eval_js(
			'setNowPlayingSongArtwork("%s");'
			%  base64.b64encode(buf.getvalue()).decode('ascii')
		)

	def skipNext(self, _=None):
		self._npc.skip_next()

	def skipPrev(self, _=None):
		if self._player.currentPlaybackTime() < 1.5:
			self._npc.skip_previous()
		else:
			self._npc.replay()

	def cmdProc(self, cmd, query):
		print('%s: %s' % (cmd, query))
		try:
			m = getattr(self, cmd)
		except AttributeError:
			self._uic.eval_js(
				r'alert("Unknown Command\n\"%s\"");' % cmd
			)
		except:
			raise
		else:
			m(query)

