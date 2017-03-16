# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import ui
import time
import re
import os
from urllib.parse import urlparse, parse_qs


class UIController(object):
	def __init__(self, l_mpc, ui_file_path):
		self._mpc = l_mpc
		self._wv = ui.WebView()
		self._filepath = ui_file_path

	def __del__(self):
		del self._filepath
		del self._wv
		del self._mpc

	def start(self):
		try:
			f = open(self._filepath, 'r')
			html_data = f.read()
			f.close()
		except:
			print('Fail to open "%s"' % self._filepath)
			raise
		t = str(time.time()).split('.')[0]
		html_data = re\
			.compile('BASEPATH', re.I|re.M)\
			.sub("file://" + os.path.dirname(os.path.abspath(self._filepath)), html_data)
		html_data = re\
			.compile(r'(\.css|\.js)', re.I|re.M)\
			.sub(r'\1?v='+t, html_data)
			#external css and javascript file is cached, and cannot be deleted easily.
			#so use "file://" scheme and abspath and Cache Busting.
			#in this function, 'BASEPATH' string in ui_file is replaced to os.path.dirname(ui_file).
		self._wv.delegate = self
		self._wv.load_html(html_data)
		print(html_data)
		self._wv.present(hide_title_bar=True)

	def stop(self):
		self._wv.delegate = None
		self._wv.close()
		self._wv.stop()

	def eval_js(self, str):
		self._wv.eval_js(str);

	def webview_should_start_load(self, webview, url, nav_type):
		u = urlparse(url)
		if u.scheme == 'app':
			self._mpc.cmdProc(u.netloc, parse_qs(u.query))
			return False
		else:
			return True

	def webview_did_start_load(self, webview):
		pass

	def webview_did_finish_load(self, webview):
		pass

	def webview_did_fail_load(self, webview, error_code, error_msg):
		print('error')

