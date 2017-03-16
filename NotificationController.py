# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from objc_util import ObjCClass, create_objc_class, sel


class NotificationController:
	def __init__(self, l_mpc):
		self._mpc = l_mpc
		self._ndc = ObjCClass('NSNotificationCenter').defaultCenter()
		def willResignActive(_self, _cmd):
			pass
		def didBecomeActive(_self, _cmd):
			pass
		def playbackStateDidChange(_self, _cmd):
			self._mpc.updatePlaybackState()
		def nowPlayingItemDidChange(_self, _cmd):
			pass
		self._method_table = {
			'UIApplicationWillResignActiveNotification'
				: willResignActive,
			'UIApplicationDidBecomeActiveNotification'
				: didBecomeActive,
			'MPMusicPlayerControllerPlaybackStateDidChangeNotification'
				: playbackStateDidChange,
			'MPMusicPlayerControllerNowPlayingItemDidChangeNotification'
				: nowPlayingItemDidChange,
		}
		self._mp4p_nc = create_objc_class(
			'NSMP4PNotificationController',
			methods = self._method_table.values()
		).new()

	def __del__(self):
		del self._mp4p_nc
		del self._method_table
		del self._ndc

	def registerAllObservers(self):
		for k,v in self._method_table.items():
			self._ndc.addObserver_selector_name_object_(
				self._mp4p_nc,
				sel(v.__name__),
				k,
				None
			)

	def removeAllObservers(self):
		for k in self._method_table.keys():
			self._ndc.removeObserver_name_object_(
				self._mp4p_nc,
				k,
				None
			)

