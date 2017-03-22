from vgc.models import UserProfile , Character, VideoGame , Rating, ListElement
import operator
from math import *
from string import punctuation
import re


#characters = recommends(UserProfile.objects.get(user=request.user.id))
#this list needs culling to x results, but is already sorted. It's also completely redundant.
def recommends(User):
    userCoeffs = getSimilarUsers(User)
    characterCoeffs = getCharacters(userCoeffs)
    return sortCharacters(characterCoeffs, User)
    
#presently has a bias towards a greater number of ratings
def getSimilarUsers(User):
    userList = {}
    ratings = Rating.objects.all().filter(user = User)
    for r in ratings:
        altUsersRatings = Rating.objects.all().filter(character = r.character)
        for u in altUsersRatings:
            coeff = 100-fabs(r.rating-Rating.objects.get(character = r.character, user = u.user).rating)
            if u.user in userList.keys():
                userList[u.user] = userList[u.user] + coeff
            else:
                userList[u.user] = coeff
    return userList
    
def getCharacters(userCoeffs):
    characterCoeffs = {}
    for u in userCoeffs.keys():
        ratings = Rating.objects.all().filter(user = u)
        for r in ratings:
            if r.character in characterCoeffs.keys():
                characterCoeffs[r.character] = characterCoeffs[r.character] + r.rating*userCoeffs[u]
            else:
                characterCoeffs[r.character] = r.rating*userCoeffs[u]
    return characterCoeffs
    
def sortCharacters(characterCoeffs, User):
    exclusions = Rating.objects.all().filter(user = User)
    for exc in exclusions:
        if exc.character in characterCoeffs.keys():
            characterCoeffs[exc.character] = None
    sortedList = sorted(characterCoeffs.items(), key=operator.itemgetter(1), reverse = True)
    return sortedList

#searchCharacters("Lieutenant in 2186")
#this list needs culling to x results, but is already sorted. It's also completely redundant.
def searchCharacters(str):
    baseTerms = cleanUp(str).split()
    if(len(baseTerms)>8):
        baseTerms = baseTerms[:8]
    searchTerms = []
    for t in baseTerms:
        for i in range(len(t)):
            front = t[:i]
            rear = t[i:]
            if(len(front)>3):
                searchTerms = searchTerms + [front]
            if(len(rear)>3):
                searchTerms = searchTerms + [rear]
    #generate a set of alternate half-words; ideally this catches most root words
    #purposefully ignores halfwords shorter than 4 characters
    #this is a shortcut to replace proper fuzzy patternmatching
                
    characters = Character.objects.all()
    coeffs = {}
    for c in characters:
        name = cleanUp(c.name)
        desc = cleanUp(c.bio)
        game = cleanUp(c.videogame.name)
        v = 0.0
        for t in searchTerms:
            v = v+measureSimilarty(t, desc)+8*measureSimilarty(t, name)+4*measureSimilarty(t, name)
            #these are arbitrary weightings
        coeffs[c] = v;
    return sorted(coeffs.items(), key=operator.itemgetter(1), reverse = True)

    
def measureSimilarty(key, passage):
    return passage.count(key)*len(key)/sqrt(1.0*len(passage))
    #to improve
    
def cleanUp(str):
    return re.sub(r'[^\w\s]','',str).lower()