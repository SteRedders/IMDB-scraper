'''

script to search on imdb given the first and last name
returns what the actor is best known for and saves a .jpg of the actor

'''
import requests
import bs4
import cv2

def imdb_search(firstname,lastname):

	site_url = 'https://www.imdb.com{}'
	search_url = 'https://www.imdb.com/find?q={}+{}&ref_=nv_sr_sm'
	
	scrape_url = search_url.format(firstname,lastname)
	res = requests.get(scrape_url)
	soup = bs4.BeautifulSoup(res.text,'lxml')

	initial_result = soup.select('.result_text')
	name_link = initial_result[0]

	actor_url = site_url.format(name_link.select('a')[0]['href'])
	actor_result = requests.get(actor_url)
	newsoup = bs4.BeautifulSoup(actor_result.text,'lxml')

	bio_string = newsoup.select('.inline')[0].text
	bio_string = bio_string.replace('\n','')
	bio_string = bio_string[:250] + ' ...\n'
	count = 0
	known_for = []
	while count < 4:
		known = newsoup.select('.knownfor-title-role')[count]('a')[0]['title']
		count += 1
		known_for.append(known)

	image = newsoup.select('.image')[0]('img')
	image_link = requests.get(image[0]['src'])
	f = open('imdbSearch.jpg','wb')
	f.write(image_link.content)
	f.close()

	return bio_string, known_for													#returns two values	


print('Welcome to IMDB search')
search_first = input('Enter First Name of Actor: ')
search_second = input('Now enter Last name: ')

bio, known_for = imdb_search(search_first,search_second)							#initializes function to fill 2 variables
print(f'\n{search_first.capitalize()} {search_second.capitalize()}\n')
print(bio)
print(known_for)

my_img = cv2.imread('imdbSearch.jpg', cv2.IMREAD_COLOR)								#opens(reads) the image file, but doesnt display it
cv2.imshow("IMDBsearch", my_img)    												#displays image in own windor
cv2.waitKey(0)																		#the time in milliseconds the window stays open, 0 is indefinite
cv2.destroyAllWindows()																#close window and dump memory usage
