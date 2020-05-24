import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import stats

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def load_data_frame(collection):
    df = pd.DataFrame(list(collection.find()))
    del df['_id']

    df = df.dropna()

    df['wind_speed'] = df['wind_speed'].apply(lambda d: d * 0.277778)  # convert km/h to m/s

    df = standardize_values(df, 'temp')
    df = standardize_values(df, 'humidity')
    df = standardize_values(df, 'wind_speed')
    df = standardize_values(df, 'pressure')
    df = standardize_values(df, 'aqi')

    # TODO balance data

    return df


def standardize_values(df, prop_name):
    std_dev = 3
    z_scores = stats.zscore(df.loc[:, prop_name])
    return df[np.abs(z_scores) < std_dev]


def show_and_save_plot_aqi_windspeed(df, regression_type):
    draw_plot_with_regression(df, regression_type, "wind_speed", "aqi", "Wind speed, m/s", "AQI, PM 2.5",
                              f"{regression_type.capitalize()}_regression_for_Air_Quality_with_Wind_Speed")
    plt.show()
    plt.close()


def show_and_save_plot_aqi_pressure(df, regression_type):
    draw_plot_with_regression(df, regression_type, "pressure", "aqi", "Pressure, millibar", "AQI, PM 2.5",
                              f"{regression_type.capitalize()}_regression_for_Air_Quality_with_Air_Pressure")
    plt.show()
    plt.close()


def show_and_save_plot_aqi_humidity(df, regression_type):
    draw_plot_with_regression(df, regression_type, "humidity", "aqi", "Humidity, %", "AQI, PM 2.5",
                              f"{regression_type.capitalize()}_regression_for_Air_Quality_with_Humidity")
    plt.show()
    plt.close()


def show_and_save_plot_temp_humidity(df, regression_type):
    draw_plot_with_regression(df, regression_type, "temp", "humidity", "Temperature, C", "Humidity, %",
                              f"{regression_type.capitalize()}_regression_for_Humidity_with_Temperature")
    plt.show()
    plt.close()


def show_and_save_plot_humidity_pressure(df, regression_type):
    draw_plot_with_regression(df, regression_type, "pressure", "humidity", "Air Pressure, millibar", "Humidity, %",
                              f"{regression_type.capitalize()}_regression_for_Humidity_with_Air_Pressure")
    plt.show()
    plt.close()


def show_and_save_plot_top10_worst_mean_aqi_by_country(df):
    draw_plot_top10_mean_aqi_by_countries("worst", df)
    plt.show()


def show_and_save_plot_top10_best_mean_aqi_by_country(df):
    draw_plot_top10_mean_aqi_by_countries("best", df)
    plt.show()


# 0 - temp | 1 - humidity | 2 - wind_speed | 3 - pressure | 4 - AQI ||| 5 - Country
def draw_plot_with_regression(df, regression_type, x_index, y_index, x_label, y_label, title):
    indexes = {
        "temp": 0,
        "humidity": 1,
        "wind_speed": 2,
        "pressure": 3,
        "aqi": 4
    }

    df = df.groupby(["city1"]).mean()
    df = df.round(1)

    x = df.iloc[:, indexes[x_index]].values.reshape(-1, 1)  # values converts it into a numpy array, -1 means that
    y = df.iloc[:, indexes[y_index]].values.reshape(-1, 1)  # calculate the dimension of rows, but have 1 column

    models = {
        'linear': LinearRegression().fit(x, y),
        'polynomial': make_pipeline(PolynomialFeatures(3), Ridge()).fit(x, y)
    }

    plt.figure(figsize=(8, 6), dpi=150)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # training points
    plt.scatter(x, y, s=0.5, label='Training points')
    # predict values
    model = models[regression_type]
    x_plot = np.linspace(min(x), max(x)).reshape(-1, 1)
    y_pred = model.predict(x_plot)
    plt.plot(x_plot, y_pred, color='red', label='Predicted values')

    plt.legend(loc='upper right')
    plt.draw()
    plt.savefig(f"draws/{title}.png")
    plt.gcf().canvas.set_window_title(title)


def draw_plot_top10_mean_aqi_by_countries(type_top, df):
    df = df.groupby(["country"]).mean()
    df = df.round(1)

    if type_top == "best":
        title = "TOP10_Countries_With_Best_Mean_AQI"
        df = df.nsmallest(10, "aqi", keep='all')
    else:
        title = "TOP10_Countries_With_Worst_Mean_AQI"
        df = df.nlargest(10, "aqi", keep='all')

    df.plot(kind='bar', y="aqi", figsize=(8, 10), legend=False)
    plt.xlabel("Countries")
    plt.ylabel("AQI, PM 2.5")

    plt.draw()
    plt.savefig(f"draws/{title}.png")
    plt.gcf().canvas.set_window_title(title)
