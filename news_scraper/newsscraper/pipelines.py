# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from newsscraper import settings


class NewsscraperPipeline:
    """
    Pipeline for piping scraped data to PostgreSQL database locally
    """

    def __init__(self):
        """
        initialization methood
        """

        self.connection = None
        self.cursor = None
        self.news_tablename = "investo_news"

        #  create connection
        self._create_connection()

        # check exitence of table then create
        self.create_table()

    def _create_connection(self):
        """
        create database connection
        """
        try:
            self.connection = psycopg2.connect(
                user=settings.DB_USER,
                password=settings.DB_PW,
                host=settings.DB_HOST,
                database=settings.DB_NAME,
                port=settings.DB_PORT,
            )

            self.cursor = self.connection.cursor()

            # print information
            print(
                "Postgres Server information:\n", self.connection.get_dsn_parameters()
            )

            self.cursor.execute("SELECT version();")

            print("\nYou are connected to", self.cursor.fetchone(), "\n")

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL\n", error)

    def _disconnect(self):
        """
        disconnect from database
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")

    def create_table(self):
        """
        Create table
        """

        self.cursor.execute(
            f"""SELECT EXISTS(SELECT * FROM pg_tables WHERE tablename='{self.news_tablename}');"""
        )
        exists = self.cursor.fetchone()[0]
        if not exists:
            create_table_query = f"""CREATE TABLE {self.news_tablename}(
                    source VARCHAR (50), 
                    headline VARCHAR (300),
                    subtitle TEXT,
                    date VARCHAR (100),
                    nepdate VARCHAR (100),
                    scraped_datetime VARCHAR (100), 
                    image_url VARCHAR (200),
                    url VARCHAR (200), 
                    scrip VARCHAR []
            )"""
            self.cursor.execute(create_table_query)

    def _store_db(self, item):
        """
        Stores in database
        """
        sql = f"""INSERT INTO
            {self.news_tablename} (source,headline,subtitle,date,nepdate,scraped_datetime,image_url,url,scrip)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s,%s,%s);
        """
        data = (
            item["source"],
            item["headline"],
            item["subtitle"],
            item["date"],
            item["nepdate"],
            item["scraped_datetime"],
            item["image_url"],
            item["url"],
            item["scrip"],
        )

        self.cursor.execute(sql, data)
        self.connection.commit()

    def process_item(self, item, spider):
        self._store_db(item)
        return item
