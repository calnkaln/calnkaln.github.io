import csv

csv_path = 'water_quality_samples.csv'
output_path = 'webmap/data/water_quality_1.js'

template_start = 'var json_water_quality_1 = { "type": "FeatureCollection",\n "name": "water_quality_1",\n "crs": { "type": "name",\n "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }\n,"features": [\n'
template_end = ']}'

output = template_start

with open(csv_path, 'r') as csv_file_obj:
    csv_reader = csv.reader(csv_file_obj)
    csv_contents = [row for row in csv_reader]

lats, lons = [], []

for enum, row in enumerate(csv_contents):
    if enum == 0:
        continue
    name, lon, lat = row[3], row[6], row[5]
    lats.append(lat)
    lons.append(lon)
    print(name)
    date = row[1]
    source = row[4]
    source = source.replace(" ", "").lower()
    problem = row[9]
    desc = row[8]
    advice = row[7]

    table = "<table><tr><th>Date</th><th>Source</th><th>Problem</th><th>Desc</th><th>Adv</th></tr><tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr></table>".format(date, source, problem, desc, advice)
    
    feature = "{" + '"type": "Feature", "properties": {{"id": "{}", "name": "{} ({})", "source":"{}" }}, "geometry": {{ "type": "Point", "coordinates": [ {}, {} ] }}\n'.format(source, name, source, table, lon, lat) + "}"
    # feature = "{" + '"type": "Feature", "properties": {{ "source": "{}", "x": "'.format(name) + table + '", "type":"{}", "z":"" }}, "geometry": {{ "type": "Point", "coordinates": [ {}, {} ] }}\n'.format(source, lon, lat) + "}"
    if enum == 1:
        output = output + feature
    else:
        output = output + ',' + feature

maxLat, maxLon = max(lats), max(lons)
minLat, minLon = min(lats), min(lons)

output = output + template_end

with open(output_path, "w") as of:
    of.write(output)

with open('webmap/index.html', 'r') as file:
    # read a list of lines into data
    webmap_index = file.read().splitlines()
webmap_index[31] = "        }}).fitBounds([[{},{}],[{},{}]]);".format(minLat, minLon, maxLat, maxLon)
print(minLat, minLon, maxLat, maxLon)
with open('webmap/index.html', 'w', newline='\n') as file:
    file.writelines((s + '\n' for s in webmap_index))
