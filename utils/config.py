import os
import json

CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))
PROOT_DIR = os.path.dirname(CONFIG_DIR)

files_dir = os.path.join(PROOT_DIR, 'files')
log_dir = os.path.join(PROOT_DIR, files_dir, 'log')
json_dir = os.path.join(PROOT_DIR, files_dir, 'json')
time_format = "%Y-%m-%d %H:%M:%S"

# website
website_names_urls = {
    'weixin': 'https://mp.weixin.qq.com/s/To-zg7x4u1pvgsay7cN41Q',
    'sina': 'http://www.sina.com.cn/',
    'baidu_news': 'https://news.baidu.com/',
    '36kr': 'https://www.36kr.com/',
    '36kr-AI': 'https://www.36kr.com/information/AI/',
    'jiqizhixin': 'https://www.jiqizhixin.com/',
    'qbitai': 'https://www.qbitai.com/',
}

# model
abs_gen_model_name = os.path.join(PROOT_DIR, 'models', 'csebuetnlp_mT5_multilingual_XLSum')

MAX_ARTICLES_NUM_EVERY_WEBSITE_I_WANT_GET = 3
PULL_AGAIN_INTERVAL_TIME_H = 8

# chatgpt
use_chatgpt = False
prefix_request_prompt = """
Please help me analyze the above sentence, and answer the following questions please:
1. Sum up some of this text for me in 100 words or less.
2. List all the network links you see, and extract the network name, return null if there is no network link
3. This paragraph describes what it is about, such as ai, computer vision, science and technology, politics and sports
Please return your answer in json format, for example:
{
    'abstract': 'xxxx',
    'urls': {
                'github': xxxx,
                'arxiv.org': xxxx,
            },
    'class': 'xxxx'
}
"""
