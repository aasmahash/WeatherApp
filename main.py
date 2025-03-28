import sys
import requests

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):#create class weatherApp which inherits from Qwidget
    def __init__(self):
        super().__init__()
        #declare different widgets that belong to weather app object
        self.city_label= QLabel("Enter city name:",self )
        self.city_input=QLineEdit(self) #textbox
        self.get_weather_button=QPushButton("Get Weather",self) #click button to make request to API
        self.temprature_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.description_label=QLabel(self)
        self.initUI() #call the method
        
        
        #intalize our user interface
    def initUI(self):
        self.setWindowTitle("Weather App") #title of window that opens
        
        #Layout Manager to handle the widgets
        vbox=QVBoxLayout()
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temprature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox) #pass in the layout manager vbox to the setlayout
        
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temprature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        #CSS Styling
        
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temprature_label.setObjectName("temprature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        self.setStyleSheet("""
        QLabel, QPushButton{
            font-family:calibri;
        }
        QLabel#city_label{
            font-size: 30px;
            font-style: italic;
        }
        QLineEdit#city_input{
            font-size: 20px;
            
        }
        QPushButton#get_weather_button{
            font-size: 20px;
            font-weight: bold;
            
        }
        QLabel#temprature_label{
            font-size: 50px;
        }
        QLabel#emoji_label{
            font-size: 100px;
            font-family: Segoe UI emoji;
        }
        QLabel#description_label{
            font-size: 100px; #Sunny at bottom of emoji
        }               
                        """)
    
        self.get_weather_button.clicked.connect(self.get_weather)
    
    def get_weather(self):
        api_key="7427ed5ffc0ee1757e48d400943736b3"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response=requests.get(url)
            response.raise_for_status() #raise exception if http errors
            data=response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key") #if you deactivate it
                case 403:
                    self.display_error("Forbidden:\nAccess is denied ")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\n Please try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nService is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                   self.display_error("HTTP error occured\n{http_error}")    
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection ")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out ")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")  
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")
    
    def display_error(self, message):  #display a message if there is an error
        self.temprature_label.setStyleSheet("font-size: 30px; ")
        self.temprature_label.setText(message)
        
    def display_weather(self, data): #display weather data if no error
        self.temprature_label.setStyleSheet("font-size: 50px; ")
        temperature_k=data["main"]["temp"]
        temperature_c=temperature_k-273.15
        temperature_f=(temperature_k*9/5)-459.67
        weather_id=data["weather"][0]["id"]
        weather_description= data["weather"][0]["description"]
        
        
        self.temprature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
   
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200<=weather_id<=232:
            return "⛈️"
        elif 300<=weather_id<=321:
            return "🌦️"
        elif 500<=weather_id<=531:
            return "🌧️"
        elif 600<=weather_id<=622:
            return "❄️"
        elif 701<=weather_id<=741:
            return "🌫️"
        elif weather_id ==762:
            return "🌋"
        elif weather_id ==771:
            return "💨"
        elif weather_id ==781:
            return "🌪️"
        elif weather_id==800:
            return "🌞"
        elif 801<=weather_id<=804:
            return "⛅️"
        else:
            return ""

if __name__ == "__main__": # if we are running file directly then create weather app object, otherwise we wont
       app= QApplication(sys.argv) 
       weather_app=WeatherApp() #create weather app object call the constructor
       weather_app.show()
       sys.exit(app.exec_())



