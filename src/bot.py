class Bot:
  def __init__(self, firstname, lastname, username, password, gender, birthDay, birthMonth, birthYear, politicalStance, profileBuilt):
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
    self.search_terms = ''
    self.profileBuilt = profileBuilt

  def getFirstname(self):
    return bot.firstname

  def getLastname(self):
    return bot.lastname

  def getUsername(self):
    return bot.username

  def getPassword(self):
    return bot.password

  def getGender(self):
    return bot.gender

  def getBirthDay(self):
    return bot.birthDay

  def getBirthMonth(self):
    return bot.birthMonth

  def getBirthYear(self):
    return bot.birthYear

  def setSearchTerms(self):
    self.search_terms = 'Trump'

  def getSearchTerms(self):
    return self.search_terms

  def getProfileBuilt(self):
    return self.profileBuilt
