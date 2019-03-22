from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from meetup.models import Meeting
from question.models import Question, Comment
from vote.models import Vote
from question.serializers import (QuestionSerializer, QuestionSerializerClass, CommentSerializer)
from meetup.serializers import MeetingSerializer
from question.permissions import IsOwnerOrReadOnly


class Questions(APIView):
    """
        this class helps with the following features;
        - adding a new question to a meeting
        - getting all questions of a particular meeting
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializerClass

    @classmethod
    @swagger_auto_schema(
        operation_description="Get all Questions for a meet up",
        operation_id="Get all questions for a meetup",
        responses={
            200: QuestionSerializer(many=True),
            400: "Invalid Meetup Id",
        },
    )
    def get(self, request, meetup_id):
        """
        get:
        Get all Questions for a meet up
        """
        mymeeting = Meeting.objects.filter(id=meetup_id)
        if mymeeting.exists():
            questions = Question.objects.filter(meetup_id=meetup_id)
            serializer = QuestionSerializer(questions, many=True)
            results = serializer.data
            all_questions = []
            for result in results:
                up_votes = len(
                    [
                        vote
                        for vote in Vote.objects.filter(
                            question_id=result["id"], vote=1
                        )
                    ]
                )
                dwn_votes = len(
                    [
                        vote
                        for vote in Vote.objects.filter(
                            question_id=result["id"], vote=-1
                        )
                    ]
                )
                votes = [{"up votes": up_votes, "down votes": dwn_votes}]

                Mserializer = MeetingSerializer(mymeeting, many=True)

                user = User.objects.filter(Q(id=result["created_by"])).distinct().first()
                result["created_by_name"] = user.username

                result["meetup_name"] = Mserializer.data[0]["title"]
                result["votes"] = votes

                all_questions.append(result)
            return Response(all_questions)
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    @swagger_auto_schema(
        operation_description="Create a question for a specific meetup.",
        operation_id="Create a question for a specific meetup",
        request_body=QuestionSerializer,
        responses={
            201: QuestionSerializer(many=False),
            400: "Invalid Format Data",
            401: "Unauthorized Access",
        },
    )
    def post(self, request, meetup_id):
        """
        post:
        Create a question for a specific meetup."
        """

        meeting = Meeting.objects.filter(id=meetup_id)
        if meeting.exists():
            current_user = request.user
            if current_user.is_superuser:
                return Response(
                    data={
                        "error": "Admin is not allowed to add questions",
                        "status": 401,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            data = {}
            for key in request.data:
                data[key] = request.data[key]
            data["meetup_id"] = meetup_id
            data["created_by"] = current_user.id

            Mserializer = MeetingSerializer(meeting, many=True)

            serializer = QuestionSerializer(data=data)
            if serializer.is_valid():

                serializer.save()
                qn_dict = dict(serializer.data)
                qn_dict["created_by_name"] = current_user.username
                qn_dict["meetup"] = Mserializer.data[0]["title"]
                return Response(
                    data={
                        "status": status.HTTP_201_CREATED,
                        "data": [
                            {
                                "question": qn_dict,
                                "success": "Question successfully added to meetup",
                            }
                        ],
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

class OneQuestion(APIView):
    """
    get:
    Get a question for a specific meetup."
    put:
    Update a question for a specific meetup."
    delete:
    Delete a question for a specific meetup."
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializerClass

    @classmethod
    @swagger_auto_schema(
        operation_description="Get a question for a specific meetup.",
        operation_id="Get a question for a specific meetup.",
        responses={
            200: QuestionSerializer(many=False),
            400: "Invalid Format Data",
            401: "Unauthorized Access",
        },
    )
    def get(cls, request, meetup_id, question_id):

        meeting = Meeting.objects.filter(id=meetup_id)
        if meeting.exists():
            question = get_object_or_404(
                Question, id=question_id, meetup_id=meetup_id
            )
            serializer = QuestionSerializer(question, many=False)
            result = serializer.data
            up_votes = len(
                [
                    votes
                    for votes in Vote.objects.filter(
                        question_id_id=result["id"], vote=1
                    )
                ]
            )
            dwn_votes = len(
                [
                    votes
                    for votes in Vote.objects.filter(
                        question_id=result["id"], vote=-1
                    )
                ]
            )
            votes = [{"up votes": up_votes, "down votes": dwn_votes}]

            Mserializer = MeetingSerializer(meeting, many=True)

            user = User.objects.filter(Q(id=result["created_by"])).distinct().first()
            result["created_by_name"] = user.username
            result["meetup_name"] = Mserializer.data[0]["title"]
            result["votes"] = votes

            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "data": [{"question": result}],
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    @swagger_auto_schema(
        operation_description="Update a question for a specific meetup.",
        operation_id="Update a question for a specific meetup.",
        request_body=QuestionSerializer,
        responses={
            200: QuestionSerializer(many=False),
            400: "Invalid Format Data",
            401: "Unauthorized Access",
        },
    )
    def put(cls, request, meetup_id, question_id):
        meeting = Meeting.objects.filter(id=meetup_id)
        if meeting.exists():
            current_user = request.user
            if current_user.is_superuser:
                return Response(
                    data={
                        "error": "Admin is not allowed to update a question",
                        "status": 401,
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            question = get_object_or_404(
                    Question,
                    id=question_id,
                    meetup_id=meetup_id,
                    delete_status=False,
                )
            if str(question.created_by) == str(current_user.username):
                serializer = QuestionSerializer(question, many=False)

                data=dict(serializer.data)
                data["date_modified"] = timezone.now()
                data["title"] = request.data.get("title", None)
                data["body"] = request.data.get("body", None)

                serializer = QuestionSerializer(question, data)
                if serializer.is_valid():
                    serializer.save()

                    Mserializer = MeetingSerializer(meeting, many=True)

                    qn_dict = dict(serializer.data)
                    qn_dict["created_by_name"] = current_user.username
                    qn_dict["meetup_name"] = Mserializer.data[0]["title"]
                    return Response(
                        data={
                            "status": status.HTTP_200_OK,
                            "data": [
                                {
                                    "question": qn_dict,
                                    "success": "Question successfully edited",
                                }
                            ],
                        },
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                    data={
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "error": "You cannot edit a question created by another user",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    @swagger_auto_schema(
        operation_description="Delete a question for a specific meetup.",
        operation_id="Delete a question for a specific meetup.",
        responses={
            200: QuestionSerializer(many=False),
            400: "Invalid Meetup ID",
            404: "Invalid Question ID",
            401: "Unauthorized Access",
        },
    )
    def delete(cls, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            question = get_object_or_404(
                Question,
                id=question_id,
                meetup_id=meetup_id,
                delete_status=False,
            )
            current_user = request.user
            if current_user.is_superuser:
                question.delete_status = True
                question.save()
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "data": [
                            {
                                "success": "Question has been soft deleted",
                                "status": status.HTTP_200_OK,
                            }
                        ],
                    },
                    status=status.HTTP_200_OK,
                )
            elif str(question.created_by) != str(current_user.username):
                return Response(
                    data={
                        "status": status.HTTP_401_UNAUTHORIZED,
                        "error": "You cannot delete question created by another user",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                question.delete()
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "data": [{"success": "Question has been deleted"}],
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"error": "invalid meetup id"}, status=status.HTTP_400_BAD_REQUEST
        )

class CommentList(APIView):
    """
    List all comments, or create a new comment.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        """Return a list of comments."""
        meetup = Meeting.objects.filter(id=self.kwargs['meetup_id'])
        question = Question.objects.filter(id=self.kwargs['question_id'])
        if meetup:
            if not question:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "error": "Question not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            queryset = Comment.objects.filter(question=self.kwargs['question_id'])
            serializer = CommentSerializer(queryset, many=True)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "comments": serializer.data
                }
            )
        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "error": "Meetup not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )


    def post(self, request, **kwargs):
        """Add a comment to a particular question."""
        meetup = Meeting.objects.filter(id=self.kwargs['meetup_id'])
        question = Question.objects.filter(id=self.kwargs['question_id'])
        if meetup:
            if question:
                serializer = CommentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(
                        created_by=self.request.user,
                        question_id=self.kwargs['question_id'])
                    return Response(
                        {
                            "comment": serializer.data,
                            "message": "Comment successfully created."
                        },
                        status=status.HTTP_201_CREATED
                    )
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "Fields cannot be left empty or missing."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Question not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "error": "Meetup not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )


class CommentDetail(APIView):
    """
    Retrieve, update or delete a comment instance.
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

    @classmethod
    def get_object(cls, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound({"error": "Comment not found."})

    def get(self, request, pk, **kwargs):
        """Return a single comment to a question."""
        if not Meeting.objects.filter(id=self.kwargs['meetup_id']):
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Meetup not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if not Question.objects.filter(id=self.kwargs['question_id']):
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Question not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if Comment.objects.filter(question=self.kwargs['question_id']):
            comment = self.get_object(pk)
            serializer = CommentSerializer(comment)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "comment": serializer.data
                }
            )

    def put(self, request, pk, **kwargs):
        """Update a single comment."""
        if not Meeting.objects.filter(id=self.kwargs['meetup_id']):
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Meetup not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if not Question.objects.filter(id=self.kwargs['question_id']):
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Question not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if Comment.objects.filter(question=self.kwargs['question_id']):
            comment = self.get_object(pk)
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": "Comment successfully updated."
                    }
                )

    def delete(self, request, pk, **kwargs):
        """Delete a single question."""
        if Meeting.objects.filter(id=self.kwargs['meetup_id']):
            if Question.objects.filter(id=self.kwargs['question_id']):
                if Comment.objects.filter(question=self.kwargs['question_id']):
                    comment = self.get_object(pk)
                    comment.delete()
                    return Response(
                        {
                            "status": status.HTTP_204_NO_CONTENT,
                            "message": "Comment successfully deleted."
                        },
                        status=status.HTTP_204_NO_CONTENT
                    )
            return Response(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Question not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "status": status.HTTP_404_NOT_FOUND,
                "error": "Meetup not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )
