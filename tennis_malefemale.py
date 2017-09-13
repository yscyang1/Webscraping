# Imports
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# Global arrays
birthdate = []
height = []
weight = []
plays = []
experience = []
wins = []
age = []
country = []
residence = []
turnedpro = []
earnings2016 = []
player_firstname = []
player_lastname = []

def open_url(url):
#  Open urls.  Gather array of player urls, then send to get_info function

	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	player_row = soup.find_all(class_ = 'player-row')
	player_link = [player.find(class_ = 'player-name').a.get('href') for player in player_row]

	for playerlink in player_link:
	# for playerlink in range(0,len(player_link)-1):
		print(playerlink)

		try:
			get_info(requests.get('http://www.tennis.com' + playerlink + '/stats/'))
		except:
			get_info(requests.get('http://www.tennis.com' + playerlink))

def get_info(player_page):
#  Don't append to global variables unless all info found

	try:
		temp = []
		soup3 = BeautifulSoup(player_page.content, 'html.parser')
		player_stats = soup3.find(class_ = 'player-stats')
		temp.append(player_stats.find(class_ = 'player-birthdate').get_text().strip())
		temp.append(player_stats.find(class_ = 'player-height').get_text().strip())
		temp.append(player_stats.find(class_ = 'player-weight').get_text().strip())
		temp.append(player_stats.find(class_ = 'player-plays').get_text().strip())
		temp.append(player_stats.find(class_ = 'player-experience').get_text().strip())
		temp.append(player_stats.find(class_ = 'player-wins').get_text().strip())

		player_about = soup3.find(class_ = 'about-wrapper')
		aboutinfo = [player_about.find_all(class_ = 'about-info')]
		temp.append(aboutinfo[0][0].get_text())
		temp.append(aboutinfo[0][1].get_text())
		temp.append(aboutinfo[0][2].get_text())
		temp.append(aboutinfo[0][3].get_text())
		temp.append(aboutinfo[0][4].get_text())

		temp.append(soup3.find(class_= 'first-name').get_text().strip())
		temp.append(soup3.find(class_ = 'last-name').get_text().strip())
	except:
		pass

	if len(temp) == 13:
		birthdate.append(temp[0])
		height.append(temp[1])
		weight.append(temp[2])
		plays.append(temp[3])
		experience.append(temp[4])
		wins.append(temp[5])

		age.append(temp[6])
		country.append(temp[7])
		residence.append(temp[8])
		turnedpro.append(temp[9])
		earnings2016.append(temp[10])

		player_firstname.append(temp[11])
		player_lastname.append(temp[12])
	

def write_file(arr, gender):
#  Write info from global arrays to csv in order specified by "order" array
#  Create and save to an appropiriate "gender" .csv file

	with open(gender + '.csv', 'w') as file:
		writer = csv.writer(file)
		[writer.writerow(i) for i in arr]


def main():
	order = [player_firstname, player_lastname, birthdate, height, weight, plays, experience, wins,
	age, country, residence, turnedpro, earnings2016]

	urls = ['http://www.tennis.com/rankings/ATP/', 'http://www.tennis.com/rankings/WTA/']
	gender = ['male', 'female']
	for i in range(len(urls)):
		open_url(urls[i])
		write_file(order, gender[i])

main()