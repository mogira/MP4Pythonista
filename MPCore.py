# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from objc_util import *

class MPCore:
	def __init__(self):
		NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
		self.player = ObjCClass('MPMusicPlayerController').systemMusicPlayer()
	
