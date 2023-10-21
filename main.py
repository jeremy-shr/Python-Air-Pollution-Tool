import numpy as np
from matplotlib import pyplot as mat_plot
import datetime

from intelligence import *
from reporting import *
from monitoring import *


def menu_setup(menu, mess):
    '''
    Used to quickly format the start of every different menu.

    @param: menu -> The type of menu being called
    @param: mess -> Message to give more information about the module (depends on the menu type) 
    '''
    print('\n'+'='*50)
    print(
        f'Welcome to the {menu} Menu. \n{mess} \n\nPlease choose one of the following options:\n')


def menu_outro(menu):
    '''
    Used to close a given menu and indicate to the user that they are back to the main menu. 

    @param: menu -> The type of menu being called
    '''
    print(f'\nThank you for using the {menu} Menu.\n'+'='*50)
    print(
        '\n\nYou have now returned to the main menu. Please make your next choice from the following:' + '\n'*2)
    menu_setup


def reporting_menu():
    '''
    Menu used to present to the user the various functions of the PR module. 
    It uses an input validation system to limit exceptions due to user input. 

    '''
    with open(f'./data/Pollution-London Marylebone Road.csv') as f:
        mary_data = f.read().split('\n')
    with open(f'./data/Pollution-London N Kensington.csv') as f:
        nken_data = f.read().split('\n')
    with open(f'./data/Pollution-London Harlington.csv') as f:
        harl_data = f.read().split('\n')

    menu_setup(
        'Reporting', 'The PR Module uses data treatment functions to providing relevant information regarding the pollution levels at the different monitoring stations.')

    print('Start by choosing a Monitoring Station: ')

    # These while loops are used throughout the function as an input validation method.
    while True:
        print(
            'M - Marylebone Road (MY1) \nN - N. Kensington (KC1) \nH - Harlington (HRL)\n')
        station = input(
            'Enter your choice for the monitoring station: ').upper()
        if station == 'M':
            data = mary_data
            break
        elif station == 'N':
            data = nken_data
            break
        elif station == 'H':
            data = harl_data
            break
        else:
            print('Please input a valid option from the following choices: ')
    print('\nNext, please choose the pollutant you will want to look at: ')
    while True:
        print(
            'NO - Nitric Oxide \nPM10 - PM10 inhalable particulate matter \nPM25 - PM2.5 inhalable particulate matter\n')
        pol = input(
            'Enter your choice for the monitoring station: ').lower()
        if pol in ['pm10', 'no', 'pm25']:
            break
        else:
            print('Please input a valid option from the following choices: ')
    while True:
        print('\nNow, choose which function to run on your selected data:\n')
        print('1 - Daily averages for your given parameters (365 values).')
        print('2 - Daily medians for your given parameters (365 values).')
        print('3 - Hourly average for your given parameters (24 values).')
        print('4 - Monthly averages for your given parameters (12 values).')
        print('5 - Returns the hour of the day with the highest pollution level for a given date and its corresponding value.')
        print('6 - Count the instances of missing data in the data associated to your given parameters.')
        print('7 - Replace current missing values in the dataset with a given value for your parameters.')
        print('Q - Quit the PR Menu.')
        choice = input('\nEnter your choice: ').upper()

        if choice == '7':
            new_val = input(
                '\nWhat value would you like to replace the missing data with?\nPlease enter it here: ')
            data = fill_missing_data(data, new_val, station, pol)
            filled_data = True
            print('\nMissing data replaced.')
            input('\nPress enter to continue.')

        elif not filled_data:
            print('Please run the "Fill missing values" functions first, thank you.')

        elif choice == '1':
            print('\nDaily Average:')
            print(daily_average(data, station, pol))
            input('\nPress enter to continue.')
        elif choice == '2':
            print('\nDaily Median:')
            print(daily_median(data, station, pol))
            input('\nPress enter to continue.')
        elif choice == '3':
            print('\nHourly Average:')
            print(hourly_average(data, station, pol))
            input('\nPress enter to continue.')
        elif choice == '4':
            print('\nMonthly Average:')
            print(monthly_average(data, station, pol))
            input('\nPress enter to continue.')
        elif choice == '5':
            # Again, this loop is to make sure the user inputs a valid date, in the correct format.
            while True:
                try:
                    date = input(
                        '\nPlease input a date for the Peak Hour function (format is YYYY-MM-DD): ')
                    print()
                    print(peak_hour_date(data, date, station, pol))
                    input('\nPress enter to continue.')
                    break
                except:
                    print('\nPlease enter a valid date.')

        elif choice == '6':
            print('\nNumber of Missing Data instances:')
            print(count_missing_data(data, station, pol))
            input('\nPress enter to continue.')
        elif choice == 'Q':
            break
        else:
            print('Please input a valid option from the following choices: ')


def main_menu():
    '''
    Ran upon initiation of main.py, this is the base for user input. It redirects to other menus depending on the input.

    Runs the quit() function to terminate the programme.
    '''

    print('\n'*2 + 'Welcome to the ACQUA platform user interface.\nThis software offers an air pollution data analytics solution using data from three different locations in London.\n\nPlease use your keyboard to navigate the menus.')
    print('\nStart by choosing a module from the following:')

    while True:  # Loop used to ensure the user enters a valid input
        print('R - Access the PR module (Pollution Reporting),\nI - Access to the MI module (Mobility Intelligence),\nM - Access to the RM module (Real Time Monitoring),\nA - About, \nQ - Quit the application')
        choice = input('\nEnter your choice: ').upper()

        if choice == 'R':
            reporting_menu()
            menu_outro('Reporting')

        elif choice == 'I':
            intelligence_menu()
            menu_outro('Intelligence')

        elif choice == 'M':
            monitoring_menu()
            menu_outro('Monitoring')

        elif choice == 'A':
            about()
            menu_outro('About')

        elif choice == 'Q':
            quit()
            return None

        else:
            print('\nPlease select one of the presented options:')


def monitoring_menu():
    '''
    Reveals menu for the RM menu functions to the user.


    '''
    menu_setup('Live Monitoring',
               'This module allows for the analysis of live data from 3 stations in London.')
    print('Start by choosing a time frame on which to fetch hourly data: \n')
    print('D - Fetch data from the day (Default) \nW - Fetch data from the current week (last monday until now)\n')
    timeframe = input('Please enter your choice: ').upper()
    if timeframe == 'W':
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=today.weekday())
    else:
        start_date = datetime.date.today()

    while True:
        print('\nMY1 - Marylebone Road\nKC1 - N.Kensignton\nHRL - Harlington\n')
        loc = input(
            'Please choose a location for which to fetch data: ').upper()
        if loc in ['MY1', 'KC1', 'HRL']:
            break
        else:
            print('\nPlease choose a valid option.')

    while True:
        print('\nPlease choose a function to run within the module: \n')
        print('1 - DISPLAY pollution statistics for a given station. \n2 - Identify whether a location is AT RISK from a given pollutant. \n3 - Return the average of each pollutant for a given station. \n4. Trace a Graph with all hourly values within your selected time frame. \nQ - Quit the Live Monitoring menu ')
        choice = input('\nPlease enter your choice: ').upper()

        if choice == '1':
            print(start_date)
            display_stats_location(loc, start_date=start_date)

        elif choice in ['2', '3', '4']:
            while True:
                print(
                    'NO - Nitric Oxide\nP10 - PM10 Inhalable particulate matter\nP25 - PM2.5 Inhalable particulate matter\n')
                pol = input('Please choose a pollutant: ').upper()
                if pol in ['NO', 'P10', 'P25']:

                    data = treat_data(
                        get_live_data_from_api(loc, pol, start_date))
                    break
                else:
                    print('Please choose a valid option.')
            if choice == '2':
                check_risk_in_area(data)
            elif choice == '3':
                average_pol(data, start_date)
            else:
                trace_data(data)

        elif choice == 'Q':
            break

        else:
            print('Please choose a valid option.')
        input('Press Enter to continue')


def intelligence_menu():
    '''
    Menu used to present to the user the various functions of the MI module. 
    It uses an input validation system to limit exceptions due to user input.

    Only terminates if the user selects 'Q' from the menu
    '''
    image = './data/map.png'

    menu_setup('Mobility Intelligence',
               'The goal of the MI module is to provide visual support to the analyses of road infrastructure in one of the stations.')
    while True:

        print('R - Download an image containing all RED pixels from the map.')
        print('C - Download an image containing all CYAN pixels from the map.')
        print('D - Detect connected components for pavements (RED image).')
        print(
            'S - Sort connected components and output an image visualising the two largest ones.\n')
        print('Q - Exit the intelligence menu')
        choice = input('Choose a function to run: ').upper()
        if choice == 'R':
            find_red_pixels(image)
            binary = True
        elif choice == 'C':
            find_cyan_pixels(image)
        elif choice == 'D' and binary:
            detect_connected_components('map-red-pixels.jpg')

        elif choice == 'S' and binary:
            detect_connected_components_sorted()

        elif choice == 'D' or choice == 'S':
            print('Try again after having run the red pixel detection function.')

        elif choice == 'Q':
            break
        else:
            print('\nPlease choose a valid option.\n')


def about():
    '''
    Student information
    '''
    print('ECM1400')
    print('720050437')


def quit():
    '''
    Function run to close out the programme. Input allows the user to read before the programme closes out.
    '''
    input('\n\nThank you for using the ACQUA platform for your data analysis needs.\n')


if __name__ == '__main__':
    main_menu()
