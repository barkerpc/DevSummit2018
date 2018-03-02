#API Reference https://developers.arcgis.com/rest/packaging/api-reference/create-map-area.htm
from arcgis.gis import GIS
from arcgis.mapping import WebMap
import json

with open('creds\creds.json') as json_data:
    # Grab the credential object
    d = json.load(json_data)

# setup the portal
gis = GIS(d[1]['portal'], d[1]['user'], d[1]['pass'])

#get the webmap to use offline
offline_map_item = gis.content.get('c9db4302670347a4830e94927764187e')
offline_webmap = WebMap(offline_map_item)

#loop through the webmap's bookmarks and try to create a map area for each one
offline_areas = offline_webmap.offline_areas

#Cleanup and remove existing preplanned areas
for ids in offline_areas.list():

    ids.delete()

for bookmark in offline_webmap.definition.bookmarks:
    name = bookmark.name

    try:
        offline_area = offline_areas.create(area=name,
                                            title=name + ' Offline Area',
                                            snippet='Offline map area created using Python API',
                                            tags='automation',
                                            folder_name='DevSummit 2018')
        print("submitting jobs for " + name)

    except:
       print("failed creating map area " + name)

