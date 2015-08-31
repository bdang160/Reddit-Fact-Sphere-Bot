import praw
import time

#Fact Sphere

###TODO: Make it so it doesn't reply to its own replies


r = praw.Reddit(user_agent = "Fact Sphere Bot /u/azangi700")
print("Logging in...")
r.login("Fact_Sphere_Bot", "Portal1!")

COMPLETED_COMMENTS = "done.txt"
KEYFACTS = "FactSphereFactsKey.txt"
keywords = []
completed = []

with open("FactSphereKeyWords.txt", "r") as f:
    for line in f:
        keywords.append(line.strip())




# ### DOCUMENT READ FUNCTION ### #
def read_config_done():
    try:
        with open(COMPLETED_COMMENTS, "r") as f:
            for line in f:
                if line.strip() not in completed:
                    completed.append(line.strip())
    except OSError:
        print(COMPLETED_COMMENTS, "not found.")
    return completed
# ### END DOCUMENT READ FUNCTION ### #





completed = read_config_done()



# ### DOCUMENT WRITE FUNCTION ### #
def write_config_done(string_in):
    with open(COMPLETED_COMMENTS, "a") as f:
        f.write("\n")
        f.write(string_in + "\n")
# ### END DOCUMENT WRITE FUNCTION ### #




# ### PICKING WHICH FACT TO SAY ### #
def fact_return(keyword_in):
    if keyword_in == "":
        return "This is Fact_Sphere_Bot"
    else:
        with open(KEYFACTS, "r") as f:
            start_word = keyword_in + " "
            word = " " + keyword_in + " "
            end_word = " " + keyword_in
            for line in f:
                s = line.strip().lower()
                if s.find(word) > -1 or s.find(start_word) > -1 or s.find(end_word) > -1 or keyword_in == s:
                    return line.strip() 
# ### END PICKING WHICH FACT TO SAY ### #

# ### CHECK IF TEXT EQUALS KEYFACTS ### #
def check_text_equals_fact(string_in):
    with open(KEYFACTS, "r") as f:
        for line in f:
            if line.strip() == string_in:
                return False #Return false if comment equals a fact
        return True #Returns true, meaning the comment is Not Bot's Reply
# ### END FUCNTION ### #



# ### MAIN PROCEDURE ### #
def run_bot():
    print("Grabbing subreddit...")
    subreddit = r.get_subreddit("test")#Subreddit variable from subreddit 'test'
    print("Grabbing comments...")
    comments = subreddit.get_comments(limit = 10)
    for comment in comments: #for each comment in the 'comments' variable
        comment_text = comment.body.lower()#gets comment text and makes it all lowercase

        #Fix this part, make sure it doesn't detect its posted comments
        isMatch = any(string in comment_text for string in keywords)
        isNotBotReply = check_text_equals_fact(comment.body)
        
        if comment.id not in completed and isMatch and isNotBotReply:
            matchedWord = ""
            for string in keywords: #Finds the matching word in the comment text
                stringVar2 = string + " "
                stringVar3 = " " + string + " "
                stringVar4 = " " + string
                if string == comment_text or comment_text.find(stringVar2) > -1 or comment_text.find(stringVar3) > -1 or comment_text.find(stringVar4) > -1:
                    matchedWord = string

            
            print("Match found! Comment ID: " + comment.id)
            s = fact_return(matchedWord)
            if s == "This is Fact_Sphere_Bot":
                print("No Reply")
                write_config_done(comment.id)
            else:
                comment.reply(s) # Uses the match word in a function to find a related fact
                print("Reply successful")
                write_config_done(comment.id)
        print("Comments loop finished, time to sleep")
# ### END MAIN PROCEDURE ### #




# ### ACTUALLY RUNS BOT ### #
while True:
    run_bot()
    time.sleep(60)#In seconds, waits 10 seconds to run again
