import time
import pandas as pd
import numpy as np
import calendar as cal

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_check = ('chicago', 'chi', 'new york city', 'ny', 'washington', 'was')
    while True:
        city = input('Which city? Chicago(CHI), New York City (NY), or Washington (WAS)? ')
        if city.lower() in city_check:
            break
        print('Your entry is not a valid city. Please reenter city.')

    if city.lower() == 'chi':
        city = 'Chicago'
    elif city.lower() == 'ny':
        city = 'New York City'
    elif city.lower() == 'was':
        city = 'Washington'

    # get user input for month (all, january, february, ... , june)
    month_check = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    while True:
        month = input('Which month ? All, January, February, March, April, May, or June? ')
        if month.lower() in month_check:
            break
        print('Your entry is not a valid month. Please reenter month.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_check = ('all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
    while True:
        day = input('Which day of the week? All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday? ')
        if day.lower() in day_check:
            break
        print('Your entry is not a valid day of the week. Please reenter day of the week.')

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #Fill in or remove all NaN


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month = df['month'].mode()[0]
    print('The most common month was {}.'.format(cal.month_abbr[pop_month]))

    # display the most common day of week
    pop_day = df['day_of_week'].mode()[0]
    print('The most common day of the week was {}.'.format(pop_day))

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    pop_start_hour = df['hour'].mode()[0]
    if pop_start_hour > 12:
        pop_start_hour = str(pop_start_hour - 12) + ' pm'
    else:
        pop_start_hour = str(pop_start_hour) + ' am'
    print('The most common start hour was {}.'.format(pop_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print('The most common starting station was {}.'.format(pop_start_station))

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print('The most common end station was {}.'.format(pop_end_station))

    # display most frequent combination of start station and end station trip
    start_end_data = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    print('The most common trip was {}.'.format(start_end_data.index[0][0] + " to " + start_end_data.index[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['time_diff'] = df['End Time'] - df['Start Time']

    days = df['time_diff'].sum().days
    hours, remainder = divmod(df['time_diff'].sum().seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    print('Total time traveling was {} days, {} hrs, {} mins, and {} seconds.'.format(days, hours, minutes, seconds))

    # display mean travel time
    hours, remainder = divmod(df['time_diff'].mean().seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print('Average trip duration was {} hrs, {} mins, and {} seconds.'.format(hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.

        Excludes Washington from gender and birth year stats."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users_type = df['User Type'].value_counts()
    print('The counts of the user types are: \n')
    print(dict(users_type))
    print('\n')
    # Display counts of gender
    if city.lower() != 'washington':
        users_gen = df['Gender'].value_counts()
        print('The counts of the user\'s gender are: \n')
        print(dict(users_gen))

        # Display earliest, most recent, and most common year of birth
        earliest_by = df['Birth Year'].min()
        recent_by = df['Birth Year'].max()
        common_by = users = df['Birth Year'].value_counts().index[0]
        print('\nThe earliest birth year was {}. \nThe most recent birth year was {}. \nThe most common birth year is {}.'.format(int(earliest_by), int(recent_by), int(common_by)))
    else:
        print('Washington does not collect data on gender and birth year.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(df):
    """Displays 5 lines of raw data based on users request. Prompts user to display 5 more or stop viewing raw data."""
    while True:
        view_data = input('\nWould you like to view the raw data? Data will be displayed 5 lines at a time. Enter yes or no.\n')
        if view_data.lower() == 'no':
            break
        n=0
        more_data = 'yes'
        while more_data.lower() == 'yes':
            print(df[n:n+5])
            more_data = input('\nWould you like to see 5 more lines? Yes or No? \n')
            if more_data.lower() == 'yes':
                n += 5
            elif more_data.lower() == 'no':
                more_data = 'no'
            else:
                more_data =('\nIncorrect entry. Would you like to see 5 more lines? Yes or No\n')
        break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
