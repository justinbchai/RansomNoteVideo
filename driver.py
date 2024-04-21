from moviepy.editor import *
import ransom_utils as ru

clip_array = list()

def main():
    passage = input("Enter the message you'd like to ransom-noteify: ").split()
    while len(passage) > 0:
        print(passage)
        clip, phrase = ru.download_video(" ".join(passage[:4]))
        print("Phrase", phrase)
        clip_array.append(clip)
        passage = passage[len(phrase.split()):]

    final_clip = concatenate_videoclips(clip_array, "compose")
    final_clip.write_videofile(filename="output/final-video.mp4", codec='mpeg4', audio_codec='aac')

if __name__ == "__main__":
    main()
