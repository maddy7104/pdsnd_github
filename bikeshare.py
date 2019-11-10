import time
import pandas as pd
import numpy as np

#Creating city data dictionary and valid months and days lists
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_list = ['all','january','february','march','april','may','june']
days_list = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']


def input_processing(input_message, input_list):
    """
    Asks user for input and returns processed user input
    Args:
        (str) input_message - message to be displayed to the user while asking for input
        (list) input_list - list of valid inputs

    Returns:
        (str) processed_input - valid user input in lower case with leading and trailing white spaces removed
    """
    while True:
        user_input = input(input_message).strip().lower()
        if user_input in input_list:
            break
        else:
            print("\nInvalid Entry\n")
    return user_input


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input_processing("Please select a city in this list: Chicago, New York City, Washington\n",CITY_DATA.keys())

   # TO DO: get user input for month (all, january, february, ... , june)
    month = input_processing("Please enter a month between January and June (inclusive) for analysis (Enter 'all' to run analysis for all 6 months):\n",months_list)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input_processing("Please enter a day of the week for analysis (Enter 'all' to run analysis for all 7 days of the week):\n",days_list)

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
   # convert the Start Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

   # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

   # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months_list.index(month)
        # filter by month to create the new dataframe
        df = df[df['month']==month]

            # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print( "The most common month is {}".format(months_list[df['month'].mode()[0]].title()) )

    # TO DO: display the most common day of week
    print( "The most common day of the week is {}".format(df['day_of_week'].mode()[0].title()) )

    df['hour'] = df['Start Time'].dt.hour
    # TO DO: display the most common start hour
    if df['hour'].mode()[0] >= 10:
        print( "The most common start hour is {}00".format(df['hour'].mode()[0]) )
    else:
        print( "The most common start hour is 0{}00".format(df['hour'].mode()[0]) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print( "The most commonly used start station is {}".format(df['Start Station'].mode()[0].title()) )

    # TO DO: display most commonly used end station
    print( "The most commonly used end station is {}".format(df['End Station'].mode()[0].title()) )

    # TO DO: display most frequent combination of start station and end station trip
    df['Start_End_Station'] = df['Start Station'] + " --> " + df['End Station']
    print( "The most frequent combination of start and end stations among all the trips is {}".format(df['Start_End_Station'].mode()[0].title()) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def timedelta_h_m_s(time_delta_object):
    """Converts a timedelta object's "total_seconds" method value to hour, minute, and second"""
    seconds = time_delta_object.total_seconds()
    hours = (seconds // 3600)
    minutes = (seconds // 60) % 60
    seconds = seconds % 60
    return round(hours),round(minutes),round(seconds,1)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    travel_time_hours, travel_time_minutes, travel_time_seconds = timedelta_h_m_s(df['Travel Time'].sum())
    print( "Total travel time is {} hours, {} minutes, and {} seconds".format(travel_time_hours,travel_time_minutes,travel_time_seconds) )


    # TO DO: display mean travel time
    travel_time_hours, travel_time_minutes, travel_time_seconds = timedelta_h_m_s(df['Travel Time'].mean())
    print( "Mean travel time is {} minutes and {} seconds".format(travel_time_minutes,travel_time_seconds) )
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types:")
    print(user_types,"\n")

    if city.lower()!='washington':
        # TO DO: Display counts of gender
        genders = df['Gender'].value_counts()
        print("Counts of Genders:")
        print(genders,"\n")

        # TO DO: Display earliest, most recent, and most common year of birth
        print( "Earliest year of birth is {}".format(int(df['Birth Year'].min())) )
        print( "Most recent year of birth is {}".format(int(df['Birth Year'].max())) )
        print( "Most common year of birth is {}".format(int(df['Birth Year'].mode())) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        pd.set_option('display.max_columns', None)
        while True:
            # Displaying 5 rows of the raw data at a time
            raw_data_initial = input("\nWould you like to get a glimpse of the raw data? Enter yes or no.\n").strip().lower()
            raw_data_recurring = ''
            if raw_data_initial == 'yes':
                i,end_value = 0,5
                raw_data_recurring = 'yes'
                while True:
                    if raw_data_recurring =='yes':
                        if city == 'washington':
                            print("\n",df[['Start Time','End Time','Trip Duration','Start Station','End Station','User Type']][i:end_value])
                        else:
                            print("\n",df[['Start Time','End Time','Trip Duration','Start Station','End Station','User Type','Gender','Birth Year']][i:end_value])
                        if end_value == len(df):
                            print("\nEnd of raw data list\n")
                            raw_data_recurring = 'no'
                            break
                        if (end_value+5)<len(df):
                            i+=5
                            end_value = i+5
                        else:
                            i = end_value
                            end_value = len(df)

                        while True:
                            raw_data_recurring = input("\n\nDo you want to see more of the raw data? Enter yes or no.\n").strip().lower()
                            if raw_data_recurring != 'yes' and raw_data_recurring != 'no':
                                print('Invalid Entry')
                            else:
                                break
                    else:
                        break
            elif raw_data_initial !='yes' and raw_data_initial !='no':
                print("Invalid Entry")
            else:
                break
            if raw_data_recurring == 'no':
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart == 'no':
            break
        elif restart !='yes' and restart !='no':
            while True:
                print("Invalid Entry")
                restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
                if restart == 'yes' or restart =='no':
                    break
            if restart == 'no':
                break



if __name__ == "__main__":
	main()
