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
		self.nmo = create_objc_class(
				'MP4PNotificationController',
				methods = [
					willResignActive,
					didBecomeActive,
					playbackStateDidChange,
					nowPlayingItemDidChange,
					MP4PWillClose
				]
			).alloc()
		self.nc = ObjCClass('NSNotificationCenter').defaultCenter()
	def registerAllObservers(self):
		self.nc.addObserver_selector_name_object_(
			self.nmo,
			sel('willResignActive'),
			'UIApplicationWillResignActiveNotification',
			None
		)
		self.nc.addObserver_selector_name_object_(
			self.nmo,
			sel('didBecomeActive'),
			'UIApplicationDidBecomeActiveNotification',
			None
		)
		self.nc.addObserver_selector_name_object_(
			self.nmo,
			sel('playbackStateDidChange'),
			'MPMusicPlayerControllerPlaybackStateDidChangeNotification',
			None
		)
		self.nc.addObserver_selector_name_object_(
			self.nmo,
			sel('nowPlayingItemDidChange'),
			'MPMusicPlayerControllerNowPlayingItemDidChangeNotification',
			None
		)
		self.nc.addObserver_selector_name_object_(
			self.nmo,
			sel('MP4PWillClose'),
			'MP4PythonistaWillCloseNotification',
			None
		)
		self.mpc.player.beginGeneratingPlaybackNotifications()
	def removeAllObservers(self):
		self.nc.removeObserver_name_object_(
			self.nmo,
			'UIApplicationWillResignActiveNotification',
			None
		)
		self.nc.removeObserver_name_object_(
			self.nmo,
			'UIApplicationDidBecomeActiveNotification',
			None
		)
		self.nc.removeObserver_name_object_(
			self.nmo,
			'MPMusicPlayerControllerPlaybackStateDidChangeNotification',
			None
		)
		self.nc.removeObserver_name_object_(
			self.nmo,
			'MPMusicPlayerControllerNowPlayingItemDidChangeNotification',
			None
		)
		self.nc.removeObserver_name_object_(
			self.nmo,
			'MP4PythonistaWillCloseNotification',
			None
		)
		self.mpc.player.endGeneratingPlaybackNotifications()

