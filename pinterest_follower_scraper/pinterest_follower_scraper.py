# Pinterest Follower Scraper - 20171002 - www.syphon5.com

#Import visualization packages
import seaborn as sns
import matplotlib.pyplot as plt
#Import HTTPS requests package
import requests
#Import web scraping package
from bs4 import BeautifulSoup
#Import data analysis package
import pandas as pd
#Import user-agent spoof package
from fake_useragent import UserAgent
#Import random number
from random import randint
#Import sleep time
from time import sleep
#Import time
import time

#Spoof the user-agent so Pinterest thinks you are visitng from a browser
ua = UserAgent()

#Set the user-agent header for the HTTPS request
headers = {'User-Agent': str(ua.chrome)}
#Action Required: Put your list of Pinterest URLs in quote, separated by commas, inside the square brackets. See example below.
urls = ['https://www.pinterest.com/deltaco/','https://www.pinterest.com/fuzzystacos/', 'https://www.pinterest.com/torchystacos/',
       'https://www.pinterest.com/tacobueno/', 'https://www.pinterest.com/tacocabana/']

#Create empty list to store future dictionary of pinterest URLs, followers, and date
output = []
#Run a for loop to iterate through list of URLs and retrieve follower data
for i, j in enumerate(urls):
    print("Scraping URL: " + j)
	#Scrape the Pinterest website code with spoofed user-agent
    response = requests.get(urls[i], headers=headers)
	#Parse the content with BeautifulSoup 
    soup = BeautifulSoup(response.content, 'html.parser')
	#Action Required: Replace the quoted contents for class_= with the updated class you find in Pinterest's website source code in tutorial. This grabs the follower counts.
    followers = soup.find_all(class_='_su _st _sv _sm _5k _sn _sr _nl _nm _nn _no')[0].get_text()
	#Only keep the number portion of the follower count text. Exampe: "583 Followers"...keep 583
    followers = ''.join(c for c in followers if c.isnumeric())
	#Convert follower number to integer
    followers = int(followers)
	#Set today's date
    today = time.strftime("%m/%d/%Y")    
	#Append to the empty list a dictionary containing pinterest URL, follower count, and today's date
    output.append({'pinterest': j, 'followers': followers, 'date': today})
    print("Quick courtesy sleep for X seconds")
	#Pause the script for random 3-9 seconds to not spam the website
    sleep(randint(3,9))

#Convert the result dictionary list to a data frame    
df = pd.DataFrame(output).sort_values("followers", ascending=False)
#Save the result data frame to CSV
df.to_csv('pinterest_followers.csv', index=False)
print("Saved CSV")

#Set color scheme for plot
sns.set_color_codes("muted")
#Create horizontal barplot of data
barplot = sns.barplot(x = "followers", y = "pinterest", data = df)
#Set the axis and title labels for barplot
barplot.set(xlabel = "Followers", ylabel = "Pinterest URL", title = "Brand Pinterest Followers")
#Save the barplot as a jpg
plt.savefig('pinterest_followers.jpg',bbox_inches='tight')
print("Saved plot")
