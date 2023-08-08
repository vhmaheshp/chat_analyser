from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_active_users(df):

    df=df[df['user']!="group_notification"]
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index':'S.No.','user': 'name', 'count': 'percent'})
    return x,df


def most_used_words(selected_user,df):

    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    new_df=df[df['user']!="group_notification"]
    new_df=new_df[new_df['message']!="<Media omitted>\n"]
    new_df=new_df[new_df['message']!="This message was deleted\n"]
    new_df=new_df[new_df['message']!="You deleted this message\n"]
    new_df=new_df[new_df['message']!="Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.\n"]
    
    words = []

    for message in new_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    df_1=pd.DataFrame(Counter(words).most_common(20))

    string=" ".join(words)
    wc=WordCloud(width=500,height=500,min_font_size=6)
    df_wc=wc.generate(str(string))
    
    return df_1,df_wc

def monthly_timeline(selected_user,df):

    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    timeline= df.groupby(['year','month','month_num']).count()['message'].reset_index()
    
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+", "+ str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):

    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    timeline= df.groupby(['only_date']).count()['message'].reset_index()
    return timeline

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def emoji_counter(selected_user,df):

    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    count=0
    emojis=[]
    for message in df['message']:
        for c in message:
            if c in emoji.UNICODE_EMOJI['en']:
                count+=1
                emojis.extend(c)
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),columns=['Emoji','Count'])

    return emoji_df,count

def most_emoji_user(text):

    emoji_count = 0
    for character in text:
        if character in emoji.UNICODE_EMOJI['en']:
            emoji_count += 1
    return emoji_count
