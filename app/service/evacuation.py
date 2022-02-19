from typing import Optional, Tuple
from app.models.alert_level import AlertLevel
from app.service.geospatial import Building, GeospatialAnalyzer, Shelter


def get_alert_level() -> AlertLevel:
    # TODO: fetch data from extenal API
    alert_level = AlertLevel.THREE
    return alert_level


class Position:
    def __init__(self, lat: float, lng: float):
        self.__lat = lat
        self.__lng = lng

    def position(self) -> Tuple[float, float]:
        return self.__lat, self.__lng

    def lat(self) -> float:
        return self.__lat

    def lng(self) -> float:
        return self.__lng


class UserAttribute:
    def __init__(
        self,
        lat: float,
        lng: float,
        current_floor_level: int,
        has_difficulty_with_family: bool,
        enough_stock: bool,
    ):
        self.__position = Position(lat=lat, lng=lng)
        self.__current_floor_level = current_floor_level
        self.__has_difficulty_with_family = has_difficulty_with_family
        self.__enough_stock = enough_stock

    def position(self) -> Position:
        return self.__position

    def current_floor_level(self) -> int:
        return self.__current_floor_level

    def has_difficulty_with_family(self) -> bool:
        return self.__has_difficulty_with_family

    def enough_stock(self) -> bool:
        return self.__enough_stock


class UserEvacuationJudgement:
    def __init__(
        self,
        user_attribute: UserAttribute,
        geospatial_analyzer: GeospatialAnalyzer,
    ):
        self.__user_attribute = user_attribute
        self.__current_alert_level = get_alert_level()
        self.__geospatial_analyzer = geospatial_analyzer

    def user_attribute(self) -> UserAttribute:
        return self.__user_attribute

    def current_alert_level(self) -> AlertLevel:
        return self.__current_alert_level

    def geospatial_analyzer(self) -> GeospatialAnalyzer:
        return self.__geospatial_analyzer

    def may_user_building_been_broken(self) -> bool:
        # TODO: write here
        return False

    def is_user_building_higher_than_flood_depth(self) -> bool:
        # TODO: write here
        return False

    def is_user_current_level_higher_than_flood_depth(self) -> bool:
        # TODO: write here
        return False

    def has_enough_stock(self) -> bool:
        return self.user_attribute().enough_stock()

    def does_user_have_difficult_family(self) -> bool:
        return self.user_attribute().has_difficulty_with_family()

    def is_building_depth_less_than_flood_level(self) -> bool:
        return False

    def is_current_level_less_than_flood_level(self) -> bool:
        return False

    def judge_what_user_should_do(
        self,
    ) -> Tuple[bool, str, Optional[Shelter], Optional[Building]]:
        current_position = self.user_attribute().position()
        lat, lng = current_position.position()
        user_building = self.geospatial_analyzer().get_building_by_position(lat, lng)
        nearest_shelter = self.geospatial_analyzer().get_nearest_shelter(lat, lng)
        if user_building is None:
            if nearest_shelter is None:
                return False, "そのまま自宅待機してください", nearest_shelter, user_building
            return True, "屋外にいますか？今すぐ避難してください", nearest_shelter, None
        if self.may_user_building_been_broken():
            if get_alert_level() == AlertLevel.THREE:
                if self.does_user_have_difficult_family():
                    return True, "屋外にいますか？今すぐ避難してください", None, user_building
                else:
                    return True, "屋外にいますか？今すぐ避難してください", nearest_shelter, None
            else:
                return True, "屋外にいますか？今すぐ避難してください", nearest_shelter, None
        if self.is_building_depth_less_than_flood_level():
            if self.is_current_level_less_than_flood_level():
                if self.has_enough_stock():
                    return False, "そのまま自宅待機してください", None, user_building
                else:
                    if get_alert_level() == AlertLevel.THREE:
                        if self.does_user_have_difficult_family():
                            return False, "そのまま自宅待機してください", None, user_building
                        else:
                            return True, "屋外にいますか？今すぐ避難してください", nearest_shelter, None
                    else:
                        return False, "そのまま自宅待機してください", None, user_building
        return False, "そのまま自宅待機してください", None, user_building
