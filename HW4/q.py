# Веб-сервис выложен по адресу http://www.vladisgrig.ru/

from flask import Flask, render_template, url_for, request, redirect, session
import urllib.request
import json
import networkx as nx
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import time
from random import randint

app = Flask(__name__)

app.secret_key = 'bF5w%C1s{ncdcdq8K?PAF9a*%o}ti0P#' # ключ для сервера

# Считает долго, поэтому нужно подождать, когда всё посчитается...

@app.route('/')
def first_page():
    return render_template('first_page.html')

@app.route('/graph')
def graph():

    access_token = request.args['access_token']
    
    req = urllib.request.Request('https://api.vk.com/method/friends.get?count=5000&v=5.78&fields=id&access_token={}'.format(access_token))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    result = json.loads(result)

    friends = []
    
    for elem in result['response']['items']
        if elem['first_name'] != "DELETED":
            friends.append(elem['id'])
    
    req = urllib.request.Request('https://api.vk.com/method/users.get?v=5.78&access_token={}'.format(access_token))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    result = json.loads(result)
    id = result['response'][0]['id']
    
    # posts
    
    posts_stats = dict()
    for friend in friends:
        posts_stats[friend] = 0
    req = urllib.request.Request('https://api.vk.com/method/wall.get?type=owner_id={}&offset=0&count=1&v=5.78&access_token={}'.format(id, access_token))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    result = json.loads(result)
    num_of_posts = result['response']['count']

    offsets = [100 * i for i in range(num_of_posts // 100 + 1)]

    post_ids = []
    for offset in offsets:
        req = urllib.request.Request('https://api.vk.com/method/wall.get?type=owner_id={}&offset={}&count=100&v=5.78&access_token={}'.format(id, offset, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        for elem in result['response']['items']:
            post_ids.append(elem['id'])
    
    for post_id in post_ids:
        time.sleep(0.4) # иначе по времени вылетает
        req = urllib.request.Request('https://api.vk.com/method/likes.getList?type=post&owner_id={}&item_id={}&friends_only=1&count=1&v=5.78&access_token={}&skip_own=1'.format(id, post_id, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        if 'response' not in result:
            return render_template('second_page.html', result=result)
        num_of_likes = result['response']['count']
        if num_of_likes == 0:
            continue
        
        offsets_ = [1000 * i for i in range(num_of_likes // 1000 + 1)]
        for offset_ in offsets_:
            time.sleep(0.4) # иначе по времени вылетает
            req = urllib.request.Request('https://api.vk.com/method/likes.getList?type=post&owner_id={}&item_id={}&friends_only=1&count=1000&v=5.78&access_token={}&offset={}&skip_own=1'.format(id, post_id, access_token, offset_))
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            result = json.loads(result)
            if 'response' in result and result['response']['items'] != []:
                for elem in result['response']['items']:
                    posts_stats[elem] += 1
    # /posts

    # post_comments
    
    post_comments_stats = dict()
    for friend in friends:
        post_comments_stats[friend] = 0

    for post_id in post_ids:
        time.sleep(0.4) # иначе по времени вылетает
        req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id={}&post_id={}&count=1&v=5.78&access_token={}'.format(id, post_id, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        num_of_comments = result['response']['count']
        
        offsets_ = [100 * i for i in range(num_of_comments // 100 + 1)]
        for offset_ in offsets_:
            time.sleep(0.4) # иначе по времени вылетает
            req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id={}&post_id={}&count=100&offset={}&v=5.78&access_token={}'.format(id, post_id, offset_, access_token))
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            result = json.loads(result)
            if 'response' in result and result['response']['items'] != []:
                for elem in result['response']['items']:
                    if elem['from_id'] in post_comments_stats:
                        post_comments_stats[elem['from_id']] += 1
                        
    # /post_comments
    
    # photos
    
    photo_stats = dict()
    for friend in friends:
        photo_stats[friend] = 0
        
    req = urllib.request.Request('https://api.vk.com/method/photos.getAll?owner_id={}&count=1&v=5.78&access_token={}'.format(id, access_token))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    result = json.loads(result)
    num_of_photos = result['response']['count']
    
    offsets = [200 * i for i in range(num_of_photos // 200 + 1)]

    photo_ids = []
    for offset in offsets:
        req = urllib.request.Request('https://api.vk.com/method/photos.getAll?owner_id={}&extended=0&count=200&offset={}&v=5.78&access_token={}'.format(id, offset, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
    
        for elem in result['response']['items']:
            photo_ids.append(elem['id'])
    
    for photo_id in photo_ids:
        time.sleep(0.4) # иначе по времени вылетает
        req = urllib.request.Request('https://api.vk.com/method/likes.getList?type=photo&owner_id={}&item_id={}&friends_only=1&count=1&v=5.78&access_token={}&skip_own=1'.format(id, photo_id, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        if 'response' not in result:
            return render_template('second_page.html', result=result)
        num_of_likes = result['response']['count']
        if num_of_likes == 0:
            continue
        
        offsets_ = [1000 * i for i in range(num_of_likes // 1000 + 1)]
        for offset_ in offsets_:
            time.sleep(0.4) # иначе по времени вылетает
            req = urllib.request.Request('https://api.vk.com/method/likes.getList?type=photo&owner_id={}&item_id={}&friends_only=1&count=1000&v=5.78&access_token={}&offset={}&skip_own=1'.format(id, photo_id, access_token, offset_))
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            result = json.loads(result)
            if 'response' in result and result['response']['items'] != []:
                for elem in result['response']['items']:
                    photo_stats[elem] += 1

    
    # /photos
    
    # photos_comments
    
    photo_comments_stats = dict()
    for friend in friends:
        photo_comments_stats[friend] = 0
    
    for photo_id in photo_ids:
        time.sleep(0.4) # иначе по времени вылетает
        req = urllib.request.Request('https://api.vk.com/method/photos.getComments?owner_id={}&photo_id={}&count=1&v=5.78&access_token={}'.format(id, photo_id, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        if 'response' not in result:
            return render_template('second_page.html', result=result)
        num_of_comments = result['response']['count']
        if num_of_comments == 0:
            continue
        
        offsets_ = [100 * i for i in range(num_of_comments // 100 + 1)]
        for offset_ in offsets_:
            time.sleep(0.4) # иначе по времени вылетает
            req = urllib.request.Request('https://api.vk.com/method/photos.getComments?owner_id={}&photo_id={}&count=100&v=5.78&access_token={}&offset={}'.format(id, photo_id, access_token, offset_))
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            result = json.loads(result)
            if 'response' in result and result['response']['items'] != []:
                for elem in result['response']['items']:
                    photo_comments_stats[elem] += 1
    
    # /photos_comments
    
    # videos
    
    video_stats = dict()
    for friend in friends:
        video_stats[friend] = 0
        
    req = urllib.request.Request('https://api.vk.com/method/video.get?owner_id={}&count=1&v=5.78&access_token={}'.format(id, access_token))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    result = json.loads(result)
    num_of_videos = result['response']['count']
    
    offsets = [200 * i for i in range(num_of_videos // 200 + 1)]
    
    video_ids = []
    for offset in offsets:
        req = urllib.request.Request('https://api.vk.com/method/video.get?owner_id={}&count=200&offset={}&v=5.78&access_token={}'.format(id, offset, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        for elem in result['response']['items']:
            if elem['owner_id'] == id:
                video_ids.append(elem['id'])

    for video_id in video_ids:
        time.sleep(0.4) # иначе по времени вылетает
        req = urllib.request.Request('https://api.vk.com/method/likes.getList?type=video&owner_id={}&item_id={}&friends_only=1&count=1&v=5.78&access_token={}&skip_own=1'.format(id, video_id, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        if 'response' not in result:
            return render_template('second_page.html', result=result)
        num_of_likes = result['response']['count']
        if num_of_likes == 0:
            continue
        
        offsets_ = [1000 * i for i in range(num_of_likes // 1000 + 1)]
        for offset_ in offsets_:
            time.sleep(0.4) # иначе по времени вылетает
            req = urllib.request.Request('https://api.vk.com/method/likes.getList?type=video&owner_id={}&item_id={}&friends_only=1&count=1000&v=5.78&access_token={}&offset={}&skip_own=1'.format(id, video_id, access_token, offset_))
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            result = json.loads(result)
            if 'response' in result and result['response']['items'] != []:
                for elem in result['response']['items']:
                    if elem in video_stats:
                        video_stats[elem] += 1

    # /videos
    
    # videos_comments
    
    video_comments_stats = dict()
    for friend in friends:
        video_comments_stats[friend] = 0
    
    for video_id in video_ids:
        time.sleep(0.4) # иначе по времени вылетает
        req = urllib.request.Request('https://api.vk.com/method/video.getComments?owner_id={}&video_id={}&count=1&v=5.78&access_token={}'.format(id, video_id, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        if 'response' not in result:
            return render_template('second_page.html', result=result)
        num_of_comments = result['response']['count']
        if num_of_comments == 0:
            continue
        
        offsets_ = [100 * i for i in range(num_of_comments // 100 + 1)]
        for offset_ in offsets_:
            time.sleep(0.4) # иначе по времени вылетает
            req = urllib.request.Request('https://api.vk.com/method/video.getComments?owner_id={}&photo_id={}&count=100&v=5.78&access_token={}&offset={}'.format(id, video_id, access_token, offset_))
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            result = json.loads(result)
            if 'response' in result and result['response']['items'] != []:
                for elem in result['response']['items']:
                    if elem in video_comments_stats:
                        video_comments_stats[elem] += 1

    # /videos_comments

    id_to_name = dict()
    dg = nx.DiGraph()

    messages_stats = dict()
    for friend in friends:
        messages_stats[friend] = 0
    
    for friend in friends:
        time.sleep(0.4)
        req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids={}&v=5.78&access_token={}'.format(friend, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        first_name = result['response'][0]['first_name']
        last_name = result['response'][0]['last_name']
        name = first_name + ' ' + last_name[0] + '.'
        dg.add_node(name)
        id_to_name[friend] = name

        time.sleep(0.4)
        req = urllib.request.Request('https://api.vk.com/method/messages.getHistory?count=1&user_id={}&v=5.78&access_token={}'.format(friend, access_token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        messages_stats[friend] = result['response']['count']
    
    req = urllib.request.Request('https://api.vk.com/method/account.getProfileInfo?v=5.78&access_token={}'.format(access_token))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    result = json.loads(result)

    first_name = result['response']['first_name']
    last_name = result['response']['last_name']
    name = first_name + ' ' + last_name[0] + '.'
    dg.add_node(name)
    id_to_name[id] = name
    
    stats = dict()
    for friend in friends:
        stats[friend] = 0
    for friend in friends:
        stats[friend] += 2 * posts_stats[friend] + 2 * post_comments_stats[friend] + 2 * photo_stats[friend] + 2 * photo_comments_stats[friend] + 2 * video_stats[friend] + 2 * video_comments_stats[friend] + 0.01 * messages_stats[friend]
        dg.add_weighted_edges_from([(id_to_name[friend], id_to_name[id], stats[friend])])
    
    pos=nx.spring_layout(dg, k=1, iterations=50) # circular_layout
    nx.draw_networkx_nodes(dg, pos, node_color='blue', node_size=10)
    nx.draw_networkx_edges(dg, pos, edge_color='red', edge_size=1)
    nx.draw_networkx_labels(dg, pos, font_size=5, font_family='Times New Roman')
    plt.axis('off')
    file = 'static/graph' + str(randint(1, 1000)) + '.png'
    plt.savefig(file, dpi=600, type="png", transparent=True)
    plt.clf()
    
    return render_template('second_page.html', file=file)

if __name__ == '__main__':
    app.run(host='0.0.0.0') # на локальном компьютере вводить localhost:5000
