# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from objc_util import NSBundle, ObjCClass
import inspect

def dp(o):
	try:
		cname = o._get_objc_classname()
		cname = cname.decode('utf-8')
	except AttributeError:
		cname = 'Non-Objective-C object'
	finally:
		for i in dir(o):
			print(i);
		print('[%s]\n' % cname)

def printMediaItem(item, verbose=False):
	print(item.title())
	if verbose:
		print('- artist: %s' % item.artist())
		print('- albumTitle: %s' % item.albumTitle())
		print('- persistentID: %d' % item.persistentID())
		print('- isCloudItem: %r' % item.isCloudItem())

def printItemCollections(ls, verbose=False):
	for item in ls:
		try:
			item.title()
		except AttributeError: #collections?
			try:
				item = item.items()[0] #item position in collections()[i]
			except AttributeError:
				print('Neither items nor collections.')
				raise
			except:
				raise
		printMediaItem(item, verbose)
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

	print()
