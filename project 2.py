import json     #accu weather data comes as json format so we need module to decode and change to a usable type
import pandas as pd
import urllib.request
import random
from datetime import datetime as dt
import time
import UCNanoleaf as NL



def currentweather(location_key):
    current="http://dataservice.accuweather.com/currentconditions/v1/"+str(location_key)+"?apikey=ddqK3u8d29p6wOlGm1YlIA1NUQH2rWoY"
    print(current)
    with urllib.request.urlopen(current) as current:
        data=json.loads(current.read().decode())
    
    df = pd.json_normalize(data)
    weather_icon = df["WeatherIcon"].values
    return(weather_icon)

def precipitation(drop_positions, weather):
    drop_position = drop_positions
    bg = (116,87,222)          #background colour
    rain_drop = (86,158,209)    #rain drop colour
    snow_flake = (255,255,255)
    colour = (86,158,209)
    cloud = (200,200,200)       #cloud colour
    cloud_accent = (170,170,170)#cloud accent colour
    cloud_data = [              #sets initial colours of each triangle in list of lists 12 down by 23 across
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,bg,bg,bg,bg],
        [bg,bg,bg,bg,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg]
    ]

    cloud_df = pd.DataFrame(cloud_data)     #resets dataframe so drops can be moved down

    #constantly updates rain drops as function runs
    rain_chance = random.randint(1,3)       #randomly generated number that generates a drop
    if rain_chance == 2:
        position = random.randint(5,17)     #sets initial position just below cloud
        drop_position.append([4,position])  #and adds it to the list of lists with position of each drop

    if weather == 'rain':
        colour = rain_drop
    elif weather == 'snow':
        colour = snow_flake

    for i in range(len(drop_position)):     #go through list of drops and updates each position to move them down
        drop_position[-i][0]+=1
        cloud_df.iloc[drop_position[-i][0],drop_position[-i][1]] = colour
        if drop_position[0][0] == 11:       #if drop hits the bottom it is removed from the list
            drop_position.pop(0)

    return [drop_position, cloud_df]

def lightning(drop_positions):
    bg = (116,87,222)          #background colour
    rain_drop = (86,158,209)    #rain drop colour
    drop_position = drop_positions         #list of lists for position of each drop
    lc = (245,232,49)           #lightning colour
    cloud_accent = (200,200,200)       #cloud colour
    cloud = (150,150,150)#cloud accent colour
    cloud_data = [              #sets initial colours of each triangle
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,bg,bg,bg,bg],
        [bg,bg,bg,bg,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg]
    ]



    rain_chance = random.randint(1,2)
    rain_chance = 2
    lightning_chance = random.randint(1,6)
    cloud_df = pd.DataFrame(cloud_data)
    #generates new rain drop
    if rain_chance == 2:
        position = random.randint(5,17)
        drop_position.append([4,position])
    
    #translates each drop down
    for i in range(len(drop_position)):
        drop_position[-i][0]+=1
        cloud_df.iloc[drop_position[-i][0],drop_position[-i][1]] = rain_drop
        if drop_position[0][0] == 11:
            drop_position.pop(0)

    #generates lightning
    lightning_pattern = []
    if lightning_chance == 2:
        lightning_position = random.randint(5,17)
        lightning_pattern.append([5,lightning_position])
        height = 5
        while height < 11:
            if height == 4:
                lightning_pattern.append([height+1,lightning_pattern[-1][1]])
            else:
                lightning_direction = random.randint(1,3) #1 for left, 2 for straight down, 3 for right
                if lightning_direction == 1:
                    lightning_pattern.append([height, (lightning_pattern[-1][1]-1)])
                    lightning_pattern.append([height+1,lightning_pattern[-1][1]])
                elif lightning_direction == 2:
                    lightning_pattern.append([height+1,lightning_pattern[-1][1]])
                elif lightning_direction == 3:
                    lightning_pattern.append([height, (lightning_pattern[-1][1]+1)])
                    lightning_pattern.append([height+1,lightning_pattern[-1][1]])
            height += 1
    
    for i in range(len(lightning_pattern)):
        cloud_df.iloc[lightning_pattern[-i][0],lightning_pattern[-i][1]] = lc
    return [drop_position, cloud_df]

#Creates dynamic moving clouds
def cloudy(sky_position):
    cloud_accent = (189,189,189)#cloud accent colour
    bg = (50, 120, 190)          #background colour    
    cloud = (210,210,210)       #cloud colour
    cloud_data = [              #sets initial colours of each triangle
        [cloud,cloud_accent,cloud,cloud_accent,cloud,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,cloud,cloud_accent],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,cloud,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud_accent,cloud,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,cloud,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,cloud,cloud,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud,cloud_accent,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [cloud,cloud,cloud_accent,cloud,cloud,cloud,cloud,cloud_accent,cloud,cloud,cloud,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg]
    ]
    if len(sky_position) == 0:
        cloud_df = pd.DataFrame(cloud_data)
    else:
        cloud_df = sky_position

    #Loop in charge of moving the top border cloud
    for i in range(1):
        end_colour1 = cloud_df.iloc[i][0]
        end_colour2 = cloud_df.iloc[i][1]
        for o in range(22):
            cloud_df.iloc[i][o]=cloud_df.iloc[i][o+2]
        cloud_df.iloc[i][22] = end_colour1
        cloud_df.iloc[i][23] = end_colour2

    #Loop in charge of moving the top cloud
    for i in range(2,6):
        end_colour1 = cloud_df.iloc[i][0]
        end_colour2 = cloud_df.iloc[i][1]
        for o in range(22):
            cloud_df.iloc[i][o]=cloud_df.iloc[i][o+2]
        cloud_df.iloc[i][22] = end_colour1
        cloud_df.iloc[i][23] = end_colour2

    #Loop in charge of moving the cloud in the middle
    if not random.randint(0,3) == 1:
        for i in range(7,10):
            end_colour1 = cloud_df.iloc[i][0]
            end_colour2 = cloud_df.iloc[i][1]
            for o in range(22):
                cloud_df.iloc[i][o]=cloud_df.iloc[i][o+2]
            cloud_df.iloc[i][22] = end_colour1
            cloud_df.iloc[i][23] = end_colour2

    #Loop in charge of moving the bottom border cloud
    if not random.randint(0,3) == 1:
        for i in range(11,12):
            end_colour1 = cloud_df.iloc[i][0]
            end_colour2 = cloud_df.iloc[i][1]
            for o in range(22):
                cloud_df.iloc[i][o]=cloud_df.iloc[i][o+2]
            cloud_df.iloc[i][22] = end_colour1
            cloud_df.iloc[i][23] = end_colour2

    return cloud_df






def sunny(rays):
    bg = (77, 180, 227)             #background colour
    sun = (247, 207, 7)             #sun colour
    sun_accent = (247, 163, 7)      #sun accent colour
    if rays == 1:                   #has two options for rays so that the animation can go back and forth between them
        sunny_data = [              #sets initial colours of each triangle
            [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,sun,bg,bg,bg,bg,bg,bg,bg,sun,sun_accent,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,sun_accent,sun,bg,sun,sun,bg,bg,sun,sun,bg,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,sun,sun,sun,sun,sun,sun,sun_accent,sun,sun,sun,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,sun,bg,sun_accent,sun,sun,sun,sun,sun,sun,sun,sun,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,sun,sun,sun,sun,sun,sun,sun_accent,sun,sun,sun,sun,sun,sun,sun,sun_accent,sun,bg,bg],
            [bg,bg,sun_accent,sun,sun,sun,sun,sun_accent,sun,sun,sun,sun,sun,sun,sun,sun_accent,sun,sun,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,sun,sun,sun,sun,sun,sun,sun,sun,sun,bg,sun,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,sun,sun,sun,sun,sun_accent,sun,sun,sun,sun,sun,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,bg,sun,sun,bg,bg,sun,sun,bg,sun_accent,sun,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,sun,sun_accent,bg,bg,bg,bg,bg,bg,bg,sun,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg]
        ]
        sunny_df = pd.DataFrame(sunny_data)
        return sunny_df
    elif rays == 2:
        sunny_data = [              #sets initial colours of each triangle
            [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,sun_accent,sun,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,bg,sun,sun,bg,bg,sun,sun,bg,sun,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,sun,sun_accent,sun,sun,sun,sun,sun,sun,sun,sun_accent,sun,sun,bg,bg,sun,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,sun_accent,sun,sun,sun,sun,sun,sun,sun,sun,bg,sun,sun_accent,bg,bg,bg,bg],
            [bg,bg,bg,bg,sun,sun,sun,sun,sun,sun,sun,sun_accent,sun,sun,sun,sun,sun,sun,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,sun,sun,sun_accent,sun,sun,sun,sun,sun,sun,sun,sun_accent,sun,sun,sun,bg,bg,bg,bg],
            [bg,bg,bg,bg,sun,sun,bg,sun,sun,sun,sun,sun,sun,sun,sun,sun,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,sun_accent,bg,bg,sun,sun,sun,sun_accent,sun,sun,sun,sun,sun,sun_accent,sun,sun,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,sun,bg,sun,sun,bg,bg,sun,sun,bg,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,sun_accent,sun,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
            [bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg]
        ]
        sunny_df = pd.DataFrame(sunny_data)
        return sunny_df

def main():
    #NL.initalize()
    start_time = dt.strftime(dt.now(),'%X')     #when program is started
    END_TIME = '22:00:00'                       #arbitrary end time at 10pm
    FMT = '%H:%M:%S'                            #format of time in calculations

    time_difference = dt.strptime(END_TIME, FMT) - dt.strptime(start_time, FMT)
    NOC = 50                #max of 50 daily api checks (the accu weather service only works for 50 checks before it stops)
    check_interval = time_difference.total_seconds()/NOC            #maximize how much data we get by utilizing all 50 checks throughout the day
    sunny_in = [1,2,3,4,5,30,31,32]
    cloudy_in = [6,7,8,11,38]
    rainy_in = [12,13,14,18,39,40]
    thunder_in = [15,16,17,41,42]
    night_in = [33,34,35,36,37]
    snowy_in = [19,20,21,22,23,24,25,26,27,28,29,43,44]

    check_interval = 10  #delete when program is done

    while True:
        KEY = 52479         #the key for calgary
        weather_icon = 6
        start = dt.strftime(dt.now(),'%X')
        if weather_icon in rainy_in:
            while True:             #each while loop runs for set duration of time then the weather is checked again
                current = dt.strftime(dt.now(),'%X')
                delta = dt.strptime(current, FMT) - dt.strptime(start, FMT)

                if delta.total_seconds() == 0 :
                    drop_position = []
                else:
                    drop_position = data[0] 

                data = precipitation(drop_positions=drop_position, weather='rain')

                NL.send(data[1])
                time.sleep(0.35)
                if delta.total_seconds() >= check_interval:
                    break
        elif weather_icon in snowy_in:
            while True:
                current = dt.strftime(dt.now(),'%X')
                delta = dt.strptime(current, FMT) - dt.strptime(start, FMT)

                if delta.total_seconds() == 0:
                    drop_position = []
                else:
                    drop_position = data[0] 

                data = precipitation(drop_positions=drop_position, weather='snow')

                NL.send(data[1], random.randint(5,8))
                time.sleep(0.55)
                if delta.total_seconds() >= check_interval:
                    break
        elif weather_icon in thunder_in:
            while True:
                current = dt.strftime(dt.now(),'%X')
                delta = dt.strptime(current, FMT) - dt.strptime(start, FMT)

                if delta.total_seconds() == 0:
                    drop_position = []
                else:
                    drop_position = data[0] 

                data = lightning(drop_positions=drop_position)

                NL.send(data[1])
                #time.sleep(0.55)
                if delta.total_seconds() >= check_interval:
                    break
        elif weather_icon in cloudy_in:
            while True:
                current = dt.strftime(dt.now(),'%X')
                delta = dt.strptime(current, FMT) - dt.strptime(start, FMT)

                if delta.total_seconds() == 0:
                    sky_position = pd.DataFrame()
                else:
                    sky_position = data

                data = cloudy(sky_position)
                
                NL.simSend(data.drop(columns=23))
                time.sleep(0.55)
        elif weather_icon in night_in:
            print('night')
            time.sleep(check_interval)
        else:
            while True:
                current = dt.strftime(dt.now(),'%X')
                delta = dt.strptime(current, FMT) - dt.strptime(start, FMT)
                data = sunny(rays=1)
                NL.send(data, random.randint(1,3))          #sends the data to the nanoleaf
                time.sleep(3)               #sets a timer of three seconds between images
                data = sunny(rays=2)
                NL.simSend(data, random.randint(1,3))
                time.sleep(3)               #sets a timer of three seconds between images
                if delta.total_seconds() >= check_interval:
                    break

main()