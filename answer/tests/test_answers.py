import json

from django.urls import reverse


def test_anonymous_user_cannot_answer_a_question(
        api_client, db, question1, meetup1
):
    response = api_client.post(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": meetup1.id, "question_id": question1.id},
        ),
        content_type="application/json",
        data=json.dumps({"body": "Django is a Python framework"}),
    )
    if not response.status_code == 403:
        raise AssertionError()

    if not response.data == {
        "detail": "Authentication credentials were not provided.",
        "status": 403,
    }:
        raise AssertionError()


def test_non_staff_user_cannot_answer_a_question(
        api_client, db, question1, meetup1, user1
):
    api_client.force_authenticate(user=user1)
    response = api_client.post(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": meetup1.id, "question_id": question1.id},
        ),
        content_type="application/json",
        data=json.dumps({"body": "Django is a Python framework"}),
    )
    if not response.status_code == 401:
        raise AssertionError()

    if not response.data == {
        "status": 401,
        "error": "Only staff are allowed to answer questions",
    }:
        raise AssertionError()


def test_admin_user_cannot_answer_a_question_with_invalid_meetup_or_quesiton_id(
        api_client, db, question1, meetup1, admin_user
):
    api_client.force_authenticate(user=admin_user)
    response1 = api_client.post(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": 1, "question_id": question1.id},
        ),
        content_type="application/json",
        data=json.dumps({"body": "Django is a Python framework"}),
    )
    response2 = api_client.post(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": meetup1.id, "question_id": 1},
        ),
        content_type="application/json",
        data=json.dumps({"body": "Django is a Python framework"}),
    )
    if not response1.status_code == 404 or not response2.status_code == 404:
        raise AssertionError()

    expected = {
        "status": 404,  # assert response.data == 4
        "error": "Meetup or question does not exist",
    }
    if not response1.data == expected or not response2.data == expected:
        raise AssertionError


def test_admin_user_cannot_answer_a_question_with_invalid_data(
        api_client, db, question1, meetup1, admin_user
):
    api_client.force_authenticate(user=admin_user)
    response1 = api_client.post(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": meetup1.id, "question_id": question1.id},
        ),
        content_type="application/json",
        data=json.dumps({}),
    )
    response2 = api_client.post(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": meetup1.id, "question_id": question1.id},
        ),
        content_type="application/json",
        data=json.dumps({"body": ""}),
    )
    if (
            not response1.status_code == 400
            # or not response2.status_code == 400
            or not response1.data
                   == {"status": 400, "error": {"body": ["This field is required."]}}
            or not response2.data
                   == {"status": 400, "error": {"body": ["This field may not be blank."]}}
    ):
        raise AssertionError()


def test_admin_user_can_answer_a_question_with_valid_data(
        api_client, db, question1, meetup1, admin_user
):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse(
            "create_read_answers",
            kwargs={"meetup_id": meetup1.id, "question_id": question1.id},
        ),
        content_type="application/json",
        data=json.dumps({"body": "Django is a Python framework"}),
    )

    if (
            not response.status_code == 201
            or not response.data["status"] == 201
            or not response.data["data"][0]["success"]
                   == "Answer added successfully"
            or not response.data["data"][0]["answers"]["body"]
                   == "Django is a Python framework"
    ):
        raise AssertionError()


def test_admin_user_cannot_add_a_duplicate_answer_to_a_question(
        api_client, db, answered_question, admin_user
):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post(
        reverse(
            "create_read_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
            },
        ),
        content_type="application/json",
        data=json.dumps({"body": "Django is a Python framework"}),
    )

    if not response.status_code == 400 or not response.data == {
        "status": 400,
        "error": {"non_field_errors": ["You cannot add a duplicate Answer."]},
    }:
        raise AssertionError()
