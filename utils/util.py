
import re
import os
import sys
import logging
import nltk
import json
from utils import config
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import openai


def create_dir_or_file(path):
    if not os.path.exists(path):
        file_name, file_extension = os.path.splitext(path)
        print("file_name, file_extension",file_name, file_extension)
        if file_extension == "":
            os.makedirs(path, exist_ok=True)
        else:
            if not os.path.exists(path):
                with open(path, 'w') as file:
                    file.write('{}') # it is json format here in this project

class FileProcess():
    def __init__(self, log_name):
        self.logger = self.get_logger(log_name)

    def get_logger(self, log_name):
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt=config.time_format,
            level=logging.INFO,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(
                    os.path.join(config.log_dir, f"{log_name}.log")
                ),
            ]
        )
        logger = logging.getLogger(__name__)
        logger.info("***** Beginning *****")
        return logger

    def save_json(self, json_content, json_file_path):
        with open(json_file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(json_content, indent=4, ensure_ascii=False))

    def get_current_time(self):
        current_time = datetime.now()
        date_suffix = current_time.strftime("_%Y%m%d")
        time_suffix = current_time.strftime("_%H%M%S")

        return '_time' + date_suffix + time_suffix


class Timer():
    def __init__(self, logger):
        self.logger = logger
        nltk.download('punkt')

    def get_formatted_current_time(self):
        current_time = datetime.now()
        formatted_current_time = current_time.strftime(config.time_format)
        return formatted_current_time

    def get_custom_publish_date(self, article):
        try:
            article.download()
            article.parse()
            article.nlp()
        except Exception as e:
            self.logger.error(f"Error parsing article: {e}")
            return None
        
        if article.publish_date:
            return article.publish_date.strftime(config.time_format), 1
        else:
            # 自定义解析逻辑可以放在这里，具体解析方式需要根据目标网站的实际情况编写
            # 比如使用 BeautifulSoup 或正则表达式来提取日期
            return self.get_formatted_current_time(), 0
    
class AbstractGenerater():
    def __init__(self, logger, model_name:str="csebuetnlp/mT5_multilingual_XLSum"):
        self.logger = logger
        
        self.WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, local_files_only=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name, local_files_only=True)

    def abstract_generater(self, article_text):
        input_ids = self.tokenizer(
            [self.WHITESPACE_HANDLER(article_text)],
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=512
        )["input_ids"]

        output_ids = self.model.generate(
            input_ids=input_ids,
            max_length=84,
            no_repeat_ngram_size=2,
            num_beams=4
        )[0]

        summary = self.tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )

        self.logger.info(f"summary: {summary}")
        return summary

class ChatGPTAPI():
    def __init__(self, logger, openai_api_key):
        self.logger = logger
        openai.api_key = openai_api_key # OpenAI API Key获取: OpenAI Platform 

    def chat_with_gpt(self, prompt, max_tokens=50):
        self.logger.info(f"ChatGPT is analyzing text: {prompt}")
        response = openai.Completion.create(
            engine="text-davinci-002",  # 使用的GPT模型引擎
            prompt=prompt,
            max_tokens=max_tokens  # 生成的最大标记数
        )
        return response.choices[0].text.strip()


if __name__ == '__main__':
    file_process = File_Process('test')
    logger = file_process.logger
    abs_gen = AbstractGenerater(logger, "/data/dev-linky/as-loki-lcy-folder/Models/csebuetnlp_mT5_multilingual_XLSum")
    article_text = "Videos that say approved vaccines are dangerous and cause autism, cancer or infertility are among those that will be taken down, the company said.  The policy includes the termination of accounts of anti-vaccine influencers.  Tech giants have been criticised for not doing more to counter false health information on their sites.  In July, US President Joe Biden said social media platforms were largely responsible for people's scepticism in getting vaccinated by spreading misinformation, and appealed for them to address the issue.  YouTube, which is owned by Google, said 130,000 videos were removed from its platform since last year, when it implemented a ban on content spreading misinformation about Covid vaccines.  In a blog post, the company said it had seen false claims about Covid jabs 'spill over into misinformation about vaccines in general'. The new policy covers long-approved vaccines, such as those against measles or hepatitis B.  We're expanding our medical misinformation policies on YouTube with new guidelines on currently administered vaccines that are approved and confirmed to be safe and effective by local health authorities and the WHO, the post said, referring to the World Health Organization."
    summary = abs_gen.abstract_generater(article_text)
    print('summary: ', summary)
