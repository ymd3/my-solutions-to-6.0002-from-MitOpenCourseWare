# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for degree in degs:
        a = pylab.polyfit(x,y, degree)
        models.append(a)
    return models

#print (generate_models(pylab.array([1961, 1962, 1963]),
#pylab.array([-4.4, -5.5, -6.6]), [1, 2]))


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    error = ((y - estimated)**2).sum()
    meanError = error/len(y)
    return 1 - (meanError/pylab.var(y))


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """

    for num in range(len(models)):
        pylab.plot(x, y, 'o', label='Data')
        esty = pylab.polyval(models[num], x)
        error = r_squared(y, esty)
        pylab.plot(x, esty , label = f'''degree {num + 1} R2 = {round(error, 5)}''', color = 'r' )

        pylab.legend(loc = 'best')
        pylab.xlabel('Years')
        pylab.ylabel('Temperature in Celsius ')
        if len(models[num]) == 2:
            standard_error = se_over_slope(x, y ,esty, models[num])
            pylab.title(f'''degree {len(models[num]) -1} \n R2 = {error} \n standard error = {standard_error}''')
        else:
            pylab.title(f'''degree {len(models[num]) - 1} \n R2 = {error} \n ''')
        pylab.show()


#k = generate_models(pylab.array([1961, 1962, 1963]),
#pylab.array([-4.4, -5.5, -6.6]), [1, 2])
#x = pylab.array([1961, 1962, 1963])
#y = pylab.array([-4.4, -5.5, -6.6])
#evaluate_models_on_training(x, y, k)

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    ave_an_tem = []
    for year in years:
        average = 0
        for city in multi_cities:
            temperatures = climate.get_yearly_temp(city, year)
            for temp in temperatures:
                average += temp
        average = average/(len(multi_cities)*len(temperatures))
        ave_an_tem.append(average)
    return pylab.array(ave_an_tem)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving = []
    num = 0
    ave = 0
    values = []
    while num + 1 <= window_length:
        values.append(y[num])
        ave += y[num]
        moving.append(ave/(num+1))
        num += 1

    for i in range(len(y)):
        if i + 1 > window_length:
            values.pop(0)
            values.append(y[i])
            moving.append(sum(values)/window_length)
    return moving

#y = [10, 20, 30, 40, 50]
#y = pylab.array(y)
#print(moving_average(y, 4))


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    upper = ((y - estimated)**2).sum()
    lower = (len(y))
    return (upper/lower)**(1/2)

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    sd = []
    for year in years:
        temps = []
        for city in multi_cities:
            temps.append(climate.get_yearly_temp(city, year))

        ave = []
        for values in range(365):
            ave.append(0.0)
        if len(temps[0]) == 366:
            ave.append(0.0)
        ave = pylab.array(ave)
        for i in temps:
            ave += i
        ave = ave/len(multi_cities)
        standard = ave.std()
        sd.append(standard)

    return sd
def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        pylab.plot(x,y, 'o', label = 'Data')
        esty = pylab.polyval(model, x)
        error = rmse(y, esty)
        pylab.plot(x, esty, color = 'r', label = 'model')
        pylab.legend(loc = 'best')
        pylab.xlabel( "Years" )
        pylab.ylabel('Temperature in Celcius')
        pylab.title(f''' degree of fit: {len(model)-1} \n RMSE = {error}''')
        pylab.show()


if __name__ == '__main__':

    # Part A.4
    data = Climate('data.csv')
    xval = []
    yval = []
    for year in TRAINING_INTERVAL:
        y = data.get_daily_temp('NEW YORK', 1, 10, year)
        yval.append(y)
        xval.append(year)
    xval = pylab.array(xval)
    yval = pylab.array(yval)
    model = generate_models(xval, yval, [1])
    evaluate_models_on_training(xval, yval, model)
    #4.II
    yval = []
    for year in TRAINING_INTERVAL:
        temps = data.get_yearly_temp('NEW YORK', year)
        average = 0
        for temp in temps:
            average += temp
        average = average/len(temps)
        yval.append(average)
    model2 = generate_models(xval, yval, [1])
    evaluate_models_on_training(xval,yval, model2)

    # Part B
    yval = gen_cities_avg(data, CITIES, TRAINING_INTERVAL)
    model3 = generate_models(xval, yval, [1])
    evaluate_models_on_training(xval, yval, model3)

    # Part C
    yvals = moving_average(yval, 5)
    model4 = generate_models(xval, yvals, [1])
    evaluate_models_on_training(xval, yvals, model4)

    # Part D.2
    model5 = generate_models(xval, yvals, [1,2,20])
    evaluate_models_on_training(xval, yvals, model5)
    y_test = gen_cities_avg(data, CITIES, TESTING_INTERVAL)
    ymove_test = moving_average(y_test, 5)
    x_test = []
    for year in TESTING_INTERVAL:
        x_test.append(year)
    evaluate_models_on_testing(x_test, ymove_test, model5)

    # Part E
    standard_deviations = gen_std_devs(data, CITIES, TRAINING_INTERVAL)
    sdy_moving = moving_average(standard_deviations, 5)
    model6 = generate_models(xval, sdy_moving, [1])
    evaluate_models_on_training(xval, sdy_moving, model6)
