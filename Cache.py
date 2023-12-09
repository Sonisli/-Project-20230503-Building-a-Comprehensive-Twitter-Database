import json
from datetime import datetime
from tabulate import tabulate
from MySQL import Sql
from datetime import datetime
import time

class Cache:

    def __init__(self, capacity=20):
        self.capacity = capacity

        with open('Cache.json', 'r') as f:
            self.dictionary = json.load(f)
        
        self.sql = Sql()
    
    def update(self):
        user_dict = self.sql.search_top_users_noprint()[1]
        for key in user_dict:
            user_dict[key]['time'] = datetime.now()
            self.dictionary[key] = user_dict[key]
        self.drop_to_capacity()


    def search(self, username):
        user_ids = []
        for key in self.dictionary:
            if self.dictionary[key]['name'] == username:
                results = self.dictionary[key]
                result_no = {'no': 1}
                result_no.update(results)
                headers = ["S.No", "User ID", "Name", "Location", "URL", "User Popularity"]
                filtered_results = {k: v for k, v in result_no.items() if k != 'time'}
                filtered_results_list = [list(filtered_results.values())]
                print(tabulate(filtered_results_list, headers=headers, tablefmt="pretty"))
                user_ids.append(self.dictionary[key]['user_id'])
        return user_ids
        

    def write_to_file(self):
        for user_id, user_info in self.dictionary.items():
            if 'time' in user_info and isinstance(user_info['time'], datetime):
                user_info['time'] = user_info['time'].strftime('%Y-%m-%d %H:%M:%S')
        with open('Cache.json', 'w') as f:
            json.dump(self.dictionary, f)


    def drop_to_capacity(self):
        while len(self.dictionary) > self.capacity:
            earliest_key = min(self.dictionary, key=lambda k: (self.dictionary[k]['time']))
            del self.dictionary[earliest_key]






if __name__ == '__main__':
    cache = Cache(20)

    begin = time.time()
    cache.search('linda')
    end = time.time()

    print(f"Time taken for the operation: {end - begin:.5f} seconds")




    