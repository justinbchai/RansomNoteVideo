import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
import pprint
from transcriber import Transcriber

def download_video():
    driver = webdriver.Firefox()

    driver.get("https://www.playphrase.me/#/search?q=you+cut+your+hair&pos=1")

    # Find the element that contains the .mp4 file link (you may need to adjust the selector)
    mp4_element = driver.find_element(By.ID, "video-player-0")

    if mp4_element:
        # Get the .mp4 file URL
        mp4_url = mp4_element.get_attribute('src')

        # obtain filename by splitting url and getting
        # last string  
        mp4_url = mp4_url.split('?')[0]
        
        # Download the .mp4 file (you can use requests or any other method)
        # Example: You can use requests.get(mp4_url) to download the file
        # Remember to handle errors and save the file appropriately
        print(f"Downloading file: {mp4_url}")

        # create response object  
        r = requests.get(mp4_url, stream = True)  
            
        # download started  
        urllib.request.urlretrieve(mp4_url, 'videoname.mp4')
        # with open(mp4_url, 'wb') as f:  
        #     for chunk in r.iter_content(chunk_size = 1024*1024):  
        #         if chunk:  
        #             f.write(chunk)  
            
        print(f"{mp4_url} downloaded!")
    driver.close()

def generate_srt_file(filename):
    model_path = "vosk-model-small-en-us-0.15"

    transcriber = Transcriber(model_path)
    transcription = transcriber.transcribe(filename)

    pprint.pprint(transcription)

if __name__ == "__main__":
    generate_srt_file("videoname.mp4")
