import ui.ui as ui
from msvcrt import getch

def main():
    departamento, limite = ui.get_entry()
    if departamento is not None and limite is not None:
        data = ui.call_api(departamento, limite)
        ui.cleanup_column_names(data)
        ui.get_data(data)
        ui.line_feed()
    else:
        print(ui.print_letter("Error in the lecture of the data...", delay=0.1))
        return None
    ui.line_extendence()
    print(ui.print_letter("Data Analysis:", delay=0.1))
    ui.understanding_data(data)
    #ui.histogram(data)
    print(ui.print_letter("Cleaning the corrupt data...", delay=0.1))
    ui.line_feed()
    print(ui.print_letter("None data...", delay=0.1))
    print(ui.print_letter("Duplicate data...", delay=0.1))
    print(ui.print_letter("Data type conversion...", delay=0.1))
    ui.line_feed()
    data = ui.clean_data_column(data)
    data = ui.delete_duplicate_data(data)
    ui.convert_to_int(data)
    ui.get_data(data)
    ui.line_extendence()
    print(ui.print_letter("Data Analysis with the clean data:", delay=0.1))
    ui.understanding_data(data)
    print(ui.print_letter("Data Visualization", delay=0.1))
    ui.line_feed()
    ui.data_visualization(data)
if __name__ == '__main__':
    main()