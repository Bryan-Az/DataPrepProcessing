# importing pandas for data manipulation
import pandas as pd
# importing geocoding library to get latitude and longitude
from geopy.geocoders import GoogleV3
fatalities_spatiotemporal_df = pd.read_csv('Fatalities_Israel-Palestine.zip', compression='zip')
# imput age with the median
fatalities_spatiotemporal_df['age'].fillna(fatalities_spatiotemporal_df['age'].median(), inplace=True)
text_columns = [
    'name', 'citizenship', 'event_location', 'event_location_district',
    'event_location_region', 'gender', 'place_of_residence',
    'place_of_residence_district', 'type_of_injury', 'ammunition',
    'killed_by', 'notes', 'took_part_in_the_hostilities'
]
# replace 'nan' with 'unknown' in text columns
for column in text_columns:
    if column in fatalities_spatiotemporal_df.columns:
        fatalities_spatiotemporal_df[column].replace('nan', 'Unknown', inplace=True)

googleAPIkey = 'your-api-key' #replace with your api key
# using geopy to get latitude and longitude
geolocator = GoogleV3(api_key=googleAPIkey)
# use geolocator to get latitude and longitude for event_location
fatalities_spatiotemporal_df['event_location_latitude'] = fatalities_spatiotemporal_df['event_location'].apply(lambda x: geolocator.geocode(x).latitude if geolocator.geocode(x) else 'Not Found')
fatalities_spatiotemporal_df['event_location_longitude'] = fatalities_spatiotemporal_df['event_location'].apply(lambda x: geolocator.geocode(x).longitude if geolocator.geocode(x) else 'Not Found')
fatalities_spatiotemporal_df.iloc[:, -2:].describe()
fatalities_spatiotemporal_df.iloc[:, -2:].isna().sum()
print('% of rows to be dropped because geolocation data was not returned using the event_location column to infer latitude and longitude using the GoogleCloud Geolocation API: ', fatalities_spatiotemporal_df.event_location_longitude.value_counts()['Not Found'] / fatalities_spatiotemporal_df.shape[0])
# Drop rows where the geolocation is 'Not Found' in both the latitude and longitude columns
fatalities_spatiotemporal_df.drop(fatalities_spatiotemporal_df[fatalities_spatiotemporal_df['event_location_latitude'] == 'Not Found'].index, inplace=True)
fatalities_spatiotemporal_df.drop(fatalities_spatiotemporal_df[fatalities_spatiotemporal_df['event_location_longitude'] == 'Not Found'].index, inplace=True)
fatalities_spatiotemporal_df.to_csv('Fatalities_Israel-Palestine_with_GEO.csv', index=False)