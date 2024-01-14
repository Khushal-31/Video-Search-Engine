import numpy as np

import mysql.connector

from flask import session

def recommended_videos_neo4j(driver,current_video_id):

    records, summary, keys = driver.execute_query(
        ''' MATCH (v:Video)
            WHERE v.id = $input
            RETURN v.title,v.categoryId,v.defaultAudioLanguage,v.channelId,v.tags''',
           input = current_video_id,
           database_="neo4j",
    )

    category_id = records[0]['v.categoryId']
    channel_id = records[0]['v.channelId']
    audio_language = records[0]['v.defaultAudioLanguage']
    tags = records[0]['v.tags']
    title = records[0]['v.title']

    video_ids = []
    video_ids_set = set()

    # Same Tags

    try:

        for tag in tags:

            records, summary, keys = driver.execute_query(
             '''MATCH (v:Video)-[ct1:CONTAINS_TAG]->(t:Tag)
                WHERE t.name = $t AND v.id <> $input
                RETURN v.title,v.id,v.viewCount''',
                input = current_video_id,
                t = tag,
                database_="neo4j",
            )
                
            for video in records:
                
                if video['v.id'] not in video_ids_set and video['v.id']!=current_video_id:
                
                    video_ids.append([video['v.id'],int(video['v.viewCount'])])
                    video_ids_set.add(video['v.id'])

    except:

        pass

    # Same Channel

    records, summary, keys = driver.execute_query(
     '''MATCH (v:Video)-[ch1:BELONGS_TO_CHANNEL]->(ch:Channel)
        WHERE ch.id = $chId AND v.id <> $input
        RETURN v.title,v.id,v.viewCount''',
        input = current_video_id,
        chId = channel_id,
        database_="neo4j",
    )    

    for video in records:
        
        if video['v.id'] not in video_ids_set and video['v.id']!=current_video_id:
            
            video_ids.append([video['v.id'],int(video['v.viewCount'])])
            video_ids_set.add(video['v.id'])

    # Same Category

    records, summary, keys = driver.execute_query(
        '''MATCH (v:Video)-[cat1:BELONGS_TO_CATEGORY]->(cat:Category)
           WHERE cat.id = $catId AND v.id <> $input
           RETURN v.title,v.id,v.viewCount''',
           input = current_video_id,
           catId = category_id,
           database_="neo4j",
    )

    for video in records:

        if video['v.id'] not in video_ids_set and video['v.id']!=current_video_id:
            
            video_ids.append([video['v.id'],int(video['v.viewCount'])])
            video_ids_set.add(video['v.id'])

    # Same Audio Language

    records, summary, keys = driver.execute_query(
     '''MATCH (v:Video)-[al1:HAS_AUDIO_LANGUAGE]->(al:AudioLanguage)
        WHERE al.audio_language = $al AND v.id <> $input
        RETURN v.title,v.id,v.viewCount''',
        input = current_video_id,
        al = audio_language,
        database_="neo4j",
    )
        
    for video in records:
        
        if video['v.id'] not in video_ids_set and video['v.id']!=current_video_id:
            
            video_ids.append([video['v.id'],int(video['v.viewCount'])])
            video_ids_set.add(video['v.id'])

    # User Click History

    conn = mysql.connector.connect(host="localhost",
                               user="root",
                               passwd ="watermelon",
                               database ="cactus_login",
                               auth_plugin='mysql_native_password')

    cursor = conn.cursor()

    username = session.get('user')

    cursor.execute("SELECT DISTINCT(video_id) FROM clicks WHERE username = '{}';".format(username))

    user_click_history = cursor.fetchall()

    user_click_history = np.array([ i[0] for i in user_click_history if i[0] not in video_ids_set ])

    np.random.shuffle(user_click_history)

    for video_id in user_click_history:

        if video_id not in video_ids_set and video_id!=current_video_id:
            
            video_ids.append([video_id,0])
            video_ids_set.add(video_id)
    
    conn.commit()

    conn.close()

    # Recommendation

    final_video_ids = np.array([None for i in range(10)])

    video_ids = np.array(video_ids)

    if (len(video_ids)>=10):

        if (len(video_ids)>=15):
            
            video_ids = np.array(sorted(video_ids[:15], key = lambda x: x[1],reverse=True))

        np.random.shuffle(video_ids)

        final_video_ids[:10] = video_ids[:10,0]

    else:

        final_video_ids[:len(video_ids)] = video_ids[:len(video_ids),0]

        remaining = 10 - len(video_ids)

        records, summary, keys = driver.execute_query(
        ''' MATCH (v:Video)
            RETURN v.id,v.viewCount ORDER BY v.viewCount DESC LIMIT {}'''.format(50),
           database_="neo4j",
        )

        video_ids = []

        for video in records:

            if video['v.id'] not in video_ids_set and video['v.id']!=current_video_id:
                
                video_ids.append(video['v.id'])

        final_video_ids[10-remaining:] = video_ids[:remaining]
   
    return list(final_video_ids)

def home_recommended_videos_neo4j(driver):

    video_ids = []
    video_ids_set = set()

    final_video_ids = np.array([None for i in range(15)])

    # Popular Videos

    records, summary, keys = driver.execute_query(
        ''' MATCH (v:Video)
            RETURN v.id ORDER BY v.viewCount DESC LIMIT {}'''.format(50),
        database_="neo4j",
    )

    video_ids = []

    for video in records:

        if video['v.id'] not in video_ids_set:

            video_ids.append([video['v.id'],0])
            video_ids_set.add(video['v.id'])

    video_ids = np.array(video_ids)

    np.random.shuffle(video_ids)

    video_ids_use = video_ids[:10]
    video_ids_left = video_ids[10:]

    final_video_ids[:10] = video_ids_use[:,0]

    # User Click History

    conn = mysql.connector.connect(host="localhost",
                               user="root",
                               passwd ="watermelon",
                               database ="cactus_login",
                               auth_plugin='mysql_native_password')

    cursor = conn.cursor()

    username = session.get('user')

    cursor.execute("SELECT DISTINCT(video_id) FROM clicks WHERE username = '{}';".format(username))

    user_click_history = cursor.fetchall()

    user_click_history = np.array([ i[0] for i in user_click_history if i[0] not in video_ids_set ])

    np.random.shuffle(user_click_history)

    video_ids = []

    for video_id in user_click_history:

        if video_id not in video_ids_set:
            
            video_ids.append([video_id,0])
            video_ids_set.add(video_id)

    video_ids = np.array(video_ids)
    
    conn.commit()

    conn.close()

    if (len(video_ids)<5 and len(video_ids)>0):

        final_video_ids[10:10+len(video_ids)] = video_ids[:len(video_ids),0]

        remaining = 5 - len(video_ids)

        final_video_ids[10+len(video_ids):] = video_ids_left[:remaining,0]

    elif (len(video_ids)==0):

        final_video_ids[10+len(video_ids):] = video_ids_left[:5,0]

    else:

        final_video_ids[10:15] = video_ids[:5,0]

    return list(final_video_ids)