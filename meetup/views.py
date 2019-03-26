
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Meeting
from question.models import Question
from tag.models import MeetingTag, Tag
from tag.serializers import MeetingTagSerializer
from .serializers import MeetingSerializer


# list all meetup or create a new meetup
# meetups/
class MeetingList(APIView):
    """
    get:
    Get all meetups
    post:
    Create a meetup
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MeetingSerializer

    @classmethod
    @swagger_auto_schema(
        operation_description="Get all meetups.",
        operation_id="Get all meetups",
        responses={200: MeetingSerializer(many=True)},
    )
    def get(cls, request):
        meetups = Meeting.objects.all()
        serializer = MeetingSerializer(meetups, many=True)

        meetupwithtags = []
        for meetup in serializer.data:

            user = User.objects.filter(Q(id=meetup["created_by"])).distinct().first()
            meetup["created_by_name"] = user.username

            questions_count = Question.objects.filter(Q(meetup_id=meetup["id"])).count()
            meetup["questions_count"] = questions_count

            meetupwithtags.append(meetup)

        return Response(
            data={
                "status": status.HTTP_200_OK,
                "data": [{"meetups": meetupwithtags}],
            },
            status=status.HTTP_200_OK,
        )

    @classmethod
    @swagger_auto_schema(
        operation_description="Create a meetup",
        operation_id="Create a meetup",
        request_body=MeetingSerializer,
        responses={
            201: MeetingSerializer(many=False),
            400: "Bad Format Data",
            401: "Unathorized Access",
        },
    )
    def post(cls, request):

        if not request.user.is_superuser:
            return Response(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Action restricted to Admins!",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = MeetingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)

            data = dict(serializer.data)
            data["created_by_name"] = request.user.username

            return Response(
                data={
                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {
                            "meetup": data,
                            "success": "Meet up created successfully",
                        }
                    ],
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# Get, update or delete a meetup
# meetups/1
class AMeeting(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MeetingSerializer

    @classmethod
    @swagger_auto_schema(
        operation_description="Get a meetup",
        operation_id="Get  specific meetup.",
        responses={
            200: MeetingSerializer(many=False),
            401: "Unathorized Access",
            404: "Meeting Does not Exist",
        },
    )
    def get(cls, request, meeting_id):

        meetup = get_object_or_404(Meeting, pk=meeting_id)
        serial_meeting = MeetingSerializer(meetup, many=False)

        meetingtags = MeetingTag.objects.filter(meetup=meeting_id)
        serial_tags = MeetingTagSerializer(meetingtags, many=True)

        tags = []
        for item in serial_tags.data:
            tag = Tag.objects.get(id=item["tag"])
            tags.append(tag.title)

        result = serial_meeting.data
        result["tags"] = tags

        questions_count = Question.objects.filter(Q(meetup_id=result["id"])).count()
        result["questions_count"] = questions_count

        user = User.objects.filter(Q(id=result["created_by"])).distinct().first()
        result["created_by_name"] = user.username

        return Response(
            data={"status": status.HTTP_200_OK, "data": [{"meetup": result}]},
            status=status.HTTP_200_OK,
        )

    @classmethod
    @swagger_auto_schema(
        operation_description="Edit a meetup",
        operation_id="Edit a specific",
        request_body=MeetingSerializer(many=False),
        responses={
            200: MeetingSerializer(many=False),
            401: "Unathorized Access",
            404: "Meeting Does not Exist",
        },
    )
    def put(cls, request, meeting_id):

        if not request.user.is_superuser:
            return Response(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Action restricted to Admins!",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        meetup = get_object_or_404(Meeting, pk=meeting_id)

        serializer = MeetingSerializer(meetup, data=request.data)
        if serializer.is_valid():
            serializer.save()

            result = dict(serializer.data)

            user = User.objects.filter(Q(id=result["created_by"])).distinct().first()
            result["created_by_name"] = user.username

            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "data": [
                        {
                            "meetup": result,
                            "success": "Meet updated successfully",
                        }
                    ],
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @classmethod
    @swagger_auto_schema(
        operation_description="Delete a meetup",
        operation_id="Delete a specific meetup",
        responses={
            200: MeetingSerializer(many=False),
            401: "Unathorized Access",
            404: "Meeting Does not Exist",
        },
    )
    def delete(cls, request, meeting_id):

        if not request.user.is_superuser:
            return Response(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Action restricted to Admins!",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        meetup = get_object_or_404(Meeting, pk=meeting_id)
        meetup.delete()

        return Response(
            data={
                "status": status.HTTP_200_OK,
                "data": [{"success": "Meet deleted successfully"}],
            },
            status=status.HTTP_200_OK,
        )
