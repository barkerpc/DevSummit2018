from arcgis.gis import GIS
import json

# Open the credential object and get the gis
with open('creds\creds.json') as json_data:
        d = json.load(json_data)

# Login to the GIS
gis = GIS(d[1]['portal'], d[1]['user'], d[1]['pass'])
append_layer_itemid = 'e7c55167622d4adabe5bd8c49c2f1c84'

# Grab the layer you want to append data into
fs_item = gis.content.get(append_layer_itemid)
fs_layer = fs_item.layers[0]

# Add the source file as an item to use with append
sourcefile = 'files\AnnualHydrantInspections.csv'
item_prop = {'title':'Temporary append file clean up later', 'type':'CSV'}
append_item = gis.content.add(item_properties=item_prop, data=sourcefile)


# Call analyze to get the source info about the file
analyze_results = gis.content.analyze(#url=None,
                                      item=append_item.id,
                                      #file_path=None,
                                      #text=None,
                                      file_type='csv',
                                      source_locale='en',
                                      #geocoding_service=None,
                                      location_type=coordinates,
                                      #source_country='None',
                                      #country_hint=None
                                      )


# Call append to add the records into the layer
try:
    fs_layer.append(item_id=append_item.id,
                    upload_format='csv',
                    source_table_name='',
                    field_mappings=[{"source":"AssignmentType","name":"assignmentType"},
                                    {"source":"Latitude","name":"Latitude"},
                                    {"source":"Longitude","name":"Longitude"},
                                    {"source":"Priority","name":"priority"},
                                    {"source":"Status","name":"status"},
                                    {"source":"workOrderID","name":"workOrderId"}],
                    edits=None,
                    source_info=analyze_results["publishParameters"],
                    upsert=False,
                    skip_updates=False,
                    use_globalids=False,
                    update_geometry=True,
                    append_fields=["assignmentType",
                                   "Latitude",
                                   "Longitude",
                                   "priority",
                                   "status",
                                   "workOrderId"],
                    rollback=True)
    print("Append completed successfully")
except:
    print("Something went wrong")

# Clean up the temporary append item now that its no longer needed
append_item.delete()

