from flask import session

def insert_views_click_data_mysql(cursor,current_video):

    username = session.get('user')

    cursor.execute("SELECT id FROM users WHERE username = '{}';".format(username))

    user_id = cursor.fetchone()[0]

    video_id = current_video[0]['videoInfo']['id']

    channel_id = current_video[0]['videoInfo']['snippet']['channelId']

    category = int(current_video[0]['videoInfo']['snippet']['categoryId'])

    cursor.execute('''
                   INSERT INTO clicks
                   (`user_id`,`username`,`video_id`,`channel_id`,`category`)
                   VALUES
                   ({},'{}','{}','{}',{});'''.format(user_id,username,video_id,channel_id,category))
    
    return None


def insert_searches_data_mysql(cursor,query):

    username = session.get('user')

    cursor.execute("SELECT id FROM users WHERE username = '{}';".format(username))

    user_id = cursor.fetchone()[0]

    cursor.execute('''
                   INSERT INTO searches
                   (`user_id`,`username`,`search_query`)
                   VALUES
                   ({},'{}','{}');'''.format(user_id,username,query))
    
    return None