"""
This module handles the downloading and parsing of political and other search
terms for bot rankings. This information is in a structured format to be
rendered in HTML.

Last updated: MB 21/09/2020 - create module.
"""
# import external libraries.
from threading import Thread

# import local modules.
from src import db_controller, cache_handler

"""
This function will update the cached political search term dictionary. Each key
in the dictionary is a political ranking and the corresponding value is a list
of political search terms.
"""
def update_political_cache():
    # clear the currently cached list of political search terms.
    cache_handler.political_search_term_dict.clear()

    # empty list of threads.
    threads = []

    # in threads, save search terms for each political ranking.
    for ranking in range(0, 5):
        # create thread and start.
        thread = Thread(target=db_controller.save_political_search_terms, args=[ranking])
        thread.start()

        # save thread to list.
        threads.append(thread)

    # wait for each thread to finish.
    for thread in threads:
        thread.join()

"""
This function will update the cached other search term dictionary. Each key
in the dictionary is an other ranking and the corresponding value is a list
of political search terms.
"""
def update_other_cache():
    # clear the currently cached list of political search terms.
    cache_handler.other_search_term_dict.clear()

    # empty list of threads.
    threads = []

    # in threads, save search terms for each other ranking.
    for ranking in range(0, 7):
        # create thread and start.
        thread = Thread(target=db_controller.save_other_search_terms, args=[ranking])
        thread.start()

        # save thread to list.
        threads.append(thread)

    # wait for each thread to finish.
    for thread in threads:
        thread.join()
