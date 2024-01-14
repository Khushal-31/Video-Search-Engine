from flask import Blueprint, render_template, request, current_app,session

from functools import wraps

from flask_pymongo import PyMongo

from website.neo4j_queries import recommended_videos_neo4j,home_recommended_videos_neo4j
from website.mongodb_queries import recommended_videos_mongodb,get_current_video,home_recommended_videos_mongodb,update_views_count_mongodb,search_results_mongodb
from website.mysql_queries import insert_views_click_data_mysql,insert_searches_data_mysql

from neo4j import GraphDatabase,basic_auth

from flask import request,redirect,url_for

import mysql.connector

views = Blueprint('views',__name__)

def login_required(f):

    @wraps(f)

    def decorated_function(*args, **kwargs):

        if session.get('user') is None or session.get('logged_in') is False:

            return redirect('/login',code=302)
        
        return f(*args, **kwargs)
    
    return decorated_function

@views.route('/')
def load():

    return redirect(url_for('views.home_page'))

@views.route('/home',methods=["GET","POST"])
@login_required
def home_page():

    # Getting IDs of recommended videos

    driver = GraphDatabase.driver("bolt://localhost:7689", auth=basic_auth("khushal","watermelon"))
    driver.verify_connectivity()

    driver.close()

    ids_home_recommended_videos = home_recommended_videos_neo4j(driver)
    
    # Getting data of recommended videos

    mongodb_client = PyMongo(current_app, uri="mongodb://localhost:27017/YT_Videos")
    db = mongodb_client.db

    home_recommended_videos = home_recommended_videos_mongodb(db,ids_home_recommended_videos)

    return render_template("home.html",
                           home_recommended_videos = home_recommended_videos)

@views.route('/load_search',methods=["POST","GET"])
@login_required
def load_search_page():
    
    if request.method == 'POST':

        query = request.form.get('query')

        session['query'] = query

        return redirect(url_for('views.search_page',query=query))
    
    return render_template("load_search.html")


@views.route('/search',methods=["POST","GET"])
@login_required
def search_page(query=None):

    # Going to the searched video

    if request.method == 'POST':

        query = request.form.get('query')

        session['query'] = query

        return redirect(url_for('views.search_page',query=query))
    
    query = session['query']
        
    # Getting data of recommended videos

    mongodb_client = PyMongo(current_app, uri="mongodb://localhost:27017/YT_Videos")
    db = mongodb_client.db

    search_results_videos = search_results_mongodb(db,query)

    search_results_thumbnails = []
    search_results_title = []
    search_results_channelTitle = []
    search_results_publishedAt = []
    search_results_viewCount = []
    search_results_stats = []
    search_results_id = []

    for sr in search_results_videos:

        search_results_thumbnails.append(sr['videoInfo']['snippet']['thumbnails']['medium']['url'])
        search_results_title.append(sr['videoInfo']['snippet']['title'])
        search_results_channelTitle.append(sr['videoInfo']['snippet']['channelTitle'])
        search_results_publishedAt.append(sr['videoInfo']['snippet']['publishedAt'])
        search_results_viewCount.append(sr['videoInfo']['statistics']['viewCount'])
        search_results_stats.append(sr['videoInfo']['statistics'])
        search_results_id.append(sr['videoInfo']['id'])

    # Storing search history 

    conn = mysql.connector.connect(host="localhost",
                               user="root",
                               passwd="watermelon",
                               database ="cactus_login",
                               auth_plugin='mysql_native_password')

    cursor = conn.cursor()
    
    insert_searches_data_mysql(cursor,query)

    conn.commit()

    conn.close()
    
    return render_template("search.html",search_results_th=search_results_thumbnails,
                                         search_results_ti=search_results_title,
                                         search_results_ct=search_results_channelTitle,
                                         search_results_p=search_results_publishedAt,
                                         search_results_vc=search_results_viewCount,
                                         search_results_s=search_results_stats,
                                         search_results_i=search_results_id,
                                         query1=[query])

@views.route('/video/<id>',methods=["POST","GET"])
@login_required
def video_page(id=None):

    # Going to the searched video

    if request.method == 'POST':

        query = request.form.get('query')

        return redirect(url_for('views.search_page', query=query))

    # Current Video ID

    current_video_id = id
    
    # Getting IDs of recommended videos

    driver = GraphDatabase.driver("bolt://localhost:7689", auth=basic_auth("khushal","watermelon"))
    driver.verify_connectivity()

    driver.close()

    ids_recommended_videos = recommended_videos_neo4j(driver,current_video_id)
    
    # Getting data of recommended videos

    mongodb_client = PyMongo(current_app, uri="mongodb://localhost:27017/YT_Videos")
    db = mongodb_client.db

    current_video = get_current_video(db,current_video_id)
    recommended_videos = recommended_videos_mongodb(db,ids_recommended_videos)
    
    # Storing Views Click Data

    conn = mysql.connector.connect(host="localhost",
                               user="root",
                               passwd="watermelon",
                               database ="cactus_login",
                               auth_plugin='mysql_native_password')

    cursor = conn.cursor()
    
    insert_views_click_data_mysql(cursor,current_video)

    conn.commit()

    conn.close()

    # Update Views Count

    update_views_count_mongodb(db,current_video_id)

    return render_template("video.html",
                           current_video=current_video,
                           recommended_videos=recommended_videos)

