from Cache import Cache
from ES import ESearch
from MySQL import Sql
from tabulate import tabulate

    
if __name__ == '__main__':

    cache = Cache(20)
    sql = Sql()
    es = ESearch()

    cache.update()
    cache.write_to_file()

    print('Welcome to the search application designed by Team 15\n')

    flag = True 

    while flag:
        
        print('Please select one of the following four options for searching\n')

        print('1. tweet')
        print('2. user')
        print('3. Top ten tweets')
        print('4. Top ten users\n')

        option = input('Please enter a single number between 1 and 4: ')
        print('')

        if option == '1':

            text = input('Please enter the text you want to search: ')
            print('')

            id_list = es.text_search(text)

            print('')
            print('If you want to know about the tweet, Please enter the number before ID')
            print('If you want to search for other informations, Please enter "C"')
            print('If you want to quit, please enter "Q"\n')

            option2 = input("Please enter 'C', 'Q' and an integer between 0 to 4: ")
            print('')

            if option2 == 'Q':
                print('Thanks for your use')
                flag = False

            elif option2 == 'C':
                continue

            else:
                try:
                    num = int(option2)
                    if 0 <= num <= 4:
                        record = sql.search_tweet_from_tweetid(id_list[num])

                        print('')
                        print('If you want to check the retweet, Please enter "R"')
                        print('If you want to search for other informations, Please enter "C"\n')

                        option3 = input("Please enter 'R' for retweet, 'C' for continue, others for quit: ")
                        print('')

                        if option3 == 'R':
                            if record:
                                data = [(index + 1, item, es.search_text_from_id(item)) for index, item in enumerate(record)]
                                headers = ["S.No", "Tweet ID", "Text"]
                                print(tabulate(data, headers=headers, tablefmt='pretty'))
                            else:
                                print('There is no retweet for this tweet.')

                            print('')
                            print('If you want to search for other informations, Please enter "C"\n')

                            option4 = input("Please enter 'C' for continue, others for quit: ")
                            print('')

                            if option4 == 'C':
                                continue

                            else:
                                print('Thanks for your use')
                                flag = False

                        elif option3 == 'C':
                            continue

                        else:
                            print('Thanks for your use')
                            flag = False

                    else:
                        raise ValueError("Invalid input. Please enter 'Q', 'C', or an integer between 0 and 4.")
                    
                except ValueError:
                    raise ValueError("Invalid input. Please enter 'Q', 'C', or an integer between 0 and 4.")
                
        elif option == '2':

            user = input('Please enter the user you want to search: ')
            print('')

            user_ids = cache.search(user)
            if user_ids:
                pass               
            else:
                user_ids = sql.search_user_from_username(user)

            num_id = len(user_ids)

            print('')
            print('If you want to search for the tweets the user posted, you can enter the corresponding number before the user id')
            print('If you want to search for other informations, Please enter "C"')
            print('If you want to quit, please enter "Q"\n')
            
            option2 = input(f"Please enter 'C', 'Q' and an integer between 1 to {num_id}: ")
            print('')

            if option2 == 'Q':
                print('Thanks for your use')
                flag = False

            elif option2 == 'C':
                continue

            else:
                try:
                    num = int(option2)
                    if 1 <= num <= num_id:
                        record = sql.search_tweet_from_userid(user_ids[num-1])
                        sql.increment_user_popularity(user_ids[num-1])

                        print('')
                        print('If you want to search for other informations, Please enter "C"\n')


                        option3 = input("Enter 'C' for continue, others for quit: ")
                        print('')

                        if option3 == 'C':
                            continue

                        else:
                            print('Thanks for your use')
                            flag = False

                    else:
                        raise ValueError(f"Invalid input. Please enter 'Q', 'C', or an integer between 1 and {num_id}.")
                    
                except ValueError:
                    raise ValueError(f"Invalid input. Please enter 'Q', 'C', or an integer between 1 and {num_id}.")

        elif option == '3':

            tweet = sql.search_top_tweets()[1]

            print('')
            print('If you want to search for the infomation of a tweet, Please enter the corresponding number before the user id')
            print('If you want to search for other informations, Please enter "C"')
            print('If you want to quit, please enter "Q"\n')
            
            option2 = input(f"Please enter 'C', 'Q' and an integer between 1 to 10: ")
            print('')

            if option2 == 'Q':
                print('Thanks for your use')
                flag = False

            elif option2 == 'C':
                continue

            else:
                try:
                    num = int(option2)
                    if 1 <= num <= 10:
                        headers = ["S.No", "Tweet ID", "User ID", "Created Time", "Retweet List", "Retweeted"]
                        record = [tweet[num-1]]
                        print(tabulate(record, headers=headers, tablefmt="pretty"))
                        

                        print('')
                        print('If you want to search for other informations, Please enter "C"\n')


                        option3 = input("Enter 'C' for continue, others for quit: ")
                        print('')

                        if option3 == 'C':
                            continue

                        else:
                            print('Thanks for your use')
                            flag = False

                    else:
                        raise ValueError(f"Invalid input. Please enter 'Q', 'C', or an integer between 1 and {num_id}.")
                    
                except ValueError:
                    raise ValueError(f"Invalid input. Please enter 'Q', 'C', or an integer between 1 and {num_id}.")

        elif option == '4':

            user_ids = sql.search_top_users()[0]

            num_id = len(user_ids)

            print('')
            print('If you want to search for the tweets the user posted, you can enter the corresponding number before the user id')
            print('If you want to search for other informations, Please enter "C"')
            print('If you want to quit, please enter "Q"\n')
            
            option2 = input(f"Please enter 'C', 'Q' and an integer between 1 to {num_id}: ")
            print('')

            if option2 == 'Q':
                print('Thanks for your use')
                flag = False

            elif option2 == 'C':
                continue

            else:
                try:
                    num = int(option2)
                    if 1 <= num <= num_id:
                        record = sql.search_tweet_from_userid(user_ids[num-1])
                        sql.increment_user_popularity(user_ids[num-1])

                        print('')
                        print('If you want to search for other informations, Please enter "C"\n')


                        option3 = input("Enter 'C' for continue, others for quit: ")
                        print('')

                        if option3 == 'C':
                            continue

                        else:
                            print('Thanks for your use')
                            flag = False

                    else:
                        raise ValueError(f"Invalid input. Please enter 'Q', 'C', or an integer between 1 and {num_id}.")
                    
                except ValueError:
                    raise ValueError(f"Invalid input. Please enter 'Q', 'C', or an integer between 1 and {num_id}.")

        else:
            raise ValueError("Invalid input. Please enter an integer between 0 and 4.")


                
                
                

           

            



    









