import tkinter as tk  # tkinter is preinstalled in windows only
import requests
import json  # to use json as json in python
import datetime
from io import BytesIO
from PIL import Image,ImageTk #image library

# api is:- api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

APPID = "cf5b791a429da5ce121f46b695d02d63"  # My_apikey


def write_into_file(data):  # data is response data
    with open('data.json', 'w') as file:  # opening in write mode
        json.dump(data, file)  # dump to file

def getWeather(window):
#def getWeather():
    city = textField.get()
    api_response_url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + APPID
    response = requests.get(api_response_url)
    response_data = response.json()  # taking json
    write_into_file(response_data)  # writing in file
    #print('function called')

    
    try:
        #icons api
        icons_url=f"http://openweathermap.org/img/wn/{response_data['weather'][0]['icon']}@2x.png"
        icon_response=requests.get(icons_url)
        icon_data = icon_response.content #taking pixel data, not exactly the image
        icon_image = ImageTk.PhotoImage(Image.open(BytesIO(icon_data)))  #changing to image

        #country flag api
        country_url=f"https://www.countryflags.io/{response_data['sys']['country']}/flat/64.png"
        country_response=requests.get(country_url)
        country_data=country_response.content
        country_image=ImageTk.PhotoImage(Image.open(BytesIO(country_data)))


        #take data from the response
        condition= response_data['weather'][0]['main']
        
        #changing background image, reading the image
        bg_image_data=Image.open('./Images/'+condition+'.jpg')
        resized_image_data = bg_image_data.resize((800,800),Image.ANTIALIAS)
        bg_image=ImageTk.PhotoImage(resized_image_data)


        temp=int(response_data['main']['temp']-273)
        temp_min=int(response_data['main']['temp_min']-273)
        temp_max=int(response_data['main']['temp_max']-273)
        pressure=response_data['main']['pressure']
        humidity=response_data['main']['humidity']
        wind=response_data['wind']['speed']
        sunrise_unix=response_data['sys']['sunrise']
        sunrise_readable=datetime.datetime.fromtimestamp(sunrise_unix)
        sunset_unix=response_data['sys']['sunset']
        sunset_readable=datetime.datetime.fromtimestamp(sunset_unix)
        final_data= f"{condition} \n {temp} °C"
        final_info=f"Min Temp: {temp_min}°C \n Max Temp: {temp_max}°C \n Pressure: {pressure} \n Humidity: {humidity} \n Wind: {wind} \n Sunrise:{sunrise_readable} \n Sunset:{sunset_readable}"
        label1.config(text=final_data)
        label2.config(text=final_info)

        #putting image
        label3.configure(image=bg_image) #configure for image
        label3.image=(bg_image)
        icons_label.configure(image=icon_image)
        icons_label.image=(icon_image)
        country_label.configure(image=country_image)
        country_label.image=(country_image)
    except KeyError:
        label1.config(text=response_data['message'])
        label2.config(text=response_data['cod'])

window = tk.Tk()  # window initialization
window.title("Weather App")  # title of window
window.geometry("800x800")  # size of window

bg_image_data=Image.open('./Images/bg.jpg')
resized_image_data = bg_image_data.resize((800,800),Image.ANTIALIAS)
bg_image=ImageTk.PhotoImage(resized_image_data)
label3=tk.Label(window,image=bg_image)
#label3.pack()
label3.place(x=0,y=0)

# textfield added
textField = tk.Entry(window, bg='#fafafa', justify='center', font=('poppins', 28, 'italic'), width=20)  # entry box
textField.pack(pady=50)  # textfield will appear,pady gices padding

# button added
button = tk.Button(window, text='Get Weather')
#button = tk.Button(window, command=getWeather, text='Get Weather',activebackground='black', activeforeground='white', bg='white', fg='black')
button.pack()
button.bind('<Button>', getWeather)
# button.bind('<Button>', command=getWeather)  # button left click trigger

icons_label= tk.Label(window,bg="#afafaf")
icons_label.pack()
label1 =  tk.Label(window,bg='#afafaf',font=('poppins',20,'italic'))
label1.pack()
country_label=tk.Label(window,bg='#afafaf')
country_label.pack()
label2 =  tk.Label(window,bg='#afafaf',font=('poppins',20,'italic'))
label2.pack()

window.mainloop()  # keeping window open, loops the program to keep diplaying the app windows
