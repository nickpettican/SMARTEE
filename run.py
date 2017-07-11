#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ___        SMARTEE V 0.0.1 by nickpettican			___
# ___        Social Media Automated Research			___
# ___        Tool for Evaluating Engagement				___

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

from src.instaCrawl import instaCrawl
import json

def parse_config(path):
	# parses config file to load parameters
	
	try:
		raw = [line.strip() for line in open(path, 'r')]
		return json.loads(''.join(raw))
		
	except:
		print 'Could not open config file, check parameters.'

def main():
	# run the damn thing!

	data = parse_config('config.json')
	app = instaCrawl(params = data)
	app.main()

if __name__ == '__main__':
	main()
