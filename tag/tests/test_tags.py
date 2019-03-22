import json

from django.urls import reverse

tag1_data = {"title": "tag_title"}


def test_non_admin_user_cannot_create_tags(api_client, db, user1):
    api_client.force_authenticate(user=user1)

    response = api_client.post(
        reverse("tags"),
        content_type="application/json",
        data=json.dumps(tag1_data),
    )
    if not response.status_code == 401:
        raise AssertionError()

    if not response.data == {
        "status": 401,
        "error": "Action restricted to Admins!",
    }:
        raise AssertionError()


def test_admin_user_cannot_create_tag_with_missing_title(api_client, db, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        reverse("tags"), content_type="application/json", data=json.dumps({})
    )
    if not response.status_code == 400:
        raise AssertionError()

    if not response.data == {
        "status": 400,
        "error": {"title": ["This field may not be null."]}
    }:
        raise AssertionError()


def test_admin_user_can_create_tags(api_client, db, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        reverse("tags"),
        content_type="application/json",
        data=json.dumps(tag1_data),
    )
    if not response.status_code == 201:
        raise AssertionError()

    if (
        response.data["data"][0]["success"] != "Tag created successfully"
        or response.data["data"][0]["tag"]["title"] != tag1_data["title"]
        or response.data["data"][0]["tag"]["created_by"] != admin_user.id
    ):
        raise AssertionError()


def test_get_tags(api_client, db, admin_user, tag_objs):
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(reverse("tags"))

    if not response.status_code == 200:
        raise AssertionError()

    if (
        not len(response.data["data"][0]["tags"]) == len(tag_objs)
        or response.data["data"][0]["tags"][0]["title"] != tag_objs[0].title
        or not isinstance(response.data["data"][0]["tags"], list)
    ):
        raise AssertionError()


def test_cannot_add_disabled_tag_to_meetup(
    api_client, db, meetup1, admin_user, disabled_tag
):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse("meetingtags", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps({"meeting": meetup1.id, "tag": disabled_tag.id}),
    )
    if not response.status_code == 403:
        raise AssertionError()
    if not response.data == {"status": 403, "error": "This Tag is disabled."}:
        raise AssertionError()


def test_cannot_add_invalid_tag_to_meetup(api_client, db, meetup1, admin_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse("meetingtags", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps({"meeting": meetup1.id, "tag": 75}),
    )

    if not response.status_code == 404:
        raise AssertionError()

    if not response.data == {
        "status": 404,
        "error": "Tag with specified id does not exist.",
    }:
        raise AssertionError()


def test_add_tag_to_meetup(api_client, db, meetup1, admin_user, tag_objs):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse("meetingtags", kwargs={"meeting_id": meetup1.id}),
        content_type="application/json",
        data=json.dumps({"meeting": meetup1.id, "tag": tag_objs[0].id}),
    )

    if not response.status_code == 201:
        raise AssertionError()

    if (
        response.data["data"][0]["success"]
        != "Tag successfully added to meetup"
        or response.data["data"][0]["tag"]["meetup"] != meetup1.id
        or response.data["data"][0]["tag"]["created_by"] != admin_user.id
    ):
        raise AssertionError()


def test_delete_tag(api_client, db, meetup1, admin_user, tag_objs):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(
        reverse("tag", kwargs={"tag_id": tag_objs[0].id})
    )

    if not response.status_code == 200:
        raise AssertionError()

    if (
        response.data["data"][0]["success"]
        != "Tag permantely deleted successfully"
    ):
        raise AssertionError()


def test_soft_a_delete_tag_attached_to_a_meetup(
    api_client, db, meetup1, admin_user, a_tag, meetup_tag
):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(reverse("tag", kwargs={"tag_id": a_tag.id}))

    if not response.status_code == 200:
        raise AssertionError()

    if response.data["data"][0]["success"] != "Tag soft deleted successfully":
        raise AssertionError()
