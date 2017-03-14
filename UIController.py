# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from objc_util import *
import ui
import time
import re
import os

class UIController(object):
	def __init__(self, l_mpc, ui_file):
		self.mpc = l_mpc
		self.wv = ui.WebView()
		try:
			f = open(ui_file, 'r')
			html_data = f.read()
			f.close()
		except:
			print('Fail to open "%s"'%ui_file)
			raise
		t = str(time.time()).split('.')[0]
		html_data = re.sub('BASEPATH', "file://"+os.path.dirname(os.path.abspath(ui_file)), html_data)
		html_data = re.compile(r'(\.css|\.js)', re.I|re.M).sub(r'\1?v='+t, html_data)
		self.wv.delegate = self
		self.wv.load_html(html_data)
		print(html_data)
		#external css and javascript file is cached, and cannot delete easily.
		#so use "file://" scheme and abspath and Cache Busting.
		#in this function, 'BASEPATH' string in ui_file is replaced to os.path.dirname(ui_file).
	def showView(self):
		self.wv.present(hide_title_bar=True)
	def cmdProc(self, com):
			print(com)
			ar = ['Stopped', 'Playing', 'Paused', 'Interrupted', 'SeekingForward', 'SeekingBackward']
			if com=='close':
				self.wv.close()
				self.wv.delegate = None
				self.wv.stop()
				self.wv = None
				ObjCClass('NSNotificationCenter').defaultCenter().postNotification(
						ObjCClass('NSNotification').notificationWithName_object_userInfo_('CustomMPCloseNotification', None, None)
				)
			elif com=='playstop':
				state = self.mpc.player.playbackState()
				if state==0 or state==2:
					self.mpc.player.play()
					self.wv.eval_js('document.getElementById("playstop").className = "PlaybackState-Playing";')
				elif (state==1):
					self.mpc.player.pause()
					self.wv.eval_js('document.getElementById("playstop").className = "PlaybackState-Paused";')
			elif com=='updatePlaybackState':
				state = self.mpc.player.playbackState()
				self.wv.eval_js('updatePlaybackState("'+ar[state]+'");')
			elif com=='next':
				self.mpc.player.skipInDirection_error_(1, None)
			else:
				return
	def webview_should_start_load(self, webview, url, nav_type):
		tmp = url.split(':')
		scheme = tmp[0]
		if scheme == 'app':
			com = tmp[1].split('/')[-1]
			self.cmdProc(com)
			return False
		return True
	def webview_did_start_load(self, webview):
		pass
	def webview_did_finish_load(self, webview):
		pass
	def webview_did_fail_load(self, webview, error_code, error_msg):
		print('error')
		
