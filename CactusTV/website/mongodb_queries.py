from bson.objectid import ObjectId
import random

def recommended_videos_mongodb(db,video_ids):

    records = list(db.videos.find({"videoInfo.id": {"$in": video_ids}}))

    videos = []
                    
    for document in records:

        videos.append(document)

    random.shuffle(videos)

    return videos

def get_current_video(db,video_id):

    video_ids = [video_id]

    records = list(db.videos.find({"videoInfo.id":{"$in":video_ids}}))

    random.shuffle(records)

    return records

def home_recommended_videos_mongodb(db,video_ids):

    records = list(db.videos.find({"videoInfo.id": {"$in": video_ids}}))

    videos = []
                    
    for document in records:

        videos.append(document)

    random.shuffle(videos)

    return videos

def update_views_count_mongodb(db,video_id):

    video_ids = [video_id]

    records = list(db.videos.find({"videoInfo.id":{"$in":video_ids}}))

    current_view_count = int(records[0]['videoInfo']['statistics']['viewCount'])

    id = ObjectId(records[0]['_id'])

    current_view_count += 1

    current_view_count = str(current_view_count)

    results = db.videos.update_one({'_id': id},{"$set": { "videoInfo.statistics.viewCount": current_view_count }})

    return None

def search_results_mongodb(db,query):

    records = list(db.videos.find( {'$text': {'$search': query} }))

    videos = []
                    
    for document in records:

        document['videoInfo']['snippet']['title'] = document['videoInfo']['snippet']['title'].replace('"','\\"')

        videos.append(document)

    return videos  