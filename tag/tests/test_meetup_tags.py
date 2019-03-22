import json

from django.urls import reverse


def test_cannot_anonymous_user_cannot_tag_to_meet_up(api_client, db, meetup1, a_tag):
    response = api_client.post(
        reverse("meetingtags", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps({"tag": a_tag.id}),
    )

    if not response.status_code == 403:
        raise AssertionError()

    if not response.data == {
        "status": 403,
        "detail": "Authentication credentials were not provided.",
    }:
        raise AssertionError()


def test_cannot_add_tag_which_does_not_exist_to_meetup(
    api_client, db, meetup1, user1
):
    api_client.force_authenticate(user=user1)
    response = api_client.post(
        reverse("meetingtags", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps({"tag": 1}),
    )

    if not response.status_code == 404:
        raise AssertionError()

    if not response.data == {
        "status": 404,
        "error": "Tag with specified id does not exist.",
    }:
        raise AssertionError()


def test_cannot_add_disabled_tag_to_meetup(
    api_client, db, meetup1, admin_user, disabled_tag
):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse("meetingtags", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps({"tag": disabled_tag.id}),
    )

    if not response.status_code == 403:
        raise AssertionError()

    if not response.data == {"status": 403, "error": "This Tag is disabled."}:
        raise AssertionError()


def test_cannot_add_tag_to_meetup_with_invalid_meetup_id(
    api_client, db, admin_user, a_tag
):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse("meetingtags", kwargs={"meeting_id": 1}),
        content_type="application/json",
        data=json.dumps({"tag": a_tag.id}),
    )

    if not response.status_code == 400:
        raise AssertionError()

    if not response.data == {
        "status": 400,
        "detail": {
            "meetup": [
                "Invalid pk \"1\" - object does not exist."
            ]
        }
    }:
        raise AssertionError()


def test_user_can_add_tag_to_meetup(api_client, db, meetup1, user1, a_tag):
    api_client.force_authenticate(user=user1)
    response = api_client.post(
        reverse("meetingtags", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps({"meeting": meetup1.id, "tag": a_tag.id}),
    )

    if not response.status_code == 201:
        raise AssertionError()

    if (
        response.data["data"][0]["success"]
        != "Tag successfully added to meetup"
        or response.data["data"][0]["tag"]["meetup"] != meetup1.id
        or response.data["data"][0]["tag"]["created_by"] != user1.id
    ):
        raise AssertionError()


def test_user_cannot_add_duplicate_tag_to_meetup(api_client, db, meetup1, user1, a_tag,tagged_meetup):
    api_client.force_authenticate(user=user1)
    response = api_client.post(
        reverse("meetingtags", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps({"meeting": meetup1.id, "tag": a_tag.id}),
    )

    if not response.status_code == 400:
        raise AssertionError()

    # if (
    #     response.data["data"][0]["success"]
    #     != "Tag successfully added to meetup"
    #     or response.data["data"][0]["tag"]["meetup"] != meetup1.id
    #     or response.data["data"][0]["tag"]["created_by"] != user1.id
    # ):
    #     raise AssertionError()

def test_user_cannot_remove_a_tag_not_added_by_them_to_a_meetup(
    api_client, db, meetup1, user2, tagged_meetup
):
    api_client.force_authenticate(user=user2)
    response = api_client.delete(
        reverse(
            "meetingtag",
            kwargs={
                "meeting_id": tagged_meetup.meetup.id,
                "tag_id": tagged_meetup.tag.id,
            },
        )
    )

    if not response.status_code == 401:
        raise AssertionError()
    if response.data != {"status": 401, "error": "Sorry. Permission denied!"}:
        raise AssertionError()


def test_user_can_remove_a_tag_added_by_them_to_a_meetup(
    api_client, db, meetup1, user1, tagged_meetup
):
    api_client.force_authenticate(user=user1)
    response = api_client.delete(
        reverse(
            "meetingtag",
            kwargs={
                "meeting_id": tagged_meetup.meetup.id,
                "tag_id": tagged_meetup.tag.id,
            },
        )
    )

    if not response.status_code == 200:
        raise AssertionError()
    if response.data != {
        "status": 200,
        "data": [{"success": "Tag successfully removed from Meet up."}],
    }:
        raise AssertionError()


def test_admin_user_can_remove_any_tag_from_a_meetup(
    api_client, db, meetup1, admin_user, tagged_meetup
):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(
        reverse(
            "meetingtag",
            kwargs={
                "meeting_id": tagged_meetup.meetup.id,
                "tag_id": tagged_meetup.tag.id,
            },
        )
    )
    if not response.status_code == 200:
        raise AssertionError()
    if response.data != {
        "status": 200,
        "data": [{"success": "Tag successfully removed from Meet up."}],
    }:
        raise AssertionError()
