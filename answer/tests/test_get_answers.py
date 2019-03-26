from django.urls import reverse


def test_anonymous_user_cannot_get_answers_to_a_question(
        api_client, db, question1, meetup1
):
    response = api_client.get(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": meetup1.id, "question_id": question1.id},
        )
    )
    if not response.status_code == 403:
        raise AssertionError()

    if not response.data == {
        "detail": "Authentication credentials were not provided.",
        "status": 403,
    }:
        raise AssertionError()


def test_authenticated_user_cannot_get_answers_to_a_question_with_invalid_meetup_or_quesiton_id(
        api_client, db, question1, meetup1, admin_user
):
    api_client.force_authenticate(user=admin_user)
    response1 = api_client.get(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": 1, "question_id": question1.id},
        )
    )
    response2 = api_client.get(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": meetup1.id, "question_id": 1},
        )
    )
    if not response1.status_code == 404 or not response2.status_code == 404:
        raise AssertionError()

    expected = {
        "status": 404,  # assert response.data == 4
        "error": "Meetup or question does not exist",
    }
    if not response1.data == expected or not response2.data == expected:
        raise AssertionError


def test_authenticated_user_can_get_answers_to__a_question(
        api_client, db, question1, meetup1, admin_user
):
    api_client.force_authenticate(user=admin_user)
    response = api_client.get(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": meetup1.id, "question_id": question1.id},
        )
    )

    if (
            not response.status_code == 200
            or not response.data["status"] == 200
            or not response.data["data"][0]["answers"] == []
    ):
        raise AssertionError()
