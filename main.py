'''This application connects to the USGS and OpenCage API's to collect earthquake data and store it in
a csv file that is overwritten whenever the app is ran'''

import requests, xmltodict, json, csv, toTime, creds    

response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson")

#if connected to USGS API
if response:

    #open file as append
    with open("earthquakes.csv", "w") as output:
        writer = csv.writer(output, lineterminator="\n")

        #load USGS json data
        data = json.loads(response.text)

        #drill down to earthquakes
        quakes = data["features"] 

        #loop through each quake and id each quality
        for quake in quakes:
            mag = str(quake["properties"]["mag"])
            time = toTime.conv(quake["properties"]["time"])
            long = str(quake["geometry"]["coordinates"][0])
            lat = str(quake["geometry"]["coordinates"][1])
            coord = "(" + lat + ", " + long + ")"

            #put together OpenCage API url
            base_url = "https://api.opencagedata.com/geocode/v1/xml?q="
            full_url =  base_url + lat + "+" + long + creds.api_key
            response2 = requests.get(full_url)

            #if connected to OpenCage API
            if response2:
                data2 = xmltodict.parse(response2.text)

                category = data2["response"]["results"]["result"]["components"]["_category"]
                
                #if in ocean
                if category == "natural/water":
                    print("Magnitude " + mag + " earthquake on " + time + " and located at " + coord + " in the ocean.\n")

                    #write to output file
                    row = [time, mag, lat, long, "N/A", "N/A"]
                    writer.writerow(row)
        
                #if on land:
                else:
                    country = data2["response"]["results"]["result"]["components"]["country"]
                    
                    #if in USA
                    if country == "United States":

                        #if county attribute exists
                        try:
                            county = data2["response"]["results"]["result"]["components"]["county"]
                            state = data2["response"]["results"]["result"]["components"]["state"]
                            print("Magnitude " + mag + " earthquake on " + time + " and located at " + coord + " in " + county + ", " + state + ".\n")

                            #write to output file
                            row = [time, mag, lat, long, county, state]
                            writer.writerow(row)
                        
                        #if county attribute missing
                        except:
                            print("Magnitude " + mag + " earthquake on " + time + " and located at " + coord + " in the US.\n")

                            #write to output file
                            row = [time, mag, lat, long, "N/A", "N/A"]
                            writer.writerow(row)

            #if couldn't connect to OpenCage API
            else:
                print("Could not connect to OpenCage API")

#if couldn't connect to USGS API
else:
    print("Could not connect to USGS API")
