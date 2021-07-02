import requests
from multiprocessing import Pool, Queue

from app.main import cache

HATCHWAYS_POSTS_API_URL = "https://api.hatchways.io/assessment/blog/posts"


def fetch_posts(tag=None):
    query_params = dict()
    if tag:
        query_params['tag'] = tag
    r = requests.get(HATCHWAYS_POSTS_API_URL, params=query_params)

    return r.json()


def get_posts_data(tag):
    data = fetch_posts(tag)
    get_posts_data.q.put(data['posts'])


def initialize_queue(queue):
    get_posts_data.q = queue


def remove_duplicate_posts(posts):
    # Used this to preserve ordering of data.
    done = set()
    unique_posts = []
    for post in posts:
        post_id = post['id']
        if post_id not in done:
            done.add(post_id)
            unique_posts.append(post)

    return unique_posts


def execute_process_based_on_tags(tags):
    tags_list = tags.split(',')

    q = Queue()
    p = Pool(3, initialize_queue, [q])
    p.imap(get_posts_data, tags_list)
    p.close()

    all_data = list()
    for i in range(len(tags_list)):
        all_data.extend(q.get())

    unique_posts = remove_duplicate_posts(all_data)
    return unique_posts


def get_tags_based_posts(tags):
    # Check cached data based on given tags string
    cached_posts_data = cache.get(tags)
    if cached_posts_data:
        return cached_posts_data

    # Get data and cache it
    unique_posts = execute_process_based_on_tags(tags)
    cache.set(tags, unique_posts)

    return unique_posts

# from app.main.service.hatchways_service import get_tags_based_posts
