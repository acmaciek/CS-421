# Manuel Adrianzen and Maciej Girek
# CS 421 Natural Language Processing
# UIC Spring 2019

import sys
import sqlite3
import nltk.tokenize
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
# stanford NER
import nltk
from nltk import Tree
from nltk.tag.stanford import StanfordNERTagger

# Proper noun import details
import os

java_path = "C:/Program Files/Java/jdk1.8.0_161/bin/java.exe"
os.environ['JAVAHOME'] = java_path
jar = './stanford-ner.jar'

model = './english.all.3class.distsim.crf.ser.gz'

# Prepare NER tagger with english model
ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')


############################### NER

try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass

import os
from nltk.parse import stanford
from nltk.tag import StanfordPOSTagger

# break the sentence up into tokens and tags

##### CONVERT TO N
from nltk.corpus import wordnet as wn
querries = []

dictionaryAward = {
    # Music keywords
    'best movie': 'BEST-PICTURE',
    'best actor': 'BEST-ACTOR',
    'best actress': 'BEST-ACTRESS',
    'best film': 'BEST-PICTURE',
    'best supporting actress': 'BEST-SUPPORTING-ACTRESS',
    'best supporting actor': 'BEST-SUPPORTING-ACTOR',
    'best director': 'BEST-DIRECTOR',
}
nationality = {
    'French': 'France',
    'Italian': 'Italy',
    'German': 'Germany',
    'Spanish': 'Spain',
    'American': 'USA',
    'English': 'UK',
    'Canadian': 'Canada',

}
def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


def personDirector(person,conn): # QUERY TO CHECK IF SOMEONE IS A DIRECTOR
    yesOrNo = "NO";
    querry = "Select Count(*) FROM Person P INNER JOIN Director D ON P.id = director_id INNER JOIN Movie M ON M.id = movie_id WHERE P.name like '%"+person+"%'"
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for i in cursor:
        if((i[0]) > 0):
            yesOrNo = "Yes"
    return yesOrNo

def isMovieByDirector(director,movie,conn):
    yesOrNo = "NO";
    querry = "Select Count(*) FROM Movie M INNER JOIN  Director D ON D.movie_id = M.id INNER JOIN  Person P ON P.id = D.director_id WHERE P.name LIKE '%"+director+"%' AND M.name LIKE '%"+movie+"%'"
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for i in cursor:
        if((i[0]) > 0):
            yesOrNo = "Yes"
    return yesOrNo

def wasPersonBornInLocation(person,location,conn):
    yesOrNo = "NO";
    querry = "Select Count(*) FROM Person P WHERE P.name LIKE '%"+person+"%' AND P.pob LIKE '%"+location+"%'"
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for i in cursor:
        if((i[0]) > 0):
            yesOrNo = "Yes"
    return yesOrNo

def didMovieWinOscar(movie,oscar,conn):
    yesOrNo = "NO";
    querry = "Select Count(*) FROM Oscar O INNER JOIN  Movie M ON movie_id = M.id Where M.name like '%"+movie+"%' and O.type = '"+oscar+"'"
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for i in cursor:
        if((i[0]) > 0):
            yesOrNo = "Yes"
    return yesOrNo

def didActorStarInMovie(movie,name,conn):
    yesOrNo = "NO";
    querry = "Select Count(*) FROM Movie M INNER JOIN  Actor A ON A.movie_id = M.id INNER JOIN  Person P ON P.id = A.actor_id WHERE P.name LIKE '%"+name+"%' AND M.name LIKE '%"+movie+"%'"
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for i in cursor:
        if((i[0]) > 0):
            yesOrNo = "Yes"
    return yesOrNo

def didWinOscarInYear(year,name,conn):
    yesOrNo = "NO";
    querry = "Select Count(*) FROM Oscar O INNER JOIN  Person P ON person_id = O.person_id Where P.name like '%"+name+"%' and O.year = '"+year+"'"
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for i in cursor:
        if((i[0]) > 0):
            yesOrNo = "Yes"
    return yesOrNo

def didWinOscarFromCountryInYear(year,country,conn):
    yesOrNo = "NO";
    querry = "Select Count(*) FROM Actor A INNER JOIN Oscar O ON O.person_id = A.actor_id INNER JOIN  Person P ON P.id = A.actor_id WHERE O.year LIKE '%"+year+"%' AND P.pob LIKE '%"+country+"%'"
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for i in cursor:
        if((i[0]) > 0):
            yesOrNo = "Yes"
    return yesOrNo

def didMovieWithPersonWonOscar(oscar,name,conn):
    yesOrNo = "NO";
    querry = """select count(*)  from oscar
        inner join movie on movie.id = oscar.movie_id
        inner join actor on actor.movie_id = movie.id
        inner join person on person.id = actor.actor_id where oscar.type = '"""+oscar+"""' and person.name like '%"""+name+"""%'"""
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for i in cursor:
        if((i[0]) > 0):
            yesOrNo = "Yes"
    return yesOrNo

def whoDirectedMovie(movie,conn):
    yesOrNo = "NO";
    querry = """select person.name from person
        inner join director on person.id = director.director_id
        inner join movie on movie.id = director.movie_id
        where movie.name like '%"""+movie+"""%'"""
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for director in cursor:
        return director

def whoDirectedBestMovieInYear(oscar,year,conn):
    querry = """select person.name from director
        inner join person on person.id = director.director_id
        inner join oscar on oscar.person_id = person.id
        inner join movie on movie.id = oscar.movie_id
        where oscar.movie_id In (select movie_id from oscar
        where oscar.type like '"""+oscar+"""' and
            oscar.year = """+year+""")"""
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for director in cursor:
        return director

def whoDWonOscarInCategoryInYear(year,award,conn):
    querry = "select person.name from person inner join oscar on oscar.person_id = person.id inner join movie on movie.id = oscar.movie_id where oscar.year = "+year+" And oscar.type like '"+award+"'"
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for actor in cursor:
        return actor

def whoWonBestActressInYear(oscar,year,conn):
    querry = """select person.name from person
        inner join oscar on oscar.person_id = person.id
        inner join movie on movie.id = oscar.movie_id
        where oscar.movie_id In (select movie_id from oscar
        where oscar.year = """+year+""" and oscar.type like '"""+oscar+"""')"""
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for actress in cursor:
        return actress

def whichMovieWonOscarInYear(oscar,year,conn):
    querry = """select movie.name from oscar
        inner join movie on movie.id = oscar.movie_id
        where oscar.movie_id In (select movie_id from oscar
        where oscar.year = """+year+""") And oscar.type = '"""+oscar+"""'"""
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for movie in cursor:
        return movie

def whenPersonWonOscar(oscar,name,conn):
    querry = """select oscar.year from oscar
        inner join movie on movie.id = oscar.movie_id
        inner join person on person.id = oscar.person_id
        where oscar.movie_id In (select movie_id from oscar
        where oscar.type like '"""+oscar+"""')and
            person.name like '%"""+name+"""%'"""
    cursor = conn.execute(querry)
    print("<QUERRY>")
    print(querry)
    for year in cursor:
        return year


def ProperNounNER(word):
    words = nltk.word_tokenize(word)
    tupple = ner_tagger.tag(words)
    tag = tupple[0][1]
    return tag


def main():
    
    # Get sentences from input file
    with open('input2.txt', 'r') as f:
        data = [line.strip() for line in f]
    #POS tag sentences
    taggedSentences = []


    pattern = """NP: {(<DT>?<NNP>+<JJR>) | (<DT>?<NN>+<JJR>)  | (<DT>?<JJ>*<NN>)|(<DT>?<JJ>*<NNP>+) | (<DT>?<NN>+<JJS>) | (<DT>?<JJS><NN>+) | (<WDT>?<WRB>?<WP>?)}
        VBD: {<VBD>}
        PP: { <IN><NP> | <IN>}
        IN: {<IN>}
        VP: {<V> | <NP> | <PP> | <NP><PP>+ }"""
    questions = []
    for s in data:
        taggedSentences.append(nltk.pos_tag(nltk.word_tokenize(s)))
        questions.append(s)
    NounList = []
    categories = []
    answers = []
    tag = ""
    movie = ""
    place = ""
    productionYear = ""
    country = ""
    director = False
    movieBool = False
    actor = False
    personName = False
    movieName = False
    whenQuestion = False
    born = False
    location = False
    award = False
    movieAward = False
    oscarAward = False
    actress = False
    countryBool = False
    whQuestion = False
    questionCounter = 0;
    year = False
    awardString = ""
    for sentence in taggedSentences:
        print("<QUESTION> " + questions[questionCounter])
        questionCounter += 1
        name = ''
        for i,j in sentence:
            if(award):
                awardString = "best " + i
                award = False
                movieAward = True
            if( i == 'by'):
                tag = "director,"
                director = True
            if (j == 'JJS'):
                if(i == 'best'):
                    tag+="award"
                    award = True
            if(j == 'JJ'):
                if(ProperNounNER(i) == 'O'):
                    country =  nationality.get(i)
                    countryBool = True
            if( j == 'VBN'):
                if(i == "born"):
                    born = True
            if( j == 'CD'):
                year = True
                productionYear = i
            if( j == 'NN'):
                if(i == "director"):  #IS PERSON A DIRECTOR ?
                    tag+="director,"
                    director = True
                if(i == 'oscar'):
                    #                    tag = "oscar" # DOESNT WORK FOR FRENCH ACTOR WIN OSCAR
                    oscarAward = True
                if(i == 'movie'):
                    movieBool = True
                if(i == 'actress'):
                    actress = True
                elif (i == 'actor' or i == 'star'):    #IS PERSON AN ACTOR ?
                    tag="actor,"
                    actor = True
        
            if(j == 'VBD'):
                director = True
            if(j == 'WRB'):
                whenQuestion = True
            if(j == 'WP'):
                whQuestion = True
            if(j == 'JJ'):
                if(i[0] == 'W'):
                    whQuestion = True
            if (j == 'NNP'):
                if (i == "Birdman"):
                    movie+= "Birdman"
                    movieName = True
                if( ProperNounNER(i) != None):
                    if(ProperNounNER(i) == "O" and i != "Was" and i != "Did"):
                        movie = i #MIGHTY to get Aphrodite do += i and movie += " "
                        movieName = True
                    if(ProperNounNER(i) == "PERSON"):
                        name += i
                        personName = True
                    if(ProperNounNER(i) == "LOCATION"):
                        location = True
                        place += i
        oscar = dictionaryAward.get(awardString)
        conn = sqlite3.connect('oscar-movie_imdb.sqlite') #SQL QUERRIES
#        print("<QUESTION> " + questions[questionCounter])
        if(personName and movieAward and oscarAward and not whenQuestion):# YES IF A MOVIE WITH GIVEN ACTOR/ACTRESS WON AN OSCAR AWARD
            answer = (didMovieWithPersonWonOscar(oscar,name,conn))
            print("<ANSWER> " + answer)
            answers.append(answer)
        if(actor and oscarAward and year and countryBool and not whQuestion):# YES IF ACTOR OR ACTRESS FROM CERTAIN COUNTRY WON OSCAR IN A GIVEN YEAR
            answer = (didWinOscarFromCountryInYear(productionYear,country,conn))
            print("<ANSWER> " + answer)
            answers.append(answer)
        if(director and personName and not movieName and not whenQuestion): # YES IF SOMEONE IS A DIRECTOR
            answer = (personDirector(name,conn))
            print("<ANSWER> " + answer)
            answers.append(answer)
        if(director and personName and movieName and not whenQuestion): #YES IF A MOVIE WAS MADE BY THE DIRECTOR
            answer = (isMovieByDirector(name,movie,conn))
            print("<ANSWER> " + answer)
            answers.append(answer)
        if(personName and born and location and not whenQuestion): #YES IF PERSON BORN IN A LOCATION
            answer = (wasPersonBornInLocation(name,place,conn))
            print("<ANSWER> " + answer)
            answers.append(answer)
        if(year and movieName and movieAward and not whenQuestion): # YES IF MOVIE WON AN OSCAR
            answer = (didMovieWinOscar(movie,oscar,conn))
            print("<ANSWER> " + answer)
            answers.append(answer)
        if(personName and movieName and actor and not whenQuestion):# YES IF AN ACTOR STARRED IN A GIVEN MOVIE
            answer = (didActorStarInMovie(movie,name,conn))
            print("<ANSWER> " + answer)
            answers.append(answer)
        if(personName and year and oscarAward and not whenQuestion):# YES IF ACTOR WON OSCAR IN A GIVEN YEAR
            answer = (didWinOscarInYear(productionYear,name,conn))
            print("<ANSWER> " + answer)
            answers.append(answer)
        if(whenQuestion and personName and actress and oscarAward):
            answer = (whenPersonWonOscar(oscar,name,conn))
            print("<ANSWER> " + str(answer[0]))
            answers.append(answer[0])
        if(whQuestion and movieBool and oscarAward and year) :
            oscar = dictionaryAward.get('best movie')
            answer = (whichMovieWonOscarInYear(oscar,productionYear,conn))
            print("<ANSWER> " + answer[0])
            answers.append(answer[0])
        if(whQuestion and actress and year and oscarAward):
            oscar = dictionaryAward.get('best actress')
            answer = (whoWonBestActressInYear(oscar,productionYear,conn))
            print("<ANSWER> " + answer[0])
            answers.append(answer[0])
        if(whQuestion and director and year and movieAward and not actor):
            answer = (whoDirectedBestMovieInYear(oscar,productionYear,conn))
            print("<ANSWER> " + answer[0])
            answers.append(answer[0])
        if(whQuestion and movieAward and year and oscarAward and actor):
            answer = (whoDWonOscarInCategoryInYear(productionYear,oscar,conn))
            print("<ANSWER> " + answer[0])
            answers.append(answer[0])
        if(whQuestion and director and movieName):
            answer = (whoDirectedMovie(movie,conn))
            print("<ANSWER> " + answer[0])
            answers.append(answer[0])

        place = ''
        name = ''
        tag = ''
        movie = ''
        productionYear = ''
        awardString = ''
        country = ''
        director = False
        movieBool = False
        actor = False
        personName = False
        movieName = False
        whenQuestion = False
        born = False
        location = False
        award = False
        movieAward = False
        oscarAward = False
        actress = False
        countryBool = False
        whQuestion = False
        year = False



    conn.close()
    count = 0
#    print("PRINTING ANSWERS !!!!")
#    for i in answers:
#        print(i)
#    print("PRINTING QUERRIES !!!!")
#    for i in querries:
#        print(i)
#    for q in questions: # PRINT QUESTIONS AND ANSWERS
#        print("<QUESTION> "+q)
#        print("<QUERRY>")
#        print()
#        print("<ANSWER> "+answer[count])
#        print()
#        count += 1

main()


