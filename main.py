# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from objc_util import NSBundle, ObjCClass
import inspect

def dp(o):
	print(o.__class__.__name__)
	if hasattr(o, '__call__'):
		print(inspect.getargspec(o))
	else:
		print(dir(o))

def printItems(ls, verbose=False):
	for item in ls:
		print(item.title())
		if verbose:
			print('- artist: %s' % item.artist())
			print('- albumTitle: %s' % item.albumTitle())
			print('- persistentID: %d' % item.persistentID())
			print('- isCloudItem: %r' % item.isCloudItem())
	print()

def createFilter(property, value, is_contains=0):
	mpp = ObjCClass('MPMediaPropertyPredicate').alloc()
	mpp.setProperty(property)
	mpp.setValue(value)
	mpp.setComparisonType(is_contains)
	return mpp
	
if __name__ == '__main__':
	NSBundle.bundleWithPath_('/System/Library/Frameworks/MediaPlayer.framework').load()
	MPMusicPlayerController = ObjCClass('MPMusicPlayerController')
	MPMediaQuery = ObjCClass('MPMediaQuery')
	
	player = MPMusicPlayerController.systemMusicPlayer()
	mq = MPMediaQuery.songsQuery()
	
	f0 = createFilter('isCloudItem', False)
	mq.addFilterPredicate(f0)
	
	player.setQueueWithQuery(mq)
	player.prepareToPlay()
	#player.play()
	
	printItems(mq.items())

