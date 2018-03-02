from arcgis.gis import GIS
import json

with open('creds\creds.json') as json_data:
    # Grab the credential object
    d = json.load(json_data)

# setup the portal
gis = GIS(d[1]['portal'], d[1]['user'], d[1]['pass'])

# get all of the feature services
search_results = gis.content.search("access:public type:Feature Service typekeywords:hosted", max_items=9999)
# list of capabilities to look for
fl_capabilities = ["Create", "Delete", "Update", "Editing"]

for result in search_results:
    try:
        result_fl = result.layers[0]
        result_capabilities = result_fl.properties.capabilities
        if any(x in result_capabilities for x in fl_capabilities):
            print(result.title + " " + result.owner + " is shared to the public and is editable")
    except:
        # Catch the error and ignore it if the item doesnt have a layers[] property
        print("")