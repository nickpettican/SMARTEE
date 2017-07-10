#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ___        SMARTEE V 0.0.1 by nickpettican			___
# ___        Social Media Automated Research 			___
# ___		 Tool for Evaluating Engagement	         	___

# ___        Copyright 2017 Nicolas Pettican            ___

# ___    This software is licensed under the Apache 2   ___
# ___    license. You may not use this file except in   ___
# ___    compliance with the License.                   ___
# ___    You may obtain a copy of the License at        ___

# ___    http://www.apache.org/licenses/LICENSE-2.0     ___

# ___    Unless required by applicable law or agreed    ___
# ___    to in writing, software distributed under      ___
# ___    the License is distributed on an "AS IS"       ___
# ___    BASIS, WITHOUT WARRANTIES OR CONDITIONS OF     ___
# ___    ANY KIND, either express or implied. See the   ___
# ___    License for the specific language governing    ___
# ___    permissions and limitations under the License. ___

import arrow
from csv import writer
from os import mkdir, path

class Logger:

	def __init__(self, module):
		# initialise the logger variables

		self.path = 'cache/' + module
		self.log_temp = ''
		
		if not path.isdir('cache/'):
			mkdir('cache/')
		
		self.init_log_name()

		if not path.isdir(self.path):
			mkdir(self.path)

		header = '\n\t\t\tSMARTEE 1.0.0 by nickpettican\
					\n\tSocial Media Automated Research Tool to Evaluate Engagement\n'

		print header

	def init_log_name(self):
		# change log file name

		self.week = self.weekAndYear()
		self.log_main = []
		self.log_file = self.path + '/log_' + self.week + '_SMARTEE.csv'

	def log(self, string):
		# write to log file

		try:
			if self.week != self.weekAndYear():
				self.init_log_name()

			if string == 'START':
				print self.header
				self.log_temp = ''
				return

			if string.endswith('\,'):
				log = string.replace('\,', '')
				print log,
				if self.log_temp:
					try:
						self.log_temp += log
					except:
						pass
				else:
					self.log_temp = log

			else:
				log = string
				print log
				if self.log_temp:
					string = self.log_temp + string
					self.log_temp = ''

				self.log_main.append([string.strip()])

			self.backup()

		except Exception as e:
			print 'Error with the logger: %s' %(e)

	def weekAndYear(self):
		# returns the week of the year

		return '_'.join(str(x) for x in arrow.now().isocalendar()[0:2])

	def backup(self):
		# backs up the log

		try:
			with open(self.log_file, 'wb') as log:
				w = writer(log)
				w.writerows(self.log_main)

		except Exception as e:
			print 'Error backing up: %s' %(e)
