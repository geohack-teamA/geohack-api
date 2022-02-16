from typing import Any, Optional
import warnings

from app.dependencies.gcp.storage import GoogleCloudStorage
from numpy import uint

warnings.simplefilter("ignore")

import pandas as pd
import geopandas as gpd
import jismesh.utils as ju
from shapely.geometry import *
from geopy.distance import geodesic


class GeospatialAnalyzer:
    def __init__(
        self, storage: GoogleCloudStorage, lat: float, lng: float, mesh_level: uint
    ) -> None:
        self.__storage = storage
        self.__bucket = self.__storage.bucket()
        self.__lat = lat
        self.__lng = lng
        self.__mesh_level = mesh_level

    def storage(self) -> GoogleCloudStorage:
        return self.__storage

    def bucket(self):
        return self.__bucket

    def lat(self):
        return self.__lat

    def lng(self):
        return self.__lng

    def mesh_level(self):
        return self.__mesh_level

    def get_geometric_file_by_meshcode(self, meshcode: str):
        geometry_file = self.storage().get_blob_by_name(
            f"/buidlings/kawasaki/bldg_{meshcode}.geojson"
        )
        return geometry_file

    def get_shelter_file(self):
        shelter_file = self.storage().get_blob_by_name("/shelters/kawasaki/shelter.csv")
        return shelter_file

    # TODO: improve typing here
    @staticmethod
    def get_meshcode(lat: float, lng: float, level: uint) -> Any:
        meshcode = ju.to_meshcode(lat, lng, level)
        return meshcode

    def get_building_by_position(self):
        mesh_code = GeospatialAnalyzer.get_meshcode(
            self.lat(), self.lng(), self.mesh_level()
        )
        geometry_file = self.get_geometric_file_by_meshcode(mesh_code)
        position = gpd.GeoDataFrame({"geometry": Point(self.lng(), self.lat())}, [0])
        result = gpd.sjoin(position, geometry_file, how="inner", op="within")

    def get_nearest_shelter(self):
        shelter_blob = self.get_shelter_file()
        if shelter_blob == None:
            return None
        # shelter_csv = pd.read_csv(str(shelter_blob, "UTF-8"))

    def analyze(self):
        pass


def run(bldg_geojson, shelter, gps_lon, gps_lat):
    evacuee_gps = gpd.GeoDataFrame({"geometry": Point(gps_lon, gps_lat)}, [0])
    result = gpd.sjoin(evacuee_gps, bldg_geojson, how="inner", op="within")

    if len(result) == 0:
        shelter["gps_lat"] = gps_lat
        shelter["gps_lon"] = gps_lon
        shelter["distance"] = shelter.apply(
            lambda x: geodesic([x["lat"], x["lon"]], [x["gps_lat"], x["gps_lon"]]).m,
            axis=1,
        )
        building_name = shelter.sort_values(by="distance").iloc[0, 1]

        return {
            "building": name,
            "storeysAboveGround": None,
            "height": None,
            "depth": None,
            "depth_rank": None,
        }

    else:
        evacuee_gps = gpd.GeoDataFrame({"geometry": Point(gps_lon, gps_lat)}, [0])
        result = gpd.sjoin(evacuee_gps, bldg_geojson, how="inner", op="within")

        bulding_id = result.sort_values(by="depth", ascending=False).iloc[0, 2]
        storeysAboveGround = result.sort_values(by="depth", ascending=False).iloc[0, 3]
        height = result.sort_values(by="depth", ascending=False).iloc[0, 4]
        depth = result.sort_values(by="depth", ascending=False).iloc[0, 5]
        depth_rank = result.sort_values(by="depth", ascending=False).iloc[0, 6]

        bulding_id = result.sort_values(by="depth", ascending=False).iloc[0, 2]
        return {
            "building": bulding_id,
            "storeysAboveGround": storeysAboveGround,
            "height": height,
            "depth": depth,
            "depth_rank": depth_rank,
        }


if __name__ == "__main__":
    gps_lat = 35.60044590382672
    gps_lon = 139.6295136313999
    meshcode = ju.to_meshcode(gps_lat, gps_lon, 3)
    bldg_geojson = gpd.read_file(f"../data/input/bldg_geojson/bldg_{meshcode}.geojson")
    shelter = pd.read_csv("../data/input/shelter.csv")

    result = run(bldg_geojson, shelter, gps_lon, gps_lat)
    print(result)
