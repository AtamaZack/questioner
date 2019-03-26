import json

from django.urls import reverse


def test_anonymous_user_cannot_edit_an_answer(
        api_client, db, answered_question
):
    response = api_client.put(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.id,
                "answer_id": answered_question.id,
            },
        )
    )
    if not response.status_code == 403:
        raise AssertionError()

    if not response.data == {
        "detail": "Authentication credentials were not provided.",
        "status": 403,
    }:
        raise AssertionError()


def test_non_staff_user_cannot_edit_an_answer_a_question(
        api_client, db, user1, answered_question
):
    api_client.force_authenticate(user=user1)
    response = api_client.put(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.id,
                "answer_id": answered_question.id,
            },
        )
    )
    if not response.status_code == 401:
        raise AssertionError()

    if not response.data == {
        "status": 401,
        "error": "Only staff are allowed to edit answers",
    }:
        raise AssertionError()


def test_Staff_user_cannot_edit_an_answer_with_invalid_answer_id(
        api_client, db, user1, answered_question
):
    api_client.force_authenticate(user=answered_question.created_by)
    response = api_client.put(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": 2,
            },
        )
    )
    if not response.status_code == 404:
        raise AssertionError()

    if not response.data == {"status": 404, "error": "Answer does not exist"}:
        raise AssertionError()


def test_any_staff_user_can_edit_an_answer_not_created_by_them(
        api_client, db, admin_user, staff2, answered_question
):
    api_client.force_authenticate(user=admin_user)
    response1 = api_client.put(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": answered_question.id,
            },
        )
    )
    api_client.force_authenticate(user=staff2)
    response2 = api_client.put(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": answered_question.id,
            },
        )
    )

    if not response1.status_code == 401 or not response2.status_code == 401:
        raise AssertionError()

    edit_answer_401_msg = {
        "error": "You are not allowed to edit another user's answer",
        "status": 401,
    }

    if (
            not response1.data == edit_answer_401_msg
            or not response2.data == edit_answer_401_msg
    ):
        raise AssertionError()


def test_admin_user_cannot_edit_an_answer_a_question_with_invalid_data(
        api_client, db, answered_question, staff1
):
    api_client.force_authenticate(user=staff1)
    response1 = api_client.put(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": answered_question.id,
            },
        ),
        content_type="application/json",
        data=json.dumps({}),
    )
    response2 = api_client.put(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": answered_question.id,
            },
        ),
        content_type="application/json",
        data=json.dumps({"body": ""}),
    )
    if (
            not response1.status_code == 400
            or not response2.status_code == 400
            or not response1.data
                   == {"status": 400, "error": {"body": ["This field is required."]}}
            or not response2.data
                   == {"status": 400, "error": {"body": ["This field may not be blank."]}}
    ):
        raise AssertionError()


def test_admin_user_can_answer_a_question_with_valid_data(
        api_client, db, answered_question, staff1
):
    api_client.force_authenticate(user=staff1)
    response = api_client.put(
        reverse(
            "edit_delete_answers",
            kwargs={
                "meetup_id": answered_question.meetup.id,
                "question_id": answered_question.question.id,
                "answer_id": answered_question.id,
            },
        ),
        content_type="application/json",
        data=json.dumps(
            {"body": "Django is a high-level Python Web framework"}
        ),
    )

    if (
            not response.status_code == 200
            or not response.data["status"] == 200
            or not response.data["data"][0]["success"]
                   == "Answer updated successfully"
            or not response.data["data"][0]["answers"]["body"]
                   == "Django is a high-level Python Web framework"
    ):
        raise AssertionError()
