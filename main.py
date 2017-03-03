# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from objc_util import ObjCClass
from DBGUtils import *
import MPUtils
	
if __name__ == '__main__':
	MPUtils.init()
	
	player = MPUtils.getPlayer()
	mq = ObjCClass('MPMediaQuery').songsQuery()
	
	f0 = MPUtils.createFilter('isCloudItem', False)
	mq.addFilterPredicate(f0)
	
	player.setQueueWithQuery(mq)
	player.prepareToPlay()
	#player.play()

	print()
