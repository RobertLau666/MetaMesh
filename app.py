import os
import sys
import newspaper
from tqdm import tqdm
from utils import util, config, FileProcess, Timer, AbstractGenerater, ChatGPTAPI


def main():
    util.create_dir_or_file(config.files_dir)
    util.create_dir_or_file(config.log_dir)
    util.create_dir_or_file(config.json_dir)
    
    file_process = FileProcess('launch')
    logger = file_process.logger
    timer = Timer(logger)
    abs_gen = AbstractGenerater(logger, config.abs_gen_model_name)
    chatgpt_api = ChatGPTAPI(logger, openai_api_key=config.openai_api_key)

    for website_name, website_url in config.website_names_urls.items():
        paper = newspaper.build(website_url, language='zh')
        categorys = paper.category_urls()
        logger.info(f"categorys nums: {len(categorys)} \ncategorys: {categorys}")

        article_json = {}
        articles = paper.articles
        logger.info(f"articles nums: {len(articles)} \narticles: {articles}")
        
        get_articles_record_number = 0
        for i, article in enumerate(tqdm(articles)):
            try:
                article.download()
                article.parse()
            except Exception as e:
                logger.error(f"The article parsing was wrong: {e}")
            else:
                publish_date, publish_date_is_office = timer.get_custom_publish_date(article)
                dict_item = {
                    "original_title": article.title,
                    "original_text": article.text,
                    "abstract_text": abs_gen.abstract_generater(article.text),
                    "chatgpt_api_analyse": chatgpt_api.chat_with_gpt(article.text + config.prefix_request_prompt) if config.use_chatgpt else "The function is not enabled",
                    "original_url": article.url,
                    "publish_date": publish_date,
                    "publish_date_is_office": publish_date_is_office,
                    "authors": article.authors,
                    "top_image": article.top_image,
                    "movies": article.movies,
                    "keywords": article.keywords,
                    "summary": article.summary,
                }
                article_json[str(get_articles_record_number)] = dict_item
                get_articles_record_number += 1
            if get_articles_record_number == config.MAX_ARTICLES_NUM_EVERY_WEBSITE_I_WANT_GET:
                break
        
        file_process.save_json(article_json, os.path.join(config.json_dir, f'{website_name}.json'))
        

if __name__ == "__main__":
    main()
