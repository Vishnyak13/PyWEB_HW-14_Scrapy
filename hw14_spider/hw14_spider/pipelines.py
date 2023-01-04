# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup
from .models import Quotes, Tags, Authors

URL = 'https://quotes.toscrape.com/'


class Hw14SpiderPipeline:
    def process_item(self, item, spider):
        engine = create_engine('sqlite:///quotes.db.sqlite3')
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            flag = 0
            if item['tags'] and item['author'] and item['quote']:
                name = item['author'][0]
                for author in session.query(Authors).all():
                    if author.author_name == f'{name}':
                        flag = 1

            if flag == 0:
                author_url = item['author_url']
                author_full_url = URL + author_url[7:-1] + '/'
                print(author_full_url)
                print('-----------------')

                response = requests.get(author_full_url)
                soup = BeautifulSoup(response.text, 'lxml')
                born_date = soup.find('span', class_='author-born-date').get_text(strip=True)
                born_location = soup.find('span', class_='author-born-location').get_text(strip=True)
                name = item['author'][0]
                author = Authors(
                    author_name=f'{name}',
                    born_date=f'{born_date}',
                    born_location=f'{born_location[3:]}',
                    author_url=f'{author_full_url}',
                )
                session.add(author)
                session.commit()

            if item['tags'] and item['author'] and item['quote']:
                author = session.query(Authors).filter(Authors.author_name == f'{name}').first()
                quote = Quotes(
                    quote=f'{item["quote"]}',
                    author_id=author.id,
                )
                session.add(quote)
                session.commit()

                for tag in item['tags']:
                    flag = 0
                    for tag_ in session.query(Tags).all():
                        if tag_.tag_name == f'{tag}':
                            flag = 1
                    if flag == 0:
                        tag_ = Tags(
                            tag_name=f'{tag}',
                        )
                        session.add(tag_)
                        session.commit()
                    tag_ = session.query(Tags).filter(Tags.tag_name == f'{tag}').first()
                    quote.tags.append(tag_)
                    session.commit()

        except Exception as e:
            print(e)
            session.rollback()

        finally:
            session.close()

        return item
