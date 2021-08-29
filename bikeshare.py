import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)    
    while True:
        try:
            city = input("Select a city to explore: Chicago, New York City or Washington\n").lower()
            err_check = CITY_DATA[city]
            break
        except:
            print("{} is not a valid city.\n".format(city.title()))
    
    # get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to filter by: January, February, March, April, May, June? Enter 'All' to view all months\n").lower()
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    # check if input is valid
    while month not in valid_months:
        print("{} is not a valid month.\n".format(month.title()))
        month = input("Which month would you like to filter by: January, February, March, April, May, June? Enter 'All' to view all months\n").lower()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Would you like to filter by day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday? Enter 'All' to view all days\n").lower()
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    # check if input is valid
    while day not in valid_days:
        print("{} is not a valid day.\n".format(day.title()))
        day = input("Would you like to filter by day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday? Enter 'All' to view all days\n").lower()
    
    print("Thank you! You have chosen to explore data for city: {}, month: {}, day: {}\n".format(city.title(), month.title(), day.title()))
    
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
    # convert inputs to lowercase for consistency
    city = city.lower()
    month = month.lower()
    day = day.lower()
    
    df = pd.read_csv(CITY_DATA[city])
    
    # convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day name from Start Time
    df['Start Month'] = df['Start Time'].dt.month
    df['Start Day'] = df['Start Time'].dt.weekday_name
    
    # apply month filter
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
            
        # create a new column for the selected month
        df = df.loc[df['Start Month'] == month]
       
    # apply day filter
    if day != 'all':
        # create a new column for the selected day
        df = df.loc[df['Start Day'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # map numerical month to a month name
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    max_month = months[df['Start Month'].value_counts().idxmax()-1]
    print("The most common month is {} with {} trips".format(max_month, df['Start Month'].value_counts().max()))
    
    # display the most common day of week
    print("The most common day is {} with {} trips".format(df['Start Day'].value_counts().idxmax(), df['Start Day'].value_counts().max()))
    
    # display the most common start hour
    # extract hour from the Start Time
    df['Start Hour'] = df['Start Time'].dt.hour
    print("The most common hour is {} with {} trips".format(df['Start Hour'].value_counts().idxmax(), df['Start Hour'].value_counts().max()))

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station    
    print("{} was the most popular Start Station. It was used {} times".format(df['Start Station'].value_counts().idxmax(), df['Start Station'].value_counts().max()))
    
    # display most commonly used end station
    print("{} was the most popular End Station. It was used {} times".format(df['End Station'].value_counts().idxmax(), df['End Station'].value_counts().max()))
    
    # display most frequent combination of start station and end station trip
    max_start_end = df.groupby(['Start Station', 'End Station'], as_index = 'false')['Start Station'].count().idxmax()
    max_start_end_count = df.groupby(['Start Station', 'End Station'], as_index = 'false')['Start Station'].count().max()
    print("The most popular Start & End Station combination was {} with {} trips".format(max_start_end, max_start_end_count))

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time was {} seconds".format(df['Trip Duration'].sum()))
    
    # display mean travel time
    print("The mean travel time was {} seconds".format(df['Trip Duration'].mean()))
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    print("Breakdown of User Types:\n{}\n".format(df['User Type'].value_counts()))

    # display counts of gender
    try:
        print("Breakdown of Gender:\n{}\n".format(df['Gender'].value_counts()))
        print("Gender was not specified for {} commuters\n".format(df['Gender'].isnull().sum()))
    except:
        print("There is no Gender to report for this city.\n")
    
    # display earliest, most recent, and most common year of birth
    try:
        print("The earliest birth year is {}".format(int(df['Birth Year'].min())))
        print("The most recent birth year is {}".format(int(df['Birth Year'].max())))
        print("The most common birth year is {} with {} commuters born this year".format(int(df['Birth Year'].value_counts().idxmax()), df['Birth Year'].value_counts().max()))
        print("Birth Year was not specified for {} commuters\n".format(df['Birth Year'].isnull().sum()))
    except:
        print("There is no Birth Year to report for this city.\n")
        
def view_data(city):
    """Displays 5 data rows from the selected city file each time."""
    
    view_data = input("Would you like to view the raw data in sets of 10 rows? Yes or No:\n").lower()
        
    with open(CITY_DATA[city.lower()], 'r') as f:
        while view_data == 'yes':
            print(f.readline())
            print(f.readline())
            print(f.readline())
            print(f.readline())
            print(f.readline())
            print(f.readline())
            print(f.readline())
            print(f.readline())
            print(f.readline())
            print(f.readline())
            view_data = input("Would you like to continue viewing the raw data? Yes or No:\n ").lower()
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(city)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
