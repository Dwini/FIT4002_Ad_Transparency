class Bot:
  def __init__(self, firstname, lastname, username, password, gender, birthDay, birthMonth, birthYear, politicalStance, search_terms, profileBuilt, zipcode):
    self.firstname = firstname
    self.lastname = lastname
    self.username = username
    self.password = password
    self.gender = gender
    self.birthDay = birthDay
    self.birthMonth = birthMonth
    self.birthYear = birthYear
    # TODO create db of political terms and then when creating bots set a political stance
    self.politcalStance = politicalStance
    self.search_terms = search_terms
    self.profileBuilt = profileBuilt
    # TODO add zipcode to db
    self.zipcode = zipcode

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

  def setSearchTerms(self):
    self.search_terms = 'Trump'

  def getSearchTerms(self):
    return self.search_terms

  def getProfileBuilt(self):
    return self.profileBuilt
