from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from meetup.models import Meeting
from question.models import Question
from .models import Comment
from .serializers import CommentSerializer


class CommentList(APIView):
    """
    List all comments, or create a new comment.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

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

            data = []
            for comment in serializer.data:
                user = User.objects.filter(Q(username=comment["created_by"])).distinct().first()
                comment["created_by_id"] = user.id
                comment["question_name"] = question.first().title
                data.append(comment)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "comments": data
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
            if not question:
                return Response(
                    {
                        "status": status.HTTP_404_NOT_FOUND,
                        "error": "Question not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            data = {}
            data["question"] = question.first().id
            data["comment"] = request.data.get("comment")

            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    created_by_id=request.user.id,
                    created_by=self.request.user,
                    question_id=self.kwargs['question_id']
                )
                data = dict(serializer.data)
                data["created_by_id"] = request.user.id
                data["question_name"] = question.first().title
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
                "error": "Meetup not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )


class CommentDetail(APIView):
    """
    Retrieve, update or delete a comment instance.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = CommentSerializer

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
        question = Question.objects.filter(id=self.kwargs['question_id'])
        if not question:
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

            data = dict(serializer.data)
            user = User.objects.filter(Q(username=data["created_by"])).distinct().first()
            print(user)
            data["created_by_id"] = user.id
            data["question_name"] = question.first().title
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "comment": data
                }
            )

    def put(self, request, pk, **kwargs):
        """Update a single comment."""
        if Meeting.objects.filter(id=self.kwargs['meetup_id']):
            if Question.objects.filter(id=self.kwargs['question_id']):
                comment = self.get_object(pk)

                serializer = CommentSerializer(comment, many=False)
                data = dict(serializer.data)
                data["comment"] = request.data["comment"]

                serializer = CommentSerializer(comment, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "status": status.HTTP_200_OK,
                            "message": "Comment successfully updated."
                        }
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
