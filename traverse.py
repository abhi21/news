from queue import Queue
import newspaper
from newspaper import Article
import datetime

unvisited_articles = Queue()
visited_articles = set()

c = 0

seed_article1 = "http://www.cnn.com/2015/05/21/us/texas-joshua-chari-teen-with-eight-degrees/?iid=ob_article_topstories_pool&iref=obnetwork"
seed_article2 = "http://www.cnn.com/2015/05/03/europe/new-british-princess-meets-relatives/?iid=ob_article_footer_expansion&iref=obnetwork"
seed_article3 = "http://www.cnn.com/2015/05/22/politics/mccain-obama-isis-mind-boggling/index.html"
seed_article4 = "http://www.cnn.com/2015/05/22/politics/patriot-act-debate-explainer-nsa/index.html"
seed_article5 = "http://www.cnn.com/2015/05/22/europe/ireland-referendum-same-sex-marriage/index.html"
seed_article6 = "http://www.cnn.com/2015/05/21/health/white-helmets-profile/index.html"
seed_article7 = "http://www.cnn.com/2015/05/21/entertainment/david-letterman-reaction-feat/index.html"
seed_article8 = "http://www.cnn.com/2015/05/22/living/beach-read-queens-feat/index.html"

unvisited_articles.put(seed_article1)
unvisited_articles.put(seed_article2)
unvisited_articles.put(seed_article3)
unvisited_articles.put(seed_article4)
unvisited_articles.put(seed_article5)
unvisited_articles.put(seed_article6)
unvisited_articles.put(seed_article7)
unvisited_articles.put(seed_article8)

non_controversial = {"60s", "70s", "addition", "address", "afternoon", "agreed", "amp", "angeles","answer", "april", "attention", "avenue", "average", "ball", "base", "bay", "beach", "beginning", "bit","block", "blue", "bowl", "box", "boy", "boys", "brother", "building", "bus", "call", "calling", "calls", "camp", "car", "cars", "central", "cents", "click", "close", "cloudy", "club", "coast", "cup", "dallas", "date", "daughter", "davis", "day", "decade", "decades", "december", "def", "delivery", "door", "download", "drive", "eagles","end", "entire", "era", "evening", "face", "faces", "facility", "fall", "fans", "father", "feel", "feeling", "feet", "fell","field", "finish", "floor", "form", "fort", "francisco", "friday", "friend", "friends", "fun", "girl", "girls", "ground","gt", "guy", "guys", "half", "hall", "hand", "hands", "hawaii", "heart", "heat", "heavy", "hill", "hits", "hold", "hopes","host", "hotel", "hour", "hours", "house", "houston", "hundreds", "husband", "ice", "illinois", "index", "indiana","innings", "island", "january", "johnson", "jones", "june", "kansas", "kind", "lack", "lake", "leave","lee", "letter", "levels", "light", "line", "lines", "lot", "lows", "lt", "main", "make", "makes", "mark", "mass", "material","matter", "medium", "men", "mid", "middle", "miles", "mind", "minneapolis", "minutes", "moment","monday", "month", "months", "morning", "mother", "mountain", "move", "mph", "museum", "names","natural", "net", "night", "north", "note", "notes", "november", "october", "opening", "park", "part", "parts","pass", "period", "person", "philadelphia", "pick", "pitch", "plant", "play", "player", "playing", "pm", "point","post", "practice", "put", "quarter", "rain", "read", "reading", "red", "rest", "restaurant", "rise", "rock", "rose","round", "sale", "san", "saturday", "scene", "search", "season", "seasons", "seconds", "selling", "september","series", "set", "showers", "showing", "shows", "sign", "signs", "smith", "son", "sox", "special", "spot","spring", "square", "stadium", "stage", "start", "starting", "starts", "station", "stay", "step", "stores", "street","student", "summer", "sun", "sunday", "thing", "things", "thinking", "thought", "thousands", "thunderstorms","thursday", "time", "title", "top", "total", "transportation", "type", "unit", "valley", "vehicle", "version","village", "visit", "wait", "walk", "wall", "watch", "water", "ways", "wednesday", "week", "weekend","weeks", "williams", "wind", "winds", "winner", "winter", "word", "writer", "yards", "year", "years", "york"}

nc_set = set(non_controversial)

contorversial = {"Abortion", "Animal rights","Border Fence","Civil Unions","Environmental Protection","European Union","Federal Reserve","Free Trade","Gold Standard","Homeschooling","Medical Marijuana,'Minimum Wage","Progressive Tax","Redistribution","Social Programs","Socialism","Term Limits","United Nations","War on Terror","Affirmative Action","Barack Obama","Capitalism","Death Penalty","Electoral College","Estate Tax","Euthanasia","Flat Tax","Gay Marriage","Globalization","Gun Rights","Labor Union","Military Intervention","National Health Care","Occupy Movement","Racial Profiling","Social Security","Torture","War in Afghanistan","Welfare"}

contorversial_set = set(contorversial)


main_file = open("news_data_CNN.txt", "a")
visited_file = open("visited_urls"+str(datetime.datetime.now()).replace(" ","_").replace(".","_").replace(":","")+".txt", "a")

def is_valid_article(link):
    print("Checking valid:\n" + link)

    if "cnn.com" not in link:
        return False
    if "html" not in link:
        return False
    article = Article(link)
    article.download()
    article.parse()
    article.nlp()
    keywords = article.keywords

    matched = False

    for key in keywords:
        if key in nc_set:
            matched = True
    for key in keywords:
        if key in contorversial_set:
            matched = False

    if matched & (len(article.authors) > 0) & (article.publish_date < datetime.datetime(2007, 12, 30, 0, 0)):
        main_file.write(article.title+"\t\t"+article.keywords+"\t\t"+link+"\t\t"+article.text+"\n")
        visited_articles.write(link+"\n")
        return True

    return False

while unvisited_articles.qsize() > 0:
    print("Item form queue dequeued \n")
    url = unvisited_articles.get()
    outlinks = newspaper.build(url)

    for outlink in outlinks.articles:
        unvisited_articles.put(outlink.url)
    #print(url)
    if is_valid_article(url) & (url not in visited_articles):
        print("Found valid url\n")
        visited_articles.add(url)
        print("Links Visited So far: "+c)
