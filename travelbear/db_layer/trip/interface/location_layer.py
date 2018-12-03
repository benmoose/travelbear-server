from django.db import transaction

from db_layer.trip import Location


def create_location(trip, display_name, lat, lng, google_place_id=""):
    return Location.objects.create(
        trip=trip,
        display_name=display_name,
        lat=lat,
        lng=lng,
        google_place_id=google_place_id,
    )


def delete_location(location):
    with transaction.atomic():
        location = Location.objects.select_for_update().get(pk=location.pk)
        if location.is_deleted:
            return location
        location.is_deleted = True
        location.save(update_fields=["is_deleted", "modified_on"])
    return location
