import json

from django.urls import reverse

meetup = {
    "title": "Meetup title",
    "body": "body of meetup this meetup",
    "date": "2019-03-07",
    "start": "10:21:39",
    "end": "12:21:39"
}
meetup_wrong = {"date": "2019-03-07", "start": "10:21:39", "end": "12:21:39"}


def test_non_admin_user_cannot_create_meetup(api_client, db, user1):
    api_client.force_authenticate(user=user1)

    response = api_client.post(
        reverse("meetings"),
        content_type="application/json",
        data=json.dumps(
            {
                "title": "Meetup title",
                "body": "body of meetup this meetup",
                "date": "2019-03-07",
                "start": "10:21:39",
                "end": "12:21:39",
            }
        ),
    )
    if not response.status_code == 401:
        raise AssertionError()

    if not response.data == {
        "status": 401,
        "error": "Action restricted to Admins!",
    }:
        raise AssertionError()


def test_post_meetup(api_client, db, admin_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse("meetings"),
        content_type="application/json",
        data=json.dumps(
            {
                "title": "Meetup title",
                "body": "body of meetup this meetup",
                "date": "2019-03-07",
                "start": "10:21:39",
                "end": "12:21:39"
            }
        ),
    )

    if not response.status_code == 201:
        raise AssertionError()

    if (
        response.data["data"][0]["success"] != "Meet up created successfully"
        or response.data["data"][0]["meetup"]["title"] != meetup["title"]
        or response.data["data"][0]["meetup"]["start"] != meetup["start"]
        or response.data["data"][0]["meetup"]["created_by"] != admin_user.id
    ):
        raise AssertionError()


def test_post_wrong_meetup(api_client, db, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        reverse("meetings"),
        content_type="application/json",
        data=json.dumps(meetup_wrong),
    )
    if not response.status_code == 400:
        raise AssertionError()

    if not response.data == {
        "status": 400,
        "error": {"title": ["This field is required."], "body": ["This field is required."]},
    }:
        raise AssertionError()


def test_get_meetups(api_client, db, admin_user, meetup1, tagged_meetup):
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(reverse("meetings"))

    if not response.status_code == 200:
        raise AssertionError()

    if (
        len(response.data["data"][0]["meetup"]) != 1
        or response.data["data"][0]["meetup"][0]["id"] != meetup1.id
        or response.data["data"][0]["meetup"][0]["title"] != meetup1.title
    ):
        raise AssertionError()


def test_non_admin_cannot_edit_meetup(api_client, db, user1, meetup1):
    api_client.force_authenticate(user=user1)

    response = api_client.put(
        reverse("meeting", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps(meetup),
    )

    if not response.status_code == 401:
        raise AssertionError()

    if not response.data == {
        "status": 401,
        "error": "Action restricted to Admins!",
    }:
        raise AssertionError()


def test_admin_can_edit_meetup(api_client, db, admin_user, meetup1):
    api_client.force_authenticate(user=admin_user)

    meetup["created_by"] = admin_user.id

    response = api_client.put(
        reverse("meeting", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps(meetup),
    )

    if not response.status_code == 200:
        raise AssertionError()

    if (
        response.data["data"][0]["meetup"]["title"] != meetup["title"]
        or response.data["data"][0]["meetup"]["start"] != meetup["start"]
        or response.data["data"][0]["meetup"]["end"] != meetup["end"]
    ):
        raise AssertionError()


def test_edit_meetup_with_missing_data(api_client, db, admin_user, meetup1):
    api_client.force_authenticate(user=admin_user)

    response = api_client.put(
        reverse("meeting", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps(meetup_wrong),
    )
    if not response.status_code == 400:
        raise AssertionError()

    if not response.data == {
        "status": 400,
        "error": {"title": ["This field is required."], "body": ["This field is required."]},
    }:
        raise AssertionError()


def test_get_a_meetup(api_client, db, admin_user, meetup1, tagged_meetup):
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(
        reverse("meeting", kwargs={"meeting_id": meetup1.id})
    )

    if not response.status_code == 200:
        raise AssertionError()

    if (
        response.data["data"][0]["meetup"]["id"] != meetup1.id
        or response.data["data"][0]["meetup"]["title"] != meetup1.title
    ):
        raise AssertionError()


def test_non_admin_user_cannot_delete_meetup(api_client, db, user1, meetup1):
    api_client.force_authenticate(user=user1)

    response = api_client.delete(
        reverse("meeting", kwargs={"meeting_id": meetup1.id})
    )

    if not response.status_code == 401:
        raise AssertionError()

    if not response.data == {
        "status": 401,
        "error": "Action restricted to Admins!",
    }:
        raise AssertionError()


def test_admin_user_can_delete_meetup(api_client, db, admin_user, meetup1):
    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(
        reverse("meeting", kwargs={"meeting_id": meetup1.id})
    )
    if not response.status_code == 200:
        raise AssertionError()

    if not response.data == {
        "status": 200,
        "data": [{"success": "Meet deleted successfully"}],
    }:
        raise AssertionError()
