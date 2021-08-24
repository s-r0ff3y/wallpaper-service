from bs4 import BeautifulSoup
from PIL import Image
import requests, random, time, ctypes, win32con, os

# GET REQUEST FOR LIST OF IMAGES
url = 'https://unsplash.com/wallpapers/desktop'
filename = os.getcwd() + '\wallpaper.png'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# GETS LIST OF IMAGES WITH LINKS
imgs = soup.findAll('img')

# CHOSES RANDOM IMAGE, FINDS SRC LINK AND CLOSES REQUEST
chosen_img = random.choice(imgs)
img_url = chosen_img['src']
page.close()

# SENDS GET REQUEST TO IMAGE LINK
response = requests.get(img_url)

# WRITES BYTES FROM IMAGE TO FILE
with open(filename, 'wb') as f:
    f.write(response.content)
    print('[INFO] IMAGE SAVED!')

# GETS USERS MONITOR SIZE
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# RESIZES IMAGE
basewidth = screensize[0]
img = Image.open(filename)
# determining the height ratio
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
# resize image and save
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img.save(filename, quality=95) 

# SETS WALLPAPER
ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETDESKWALLPAPER, 0, 0)