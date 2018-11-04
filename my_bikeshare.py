import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see the data for Chicago, New York City or Washington? (default: NY) ").lower() or "new york city"
        if city in CITY_DATA:
            break
        else:
            print("Invalid input for city")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter month (all, january, february, ... , june) (default: all): ").lower() or "all"
        if month == 'all' or month in MONTHS:
            break
        else:
            print("Invalid input for month")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter day (all, monday, tuesday, ... sunday) (default: all): ").lower() or "all"
        if day == 'all' or day in DAYS:
            break
        else:
            print("Invalid input for day")

    print("")
    print("Filter by {}, month: {}, day: {}".format(city.title(), month.title(), day.title()))
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)+1
            
        # filter by month to create the new dataframe
        df = df[df['month']==month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    # prepare table for statistics
    df['hour'] = df['Start Time'].dt.hour
    df['Start-End']=df['Start-End']=df['Start Station']+" - "+df['End Station']


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_cnt = df['month'][df['month']==popular_month].count()
    print("Most popular month: {}   Count: {}".format(popular_month,popular_month_cnt))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    popular_day_cnt = df['day_of_week'][df['day_of_week']==popular_day].count()
    print("Most popular day of week: {}   Count: {}".format(popular_day, popular_day_cnt))


    # display the most common start hour
    popular_hour = df['hour'].value_counts()[:1].keys()[0]
    popular_hour_cnt = df['hour'][df['hour']==popular_hour].count()
    print("Most popular start hour: {}   Count: {}".format(popular_hour,popular_hour_cnt))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    cnt = df['Start Station'][df['Start Station']==start_station].count()
    print("Most popular start station: {}   Count: {}".format(start_station,cnt))


    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    cnt = df['End Station'][df['End Station']==end_station].count()
    print("Most popular end station: {}   Count: {}".format(end_station,cnt))


    # display most frequent combination of start station and end station trip
    start_end = df['Start-End'].mode()[0]
    cnt = df['Start-End'][df['Start-End']==start_end].count()
    print("Most popular route: {}   Count: {}".format(start_end,cnt))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_min = df['Trip Duration'].sum()
    total_h = total_min / 60
    total_days = total_h / 24
    print("Total travel time: {} minutes".format(total_min))
    print("     = {} hours".format(total_h))
    print("     = {} days".format(total_days))

    # display mean travel time
    print("Mean travel time: {} minutes".format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if "User Type" not in df.columns:
        print("No user data available")
    else:
    # Display counts of user types
        print("")
        print("User count per type:")
        type_cnt = df.groupby(['User Type'])['User Type'].count()
        for user_type in type_cnt.index:
            print("{}: {}".format(user_type,type_cnt[user_type]))

    # Display counts of gender
    if "Gender" not in df.columns:
        print("No gender data available")
    else:
        print("")
        print("User count per gender: ")
        gender_cnt=df.groupby(['Gender'])['Gender'].count()
        for gender in gender_cnt.index:
            print("{}: {}".format(gender,gender_cnt[gender]))


    # Display earliest, most recent, and most common year of birth
    if "Birth year" not in df.columns:
        print("No information about birth year available")
    else:
        print("")
        eldest_user = df['Birth Year'].min()
        print("Birth year of oldest user: {}".format(eldest_user))
        youngest_user = df['Birth Year'].max()
        print("Birth year of youngest user: {}".format(youngest_user))
        most_users = df['Birth Year'].mode()[0]
        print("Birth year of most users: {}".format(most_users))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def get_rows(df,start_row,number_of_rows):
    ''' 
    Args:
    (pandas.dataframe) df - dataframe to extract rows from
    (int) start_row - first row index of the data chunk to return
    (int) number_of_rows - length of the data chunk

    Returns:
    (pandas.dataframe) number_of_rows from df starting with start_row
    '''

    end_row=start_row+number_of_rows
    if end_row>len(df):
        end_row=len(df)
    return df[start_row:end_row]


def print_rows(df):
    ''' calls get_rows() as long as the user types 'y' or there are rows left to display '''

    row_no = 0    # start with 1st row
    chunk_len = 5

    # check if there are more rows left to print
    while row_no<len(df):
        chunk = get_rows(df,row_no,chunk_len)
        print(chunk.loc[:])     # prints records as a table
        # for ix in chunk.index:    # prints record values with 
        #     print(chunk.loc[ix])  #       columnnames as a series
        row_no += chunk_len
    
    # ask to display more rows or inform that the end of the dataset has been reached
        if row_no < len(df):
            show_rows = input('\nPrint {} more rows? Enter y or n:'.format(chunk_len)).strip().lower()
            if (show_rows != 'y'):
                break
        else:
            print('\nEnd of dataset reached')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_rows = input('\nWould you like to see the first 5 rows? Enter y or n: ').strip().lower()
        if show_rows != 'y':
            break
        else:
            print_rows(df)

        restart = input('\nWould you like to restart? Enter y or n.\n').strip().lower()
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
