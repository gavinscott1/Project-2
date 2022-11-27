import json     #accu weather data comes as json format so we need module to decode and change to a usable type
import pandas as pd
import urllib.request
import random
from datetime import datetime as dt
import time
import UCNanoleaf as NL
#Project By; Tanner O., Morgan H., Gavin S., Reid M.

#ADDING THIS COMMENT TO CHANGE THE CODE FOR GITHUB

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

def night_time():
    null = (12, 20, 69) #using this vairable to show triangles out of the shape of the Nanoleaf helps for the dataframe below when I was designing
    bg = (12, 20, 69) #night background colour
    star = (250, 254, 250)  #star colour #FIXME
    moon = (240,196,32) #moon main colour     
    accent= (245,217,113)    #moon accent colour


    moon_data = [              #sets initial colours of each triangle (12 indexs, 23 columns) adding two additional columns to the end to allow the df to check first two columns for star positioning below
                [null,null,null,null,null,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,null,null,null,null,null],
        [null,null,null,null,bg,bg,bg,bg,bg,bg,moon,accent,moon,moon,accent,bg,bg,bg,bg,null,null,null,null],
        [null,null,null,bg,bg,bg,bg,moon,moon,accent,moon,moon,accent,moon,moon,moon,moon,accent,bg,bg,null,null,null],
        [null,null,bg,bg,bg,bg,moon,accent,moon,accent,bg,bg,bg,bg,bg,moon,moon,accent,bg,bg,bg,null,null],
        [null,bg,bg,bg,bg,moon,moon,accent,moon,bg,bg,bg,bg,bg,bg,bg,moon,bg,bg,bg,bg,bg,null],
        [bg,bg,bg,bg,moon,moon,accent,moon,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [bg,bg,bg,bg,moon,moon,moon,accent,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg],
        [null,bg,bg,bg,bg,moon,moon,accent,moon,bg,bg,bg,bg,bg,bg,bg,bg,bg,moon,bg,bg,bg,null],
        [null,null,bg,bg,bg,bg,moon,accent,moon,accent,bg,bg,bg,bg,bg,bg,bg,moon,accent,bg,bg,null,null],
        [null,null,null,bg,bg,bg,bg,moon,moon,moon,accent,moon,moon,moon,moon,moon,accent,moon,bg,bg,null,null,null],
        [null,null,null,null,bg,bg,bg,bg,bg,bg,moon,moon,accent,moon,moon,bg,bg,bg,bg,null,null,null,null],
        [null,null,null,null,null,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,bg,null,null,null,null,null]
    ]
    moon_df = pd.DataFrame(moon_data)   #makes it into a pandas dataframe

    for index in range(12):
        for column in range(23):
            
            moon_colours = [moon, accent]

            if (moon_df.iat[index,column] in moon_colours): #changes the colours of moon spaces between the accent and moon colour randomly creating a twinkle effect
                potential_colours = [moon, accent]
                moon_df.iat[index,column] = potential_colours[random.randrange(len(potential_colours))]

            if (moon_df.iat[index,column] == bg):    #randomly changes the colour of background to either be a star or stay as background to create dynamic glimmeirng start
                potential_colours = [star, bg, bg, bg, bg] #gives star generation 1/5 chance
                moon_df.iat[index,column] = potential_colours[random.randrange(len(potential_colours))]


                if moon_df.iat[index,column] == star:
                #tracking the star placement to ensure they don't generate too close to the moon or each other

                    if (index == 0) and (column == 0): 
                        continue 

                    elif (index == 0) and (column == 1):
                        continue

                    elif (index == 0) and (column == 21):
                        continue

                    elif (index == 0) and (column == 22):
                        continue

                    elif (index == 11) and (column == 0):
                        continue

                    elif (index == 11) and (column == 1):
                        continue
                    
                    elif (index == 11) and (column == 21):
                        continue 
                
                    elif (index == 11) and (column == 22):
                        continue

                    else:

                        if index == 0: #No need to check above (star or moon) or no need to check for moon on same row
                            
                            if  (moon_df.iat[index,column - 1] == star) or (moon_df.iat[index,column - 2] == star):
                                moon_df.iat[index,column] = bg  #checks to see if either of the two triangles before it are already a star (no need to check after as it runs line by line) and changes it back to a background colour if it is the case (not worried about the edge given its null at both ends)

                            elif (moon_df.iat[index + 1,column - 2] in moon_colours) or (moon_df.iat[index + 1,column - 1] in moon_colours) or (moon_df.iat[index + 1,column] in moon_colours) or (moon_df.iat[index + 1 ,column + 1] in moon_colours) or (moon_df.iat[index + 1,column +2] in moon_colours):
                                moon_df.iat[index,column] = bg  #check to see if any of the five triangles directly below the star are either of the moon colours and changes it back to a background colour if it is the case

                        elif index == 11: #No need to check for moon below or moon on same index at all 
                            
                            if  (moon_df.iat[index,column - 1] == star) or (moon_df.iat[index,column - 2] == star):
                                moon_df.iat[index,column] = bg  #checks to see if either of the two triangles before it are already a star (no need to check after as it runs line by line) and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index - 1,column - 2] in moon_colours) or (moon_df.iat[index - 1,column - 1] in moon_colours) or (moon_df.iat[index - 1,column] in moon_colours) or (moon_df.iat[index - 1 ,column + 1] in moon_colours) or (moon_df.iat[index - 1,column +2] in moon_colours):
                                moon_df.iat[index,column] = bg  #check to see if any of the five triangles directly above the star are either of the moon colours and changes it back to a background colour if it is the case
                         
                            elif (moon_df.iat[index - 1,column - 2] == star) or (moon_df.iat[index - 1,column - 1] == star) or (moon_df.iat[index - 1,column] == star) or (moon_df.iat[index -1 ,column + 1] == star) or (moon_df.iat[index -1,column +2] == star):
                                moon_df.iat[index,column] = bg  #checks to see if any of the five trianlges above it are already a star and changes it back to a background colour if it is the case

                        elif column == 0: #no need to check column 1 and 2 before 

                            if (moon_df.iat[index - 1,column] == star) or (moon_df.iat[index -1 ,column + 1] == star) or (moon_df.iat[index -1,column +2] == star):
                                moon_df.iat[index,column] = bg  #checks to see if any of the three trianlges above it (above and 2 columns to the right) are already a star and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index - 1,column] in moon_colours) or (moon_df.iat[index -1 ,column + 1] in moon_colours) or (moon_df.iat[index -1,column +2] in moon_colours):
                                moon_df.iat[index,column] = bg #checks to see if any of the 3 triangles above it are moon coloured and changes it back to a background colour if it is the case (no need to check column -1 or -2)

                            elif (moon_df.iat[index + 1,column] in moon_colours) or (moon_df.iat[index + 1 ,column + 1] in moon_colours) or (moon_df.iat[index + 1,column +2] in moon_colours):
                                moon_df.iat[index,column] = bg #check to see if any of the 3 triangles directly below the star are the moon colour and changes it back to a background colour if it is the case (no need to check column -1 or -2)

                            elif (moon_df.iat[index,column + 1] in moon_colours) or (moon_df.iat[index,column + 2] in moon_colours):
                                moon_df.iat[index,column] = bg  #checks to see if any of the two triangles past the star are a moon coloured and changes it back to a background colour if it is the case

                        elif column == 1: #no need to check 2 before (only 1)
                            if  (moon_df.iat[index,column - 1] == star):
                                moon_df.iat[index,column] = bg  #checks to see if either of the one triangles before it are already a star (no need to check after as it runs line by line) and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index - 1,column - 1] == star) or (moon_df.iat[index - 1,column] == star) or (moon_df.iat[index -1 ,column + 1] == star) or (moon_df.iat[index -1,column +2] == star):
                                moon_df.iat[index,column] = bg  #checks to see if any of the four trianlges above it (1 column to the left, above it, and 2 columns to the right) are already a star and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index - 1,column - 1] in moon_colours) or (moon_df.iat[index - 1,column] in moon_colours) or (moon_df.iat[index -1 ,column + 1] in moon_colours) or (moon_df.iat[index -1,column +2] in moon_colours):
                                moon_df.iat[index,column] = bg  #checks to see if any of the four triangles above it are moon coloured and changes it back to a background colour if it is the case (no need to do column - 2)

                            elif (moon_df.iat[index + 1,column - 1] in moon_colours) or (moon_df.iat[index + 1,column] in moon_colours) or (moon_df.iat[index + 1 ,column + 1] in moon_colours) or (moon_df.iat[index + 1,column +2] in moon_colours):
                                moon_df.iat[index,column] = bg #check to see if any of the four triangles directly below the star are the moon colour and changes it back to a background colour if it is the case (no need to do column - 2)

                            elif (moon_df.iat[index,column + 1] in moon_colours) or (moon_df.iat[index,column + 2] in moon_colours):
                                moon_df.iat[index,column] = bg  #checks to see if any of the two triangles past the star are a moon coloured and changes it back to a background colour if it is the case

                        elif column == 21: #no need to check moon 2 past it (only one past it)

                            if  (moon_df.iat[index,column - 1] == star) or (moon_df.iat[index,column - 2] == star):
                                moon_df.iat[index,column] = bg  #checks to see if either of the two triangles before it are already a star (no need to check after as it runs line by line) and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index - 1,column - 2] == star) or (moon_df.iat[index - 1,column - 1] == star) or (moon_df.iat[index - 1,column] == star) or (moon_df.iat[index -1 ,column + 1] == star):
                                moon_df.iat[index,column] = bg  #checks to see if any of the four trianlges above it are already a star and changes it back to a background colour if it is the case

                            elif  (moon_df.iat[index,column - 1] in moon_colours) or (moon_df.iat[index,column - 2] in moon_colours):
                                moon_df.iat[index,column] = bg #checks to see if either of the two trianges before it are moon coloured and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index,column + 1] in moon_colours):
                                moon_df.iat[index,column] = bg  #checks to see if the one triangle past the star are a moon coloured and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index - 1,column - 2] in moon_colours) or (moon_df.iat[index - 1,column - 1] in moon_colours) or (moon_df.iat[index - 1,column] in moon_colours) or (moon_df.iat[index -1 ,column + 1] in moon_colours):
                                moon_df.iat[index,column] = bg #checks to see if any of the 4 triangles (not farthest right) above it are moon coloured and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index + 1,column - 2] in moon_colours) or (moon_df.iat[index + 1,column - 1] in moon_colours) or (moon_df.iat[index + 1,column] in moon_colours) or (moon_df.iat[index + 1 ,column + 1] in moon_colours):
                                moon_df.iat[index,column] = bg #check to see if any of the 4 triangles (not farthest right) directly below the star are the moon colour and changes it back to a background colour if it is the case

                        elif column == 22: #no need to check moon past it at all
                            
                            if  (moon_df.iat[index,column - 1] == star) or (moon_df.iat[index,column - 2] == star):
                                moon_df.iat[index,column] = bg  #checks to see if either of the two triangles before it are already a star (no need to check after as it runs line by line) and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index - 1,column - 2] == star) or (moon_df.iat[index - 1,column - 1] == star) or (moon_df.iat[index - 1,column] == star):
                                moon_df.iat[index,column] = bg  #checks to see if any of the three trianlges above it are already a star and changes it back to a background colour if it is the case

                            elif  (moon_df.iat[index,column - 1] in moon_colours) or (moon_df.iat[index,column - 2] in moon_colours):
                                moon_df.iat[index,column] = bg #checks to see if either of the two trianges before it are moon coloured and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index - 1,column - 2] in moon_colours) or (moon_df.iat[index - 1,column - 1] in moon_colours) or (moon_df.iat[index - 1,column] in moon_colours):
                                moon_df.iat[index,column] = bg #checks to see if any of the 3 triangles (not the 2 farthest right) above it are moon coloured and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index + 1,column - 2] in moon_colours) or (moon_df.iat[index + 1,column - 1] in moon_colours) or (moon_df.iat[index + 1,column] in moon_colours):
                                moon_df.iat[index,column] = bg #check to see if any of the 4 triangles (not the 2 farthest right) directly below the star are the moon colour and changes it back to a background colour if it is the case

                        else: #any non corcern of df index and column

                            #only need these two for stars no need to check after the star or below as not generated yet
                            if  (moon_df.iat[index,column - 1] == star) or (moon_df.iat[index,column - 2] == star):
                                moon_df.iat[index,column] = bg  #checks to see if either of the two triangles before it are already a star (no need to check after as it runs line by line) and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index - 1,column - 2] == star) or (moon_df.iat[index - 1,column - 1] == star) or (moon_df.iat[index - 1,column] == star) or (moon_df.iat[index -1 ,column + 1] == star) or (moon_df.iat[index -1,column +2] == star):
                                moon_df.iat[index,column] = bg  #checks to see if any of the five trianlges above it are already a star and changes it back to a background colour if it is the case


                            elif  (moon_df.iat[index,column - 1] in moon_colours) or (moon_df.iat[index,column - 2] in moon_colours):
                                moon_df.iat[index,column] = bg #checks to see if either of the two trianges before it are moon coloured and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index,column + 1] in moon_colours) or (moon_df.iat[index,column + 2] in moon_colours):
                                moon_df.iat[index,column] = bg  #checks to see if any of the two triangles past the star are a moon coloured and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index - 1,column - 2] in moon_colours) or (moon_df.iat[index - 1,column - 1] in moon_colours) or (moon_df.iat[index - 1,column] in moon_colours) or (moon_df.iat[index -1 ,column + 1] in moon_colours) or (moon_df.iat[index -1,column +2] in moon_colours):
                                moon_df.iat[index,column] = bg #checks to see if any of the 5 triangles above it are moon coloured and changes it back to a background colour if it is the case

                            elif (moon_df.iat[index + 1,column - 2] in moon_colours) or (moon_df.iat[index + 1,column - 1] in moon_colours) or (moon_df.iat[index + 1,column] in moon_colours) or (moon_df.iat[index + 1 ,column + 1] in moon_colours) or (moon_df.iat[index + 1,column +2] in moon_colours):
                                moon_df.iat[index,column] = bg #check to see if any of the five triangles directly below the star are the moon colour and changes it back to a background colour if it is the case

    return moon_df


def main():
    NL.initalize()
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
        weather_icon = 33
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
                time.sleep(0.55)
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
                time.sleep(0.35)
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
                time.sleep(0.55)
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
                
                NL.send(data.drop(columns=23))
                time.sleep(1.2)
                

        elif weather_icon in night_in:
            while True:
                current = dt.strftime(dt.now(),'%X')
                delta = dt.strptime(current, FMT) - dt.strptime(start, FMT)
                data = night_time()
                NL.simSend(data, random.randint(1,3))          #sends the data to the nanoleaf
                time.sleep(1)               #sets a timer of three seconds between images
                if delta.total_seconds() >= check_interval:
                    break

        else:
            while True:
                current = dt.strftime(dt.now(),'%X')
                delta = dt.strptime(current, FMT) - dt.strptime(start, FMT)
                data = sunny(rays=1)
                NL.send(data, random.randint(1,3))          #sends the data to the nanoleaf
                time.sleep(3)               #sets a timer of three seconds between images
                data = sunny(rays=2)
                NL.send(data, random.randint(1,3))
                time.sleep(3)               #sets a timer of three seconds between images
                if delta.total_seconds() >= check_interval:
                    break
if __name__ == '__main__':
    main()