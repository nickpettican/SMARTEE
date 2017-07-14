#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ___        SMARTEE V 0.0.1 by nickpettican            ___
# ___        Social Media Automated Research            ___
# ___        Tool for Evaluating Engagement             ___

# ___        Copyright 2017 Nicolas Pettican			___

# ___    This software is licensed under the Apache 2	___
# ___    license. You may not use this file except in 	___
# ___    compliance with the License.					___
# ___    You may obtain a copy of the License at 		___

# ___    http://www.apache.org/licenses/LICENSE-2.0		___

# ___    Unless required by applicable law or agreed	___
# ___    to in writing, software distributed under		___
# ___    the License is distributed on an "AS IS"		___
# ___    BASIS, WITHOUT WARRANTIES OR CONDITIONS OF 	___
# ___    ANY KIND, either express or implied. See the 	___
# ___    License for the specific language governing	___
# ___    permissions and limitations under the License.	___

from instaFunctions import *
from logger import Logger
from excelWriter import outputExcel
from requests.exceptions import ConnectionError
from time import sleep
from os import path, mkdir

class instaCrawl:
	# the continuous version of instaCrawl
	
	def __init__(self, params = {'project': 'default', 'tags': [], 'tags_to_avoid': [], 'list_of_users': [], 'only_top_performing': False}):
		# get everything started

		self.name = params['project']
		self.only_top = params['only_top_performing']
		self.list_of_users_path = params['list_of_users']
		self.tags = params['tags']
		self.tags_to_avoid = params['tags_to_avoid']
		self.console = Logger('instaCrawlLog')
		self.timelimit = return_timelimit(self.console)
		self.browser = start_requests(self.console)
		self.import_data()
		
	def import_data(self):
		# import the data or initiate it

		try:
			# import previous JSON if available
			# this way it will continue from when it stopped
			if path.isfile('cache/JSON/%s.json' %(self.name)):
				with open('cache/JSON/%s.json' %(self.name)) as data_file:
					self.data = json.load(data_file)
			
			else:
				# just for guiding purposes
				post_temp = {
					'caption': False,
					'id': False,
					'timestamp': False,
					'date': False,
					'code': False,
					'display_src': False,
					'url': False,
					'owner_username': False,
					'likes_count': 0,
					'comments_count': 0,
					'owner_id': False,
					'hashtags': False,
					'popularity': False
				}
				person_temp = {
					'followers': False,
					'following': False,
					'media': {
						'count': 0,
						'nodes': [post_temp]
					}	
				}
				self.data = {
					# it would look like -> 'hashtags': {'hashtag': [{'username': person_temp}]},
					'hashtags': {},
					'post_ids': [],
					'users': []
				}

			self.users = False

			if type(self.list_of_users_path) == str:
				# import user list and flip to columns
				users_matrix_raw = [[box.strip() for box in line.split(',')] for line in open(self.list_of_users_path, 'rb') if line]
				users_matrix = zip(*users_matrix_raw)
				
				if not any('instagram' in group[0].lower() for group in users_matrix):
					# if there is a list, it has to be read somehow
					self.console.log('Could not read the imported file properly or data is missing: no Instagram column')
					exit('\nAborted\n')

				for group in users_matrix:
					if 'instagram' in group[0].lower():
						self.users = group[1:]
						break

			elif type(self.list_of_users_path) == list and self.list_of_users_path:
				self.users = self.list_of_users_path

		except Exception as e:
			self.console.log('Error importing data: %s' %(e))
			exit('\nCannot start due to error\n')
			
	def backup_data(self):
		# what does this do? oh yes: back up the data

		try:
			backupPath = 'cache/JSON'
			
			if not path.isdir(backupPath):
				mkdir(backupPath)

			with open('%s/%s.json' %(backupPath, self.name), 'wb') as outfile:
				json.dump(self.data, outfile)

		except Exception as e:
			self.console.log('Error backing up: %s' %(e))
			
	def organise_data(self, tag, posts, data):
		# will handle the organisation of data
		
		for post in posts:
			print '# ',
			try:
				if any(n in post['caption'] for n in self.tags_to_avoid):
					# skip this one
					continue

				if tag not in data['hashtags'].keys():
					# new hashtag entry
					data['hashtags'][tag] = []

				user_data = get_user_data(post['owner_username'], self.browser, self.console)

				try:
					post['popularity'] = ((post['likes_count'] + post['comments_count']) * 100) / user_data['followers']
				except ZeroDivisionError:
					post['popularity'] = 0
				
				if user_data:
					if post['owner_username'] in data['users']:
						# update user data
						for i, user in enumerate(data['hashtags'][tag]):
							if post['owner_username'] == user.keys()[0]:
								data['hashtags'][tag][i][post['owner_username']]['followers'] = user_data['followers']
								data['hashtags'][tag][i][post['owner_username']]['following'] = user_data['following']
								data['hashtags'][tag][i][post['owner_username']]['media']['count'] = user_data['media']['count']
								if post['id'] not in data['post_ids']:
									# new post
									data['hashtags'][tag][i][post['owner_username']]['media']['nodes'].append(post)
									data['post_ids'].append(post['id'])
									break
								# update post data
								for n, node in enumerate(data['hashtags'][tag][i][post['owner_username']]['media']['nodes']):
									if post['id'] == node['id']:
										data['hashtags'][tag][i][post['owner_username']]['media']['nodes'][n] = post
										break
								break
						continue
					# user is new
					data['users'].append(post['owner_username'])
					data_to_add = {post['owner_username']: user_data}
					data_to_add[post['owner_username']]['media']['nodes'] = [post]
					data['hashtags'][tag].append(data_to_add)
					data['post_ids'].append(post['id'])

			except Exception as e:
				self.console.log("Error organising %s's data: %s" %(post['owner_username'], e))

		return data
			
	def main(self):
		# main loop

		self.console.log('Starting operations - %s\n' %(arrow.now().format('HH:mm:ss DD/MM/YYYY')))

		while True:
			try:
				for tag in self.tags:
					self.console.log('Looking for %s posts... \,' %(tag))
					posts = return_top_posts(tag, self.console, self.timelimit)
					if not self.only_top:
						self.console.log('checking most recent... \,')
						posts.extend(return_recent_posts(tag, self.console, self.timelimit))
					self.console.log('found %s.\nOrganising data... \,' %(len(posts)))
					self.data = self.organise_data(tag, posts, self.data)
					self.console.log('done.\n')
					
					if not internet_connection():
						raise ConnectionError

				self.backup_data()
				self.excel = outputExcel('instagram', self.console)
				self.excel.write(self.data)

				# sleep for an hour
				self.console.log('Sleeping for an hour...\n')
				sleep(60*60)

			except ConnectionError:
				if not internet_connection():
					while not internet_connection():
						self.console.log('NO INTERNET - re-establish connection to continue')
						sleep(60)

			except KeyboardInterrupt:
				self.console.log('Quitting')
				self.excel = outputExcel('instagram', self.console)
				self.excel.write(self.data)
				break

			except Exception as e:
				self.console.log('Error: %s' %(e))
