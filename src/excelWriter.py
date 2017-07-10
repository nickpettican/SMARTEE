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

from openpyxl import Workbook
from openpyxl.styles import Alignment
from os import path, mkdir
import arrow

class outputExcel:

	def __init__(self, mode, console):
		# initialise Excel writer with the mode

		self.mode = mode
		self.console = console
		self.check_path()

	def check_path(self):
		# create folder if not present

		if not path.isdir('results'):
			mkdir('results')

		self.day_path = 'results/' + str(arrow.now().format('DD_MM_YYYY/'))

		if not path.isdir(self.day_path):
			mkdir(self.day_path)

		self.out_path = 'results/' + str(arrow.now().format('DD_MM_YYYY/')) + 'Instagram/'

		if not path.isdir(self.out_path):
			mkdir(self.out_path)

	def prepareData(self, data):
		# organises the data into an easily writable format
		# matrix of posts as the rows, columns being the data fields in those posts
		# organised by username and popularity

		header = ['Username', 'Followers', 'Following', 'Media', 'Date Published', 'Popularity Score', 'Likes', 'Comments', 'Caption', 'URL', 'Image URL', 'Hashtags']
		final = {key: header for key in data['hashtags'].keys()}
		order = ['date', 'popularity', 'likes_count', 'comments_count', 'caption', 'url', 'display_src', 'hashtags']

		for hashtag, user_data_list in data['hashtags'].items():
			for user_data in user_data_list:
				rows = [[user_data.keys()[0], user_data.values()[0]['followers'], user_data.values()[0]['following'], user_data.values()[0]['media']['count']] +
						[post_data[i] for i in order] for post_data in user_data.values()[0]['media']['nodes'] if post_data]

				sorted_rows = sorted(rows, key = lambda x: -x[5])
				final[hashtag].extend(sorted_rows)

		return final

	def write(self, data):
		# writes the instaCrawl object to xlsx

		final = self.prepareData(data)
		for row in final.values()[0]:
			print row
