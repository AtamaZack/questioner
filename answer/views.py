from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from answer.serializers import AnswerSerializer
from question.models import Question
from .models import Answers


class CreateReadAnswers(APIView):
    """
    post:
    Create an answer to a specific question
    get:
    Get answers to a specific question
    """

    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(cls, request, meetup_id, question_id, format=None):
        """
        Creates an answer for a specific question.
        Only staff can answer a question
        """
        active_user = request.user
        if not active_user.is_staff:
            return Response(
                data={
                    "status": 401,
                    "error": "Only staff are allowed to answer questions",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        response = None
        try:
            question = Question.objects.get(
                id=question_id, meetup_id=meetup_id
            )
            data = request.data
            data["created_by"] = request.user.username
            data["question"] = question.id
            data["meetup"] = meetup_id
            serializer = AnswerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(
                    data={
                        "status": 201,
                        "data": [
                            {
                                "answers": serializer.data,
                                "success": "Answer added successfully",
                            }
                        ],
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                response = Response(
                    data={"status": 400, "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Question.DoesNotExist:

            response = Response(
                data={
                    "status": 404,
                    "error": "Meetup or question does not exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return response

    @classmethod
    def get(cls, request, meetup_id, question_id, format=None):
        """
        Creates an answer for a specific question.
        Only staff can answer a question
        """
        response = None
        try:
            question = Question.objects.get(
                id=question_id, meetup_id=meetup_id
            )
            answers = Answers.objects.filter(
                question=question.id, meetup=question.meetup_id
            )
            serializer = AnswerSerializer(answers, many=True)
            response = Response(
                data={"status": 200, "data": [{"answers": serializer.data}]},
                status=status.HTTP_200_OK,
            )
        except Question.DoesNotExist:

            response = Response(
                data={
                    "status": 404,
                    "error": "Meetup or question does not exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return response


class EditDeleteAnswers(APIView):
    """
    put:
    Edit an answer to a specific question
    delete:
    Delete an answer to a specific question
    """

    permission_classes = (IsAuthenticated,)

    @classmethod
    def delete(cls, request, meetup_id, question_id, answer_id):
        response = None
        current_user = request.user

        if not current_user.is_staff:
            return Response(
                data={
                    "status": 401,
                    "error": "Only staff are allowed to delete answers",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            answer = Answers.objects.get(
                id=answer_id, meetup=meetup_id, question_id=question_id
            )
            if not current_user.is_superuser and not str(
                    answer.created_by
            ) == str(current_user.username):
                response = Response(
                    data={
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "error": "You cannot delete an answer created by another user",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                answer.delete()
                response = Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "data": [
                            {
                                "success": "Answer deleted deleted",
                                "status": status.HTTP_200_OK,
                            }
                        ],
                    },
                    status=status.HTTP_200_OK,
                )

        except Answers.DoesNotExist:
            response = Response(
                data={"status": 404, "error": "Answer does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return response
    @classmethod
    def put(cls, request, meetup_id, question_id, answer_id):
        response = None
        current_user = request.user

        if not current_user.is_staff:
            return Response(
                data={
                    "status": 401,
                    "error": "Only staff are allowed to edit answers",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            answer = Answers.objects.get(
                id=answer_id, meetup=meetup_id, question=question_id
            )
            if not str(current_user.username) == str(answer.created_by):
                response = Response(
                    data={
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "error": "You are not allowed to edit another user's answer",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except Answers.DoesNotExist:
            response = Response(
                data={
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Answer does not exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if response:
            return response
        else:
            data = request.data
            data["created_by"] = answer.created_by
            data["meetup"] = answer.meetup.id
            data["question"] = answer.question.id

            serializer = AnswerSerializer(answer, data=data)
            if serializer.is_valid():
                serializer.save()

                response = Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "data": [
                            {
                                "answers": serializer.data,
                                "success": "Answer updated successfully",
                            }
                        ],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                response = Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return response
