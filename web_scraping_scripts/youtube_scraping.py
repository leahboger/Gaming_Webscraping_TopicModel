#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 18:09:58 2024

@author: leahboger
"""

#set up API access 

dev = "insert your dev key here"

import googleapiclient.discovery
import pandas as pd



api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = dev

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)




#create function to grab comments of video (iterate through multiple ids)

def getcomments(video):
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=video,
        maxResults=100
    )

    comments = []

    # Execute the request.
    response = request.execute()

    # Get the comments and their replies from the response.
    for item in response['items']:
        # Top-level comment
        comment = item['snippet']['topLevelComment']['snippet']
        public = item['snippet']['isPublic']
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['likeCount'],
            comment['textOriginal'],
            comment['videoId'],
            public
        ])

        # Check if there are replies and add them as well
        if 'replies' in item:
            for reply in item['replies']['comments']:
                reply_comment = reply['snippet']
                reply_public = reply_comment.get('isPublic', True)  # Replies may not have this field
                comments.append([
                    reply_comment['authorDisplayName'],
                    reply_comment['publishedAt'],
                    reply_comment['likeCount'],
                    reply_comment['textOriginal'],
                    video,  # Use the same video ID as the top-level comment
                    reply_public
                ])
    #grab responsed from all pages of comments
    while 'nextPageToken' in response:
        nextPageToken = response['nextPageToken']
        nextRequest = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video,
            maxResults=100,
            pageToken=nextPageToken
        )
        response = nextRequest.execute()
        for item in response['items']:
            # Top-level comment
            comment = item['snippet']['topLevelComment']['snippet']
            public = item['snippet']['isPublic']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['likeCount'],
                comment['textOriginal'],
                comment['videoId'],
                public
            ])

            # Check for replies, grab replies too
            if 'replies' in item:
                for reply in item['replies']['comments']:
                    reply_comment = reply['snippet']
                    reply_public = reply_comment.get('isPublic', True)
                    comments.append([
                        reply_comment['authorDisplayName'],
                        reply_comment['publishedAt'],
                        reply_comment['likeCount'],
                        reply_comment['textOriginal'],
                        video,
                        reply_public
                    ])
    #create pandas df       
    df2 = pd.DataFrame(comments, columns=['author', 'updated_at', 'like_count', 'text', 'video_id', 'public'])
    return df2











#iterate through video ids
df = pd.DataFrame()
for i in ['GgJj9Mok9dA','4BXOa7Eqzxc','Ko8ubyWDy58', 'uMBEvgiKqBs', 'YYz7vazmu00', 'QU_Q4uBMInM' ]:
  df2 = getcomments(i)
  df = pd.concat([df, df2])
  
#dictionary of ids and video titles
video_names = {'GgJj9Mok9dA':'PC vs Console in 2024... time to ditch PC?','4BXOa7Eqzxc': 'Finally ENDING the PC Gaming vs Console Debate', 'Ko8ubyWDy58':'PC Gaming vs Console - What’s ACTUALLY Better? 🤔', 'uMBEvgiKqBs': 'Call of Duty Warzone is not fair ( PC vs Console )', 'YYz7vazmu00': 'Cyberpunk 2077: PC Vs Next Gen Console Comparison (NVIDIA 4080 GPU)', 'QU_Q4uBMInM':'Halo Infinite: PC vs Xbox Series X Performance Review' }

  
# how many comments from each video?
grouped_counts = df.groupby('video_id').size().reset_index(name='counts')
grouped_counts['video_name'] = grouped_counts['video_id'].map(video_names)
print(grouped_counts)
     
#rename
youtube_comments = df


youtube_comments.to_csv('youtube_comments.csv', index = False)


