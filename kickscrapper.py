import requests

import pandas as pd

import os


class kickstarter_scraper:
	def __init__(self):
		self.sess = requests.Session()


	def scrape_tag(self, tag):
		#def get_tag_info(tag):
		directory = "./shops_info/{tag}".format(tag=tag)
		if not os.path.exists(directory):
			os.makedirs(directory)

		tag_dataframe_dict = dict()
		index = 0

		page_num = 1

		while True:
			get = requests.get("https://www.kickstarter.com/projects/search.json?search=&term={tag}&page={page_num}".format(tag=tag, page_num=page_num))
			if get.status_code == 200:
				json_request = get.json()
 
				if not json_request["projects"]:
					print("END")
					return False

			else:
				print("Wrong request")
				return False

			json_reqiured = dict()

			for item in json_request["projects"]:
				try:
					tag_dataframe_dict[index] = {
											"tag": tag,
											"name": item["name"], 
										 	"category_name": item["category"]["name"], 
										 	"URL": item["urls"]["web"]["project"], 
										 	"creator_name": item["creator"]["name"], 
										 	"creator_URL": item["creator"]["urls"]["web"]["user"],
										 	"created": item["created_at"],
										 	"launched": item["launched_at"],
										 	"deadline": item["deadline"],
										 	"goal": item["goal"],
										 	"pledged": str(item["pledged"]) + item["currency"],
										 	"pledged_usd": item["usd_pledged"],
										 	"current_state": item["state"],
										 	"backers": item["backers_count"],
										 	"location": item["location"]["displayable_name"]
											}

					index += 1
				except:
					pass

			page_num += 1


			tag_dataframe = pd.DataFrame.from_dict(tag_dataframe_dict, "index")
			tag_dataframe.to_csv(directory + "/{filename}.csv".format(filename=tag))


	def scrape_all(self): # EXPERIMENTAL
		directory = "./shops_info/all"
		if not os.path.exists(directory):
			os.makedirs(directory)

		dataframe_dict = dict()
		index = 0

		page_num = 1

		while True:
			get = requests.get("https://www.kickstarter.com/projects/search.json?&page={page_num}".format(page_num=page_num))
			if get.status_code == 200:
				json_request = get.json()
 
				if not json_request["projects"]:
					print("END")
					return False

			else:
				print(get.status_code)
				print("Wrong request")
				return False

			json_reqiured = dict()

			for item in json_request["projects"]:
				dataframe_dict[index] = {
										"name": item["name"], 
									 	"category_name": item["category"]["name"], 
									 	"URL": item["urls"]["web"]["project"], 
									 	"creator_name": item["creator"]["name"], 
									 	"creator_URL": item["creator"]["urls"]["web"]["user"],
									 	"created": item["created_at"],
									 	"launched": item["launched_at"],
									 	"deadline": item["deadline"],
									 	"goal": item["goal"],
									 	"pledged": str(item["pledged"]) + item["currency"],
									 	"pledged_usd": item["usd_pledged"],
									 	"current_state": item["state"],
									 	"backers": item["backers_count"],
									 	"location": item["location"]["displayable_name"]
										}

				index += 1

			page_num += 1
			print(page_num)


			tag_dataframe = pd.DataFrame.from_dict(dataframe_dict, "index")
			tag_dataframe.to_csv(directory + "/all.csv")
