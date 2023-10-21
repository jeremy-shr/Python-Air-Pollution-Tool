import requests
import datetime
import matplotlib.pyplot as plt


def get_live_data_from_api(site_code='MY1', species_code='NO', start_date=None, end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API.

    @param: site_code --> location to draw data from. 
    @param: species_code --> pollution for which to draw data
    @param: start_date and end_date --> determine the time frame for which to draw data. 
    """
    start = datetime.date.today() if start_date is None else start_date
    end = datetime.date.today() + datetime.timedelta(days=1)

    url = f"https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start}/EndDate={end}/Json"

    res = requests.get(url)
    print(res)
    return res.json()


def treat_data(raw_data):
    '''
    Function used to take data from the JSON output of the live data function and output it in a more readable / treatable format. 

    @param: raw_data --> output from live data function

    @return: out --> list of lists for every line including the value of the pollutant and the date/time. 
    '''
    data = raw_data['RawAQData']['Data']

    out = []
    for line in data:
        hour, val = line.values()
        if not val:
            out.append([hour, 'N/A'])
            continue
        out.append([hour, float(val)])

    return out


def check_risk_in_area(data):
    '''
    This function uses the statistical "outlier" method to detect a risk in a given area.
    It takes the values at the lower quartile and upper quartile of the data for the given pollutant to figure out the interquartile range (IQR).
    If any of of the values are greater than Q3 + 1.5*IQR, the area in which it is found is flagged as "At Risk".

    @param: pol -> The choice of pollutant for which the data is checked.
    @param: mdata, kdata, hdata -> treated data from each location.

    @return: If there is an outlier -> location(s) and time at which happened
    '''
    arr = [(line[1], line[0])
           for line in data if type(line[1]) == float].sort()

    if arr is None or len(arr) < 5:
        print('\nThere isn\'t enough data for your pollutant in the station you chose. \nPlease run the function again with different choices (eg: Marylebone Road, NO)\n')
        return 'Failed due to lack of data'
    median = arr[len(arr)//2]
    q1 = len(arr)//4
    q3 = len(arr)//2 + len(arr)//4

    # For the cases where the array is of odd length, the values are incremented by 1 as we used integer division for their definition.
    if len(arr) % 2 != 0:
        median, q1, q3 = list(
            map(lambda x: x + 1, [x for x in (median, q1, q3)]))

    iqr = arr[q3][0] - arr[q1][1]
    outliers = []
    for i in arr[q3:]:
        if i[0] >= arr[q3][0] + 1.5*iqr:
            outliers.append(i)
    print(
        f'\nThe median value for this set of data is {median}. \nThe interquartile range is {iqr}.')
    max_val, max_time = arr[-1]
    if len(outliers) == 0:
        print(
            f'\nNo outliers were found in the provided data. \nThe maximum value is {max_val} which occured at at this date and time: {max_time}')
    else:
        print('\nThese are the outlier(s) and the times at which they occured:\n')
        for val, date in outliers:
            print(f'{val}, at {date}')
    return outliers


def display_stats_location(loc, start_date):
    '''
    Returns a readable output of live data from all pollutants in a chosen station. Takes into account missing data points. 

    @param: loc --> Location chosen by user.
    @param: start_date --> defines time frame from which to fetch data (week or day)

    @return: None, the function prints its results
    '''
    pols = ('NO', 'PM10', 'PM25')
    out = []
    # out = [treat_data(get_live_data_from_api(loc, pol)) for pol in pols]
    for pol in pols:
        out.append(treat_data(get_live_data_from_api(
            loc, pol, start_date)))

    print(out)
    print(len(out))
    print('\n{}Date & Time{}| NO | PM10 | PM25'.format(5*' ', 5*' '))
    for hour in range(len(out[0])):
        print(out[0][hour][0], ' ', out[0][hour][1], ' ',
              out[1][hour][1], '  ', out[2][hour][1])

    print(f'\nLOCATION: {loc}\n')

    return None


def trace_data(data, *args, **kwargs):
    '''
    Traces a graph from data imported from the LondonAir API using Matplotlib 

    @param: data --> input data from the api. It is for one specific pollutant and location

    @return: Success/Failure depending on whether or not the graph was traced
    '''
    arr = []
    for line in data:
        if line[1] != 'N/A':
            arr.append((float(line[1]), line[0]))
    if len(arr) == 0:
        print('\nThere is insufficient data in your selected parameters to complete this function. Try NO at Marylebone Road station if problem persists.\n')
        return 'Failure'
    print(len(arr))
    x = [datetime.datetime.strptime(d[1], '%Y-%m-%d %H:%M:%S') for d in arr]
    y = [d[0] for d in arr]
    plt.style.use('dark_background')
    plt.plot(x, y, marker='.', linestyle='dashed', markersize=12)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()

    return 'Success'


def average_pol(data, start_date, *args, **kwargs):
    """Your documentation goes here"""
    print(data[11])
    arr = []
    for line in data:
        if line[1] != 'N/A':
            arr.append(float(line[1]), line[0])

    if arr is None:
        print('\nThere is insufficient data in your selected parameters to complete this function. Try NO at Marylebone Road station if problem persists.\n')
        return 'Failure'

    time_span = 'since midnight' if start_date is datetime.date.today(
    ) else 'over the course of this week'
    print(
        f'Average value for your chosen location and pollution {time_span} is {sum(arr) / len(arr)}')
    return 'Success'
