import re
import pandas as pd
from RegexGenerator import RegexGenerator
def preprocess(data):

    myRegexGenerator = RegexGenerator(data.split("-")[0])
    pattern = myRegexGenerator.get_regex()

    messages = re.split(pattern, data)[1:]
    messages_new=[]
    for message in messages:
        messages_new.append(message.strip("- "))
    
    dates = re.findall(pattern, data)
    dates_new=[]
    for date in dates:
        dates_new.append(date.strip("- "))

    df = pd.DataFrame({'user_message': messages_new, 'message_date': dates_new})
    
    try:
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M')
    except:
        try:
            df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p')
        except:
            try:
                df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M')
            except:
                df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%Y, %I:%M %p')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    
    return df
