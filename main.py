# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
from DBGUtils import *
from MPCore import MPCore

import settings

def main():
	_path = os.path.dirname(os.path.abspath(__file__))
	mpc = MPCore(_path + '/' + settings.ui.dir + '/' + settings.ui.top_page)
	#give a abspath
	mpc.start()

if __name__ == '__main__':
	main()

