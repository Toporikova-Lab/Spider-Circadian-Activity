#Creating a list of dataframes which splits each day into its own dataframe
list_of_days = df['Date'].unique()
def create_list_of_df(list_of_days):
    list_of_df = []
    for x in range(len(list_of_days)):
        list_of_df.append(df[df.Date==str(list_of_days[x])])
    return(list_of_df)

#Drop days that are in DD
def drop_dd_days(df):
    list_of_df = create_list_of_df(list_of_days)
    for i in list_of_df:
        for x in i['Date']:
            lights = (i['lights'].value_counts()[0] == len(i.index))
            if lights == True:
                df.drop(df[df['Date'] == x].index, inplace = True)

#Create LD DataFrame
def create_ld(df, list_of_days):
    create_list_of_df(list_of_days)
    drop_dd_days(df)

#For flattening a list of lists:
def flatten_list(list1):
    flat_list = []
    
    # Iterate through the outer list
    for element in list1:
        if type(element) is list:
            
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

#for adding minutes to a dataframe:
def add_minutes(df):
    
    #Create nested list containing the total number of minutes in each day with the length of the number of days
    total_minutes = []
    minutes = np.arange(1,1441).tolist()
    num_days = len(pd.unique(df['Date']).tolist())
    total_minutes.extend([minutes for i in range(num_days)])
    
    #create new list with the total number of minutes in a day multiplied by the number of full days
    total_minutes_list = flatten_list(total_minutes)
    
    #append the flattened list to the original dataframe
    df['Total Minutes'] = total_minutes_list

#for dropping incomplete days
def drop_incomplete(df):
    minutes_in_day = 24*60
    all_days = df.Date.unique()
    #loop through minutes in day, drop the date from original dataframe when the number of values for that day doesnt equal minute in day
    for i in all_days:
        minutes = (sum(df.Date == i) == minutes_in_day)
        if minutes == False:
            df.drop(df[df['Date'] == i].index, inplace = True)
            
#For adding the rolling average of activity for a single spider
def add_rolling_single_spider(df):
    #calculate rolling average of dataframe
    activ = df.s2
    rolling = activ.rolling(30).mean().dropna()

    #Add new column to dataframe with the rolling mean
    df['Rolling'] = rolling

#For adding the rolling average of activity for multiple spiders; need to use for loop
def add_rolling_multiple_spiders(df):
    #calculate rolling average of dataframe
    activ = df.iloc[: , 0]
    rolling = activ.rolling(30).mean().dropna()

    #Add new column to dataframe with the rolling mean
    df['Rolling'] = rolling