from decimal import Decimal

import pytest

from db_layer.trip import Location
from db_layer.user import get_or_create_user
from .trip_layer import create_trip
from .location_layer import (
    create_location,
    delete_location,
    get_moves_starting_at_location,
    get_moves_ending_at_location,
)
from .move_layer import create_move


@pytest.fixture
def user():
    user, _ = get_or_create_user(external_id="test-id")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, title="test trip")


@pytest.mark.django_db
def test_create_location(trip):
    assert 0 == len(Location.objects.all())
    create_location(
        trip,
        display_name="London",
        lat=51.0056459234001,
        lng=0,
        google_place_id="foobar",
    )
    assert 1 == len(Location.objects.all())

    location_in_db = Location.objects.all()[0]
    assert location_in_db.display_name == "London"
    assert location_in_db.lat == Decimal("51.005646")
    assert location_in_db.lng == Decimal("0")
    assert location_in_db.google_place_id == "foobar"


@pytest.mark.django_db
def test_delete_location(trip):
    location = create_location(trip, display_name="London", lat=51, lng=0)
    assert not location.is_deleted

    returned_location = delete_location(location)

    assert returned_location.pk == location.pk
    assert returned_location.is_deleted
    location.refresh_from_db()
    assert location.is_deleted


@pytest.mark.django_db
def test_get_related_moves(trip):
    location_1 = create_location(trip, "location 1", lat=0, lng=0)
    location_2 = create_location(trip, "location 2", lat=0, lng=0)
    move_1 = create_move(location_1, location_2)
    move_2 = create_move(location_2, location_1)

    assert get_moves_starting_at_location(location_1) == [move_1]
    assert get_moves_starting_at_location(location_2) == [move_2]

    assert get_moves_ending_at_location(location_1) == [move_2]
    assert get_moves_ending_at_location(location_2) == [move_1]