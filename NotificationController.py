# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from objc_util import *

class NotificationController:
	def __init__(self, l_mpc):
		self.mpc = l_mpc
		def willResignActive(_self, _cmd):
			pass
		def didBecomeActive(_self, _cmd):
			pass
		def playbackStateDidChange(_self, _cmd):
			pass
		def nowPlayingItemDidChange(_self, _cmd):
			pass
		def MP4PWillClose(_self, _cmd):
			self.removeAllObservers()
		self.method_table = {
			'UIApplicationWillResignActiveNotification'
				: willResignActive,
			'UIApplicationDidBecomeActiveNotification'
				: didBecomeActive,
			'MPMusicPlayerControllerPlaybackStateDidChangeNotification'
				: playbackStateDidChange,
			'MPMusicPlayerControllerNowPlayingItemDidChangeNotification'
				: nowPlayingItemDidChange,
			'MP4PythonistaWillCloseNotification'
				: MP4PWillClose,
		}
		self.mp4p_nc = create_objc_class(
				'MP4PNotificationController',
				methods = self.method_table.values()
		).alloc()
		self.ndc = ObjCClass('NSNotificationCenter').defaultCenter()
	def registerAllObservers(self):
		for k,v in self.method_table.items():
			self.ndc.addObserver_selector_name_object_(
				self.mp4p_nc,
				sel(v.__name__),
				k,
				None
			)
		self.mpc.player.beginGeneratingPlaybackNotifications()
	def removeAllObservers(self):
		for k in self.method_table.keys():
			self.ndc.removeObserver_name_object_(
				self.mp4p_nc,
				k,
				None
			)
		self.mpc.player.endGeneratingPlaybackNotifications()

