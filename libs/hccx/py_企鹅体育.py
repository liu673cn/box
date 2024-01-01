#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import json
import math
import re

class Spider(Spider):
	def getName(self):
		return "企鹅体育"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"全部": "",
			"足球": "Football",
			"篮球": "Basketball",
			"NBA": "NBA",
			"台球": "Billiards",
			"搏击": "Fight",
			"网排": "Tennis",
			"游戏": "Game",
			"其他": "Others",
			"橄棒冰": "MLB"
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name': k,
				'type_id': cateManual[k]
			})

		result['class'] = classes
		if (filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		url = 'https://live.qq.com/api/live/vlist?page_size=60&shortName={0}&page={1}'.format(tid, pg)
		rsp = self.fetch(url)
		content = rsp.text
		jo = json.loads(content)
		videos = []
		vodList = jo['data']['result']
		numvL = len(vodList)
		pgc = math.ceil(numvL/15)
		for vod in vodList:
			aid = (vod['room_id'])
			title = vod['room_name'].strip()
			img = vod['room_src']
			remark = (vod['game_name']).strip()
			videos.append({
				"vod_id": aid,
				"vod_name": title,
				"vod_pic": img,
				"vod_remarks": remark
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = pgc
		result['limit'] = numvL
		result['total'] = numvL
		return result

	def detailContent(self,array):
		aid = array[0]
		url = "https://m.live.qq.com/{0}".format(aid)
		rsp = self.fetch(url)
		html = self.cleanText(rsp.text)
		if self.regStr(reg=r'\"show_status\":\"(\d)\"', src=html) == '1':
			title = self.regStr(reg=r'\"room_name\":\"(.*?)\"', src=html)
			pic = self.regStr(reg=r'\"room_src\":\"(.*?)\"', src=html)
			typeName = self.regStr(reg=r'\"game_name\":\"(.*?)\"', src=html)
			remark = self.regStr(reg=r'\"nickname\":\"(.*?)\"', src=html)
			purl = self.regStr(reg=r'\"hls_url\":\"(.*?)\"', src=html)
		else:
			return {}
		vod = {
			"vod_id": aid,
			"vod_name": title,
			"vod_pic": pic,
			"type_name": typeName,
			"vod_year": "",
			"vod_area": "",
			"vod_remarks": remark,
			"vod_actor": '',
			"vod_director":'',
			"vod_content": ''
		}
		playUrl = '{0}${1}#'.format(typeName, purl)
		vod['vod_play_from'] = '🌸荷城茶秀接口🌸企鹅线路'
		vod['vod_play_url'] = playUrl

		result = {
			'list': [
				vod
			]
		}
		return result

	def searchContent(self,key,quick):
		result = {}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		url = id
		header = {
					 'Referer': 'https://m.live.qq.com/',
					 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
				 }
		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = header
		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	def localProxy(self,param):
		action = {
			'url':'',
			'header':'',
			'param':'',
			'type':'string',
			'after':''
		}
		return [200, "video/MP2T", action, ""]