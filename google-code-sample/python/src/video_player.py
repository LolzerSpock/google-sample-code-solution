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
        with open("videos.txt", "r") as f:
            lines = f.readlines()
            for i in lines:
                i = i.strip()
                i = i.split(" | ")
                total_videos += [i]
                if i[0] == "Video about nothing":
                    i[1] = "nothing_video_id"
                    i += [""]
        total_videos = sorted(total_videos)
        return total_videos

    def show_all_videos(self):
        total_videos = VideoPlayer.list_all_videos(self)
        print("Here's a list of all available videos: ")
        for i in total_videos:
            print("   " + i[0], "("+i[1]+")", "["+i[2]+"]")


    def play_video(self, video_id, playing = False):
        global current
        try:
            if len(current)>0:
                playing=True
        except:
            pass
        def playing_vid():
            global current
            incorrect_count=0
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

            if incorrect_count == len(total_videos):
                print("Cannot play video: Video does not exist")

        if playing == False:
            playing_vid()

        if playing == True:
            VideoPlayer.stop_video(self)
            playing = False
            playing_vid()

    def stop_video(self):
        global current
        try:
            if len(current)>0:
                print("Stopping video: " + current[0])
                current = ""
        except:
            print("Cannot stop video: No video is currently playing")


    def play_random_video(self):
        random_video = ""
        random_video_id = ""
        total_id = []
        total_videos = VideoPlayer.list_all_videos(self)
        for i in total_videos:
            total_id += [i[1]]
        random_video_id = random.choice(total_id)
        for i in total_videos:
            if random_video_id in i:
                random_video = i

        VideoPlayer.play_video(self, random_video_id)

    def pause_video(self, paused=0):
        try:
            global current
            if paused ==0:
                print("Pausing video: " + current[0] + " - PAUSED")
                paused=1
            else:
                print("Cannot pause video: Video is not paused")
        except:
            print("Cannot pause video: no video is currently playing")

    def continue_video(self, cont=0):
        global current
        try:
            if len(current)==0:
                print("Cannot continue video: no video is currently continuing")
        except:
            if cont == 0:
                print("Continuing video: " + current[0])
            if cont == 1:
                print("Cannot continue video: Video is not paused")


    def show_playing(self):
        global current
        try:
            if len(current)>0:
                print("Currently playing: " + current[0], "("+current[1]+")", "["+current[2]+"]")
        except:
            try:
                if len(current)==0:
                    print("No video is currently playing")
            except:
                pass

    def create_playlist(self, playlist_name):
        global total_playlists
        for playlist_name in total_playlists:
            if playlist_name.lower() == playlist_name.lower():
                total_playlists[playlist_name] = []
                print("Successfully created new playlist: " + playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        global total_playlists
        total_videos = VideoPlayer.list_all_videos(self)
        if playlist_name in total_playlists:
            for i in total_videos:
                if video_id in i:
                    if i in total_playlists[playlist_name]:
                        print("Cannot add video to " + playlist_name + ": Video is already added")
                    adding = i
                    total_playlists[playlist_name] += [adding]
                    print("Added video to " + playlist_name + ": Video does not exist")
                else:
                    print("Cannot add video to " + playlist_name + ": Playlist does not exist")

    def show_all_playlists(self):
        try:
            global total_playlists
            if len(total_playlists) > 0:
                print("Showing all playlists:")
                for i in total_playlists:
                    print("  " + i)
        except:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        global total_playlists
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
                    total_playlists[playlist_name].remove(remove_video)
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
