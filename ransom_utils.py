import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
import whisper
import whisper_timestamped
import pprint
from moviepy.editor import *



def download_video(target_phrase):

    driver = webdriver.Firefox()
    
    url = 'https://www.playphrase.me/#/search?q=' + target_phrase.replace(' ', '+') + '&pos=0'

    driver.get(url)

    filename = f'{target_phrase.replace(' ', '-')}.mp4'

    try:

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
            urllib.request.urlretrieve(mp4_url, filename)
            # with open(mp4_url, 'wb') as f:  
            #     for chunk in r.iter_content(chunk_size = 1024*1024):  
            #         if chunk:  
            #             f.write(chunk)  
                
            print(f"{mp4_url} downloaded!")
        driver.quit()
        cut_clip(filename, target_phrase)
    except:
        driver.close()
        download_video(target_phrase.rsplit(' ', 1)[0])

def get_timestamps(filename, target_string):
    delta = 0.1
    audio = whisper.load_audio(filename)
    model = whisper_timestamped.load_model("medium", device="cpu")
    result = whisper_timestamped.transcribe(model, audio, language="en")

    timestamps = list()
    l = 0
    while l < len(result):
        temp = result["segments"][0]["words"][l]
        if temp["text"].lower() in target_string:
            break
        l+=1
    timestamps.append(result["segments"][0]["words"][l]["start"])
    l += len(target_string.split()) - 1
    timestamps.append(result["segments"][0]["words"][l]["start"])

    return max(0, timestamps[0] - delta), timestamps[1] + delta

def cut_clip(filename, target_string):
    l, r = get_timestamps(filename, target_string)
    clip = VideoFileClip(filename).subclip(l, r)
    clip.write_videofile(f"cut-{filename}")
    return clip, filename

def main():
    phrase = "round your city round"
    download_video(phrase)
    


if __name__ == "__main__":
    main()
