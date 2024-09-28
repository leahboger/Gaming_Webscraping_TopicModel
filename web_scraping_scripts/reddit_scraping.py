#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 07:04:48 2024

@author: areuschel
"""


# import libraries
import requests
import requests.auth
import logging
import praw


# secret: hidden for privacy, enter your own
# client id: hidden for privacy, enter your own


### authentication & request a token
user_agent = "mac:My_Example_App:v1.0 (by /u/username)"


client_auth = requests.auth.HTTPBasicAuth('your client id here', 'your secret')
post_data = {"grant_type": "password", "username": "username", "password": "password"}
headers = {"User-Agent": user_agent}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
response.json()

# use the token
headers = {"Authorization": "bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzIxMTQ0NzM3Ljg0MjAxOSwiaWF0IjoxNzIxMDU4MzM3Ljg0MjAxOSwianRpIjoiY01fRm9PZlRMWEZUZXFSdXFfZ01aUjVRcXNHVzV3IiwiY2lkIjoiOTRyNHJkSUhKSi16X2RGRmo4M1BwZyIsImxpZCI6InQyXzlzeHNkd2tvIiwiYWlkIjoidDJfOXN4c2R3a28iLCJsY2EiOjE2MTA1NTYwNzYzMDYsInNjcCI6ImVKeUtWdEpTaWdVRUFBRF9fd056QVNjIiwiZmxvIjo5fQ.dSd5lKSDlK3AiDx9UkQCZr3Y3qP-3Er3YV2qpXsLfx7HR8AdAZuvBM8ZSmEyZePRerbR9MjI4_fVHEVJ9rkZcSu_R2vfhAFe5Ol0i1tC07WlxpU5fvU9QGkZuIANFvAy-dPSImxAk68fRwkgp5OgLygW-qu8xa9yvvKwJz7ChtyibkocJ6e4UBzuf6V1W4jREbccM_3E4d8cvATiIHvAjeegjnmmitYoOb7d43lu-nt1mvmqgcNqNX3h2YClKzrWZOLWeCGzNcMbMp2i_VFnmXMD-KKxiKLeqAnuHewhne5NG4nw0WqaxLRZLCtabuZ37euyyvAAjZga09ZD0lOrww", "User-Agent": user_agent}
response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)



'''
This is the test code
'''


#### COMMENT EXTRACTION AND PARSING

## STEP 1: Create an instance of reddit

reddit = praw.Reddit(
    client_id='your client id here',
    client_secret='your secret here',
    username='username',
    password='password',
    user_agent='mac:My_Example_App:v1.0 (by /u/username)'
)


## STEP 2: obtain a submission object

# option 1: whole url
# submission = reddit.submission(url=url)

# option 2: submission id
submission = reddit.submission("3g1jfi")


## STEP 3: getting "top-level" comments
from praw.models import MoreComments


# calling replace_more() is destructive. calling it again on the same submission instance has no effect.

submission.comments.replace_more(limit=None) # limit NONE means all are replaced
for top_level_comment in submission.comments:
    print(top_level_comment.body)
    
## STEP 4: getting replies to the "top-level" comments

    
# list() returns the same output structure as BFS
submission.comments.replace_more(limit=None)
for comment in submission.comments.list():
    print(comment.body)




'''
This is where we scraped data from
'''

#### Reddit places to scrape:

    # subreddits
#r/pcmasterrace
#r/gaming
#r/PS5
#r/XboxSeriesX
#r/PlayStation
#r/Xbox

    # keyword searches... this seemed to be the best option bc need individual posts
# "PC vs console"



# urls
# https://www.reddit.com/r/pcmasterrace/comments/5bkhra/pc_vs_console/
# https://www.reddit.com/r/memes/comments/1aui3z0/a_response_to_that_pc_vs_console_post/
# https://www.reddit.com/r/gamingsetups/comments/1e0qlux/pc_vs_console/
# https://www.reddit.com/r/Funnymemes/comments/179156h/pc_vs_console/
# https://www.reddit.com/r/ModernWarfareIII/comments/1ena41m/pc_vs_console/
# https://www.reddit.com/r/consoles/comments/161galc/console_vs_pc/
# https://www.reddit.com/r/pcmasterrace/comments/50hitp/pc_vs_consoles_be_like/
# https://www.reddit.com/r/gaming/comments/r41zj0/pc_vs_console/
# https://www.reddit.com/r/Rainbow6/comments/a4mfit/maciejay_testing_kaids_shotgun_recoil_pc_vs/
# https://www.reddit.com/r/ModernWarfareII/comments/16hvha0/pc_vs_console_aim_assist_no_difference_myth_bust/
# https://www.reddit.com/r/CallOfDuty/comments/puzbxi/cod_made_something_for_the_recent_pc_vs_console/
# https://www.reddit.com/r/truegaming/comments/676e39/what_are_some_points_in_the_pc_vs_console/
# https://www.reddit.com/r/Warframe/comments/1ctalxl/difficulty_pc_vs_console/
# https://www.reddit.com/r/deadbydaylight/comments/9ge9hw/pc_vs_console/
# https://www.reddit.com/r/LegionGo/comments/18p9937/pc_vs_console_people/


# game specific urls
  # Halo
    # https://www.reddit.com/r/haloinfinite/comments/18tbet1/pc_vs_console_playing_both/
    # https://www.reddit.com/r/halo/comments/r5t2hp/pc_vs_console_responsiveness_controller/
    # https://www.reddit.com/r/halo/comments/14wilja/pc_or_console/
    # https://www.reddit.com/r/halo/comments/quu6gt/pc_controller_aim_assist/
    # https://www.reddit.com/r/halo/comments/qurwr9/infinite_forced_crossplay_is_a_mistake/
    # https://www.reddit.com/r/halo/comments/17gvpb1/option_to_turn_off_crossplay/
  # Call of Duty
    # https://www.reddit.com/r/CallOfDuty/comments/10wtjva/mw2_do_pc_players_have_an_advantage_over_console/
    # https://www.reddit.com/r/CallOfDuty/comments/9h3924/cod_do_top_players_play_better_on_pc_or_console/
    # https://www.reddit.com/r/CallOfDuty/comments/1dq8dso/cod_crossplay_between_pc_and_console_should_end/
    # https://www.reddit.com/r/CallOfDuty/comments/17eexom/cod_crossplay_is_not_implemented_properly_this/
    # https://www.reddit.com/r/CallOfDuty/comments/1dssg17/cod_should_i_get_a_ps5_or_a_pc_for_cod/
    # https://www.reddit.com/r/CODWarzone/comments/g2pooq/the_reality_of_the_advantage_that_pc_players_have/
    # https://www.reddit.com/r/CODWarzone/comments/14dz5nd/pc_and_console_experience_in_game_is_completely/
   # Cyberpunk
    # https://www.reddit.com/r/cyberpunkgame/comments/1aoy1ml/pc_vs_console/
    # https://www.reddit.com/r/cyberpunkgame/comments/18c93jo/how_much_better_is_cyberpunk_on_pc_than_on_console/
    # https://www.reddit.com/r/cyberpunkgame/comments/sq1prz/cyberpunk_on_pc_is_literally_an_entirely/
    # https://www.reddit.com/r/cyberpunkgame/comments/11x3634/cyberpunk_on_pc_is_like_a_completely_different/
    # https://www.reddit.com/r/cyberpunkgame/comments/xzrn5q/is_cyberpunk_2077_better_on_ps5_or_pc/
    # https://www.reddit.com/r/cyberpunkgame/comments/t7z0br/why_does_mostly_everyone_play_on_pc/
    # https://www.reddit.com/r/cyberpunkgame/comments/16ruxjg/pc_players_what_is_one_mod_you_cant_live_without/
    





'''
Actually extracting here
# # # # # # # # # # # # general pc vs. console opinions # # # # # # # # # # # 
'''
import pandas as pd

#### Extracting comments about pc vs console debate

# posts
submission_ids = ['5bkhra', '1aui3z0', '1e0qlux', '179156h', '1ena41m',
                  '161galc', '50hitp', 'r41zj0', 'a4mfit', '16hvha0',
                  'puzbxi', '676e39', '1ctalxl', '9ge9hw', '18p9937']

# initialize list
comments_data = []

# collect info

for submission_id in submission_ids:
    # connect to reddit API
    submission = reddit.submission(submission_id)
    
    # load all comments and replies
    submission.comments.replace_more(limit=None) # limit NONE means all are replaced
    
    # loop through each comment
    for comment in submission.comments.list():
        comment_data = {
            "comment_id": comment.id,
            "comment_body": comment.body,
            "author": str(comment.author),
            "score": comment.score,
            "created_utc": comment.created_utc,
            "parent_id": comment.parent_id,
            "submission_id":submission.id ,
            "post_title":submission.title
            }
        comments_data.append(comment_data)


# convert to df
comments_df = pd.DataFrame(comments_data)

# UTC is reported in seconds... changing to more readable format
comments_df['created_utc'] = pd.to_datetime(comments_df['created_utc'], unit= 's')




'''
# # # # # # # # game specific df's  # # # # # # # # # # # # # # # # # 
'''

# HALO
submission_halo = ['18tbet1', 'r5t2hp', '14wilja', 'quu6gt', 'qurwr9',
                  '17gvpb1']


# initialize list
halo_data = []

# collect info

for submission_id in submission_halo:
    # connect to reddit API
    submission = reddit.submission(submission_id)
    
    # load all comments and replies
    submission.comments.replace_more(limit=None) # limit NONE means all are replaced
    
    # loop through each comment
    for comment in submission.comments.list():
        halo_comm_data = {
            "comment_id": comment.id,
            "comment_body": comment.body,
            "author": str(comment.author),
            "score": comment.score,
            "created_utc": comment.created_utc,
            "parent_id": comment.parent_id,
            "submission_id":submission.id ,
            "post_title":submission.title
            }
        halo_data.append(halo_comm_data)


# convert to df
halo_df = pd.DataFrame(halo_data)

# UTC is reported in seconds... changing to more readable format
halo_df['created_utc'] = pd.to_datetime(halo_df['created_utc'], unit= 's')





# CoD
submission_cod = ['10wtjva', '9h3924', '1dq8dso', '17eexom', '1dssg17',
                  'g2pooq', '14dz5nd']


# initialize list
cod_data = []

# collect info

for submission_id in submission_cod:
    # connect to reddit API
    submission = reddit.submission(submission_id)
    
    # load all comments and replies
    submission.comments.replace_more(limit=None) # limit NONE means all are replaced
    
    # loop through each comment
    for comment in submission.comments.list():
        cod_comm_data = {
            "comment_id": comment.id,
            "comment_body": comment.body,
            "author": str(comment.author),
            "score": comment.score,
            "created_utc": comment.created_utc,
            "parent_id": comment.parent_id,
            "submission_id":submission.id ,
            "post_title":submission.title
            }
        cod_data.append(cod_comm_data)


# convert to df
cod_df = pd.DataFrame(cod_data)

# UTC is reported in seconds... changing to more readable format
cod_df['created_utc'] = pd.to_datetime(cod_df['created_utc'], unit= 's')





# Cyberpunk

submission_cyb = ['1aoy1ml', '18c93jo', 'sq1prz', '11x3634', 'xzrn5q',
                  't7z0br', '16ruxjg']


# initialize list
cyb_data = []

# collect info

for submission_id in submission_cyb:
    # connect to reddit API
    submission = reddit.submission(submission_id)
    
    # load all comments and replies
    submission.comments.replace_more(limit=None) # limit NONE means all are replaced
    
    # loop through each comment
    for comment in submission.comments.list():
        cyb_comm_data = {
            "comment_id": comment.id,
            "comment_body": comment.body,
            "author": str(comment.author),
            "score": comment.score,
            "created_utc": comment.created_utc,
            "parent_id": comment.parent_id,
            "submission_id":submission.id ,
            "post_title":submission.title
            }
        cyb_data.append(cyb_comm_data)


# convert to df
cyb_df = pd.DataFrame(cyb_data)

# UTC is reported in seconds... changing to more readable format
cyb_df['created_utc'] = pd.to_datetime(cyb_df['created_utc'], unit= 's')



#### saving dataframes to use with lexicons

# general
comments_df.to_csv("/Users/areuschel/Desktop/Projects/ML_Summer24/general_comments.csv", index=False)

# Halo
halo_df.to_csv("/Users/areuschel/Desktop/Projects/ML_Summer24/halo_comments.csv", index= False)

# CoD
cod_df.to_csv("/Users/areuschel/Desktop/Projects/ML_Summer24/cod_comments.csv", index = False)

# Cyberpunk
cyb_df.to_csv("/Users/areuschel/Desktop/Projects/ML_Summer24/cyber_comments.csv", index = False)



