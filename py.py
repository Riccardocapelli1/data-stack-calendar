import tweepy
import pandas as pd

# Autenticazione con le tue chiavi di Twitter
consumer_key = 'Goowh3AzIK9PpTUpdpnrAQGYp'
consumer_secret = 'lV0eGyTUJjcSPYLIPJZk2cg1x6MCZjmazXdsolJPMB4R7VSRaQ'
access_token = '1607466746612531206-qJ3L9tuG9RDyey0E71ZVkiAboGdZ2M'
access_token_secret = 'y0Irfmbpt8cJFbGY9LEcnVevVWdfzIqpjdbG0ChSawrei'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Crea una lista dei profili di cui vuoi scaricare i tweet
profiles = ["airflow", "getdbt", "dbt_labs","tableau","microsoft","apachesuperset"]

# Crea una lista vuota per i tweet
tweets = []

# Scarica i tweet dei profili specificati
for profile in profiles:
    for tweet in api.user_timeline(screen_name=profile, count=20, include_rts=False, tweet_mode="extended"):
        tweets.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])

# Crea un dataframe dei tweet scaricati
df = pd.DataFrame(tweets, columns=['Time', 'User', 'Tweet'])

# Filtra il dataframe per i tweet che contengono le parole "event" o "conference" nel testo
df = df[df['Tweet'].str.contains('event|conference')]

# Crea una stringa vuota per il contenuto del file HTML
html_content = ""

# Aggiungi il contenuto iniziale del file HTML
html_content  = "<!DOCTYPE html>\n"
html_content += "<html>\n"
html_content += "<head>\n"
html_content += "  <link rel='stylesheet' type='text/css' href='assets/style.css'>\n"
html_content += "  <script src='assets/script.js'></script>\n"
html_content += "  <title>Modern-data-stack events and conferences for the analytics community</title>\n"
html_content += "</head>\n"
html_content += "<body>\n"
html_content += "  <h1>Events and conferences list updated every 24H</h1>\n"
html_content += "  <p>A modern data stack calendar aggregating events and conferences from Twitter for data engineers, analytics engineers and data analysts.</p>\n"

for _, row in df.iterrows():
        user = row["User"]
        date = row["Time"]
        text = row["Tweet"]
        
        html_content += f"  <h2>{user} date: {date}</h2>\n"
        html_content += f"  <p>{text}</p>\n"

html_content += "</body>\n"
html_content += "</html>\n"

with open("./index.html", "w") as f:
    f.write(html_content)
