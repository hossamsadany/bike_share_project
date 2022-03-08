import time

import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
Cities = ['chicago', 'new york city', 'washington']
Months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
Days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print()
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington? \n').lower()
        if city in Cities:
            break
        else:
            print('Sorry this input is not in choices')

    print('Great! you would like to see {} data. '.format(city))
    print()

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Which month ('January', 'February', 'March', 'April', 'May', 'June') would you filter by or would you see "
            "all? for all just say 'all' \n").lower()
        if month in Months:
            break
        else:
            print('Sorry this input is not in choices')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Which day ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday') would you see? "
            "for all just say 'all' ( \n").lower()
        if day in Days:
            break
        else:
            print('Sorry this input is not in choices')
    print('-' * 40)
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

    # Load data into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    else:
        month = df['month']
    # Filter by month to create the new dataframe
    df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != "all":
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: ', Months[common_month])
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of week is: ', common_day)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is: ', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print('The most common start station is : ', most_start_station)
    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is :', most_end_station)
    # display most frequent combination of start station and end station trip
    most_frequent = df.groupby(["Start Station", 'End Station']).size().idxmax()
    print('The most frequent combination of start station and start station : ', most_frequent)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total trip duration : ', total_travel_time)
    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean(), 2)
    print('the mean of travel time is : ', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types = df['User Type'].value_counts().to_frame()
    print('Counts of user types: ', counts_user_types)
    # Display counts of gender
    try:
        counts_gender = df['Gender'].value_counts().to_frame()
        print('Counts of Gender: ', counts_gender)
    except KeyError:
        print("Sorry Gender is not available in this input")
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_birth = int(df['Birth Year'].min())
        most_recent_year_birth = int(df['Birth Year'].max())
        most_common_year_birth = int(df['Birth Year'].mode())
        print(
            'The earliest year of birth {}, the most recent year of birth {}, the most common year of birth {} '.format(
                earliest_year_birth, most_recent_year_birth, most_common_year_birth))
    except KeyError:
        print('Sorry the birth year is not available in this input ')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower() == 'yes':
            main()
        else:
            print('Thank you !')
            break


if __name__ == "__main__":
    main()