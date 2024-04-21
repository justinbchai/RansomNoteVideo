from moviepy.editor import *
import ransom_utils as ru

def main():
    clip_array = list()
    passage = input("Enter the message you'd like to ransom-noteify: ").split()
    final_name = input("Enter the file name: ")
    while len(passage) > 0:
        print(passage)
        clip, phrase = ru.download_video(" ".join(passage[:4]))
        print("Phrase", phrase)
        clip_array.append(clip)
        padding = ColorClip(size=clip_array[0].size, color=(0, 0, 0), duration=0.3)
        clip_array.append(padding)


        passage = passage[len(phrase.split()):]

    final_clip = concatenate_videoclips(clip_array, "compose")
    final_clip.write_videofile(filename=f"output/{final_name}.mp4", codec='mpeg4', audio_codec='aac')

if __name__ == "__main__":
    main()
