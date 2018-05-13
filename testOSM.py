# -*-coding:Utf-8 -*
#http://www.fabienpoulard.info/post/2011/01/24/Interroger-OpenStreetMap-en-Python-avec-OsmApi
#http://osmapi.metaodi.ch/
# attention python 2
# http://overpass-turbo.eu/ equivalement sparl
# exemple https://georezo.net/forum/viewtopic.php?id=90141
# doc overpass https://wiki.openstreetmap.org/wiki/FR:Overpass_API/Overpass_QL#Par_attribut_.28has-kv.29
# idee recup id node avec overpass et recup info avec osmapi getnode (dico)
#Cf exemple en commentaire pour champs à récupérer
import OsmApi
MyApi = OsmApi.OsmApi()
def Map(self, min_lon, min_lat, max_lon, max_lat):
    """
    Download data in bounding box.
    Returns list of dict:
        #!python
        {
            type: node|way|relation,
            data: {}
        }
    """
    uri = (
        "/api/0.6/map?bbox=%f,%f,%f,%f"
        % (min_lon, min_lat, max_lon, max_lat)
    )
    data = self._get(uri)
    return self.ParseOsm(data)
print MyApi.NodeGet(1902399720)

