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

import json, requests, socket, arrow
from lxml import etree

def start_requests(console):
	# returns a requests Session object

	try:
		browser = requests.Session()
		browser.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})
		return browser

	except Exception as e:
		console.log('Error starting requests: %s' %(e))
	
	return False

def return_timelimit(console):
	# returns the timestamp before which posts will be ignored
	# avoids picking up posts that are older than a week 

	try:
		return int(arrow.now().timestamp) - 60*60*24*7
		# make int just in case
	except Exception as e:
		console.log('Error obtaining time limit: %s' %(e))

	return False
	
def return_top_posts(tag, console, timelimit):
	# returns the top posts for a tag

	return return_posts_by_type(tag, 'top_posts', console, timelimit)

def return_recent_posts(tag, console, timelimit):
	# returns the most recent posts for a tag

	return return_posts_by_type(tag, 'media', console, timelimit)

def return_posts_by_type(tag, category, console, timelimit):
	# returns either top or recent posts

	try:
		browser = start_requests(console)
		data = return_SharedData('https://www.instagram.com/explore/tags/%s/?hl=en' %(tag), browser, console)
		posts = return_posts(data, category, browser, console, timelimit)
		return posts

	except Exception as e:
		console.log('Error returning %s post: %s' %(category, e))

	return False	

def return_SharedData(url, browser, console):
	# returns the JSON object from sharedData

	try:
		site = browser.get(url)
		tree = etree.HTML(site.text)
		identifier = 'window._sharedData = '
		for a in tree.findall('.//script'):
			try:
				if a.text.startswith(identifier):
					try:
						return json.loads(a.text.replace(identifier, '')[:-1])
					except Exception as e:
						print 'Error parsing the data: %s' %(e)
			except:
				continue

	except Exception as e:
		console.log('Error returning SharedData: %s' %(e))

	return False

def return_hashtags(caption, console):
	# returns hashtags from caption

	try:
		broken_up = caption.lower().split()
		if any(n.startswith('#') for n in broken_up):
			hashtags = [n for n in broken_up if n.startswith('#')]
			for tag in hashtags:
				if tag.count('#') > 1:
					hashtags.remove(tag)
					hashtags.extend(['#' + n for n in tag.split('#') if n])
	
	except Exception as e:
		console.log('Error returning hashtags: %s' %(e))

	return []

def return_posts(data, key, browser, console, timelimit):
	# returns the post data

	posts = []

	try:
		nodes = data['entry_data']['TagPage'][0]['tag'][key]['nodes']
		for node in nodes:
			post_temp = {'date': False}
			try:
				post_temp = {
					'caption': node['caption'],
					'id': node['id'],
					'timestamp': node['date'],
					'date': arrow.get(node['date']).format('YYYY-MM-DD'),
					'time': arrow.get(node['date']).format('HH:mm'),
					'code': node['code'],
					'display_src': node['display_src'],
					'url': 'https://www.instagram.com/explore/tags/%s/?hl=en' %(node['code']),
					'owner_username': return_username(node['code'], browser, console),
					'likes_count': node['likes']['count'],
					'comments_count': node['comments']['count'],
					'owner_id': node['owner']['id'],
					'hashtags': return_hashtags(node['caption'], console),
					'popularity': False
				}

			except Exception as e:
				console.log('sorting data error: %s' %(e))
					
			if any(n for n in post_temp.values()):
				if post_temp['timestamp'] and timelimit:
					try:
						# if the timestamp is 1 week earlier to when SMARTEE started
						if int(post_temp['timestamp']) < timelimit:
							# skip it
							continue
					except:
						pass
				posts.append(post_temp)

	except Exception as e:
		console.log('Error returning posts: %s' %(e))

	return posts

def return_username(code, browser, console):
	# returns the username

	try:
		data = return_SharedData('https://www.instagram.com/p/%s/' %(code), browser, console)
		return data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username']
	
	except Exception as e:
		console.log('Error getting username: %s \,' %(e))
		
	return False
	
def return_users(posts, console):
	# handles user data collection and returns users data

	try:
		users = []
		browser = start_requests(console)
		for post in posts:
			if post['owner_username']:
				user = get_user_data(post['owner_username'], browser, console)
				if user:
					users.append({
							'username': post['owner_username'], 
							'data': user
						})
	
	except Exception as e:
		console.log('Error returning user data: %s' %(e))
	
	return users
	
def get_user_data(username, browser, console):
	# return user data

	data = return_SharedData('https://www.instagram.com/%s/' %(username), browser, console)
	userdata = data['entry_data']['ProfilePage'][0]['user']
	try:
		return {
			'media': {
				'count': userdata['media']['count'],
				'nodes': []
			},
			'following': userdata['follows']['count'],
			'followers': userdata['followed_by']['count']
		}

	except Exception as e:
		console.log('Error returning user data: %s' %(e))

	return False

def internet_connection(host = '8.8.8.8', port = 53, timeout = 3):
	# check for internet connection
	
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True

	except:
		return False
