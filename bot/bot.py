import requests
import logging
import random
import os

log = logging.getLogger()

def fetch_details(username):
  """
  Query db for bot details
  :param username: Username of bot
  """
  log.info('Fetching bot details')
  url = os.getenv('DB_URL') + '/bot/' + username
  r = requests.get(url)
  r.raise_for_status()
  return r.json()

def get_search_terms(political_ranking, other_terms_category):
  """
  Query db for search terms
  :param political_ranking: Stance of bot to get political terms
  :param other_terms_category: Demographic of bot
  """
  log.info('Fetching political search terms')
  url = os.getenv('DB_URL') + '/search_terms/political/' + str(political_ranking)
  r = requests.get(url)
  r.raise_for_status()
  search_terms = r.json()

  log.info('Fetching other search terms')
  url = os.getenv('DB_URL') + '/search_terms/other/' + str(other_terms_category)
  r = requests.get(url)
  r.raise_for_status()
  search_terms = search_terms + r.json()

  log.info('Shuffling terms')
  random.shuffle(search_terms)
  random.shuffle(search_terms)
  random.shuffle(search_terms)
  return search_terms[:int(os.getenv('NUM_TERMS'))]

class Bot:
  def __init__(self, username):
    log.info('Initialising bot ' + username)
    details = fetch_details(username)

    self.firstname = details['name'][0]
    self.lastname = details['name'][1]
    self.username = details['username']
    self.password = details['password']
    self.gender = details['gender']
    self.birthDay = details['DOB'][:2]
    self.birthMonth = details['DOB'][3:5]
    self.birthYear = details['DOB'][6:]
    self.politcalStance = details['political_ranking']
    self.profileBuilt = True
    self.zipcode = 91210    # TODO add zipcode to db
    self.position = {
      'lat': float(details['location']['latitude']),
      'lon': float(details['location']['longitude'])
    }
    self.search_terms = get_search_terms(details['political_ranking'], details['other_terms_category'])
    random.shuffle(self.search_terms)

  def getFirstname(self):
    return self.firstname

  def getLastname(self):
    return self.lastname

  def getUsername(self):
    return self.username

  def getPassword(self):
    return self.password

  def getGender(self):
    return self.gender

  def getBirthDay(self):
    return self.birthDay

  def getBirthMonth(self):
    return self.birthMonth

  def getBirthYear(self):
    return self.birthYear

  def getSearchTerms(self):
    return self.search_terms

  def getSearchTerm(self):
    return self.search_terms.pop()

  def getProfileBuilt(self):
    return self.profileBuilt

  def updateStatus(self, status):
    url = os.getenv('DB_URL') + '/bot_scheduler/update_status'
    r = requests.post(url, data={
      'username': self.username,
      'status': status
    })
    r.raise_for_status()