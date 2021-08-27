import gspread,datetime
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep
from ds18b20 import DS18B20

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('raspberry-pi-304822-9b7cb6570988.json', scope) # replace it with your own json file
gc = gspread.authorize(credentials)

wks = gc.open("Aquarium_Water_Temperature").sheet1  # replace it with your own worksheet name

def main():
    sensor = DS18B20()
    
    while True:
        current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        temperatures = sensor.get_temperatures([DS18B20.DEGREES_C, DS18B20.DEGREES_F])
        
        print current_time
        print("Degrees Celsius: %f" % temperatures[0])
        print("Degrees Fahrenheit: %f" % temperatures[1])
        
        x = 0
        try:
            for values in wks.col_values(1): 
                    x = x + 1
            row_added = [current_time, temperatures[0],temperatures[1]] 
            wks.resize(x)
            wks.append_row(row_added)
            print("######### adding another entry #########")
            sleep(10)
        except:
            print("Done")
            break;

if __name__ == "__main__":
    main()