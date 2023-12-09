
import mysql.connector
import pandas as pd
from tabulate import tabulate
from ES import ESearch
import time



class Sql:

    def __init__(self, user='root', password='emmerich0315', database='DatabaseFinal'):
        self.user = user
        self.password = password
        self.database = database
        self.es = ESearch()

        self.mydb = mysql.connector.connect(
            host="localhost",
            user=self.user,
            password=self.password,
            database=self.database
            )
        self.cursor = self.mydb.cursor()

    def search_tweet_from_username(self, user_name):
        query1 = f"SELECT user_id FROM user_information WHERE name = '{user_name}'"
        self.cursor.execute(query1)
        result = self.cursor.fetchone()
        if result:
            user_id = result[0]
            query2 = f"SELECT * FROM tweet_information WHERE user_id = '{user_id}'"
            record = pd.read_sql(query2, con=self.mydb)
            return record
        else:
            print(f"No user found with name = {user_name}")

    def search_tweet_from_tweetid(self, tweet_id):
        query = f"SELECT * FROM tweet_information WHERE tweet_id = '{tweet_id}'"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results_with_serial = [(i+1, *result) for i, result in enumerate(results)]
        headers = ["S.No", "Tweet ID", "USER ID", "Creat Time", "Retweet List", "Retweet"]
        print(tabulate(results_with_serial, headers=headers, tablefmt="pretty"))
        retweet = eval(results[0][3])
        return retweet
    
        # return a list of tweet id
    def search_tweet_from_userid(self, user_id):
        query = f"SELECT * FROM tweet_information WHERE user_id = '{user_id}' ORDER BY CONVERT_TZ(STR_TO_DATE(SUBSTR(created_at, 1, 20), '%a %b %d %H:%i:%s %Y'), SUBSTR(created_at, 21, 6), '+00:00') DESC LIMIT 5"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        tweet_ids = []
        results_with_serial = [(i+1, *result) for i, result in enumerate(results)]
        headers = ["S.No", "Tweet ID", "USER ID", "Creat Time", "Retweet List", "Retweet"]
        print(tabulate(results_with_serial, headers=headers, tablefmt="pretty"))
        for result in results:
            tweet_ids.append(result[0])
        return tweet_ids




    def search_user_from_tweetid(self, tweet_id):
        query1 = f"SELECT user_id FROM tweet_information WHERE tweet_id = '{tweet_id}'"
        self.cursor.execute(query1)
        result = self.cursor.fetchone()
        if result:
            user_id = result[0]
            query2 = f"SELECT * FROM user_information WHERE user_id = '{user_id}'"
            record = pd.read_sql(query2, con=self.mydb)
            return record
        else:
            print(f"No user found with tweet ID = {tweet_id}")

    # return a list of user id
    def search_user_from_username(self, user_name):
        query = f"SELECT * FROM user_information WHERE name = '{user_name}'"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        user_ids = []
        if results:
            results_with_serial = [(i+1, *result) for i, result in enumerate(results)]
            headers = ["S.No", "User ID", "Name", "Location", "URL", "User Popularity"]
            print(tabulate(results_with_serial, headers=headers, tablefmt="pretty"))
            for result in results:
                user_ids.append(result[0])
            return user_ids
        else:
            print(f"No record found with user name = {user_name}")

        


    def increment_user_popularity(self, user_id):
        query = f"UPDATE user_information SET user_popularity = user_popularity + 1 WHERE user_id = '{user_id}'"
        self.cursor.execute(query)
        self.mydb.commit()

    def set_user_popularity_zero(self):
        query = "UPDATE user_information SET user_popularity = 0"
        self.cursor.execute(query)
        self.mydb.commit()




    def search_top_users(self, top_n=10):
        query = f"SELECT * FROM user_information WHERE user_popularity > 0 ORDER BY user_popularity DESC LIMIT {top_n}"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        user_ids = []
        top_users = {}
        column_names = [column[0] for column in self.cursor.description]
        if results:
            top_users = {row[0]: dict(zip(column_names, row)) for row in results}
            results_with_serial = [(i+1, *result) for i, result in enumerate(results)]
            headers = ["S.No", "User ID", "Name", "Location", "URL", "User Popularity"]
            print(tabulate(results_with_serial, headers=headers, tablefmt="pretty"))
            for result in results:
                user_ids.append(result[0])
        return user_ids, top_users
    
    def search_top_users_noprint(self, top_n=10):
        query = f"SELECT * FROM user_information WHERE user_popularity > 0 ORDER BY user_popularity DESC LIMIT {top_n}"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        user_ids = []
        top_users = {}
        column_names = [column[0] for column in self.cursor.description]
        if results:
            top_users = {row[0]: dict(zip(column_names, row)) for row in results}
            for result in results:
                user_ids.append(result[0])
        return user_ids, top_users
    
        
        

    def search_top_tweets(self, top_n=10):
        query = f"SELECT ti.* FROM tweet_information ti JOIN tweet_popularity tp ON ti.tweet_id = tp.tweet_id ORDER BY tp.popularity DESC LIMIT {top_n}"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        tweeter_ids = []

        if results:
            results_with_serial = [(i+1, *result) for i, result in enumerate(results)]
            for result in results:
                tweeter_ids.append(result[0])

            data = [(index + 1, item, self.es.search_text_from_id(item)) for index, item in enumerate(tweeter_ids)]
            headers = ["S.No", "Tweet ID", "Text"]
            print(tabulate(data, headers=headers, tablefmt='pretty'))

        return tweeter_ids, results_with_serial
       

    

if __name__ == '__main__':
    sql = Sql()
    
    begin = time.time()
    sql.search_user_from_username('cheche')
    end = time.time()

    print(f"Time taken for the operation: {end - begin:.5f} seconds")

    


    
