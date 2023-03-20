import requests
from bs4 import BeautifulSoup


# The URL of the web page will provide links to all video lectures. 


URL = "https://www.youtube.com/watch?v=XQ2KRKz-MkQ"

def get_video_links():
	
	# create response object
	response = requests.get(URL)
	
	# create a beautiful-soup object
	soup = BeautifulSoup(response.content,'html.parser')
	
	# find all links on a given web-page
	total_links = soup.findAll('a')

	# filter the link sending with .mp4
	video_links = [URL + link['href'] for link in total_links if link['href'].endswith('mp4')]

	return video_links


def download_videos(extracted_video_links):

	for link in extracted_video_links:

		# iterate through all links in video_links and download them one by one
		
		# obtain the filename by splitting the URL 
		name_of_file = link.split('/')[-1]

		print( "Downloading file:%s"%name_of_file)
		
		# create a response object
		response = requests.get(link, stream = True)
		
		# download started
		with open(name_of_file, 'wb') as f:
			for chunk in response.iter_content(chunk_size = 1024*1024):
				if chunk:
					f.write(chunk)
		
		print( "%s downloaded!\n"%name_of_file )

	print ("All videos downloaded!")
	return


if __name__ == "__main__":

	# extracting all video links
	extracted_video_links = get_video_links()

	# download all videos using their URLs
	download_videos(extracted_video_links)
	
