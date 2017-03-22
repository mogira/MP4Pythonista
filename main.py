# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
from DBGUtils import *
from MPCore import MPCore


if __name__ == '__main__':
	_path = os.path.dirname(os.path.abspath(__file__))
	mpc = MPCore(_path + '/UI/UI.html')
	#please abspath
	mpc.start()

