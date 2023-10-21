indices = {'date': 0,
           'time': 1,
           'no': 2,
           'pm10': 3,
           'pm25': 4}  # Dictionary to keep track of columns within the data file


def daily_average(data, monitoring_station, pollutant):
    '''
    Returns the average for each day of the year

    @param: data --> csv file with data to treat
    @param: pollutant --> the user's chosen pollutant. Indicates which column to read data from

    @return: averages --> list of 365 values containing the average value for each day's data
    '''
    averages = []
    # Uses dictionary to identify the index to use within the split line of data
    ind = indices[pollutant]
    try:
        for day_number in range(365):
            total = 0
            for hour in range(1, 25):
                # Finds the line of data for the concerned day and hour.
                hour_line = data[(day_number*24)+hour].split(',')
                total += float(hour_line[ind])
            averages.append(total / 24)
    except:
        print('There are missing values in this data, run th Fill Missing Data function first. \nHere are the averages up until the point of the error')
    return averages


def daily_median(data, monitoring_station, pollutant):
    '''
    Returns the median for each day of the year

    @param: data --> csv file with data to treat
    @param: pollutant --> the user's chosen pollutant. Indicates which column to read data from

    @param: medians --> list of 365 values containing the median value for each day's data
    '''
    medians = []
    ind = indices[pollutant]
    for day_number in range(365):

        values = []
        for hour in range(1, 25):
            hour_line = data[day_number*24 + hour].split(',')
            values.append(float(hour_line[ind]))
        values.sort()
        # if len(values) % 2 == 0:
        #     medians.append(
        #         (values[len(values)//2]+values[len(values)//2 + 1])/2)
        # else:
        #     medians.append(values[int(len(values)/2)])
        medians.append((values[12]+values[13]) / 2)
    return medians


def hourly_average(data, monitoring_station, pollutant):
    '''
    Hourly average for a given pollutant across the whole year. 

    @param: data --> csv file with data to treat
    @param: pollutant --> the user's chosen pollutant. Indicates which column to read data from

    @return: avg --> list of 24 values each representing the average for the according hour. 
    '''
    ind = indices[pollutant]
    avg = [0 for _ in range(24)]

    for day_number in range(365):
        for hour_number in range(1, 25):
            value = data[day_number*24 + hour_number].split(',')[ind]
            print('VALUE = ' + value)
            avg[hour_number-1] += float(value)

    for value in range(24):
        avg[value] /= 365

    return avg


def monthly_average(data, monitoring_station, pollutant):
    '''
    Reads a year of data and returns an average for each month. 

    @param: data --> csv file with data to treat
    @param: pollutant --> the user's chosen pollutant. Indicates which column to read data from

    @return: 12 values corresponding to the monthly averages
    '''

    months = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
    # List with the number of days elapsed before the end of each month.
    # This allows us to which month each day falls into

    no_of_hours = [0 for _ in range(12)]
    # To keep track of the number of hours in each month as we iterate

    avgs = [0 for _ in range(12)]
    ind = indices[pollutant]

    for day_number in range(1, 365):
        for hour in range(1, 25):
            val = float(data[day_number*24+hour].split(',')[ind])

            avgs[12-len(months)] += val
            no_of_hours[12-len(months)] += 1
            if day_number == months[0] and hour == 24:
                months.pop(0)

    for i in range(12):
        avgs[i] = avgs[i] / no_of_hours[i]
    return avgs


def peak_hour_date(data, date, monitoring_station, pollutant):
    '''
    Returns the peak value of the chosen pollutant in a given day.

    @param: data --> csv file to be used as data
    @param: date --> the date chosen by the user
    @param: pollutant --> the pollutant chosen by the user

    @return --> Peak hour and its value 
    '''
    ind = indices[pollutant]

    month, day = date.split('-')[1:]
    max_val = 0
    max_hour = 0
    months = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
    for i in range(1, 25):
        val = data[months[(month-1)*24+day+i]][ind]
        if val > max_val:
            max_val = val
            max_hour = f'{i}:00'

    return f'{max_hour}, {max_val}'


def count_missing_data(data,  monitoring_station, pollutant):
    '''
    Counts the instances of missing data in a file of data
    '''

    count = 0
    ind = indices[pollutant]
    for line in data:
        if line[ind] == 'No data':
            count += 1
        else:
            pass

    return count


def fill_missing_data(data, new_value,  monitoring_station, pollutant):
    '''
    Replaces all instances of missing values by a user-given value. 
    '''
    for L in range(1, len(data)):
        data[L] = data[L].replace('No data', new_value)

    return data
