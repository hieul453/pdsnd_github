import time
import pandas as pd
import numpy as np
import json

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Enter the city name (chicago, new york city, washington): ").lower()
        if city not in CITY_DATA:
            print("Invalid input. Please enter a valid city name.")
        else:
            break

    while True:
        month = input("Enter the month to filter by (all, january, february, ... , june): ").lower()
        if month not in MONTH:
            print("Invalid input. Please enter a valid month.")
        else:
            break

    while True:
        day = input("Enter the day of week to filter by (all, monday, tuesday, ... sunday): ").lower()
        if day not in DAY:
            print("Invalid input. Please enter a valid day of week.")
        else:
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # month = MONTH.index(month) + 1
        month = MONTH.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', popular_day)

    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', popular_end_station)

    df['Start-End Station'] = df['Start Station'] + ' - ' + df['End Station']
    popular_station_combo = df['Start-End Station'].mode()[0]
    print('Most Common Trip (Start-End):', popular_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    if city != 'washington':
        
        gender_counts = df['Gender'].value_counts()
        print('\nGender Counts:\n', gender_counts)

        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()

        (values, counts) = np.unique(df['Birth Year'].dropna(), return_counts=True)
        ind = np.argmax(counts)
        most_common_year = values[ind]
        print('\nEarliest Year of Birth:', int(earliest_year))
        print('Most Recent Year of Birth:', int(most_recent_year))
        print('Most Common Year of Birth:', int(most_common_year))
    else:
        print('\nGender Counts:\nNo data found')
        print('\nEarliest Year of Birth: No data found')
        print('Most Recent Year of Birth: No data found')
        print('Most Common Year of Birth: No data found')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """Displays 5 lines of raw data in pretty-printed JSON format upon user's request."""

    start = 0
    end = 5
    is_continued = True

    while is_continued:
        show_data = input("\nWould you like to see raw data? Enter yes or no: ").lower()

        if show_data == 'yes':
            while end <= df.shape[0] - 1:
                raw_data_json = df.iloc[start:end, :].to_json(orient='records')
                pretty_json = json.dumps(json.loads(raw_data_json), indent=4)
                print(pretty_json)

                start += 5
                end += 5

                while True:
                    show_more = input("\nWould you like to see more 5 lines of raw data? Enter yes or no: ").lower()

                    if show_more == 'no':
                        is_continued = False
                        break
                    elif show_more == 'yes':
                        break
                    else:
                        print("Invalid input. Please enter yes or no.")

                if not is_continued:
                    break

        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter yes or no.")

    print('-' * 40)


def main():
    is_continued = True
    while is_continued:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no: ')

            if restart.lower() == 'no':
                is_continued = False
                break
            elif restart.lower() == 'yes':
                break
            else:
                print("Invalid input. Please enter yes or no.")


if __name__ == "__main__":
    main()
