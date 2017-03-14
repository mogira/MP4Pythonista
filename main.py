# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from DBGUtils import *
from MPCore import MPCore
from NotificationController import NotificationController
from UIController import UIController
	
if __name__ == '__main__':
	mpc = MPCore()
	nc = NotificationController(mpc)
	nc.registerAllObservers()
	uic = UIController(mpc, 'UI/UI.html')
	uic.showView()
