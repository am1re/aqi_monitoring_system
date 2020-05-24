import pathlib

from consolemenu import SelectionMenu
from src import datamanipulation
from src import database

df = datamanipulation.load_data_frame(database.get_collection())


def show_start_menu():
    main_menu = ['Regression analysis for AQI with Wind Speed',
                 'Regression analysis for AQI with Air Pressure',
                 'Regression analysis for AQI with Humidity',
                 'Regression analysis for Humidity with Temperature',
                 'Regression analysis for Humidity with Air Pressure',
                 'Top 10 countries with worst mean AQI',
                 'Top 10 countries with best mean AQI']

    regression_types = {
        0: ['linear', 'Linear regression'],
        1: ['polynomial', 'Polynomial regression']
    }
    regression_menu = []
    for key in regression_types:
        regression_menu.append(regression_types[key][1])

    menu = SelectionMenu(main_menu, title="Select one of these amazing options :)")
    menu.show()

    if menu.is_selected_item_exit():
        print("bye")
        return

    item = menu.selected_option

    if item in range(0, 5):
        menu = SelectionMenu(regression_menu, title='Select regression type', show_exit_option=False)
        menu.show()
        regression_selected = menu.selected_option
        regression_type = regression_types[regression_selected][0]
        if item == 0:
            datamanipulation.show_and_save_plot_aqi_windspeed(df, regression_type)
        elif item == 1:
            datamanipulation.show_and_save_plot_aqi_pressure(df, regression_type)
        elif item == 2:
            datamanipulation.show_and_save_plot_aqi_humidity(df, regression_type)
        elif item == 3:
            datamanipulation.show_and_save_plot_temp_humidity(df, regression_type)
        elif item == 4:
            datamanipulation.show_and_save_plot_humidity_pressure(df, regression_type)

    if item == 5:
        datamanipulation.show_and_save_plot_top10_worst_mean_aqi_by_country(df)
    elif item == 6:
        datamanipulation.show_and_save_plot_top10_best_mean_aqi_by_country(df)

    show_start_menu()


if __name__ == '__main__':
    pathlib.Path("draws/").mkdir(parents=True, exist_ok=True)
    show_start_menu()
