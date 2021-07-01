"""A video player class."""
import random
from .video_library import VideoLibrary


class VideoPlayer:
    """A class used to represent a Video Player."""
    flag = {}
    total_playlists = {}
    current = ""
    def __init__(self):
        self._video_library = VideoLibrary()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def list_all_videos(self):
        total_videos = []
        with open("videos.txt", "r") as f: #reads file line by line
            lines = f.readlines()
            for i in lines:
                i = i.strip() #strips "/n" off the line
                i = i.split(" | ") #splits the line into a list separated by " | "
                total_videos += [i]
                if i[0] == "Video about nothing":
                    i[1] = "nothing_video_id" #edits the nothing video as it has a different set up than the other videos
                    i += [""]
        total_videos = sorted(total_videos) #sorts videos in alphabetical order
        return total_videos

    def show_all_videos(self):
        total_videos = VideoPlayer.list_all_videos(self) #calls list_all_videos function for list of all the videos
        print("Here's a list of all available videos: ")
        for i in total_videos:
            print("   " + i[0], "("+i[1]+")", "["+i[2]+"]") #prints the output in the right order


    def play_video(self, video_id, playing = False): # adds in playing parameter to check if there is currently a video playing
        global current #calls the global variable current
        try:
            if len(current)>0:
                playing=True
        except:
            pass
        def playing_vid(): #defines an inner functioj to be used later throughout the outside function
            global current
            incorrect_count=0 #counting increment for every time i is not in total_videos
            total_videos = VideoPlayer.list_all_videos(self)
            for i in total_videos:
                if video_id == i[1]:
                    playing_video = i
                    print("Playing video: " +playing_video[0])
                    current = playing_video
                    playing = True
                    break
                else:
                    incorrect_count +=1

            if incorrect_count == len(total_videos): #if the total amount of incorrect counts is equal to the length of the total_videos
                print("Cannot play video: Video does not exist")

        if playing == False:
            playing_vid()

        if playing == True:
            VideoPlayer.stop_video(self) #calls the stop function to stop the video that is currently playing
            playing = False
            playing_vid()

    def stop_video(self):
        global current # alls the global variable current
        try: #using try to test if current would be able to be called or if an error would occur
            if len(current)>0:
                print("Stopping video: " + current[0])
                current = ""
        except:
            print("Cannot stop video: No video is currently playing")


    def play_random_video(self):
        random_video = ""
        random_video_id = ""
        total_id = []
        total_videos = VideoPlayer.list_all_videos(self) #calls the list_all_videos function
        for i in total_videos: #for loop for total_videos
            total_id += [i[1]]
        random_video_id = random.choice(total_id)
        for i in total_videos:
            if random_video_id in i:
                random_video = i

        VideoPlayer.play_video(self, random_video_id) #calls the play_video function to play the randomly picked video using the random id picked

    def pause_video(self, paused=0): #added extra parameter paused to check if the current video is already paused or not
        try: #using try and except to try to call the global variable current
            global current #calls global variable current
            if paused ==0:
                print("Pausing video: " + current[0] + " - PAUSED")
                paused=1
            else:
                print("Cannot pause video: Video is not paused")
        except:
            print("Cannot pause video: no video is currently playing")

    def continue_video(self, cont=0): #added extra parameter cont to check if the video is currently playing or not
        global current
        try: #uses try and except to determine if it is possible to run the code below
            if len(current)==0:
                print("Cannot continue video: no video is currently continuing")
        except:
            if cont == 0:
                print("Continuing video: " + current[0])
            if cont == 1:
                print("Cannot continue video: Video is not paused")


    def show_playing(self):
        global current
        try: #uses try and except to determine if it is possible to run the code below
            if len(current)>0:
                print("Currently playing: " + current[0], "("+current[1]+")", "["+current[2]+"]")
        except:
            try: #uses second try and except to attempt to run code below
                if len(current)==0:
                    print("No video is currently playing")
            except:
                pass

    def create_playlist(self, playlist_name):
        global total_playlists #calls global dictionary total_playlists
        for playlist in total_playlists: #for loop for each playlist name within the total_playlists
            if playlist.lower() == playlist_name.lower(): #sets each playlist name to lowercase to easily check if they match
                total_playlists[playlist_name] = [] #sets a new key to the dictionary total_playlists using playlist_name as the key
                print("Successfully created new playlist: " + playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        incorrect_count = 0
        global total_playlists #calls global dictionary total_playlists
        total_videos = VideoPlayer.list_all_videos(self)
        if playlist_name in total_playlists: # checks if the playlist_name already exists as a key in total_playlists
            for i in total_videos: #for loop about each video(i) in total_videos
                if video_id in i: #if the selected video id is in the video(i)
                    if i in total_playlists[playlist_name]: #if the video(i) exists as a value in the list of total_playlists[playlist_name]
                        print("Cannot add video to " + playlist_name + ": Video is already added")
                    adding = i
                    total_playlists[playlist_name] += [adding]
                    print("Added video to " + playlist_name + ": Video does not exist")
                else:
                    incorrect_count += 1
            if len(total_videos) == incorrect_count:
                    print("Cannot add video to " + playlist_name + ": Video does not exist")
        else:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")

    def show_all_playlists(self):
        try:
            global total_playlists #calls global dictionary total_playlists
            if len(total_playlists) > 0:
                print("Showing all playlists:")
                for i in total_playlists:
                    print("  " + i)
        except:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        global total_playlists #calls global dictionary total_playlists
        if playlist_name in total_playlists:
            print("Showing playlist: " + playlist_name)
            for i in playlist_name:
                print(i)
        elif playlist_name not in total_playlists:
            print("Cannot show" + playlist_name + "Playlist does not exist")
        elif len(total_playlists[playlist_name]) == 0:
            print("No videos here yet")

    def remove_from_playlist(self, playlist_name, video_id):
        removing = True
        global total_playlists
        remove_video = ""
        total_videos = VideoPlayer.list_all_videos(self)
        for i in total_videos:
            if video_id in i:
                remove_video = i
                removing = True
                break
            else:
                removing = False
        if removing == True:
            if playlist_name in total_playlists:
                try:
                    total_playlists[playlist_name].remove(remove_video) #uses .remove to remove the selected video from the list in the value from the dictionary key
                    print("remove video from " + playlist_name + ": " + remove_video)
                except:
                    print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
            else:
                print("Cannot remove video from " + playlist_name + ": Playlist does not exist")
        else:
            print("Cannot remove video from " + playlist_name + ": Video does not exist")

    def clear_playlist(self, playlist_name):
        global total_playlists
        if playlist_name in total_playlists:
            total_playlists[playlist_name] = []
            print("Successfully removed all videos from " + playlist_name)
        else:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")


    def delete_playlist(self, playlist_name):
        global total_playlists
        if playlist_name in total_playlists:
            del total_playlists[playlist_name]
            print("Deleted playlist" + playlist_name)
        else:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")


    def search_videos(self, search_term):
        results = {}
        index = 1

        lower_search = search_term.lower()
        total_videos = VideoPlayer.list_all_videos(self)
        for i in total_videos:
            if lower_search in i[0].lower() or lower_search in i[1].lower():
                results[str(index)] = [i]
                index += 1
        index = 1
        if len(results) > 0:
            print("Here are the results for " + search_term)
            for i in results:
                print(str(index) + ")" + i)
            else:
                print("No search for " + search_term)
            answer = input("Would you like to play any of the above? If yes, specify the number of the video. If your answer is not a valid number, we will assume it is a no.")
            try:
                answer = int(answer)
                if answer in results:
                    VideoPlayer.play_video(self, results[str(answer)][1])
            except:
                pass

    def search_videos_tag(self, video_tag):
        results = {}
        index = 1

        lower_search = video_tag.lower()
        total_videos = VideoPlayer.list_all_videos(self)
        for i in total_videos:
            if lower_search in i[2].lower():
                results[str(index)] = [i]
                index += 1
        index = 1
        if len(results) > 0:
            print("Here are the results for " + video_tag)
            for i in results:
                print(str(index) + ")" + i)
        else:
            print("No search results for " + video_tag)
        answer = input("Would you like to play any of the above? If yes, specify the number of the video. If your answer is not a valid number, we will assume it is a no.")
        try:
            answer = int(answer)
            if answer in results:
                VideoPlayer.play_video(self, results[str(answer)][1])
        except:
            pass

    def flag_video(self, video_id, flag_reason=""):
        global flag

        total_videos = VideoPlayer.list_all_videos(self)
        for i in total_videos:
            if video_id in i:
                if i[0] in flag:
                    print("Cannot flag video: Video is currently flagged (reason:" + flag[i[0]] + ")")
                    break
                else:
                    print("Successfully flagged video: " + i[0] + "(reason: " + flag_reason + ")")
                    break
            else:
                print("Cannot flag video: Video does not exist")
                break


    def allow_video(self, video_id):
        global flag
        total_videos = VideoPlayer.list_all_videos(self)
        for i in total_videos:
            if len(flag[i[0]]) > 0:
                del flag[i[0]]
                print("Successfully removed flag from video: " + i[0])
                break
            elif len(flag[i[0]]) == 0:
                print("Cannot remove flag from video: Video is not flagged")
            else:
                print("Cannot remove flag from video: Video does not exist")
