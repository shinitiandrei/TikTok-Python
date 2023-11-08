import asyncio
import os
import csv
from TikTokApi import TikTokApi
from datetime import datetime

ms_token = os.environ.get(
    "ms_token", "token"
)  # set your own ms_token, think it might need to have visited a profile


async def getUserVideos(username):
    videos = []
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False, override_browser_args=["--incognito"])
        user = api.user(username)
        # user_data = await user.info()
        async for video in user.videos(count=100):
            videos.append(video.as_dict)
    return videos


def tiktokUrlBuilder(username, videoID):
    return f"https://www.tiktok.com/@{username}/video/{videoID}"

def convertTimestampToDate(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')

async def getVideoInfo(username, video):
    videoUrl = tiktokUrlBuilder(username, video['id'])
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video_object = api.video(url=videoUrl)
        videoInfo = await video_object.info()
        return videoInfo

if __name__ == "__main__":
    username = "liana.melabimage"
    videos = asyncio.run(getUserVideos(username))

    with open('tiktok_videos.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['VideoURL', 'Description', 'Likes', 'Shares', 'Comments', 'Views', 'Saves']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
        for video in videos:
            videoInfo = asyncio.run(getVideoInfo(username, video))
            videoUrl = tiktokUrlBuilder(username, video['id'])
            writer.writerow({
                'Date': convertTimestampToDate(videoInfo['createTime']),
                'Description': videoInfo['desc'],
                'Likes': videoInfo['stats']['diggCount'],
                'Shares': videoInfo['stats']['shareCount'],
                'Comments': videoInfo['stats']['commentCount'],
                'Views': videoInfo['stats']['playCount'],
                'Saves': videoInfo['stats']['collectCount'],
                'VideoURL': videoUrl,
                
            })

    # for video in videos:
    #     videoInfo = asyncio.run(getVideoInfo("liana.melabimage", video))
    #     print(f"VIDEO: {videoInfo['id']}")
    #     print(f"Likes: {videoInfo['stats']['diggCount']}")
    #     print(f"Shared: {videoInfo['stats']['shareCount']}")
    #     print(f"Comments: {videoInfo['stats']['commentCount']}")
    #     print(f"Watched: {videoInfo['stats']['playCount']}")
    #     print(f"Saved: {videoInfo['stats']['collectCount']}")
    #     print(f"=====================================================================================")
    # videos = getUserVideos()
    # print(getVideoInfo(videos[0]))
    # asyncio.run(getUserVideos())