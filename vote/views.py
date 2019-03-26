from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from meetup.models import Meeting
from question.models import Question
from vote.models import Vote
from vote.serializers import VoteSerializer


class UpVote(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(self, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            if Question.objects.filter(id=question_id):
                current_user = request.user

                data = {}
                data["vote"] = request.data.get("vote", None)
                data["question_id"] = question_id
                data["voter_id"] = current_user.id
                data["date_modified"] = timezone.now()
                data['vote'] = 1
                serializer = VoteSerializer(data=data)
                if not Question.objects.filter(id=question_id, created_by=current_user.id):
                    my_vote = Vote.objects.filter(question_id=question_id, voter_id=current_user.id)
                    my_vote_is_up = Vote.objects.filter(question_id=question_id, voter_id=current_user.id, vote=1)
                    if my_vote:
                        if my_vote_is_up:
                            my_vote.delete()
                            return Response(
                                data={
                                    "status": status.HTTP_200_OK,
                                    "data": [{"success": "your up-vote has been cancelled"}],
                                },
                                status=status.HTTP_200_OK,
                            )
                        my_vote = get_object_or_404(Vote, question_id=question_id, voter_id=current_user.id, vote=-1)
                        serializer = VoteSerializer(my_vote, data)
                    if serializer.is_valid():
                        serializer.save()

                        data = dict(serializer.data)
                        data["voter"] = request.user.username

                        return Response(
                            data={
                                "status": status.HTTP_200_OK,
                                "data": [
                                    {
                                        "vote": data,
                                        "success": "you have up-voted this question",
                                    }
                                ],
                            },
                            status=status.HTTP_200_OK,
                        )
                return Response(
                    {
                        "error": "vote rejected",
                        "message": "question belongs to you",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"error": "invalid url (either wrong meetup id or question id)"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DownVote(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(self, request, meetup_id, question_id):
        if Meeting.objects.filter(id=meetup_id):
            if Question.objects.filter(id=question_id):
                current_user = request.user
                data = request.data
                data["question_id"] = question_id
                data["voter_id"] = current_user.id
                data["date_modified"] = timezone.now()
                data['vote'] = -1
                serializer = VoteSerializer(data=data)
                if not Question.objects.filter(id=question_id, created_by=current_user.id):
                    my_vote = Vote.objects.filter(question_id=question_id, voter_id=current_user.id)
                    my_vote_is_down = Vote.objects.filter(question_id=question_id, voter_id=current_user.id, vote=-1)
                    if my_vote:
                        if my_vote_is_down:
                            my_vote.delete()
                            return Response(
                                data={
                                    "status": status.HTTP_200_OK,
                                    "data": [{"success": "your up-vote has been cancelled"}],
                                },
                                status=status.HTTP_200_OK,
                            )
                        my_vote = get_object_or_404(Vote, question_id=question_id, voter_id=current_user.id, vote=1)
                        serializer = VoteSerializer(my_vote, data)
                    if serializer.is_valid():
                        serializer.save()

                        data = dict(serializer.data)
                        data["voter"] = request.user.username

                        return Response(
                            data={
                                "status": status.HTTP_200_OK,
                                "data": [
                                    {
                                        "vote": data,
                                        "success": "you have up-voted this question",
                                    }
                                ],
                            },
                            status=status.HTTP_200_OK,
                        )
                return Response(
                    {
                        "error": "vote rejected",
                        "message": "question belongs to you",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"error": "invalid url (either wrong meetup id or question id)"},
            status=status.HTTP_400_BAD_REQUEST,
        )
