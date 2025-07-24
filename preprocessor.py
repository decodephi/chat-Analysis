import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    sms = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    df = pd.DataFrame({
    'User_Text': sms,
    'Text_date':dates
    })

    df['Text_date'] = pd.to_datetime(df['Text_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns= {'Text_date': 'date'}, inplace=True)
     
    users =[]
    messages =  []
    for message in df['User_Text']:
     entry = re.split('([\w\W]+?):\s', message, maxsplit=1)
     if entry[1:]:
      users.append(entry[1])
      messages.append(entry[2])
     else:
      users.append('group_notification')
      messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns = ['User_Text'], inplace = True) 
    
    
    df['year']= df['date'].dt.year
    df['Month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    
    period = []
    for hour in df[['day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
