import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib
import whisper
import whisper_timestamped
from moviepy.editor import *
import time
import string
from selenium.webdriver.firefox.options import Options

# TODO remove print statements

def download_video(target_phrase:string) -> list[int]:
    if (target_phrase == ''):
        raise Exception("Could not find any movie clips")
    filename = f'{target_phrase.replace(' ', '-')}.mp4'
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    url = 'https://www.playphrase.me/#/search?q=' + target_phrase.replace(' ', '+') + '&pos=0'

    driver.get(url)
    try: 
        # Wait until at least one video tag is present
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'video')))
        # Find the elements that contain the .mp4 file links (you may need to adjust the selector)
        mp4_elements = driver.find_elements(By.TAG_NAME, 'video')
        time.sleep(2)
        print(mp4_elements)

        if mp4_elements:
            for mp4_element in mp4_elements:
                # Get the .mp4 file URL
                mp4_url = mp4_element.get_attribute('src')

                # obtain filename by splitting url and getting
                # last string  
                mp4_url = mp4_url.split('?')[0]
                
                # Download the .mp4 file (you can use requests or any other method)
                print(f"Downloading file: {mp4_url}")

                # create response object  
                r = requests.get(mp4_url, stream = True)  
                    
                # download started  
                urllib.request.urlretrieve(mp4_url, filename) 
                    
                print(f"{mp4_url} downloaded!")
                
                try:
                    clip, target_string = cut_clip(filename, target_phrase)
                    driver.quit()
                    return clip, target_string
                except:
                    # when cut_clip() raises exception, move on to next clip. May result
                    # in idle windows of Firefox being left open
                    pass
    except:
        # no clips exist for given phrase. Try again with same phrase minus the last word
        driver.close()
        return download_video(target_phrase.rsplit(' ', 1)[0])
        

def get_timestamps(filename:string, target_string:string):
    delta = 0
    audio = whisper.load_audio(filename)
    model = whisper_timestamped.load_model("large", device="cpu")
    result = whisper_timestamped.transcribe(model, audio, language="en", initial_prompt=f"the phrase {target_string} should be transcribed")
    target_list = target_string.split()
    
    import json
    print(json.dumps(result, indent = 2, ensure_ascii = False))
    print(target_list)
    timestamps = list()
    l = 0
    r = len(target_list)-1
    for i in range(len(result["segments"])):
        while r < len(result["segments"][i]["words"]):
            left_word = result["segments"][i]["words"][l]["text"].lower().translate(str.maketrans('', '', string.punctuation))
            right_word = result["segments"][i]["words"][r]["text"].lower().translate(str.maketrans('', '', string.punctuation))
            print(left_word, right_word)
            if left_word == target_list[0].lower().translate(str.maketrans('', '', string.punctuation)) and right_word == target_list[-1].lower().translate(str.maketrans('', '', string.punctuation)):
                print(result["segments"][i]["words"][l], result["segments"][i]["words"][r], target_string)
                timestamps.append(result["segments"][i]["words"][l]["start"])
                timestamps.append(result["segments"][i]["words"][r]["end"])
                clip = VideoFileClip(filename)
                duration = clip.duration
                return max(0, timestamps[0]-delta), min(timestamps[1]+delta, duration)
            l+=1
            r+=1
        l = 0
        r = len(target_list)-1
    raise Exception("Something went wrong")

    

def cut_clip(filename:string, target_string:string):
    l, r = get_timestamps(filename, target_string)
    print(l, r)
    clip = VideoFileClip(filename).subclip(l, r)
    return clip, target_string

def main():
    phrase = "my project"
    download_video(phrase)
    


if __name__ == "__main__":
    main()
