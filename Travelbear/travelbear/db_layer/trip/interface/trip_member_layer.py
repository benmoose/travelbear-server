from django.db import IntegrityError

from ..helpers.user_trips import user_trips_qs
from ..models import TripMember


class UserIsAlreadyMember(IntegrityError):
    pass


def add_member_to_trip(user, trip, is_admin=False):
    if is_user_member_of_trip(user, trip):
        # need to raise because if user already exists their is_admin is not updated
        raise UserIsAlreadyMember
    return TripMember.objects.create(user=user, trip=trip, is_admin=is_admin)


def get_members_of_trip(trip):
    return list(TripMember.objects.filter(trip=trip).prefetch_related("trip"))


def get_trips_for_user(user, ascending=False):
    return list(
        user_trips_qs(user).order_by("created_on" if ascending else "-created_on")
    )


def is_user_member_of_trip(user, trip):
    return TripMember.objects.filter(user=user, trip=trip).exists()
