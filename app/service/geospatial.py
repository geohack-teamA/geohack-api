from typing import Any, Optional
import warnings
import pandas as pd
import geopandas as gpd
import jismesh.utils as ju
from shapely.geometry import *  # noqa
from geopy.distance import geodesic

from app.dependencies.gcp.storage import GoogleCloudStorage
from numpy import uint

warnings.simplefilter("ignore")


class Shelter:
    def __init__(self, name: str, lat: float, lng: float):
        self.name = name
        self.lat = lat
        self.lng = lng


class Building:
    def __init__(
        self,
        id: str,
        storeys_above_ground: float,
        height: float,
        depth: float,
        depth_rank: float,
    ):
        self.id = id
        self.storeys_above_ground = storeys_above_ground
        self.height = height
        self.depth = depth
        self.depth_rank = depth_rank


class GeospatialAnalyzer:
    def __init__(self, storage: GoogleCloudStorage, mesh_level: uint) -> None:
        self.__storage = storage
        self.__bucket = self.__storage.bucket()
        self.__mesh_level = mesh_level

    # ******Getter******
    def storage(self) -> GoogleCloudStorage:
        return self.__storage

    def bucket(self):
        return self.__bucket

    def mesh_level(self):
        return self.__mesh_level

    # ******Get files from external datasource******
    def get_geometric_file_by_meshcode(self, meshcode: str):
        geometry_file = self.storage().get_blob_by_name(
            f"buildings/kawasaki/bldg_{meshcode}.geojson"
        )
        return geometry_file

    def get_shelter_file(self):
        shelter_file = self.storage().get_blob_by_name("shelters/kawasaki/shelter.csv")
        return shelter_file

    # TODO: improve typing here
    @staticmethod
    def get_meshcode(lat: float, lng: float, level: uint) -> Any:
        meshcode = ju.to_meshcode(lat, lng, level)
        return meshcode

    # ******Core logics******
    def get_building_by_position(self, lat: float, lng: float) -> Optional[Building]:
        mesh_code = GeospatialAnalyzer.get_meshcode(lat, lng, self.mesh_level())

        # mesh_codeから対象のGeoJSONファイルをGCSから取得
        geometry_file = self.get_geometric_file_by_meshcode(mesh_code)
        if geometry_file is None:
            return None
        geo_data_frame = gpd.read_file(
            GoogleCloudStorage.convert_blob_to_byte_string(geometry_file)
        )
        point = Point(lng, lat)  # noqa
        position = gpd.GeoDataFrame({"geometry": point}, [0])

        # ユーザー位置情報とGeoJSONデータを空間結合・ユーザーが居る建物情報を取得
        result = gpd.sjoin(position, geo_data_frame, how="inner", op="within")
        building = result.sort_values(by="depth", ascending=False).iloc[0]
        building_id = building[2]
        storeys_above_ground = building[3]
        height = building[4]
        depth = building[5]
        depth_rank = building[6]

        return Building(building_id, storeys_above_ground, height, depth, depth_rank)

    def get_nearest_shelter(self, lat: float, lng: float) -> Optional[Shelter]:
        # 避難所一覧情報(lat, lng, name)をGCSから取得
        shelter_blob = self.get_shelter_file()
        if shelter_blob is None:
            return None

        # 避難所一覧から最寄りの避難所を取得
        data_frame = pd.read_csv(
            GoogleCloudStorage.convert_blob_to_byte_string(shelter_blob)  # noqa
        )
        data_frame["gps_lat"] = lat
        data_frame["gps_lon"] = lng
        data_frame["distance"] = data_frame.apply(
            lambda x: geodesic([x["lat"], x["lon"]], [x["gps_lat"], x["gps_lon"]]).m,
            axis=1,
        )

        nearest_shelter = data_frame.sort_values(by="distance").iloc[0]
        shelter_name = nearest_shelter[1]
        shelter_lat = nearest_shelter[2]
        shelter_lng = nearest_shelter[3]
        return Shelter(shelter_name, shelter_lat, shelter_lng)
