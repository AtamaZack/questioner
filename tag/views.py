from django.contrib.auth.models import User
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MeetingTag
from .models import Tag
from .serializers import MeetingTagSerializer
from .serializers import TagSerializer


# list all tags or create a tag
# tags/
class TagList(APIView):
    """
    get:
    Get all tags
    post:
    Create a tag
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer

    @classmethod
    @swagger_auto_schema(
        operation_description="Get all tags",
        operation_id="Get all tags",
        responses={
            200: TagSerializer(many=False),
            401: "Unathorized Access",
            400: "Meeting Does not Exist",
        },
    )
    def get(cls, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        tags = []
        for tag in serializer.data:
            user = User.objects.filter(Q(id=tag["created_by"])).distinct().first()
            tag["created_by_name"] = user.username
            tags.append(tag)

        return Response(
            data={
                "status": status.HTTP_200_OK,
                "data": [{"tags": tags}],
            },
            status=status.HTTP_200_OK,
        )

    @classmethod
    @swagger_auto_schema(
        operation_description="Create a tags",
        operation_id="Create a Tag.",
        request_body=TagSerializer,
        responses={
            201: TagSerializer(many=False),
            401: "Unathorized Access",
            400: "Missing title or tag already exists",
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

        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)

            data = dict(serializer.data)
            data["created_by"] = request.user.id
            data["created_by_name"] = request.user.username

            return Response(
                data={
                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {
                            "tag": data,
                            "success": "Tag created successfully",
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


# delete a tag object
# tags/1
class ATag(APIView):
    """
    delete:
    Delete a specific tag.
    """

    permission_classes = (IsAdminUser,)
    serializer_class = TagSerializer

    @classmethod
    @swagger_auto_schema(
        operation_description="Delete a tag",
        operation_id="Delete a tag",
        responses={
            200: TagSerializer(many=False),
            401: "Unathorized Access",
            404: "Tag Does not exist",
        },
    )
    def delete(cls, request, tag_id):
        """
        delete:
        Delete a Tag
        """
        tag = get_object_or_404(Tag, pk=tag_id)
        response = None
        try:
            tag.delete()
            response = Response(
                data={
                    "status": status.HTTP_200_OK,
                    "data": [
                        {"success": "Tag permantely deleted successfully"}
                    ],
                },
                status=status.HTTP_200_OK,
            )
        except ProtectedError:
            tag.active = False
            tag.save()
            response = Response(
                data={
                    "status": status.HTTP_200_OK,
                    "data": [{"success": "Tag soft deleted successfully"}],
                },
                status=status.HTTP_200_OK,
            )
        return response


# Add a tag to a meetup
# /meetups/{meet_up_id}tags/
class AddMeetupTag(APIView):
    """
    post:
    A tag to a meet up
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MeetingTagSerializer

    @classmethod
    @swagger_auto_schema(
        operation_description="Add a tag to a meetup",
        operation_id="Add a tag to a meetup.",
        request_body=MeetingTagSerializer,
        responses={
            201: MeetingTagSerializer(many=False),
            401: "Unathorized Access",
            403: "Tag is disabled",
            404: "Tag Does not exist",
            400: "Meet up does not exist or Tag already exists",
        },
    )
    def post(cls, request, meeting_id):

        data = {}
        data["tag"] = request.data["tag"]
        data["created_by"] = request.user.id
        data["meetup"] = meeting_id
        try:
            tag = Tag.objects.get(pk=data["tag"])
            serializer = MeetingTagSerializer(data=data)

        except Tag.DoesNotExist:
            return Response(
                data={
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "Tag with specified id does not exist.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        response = None

        if not tag.active:
            response = Response(
                data={
                    "status": status.HTTP_403_FORBIDDEN,
                    "error": "This Tag is disabled.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        elif serializer.is_valid():
            serializer.save(created_by= request.user)

            data = dict(serializer.data)
            data["created_by_name"] = request.user.username

            response = Response(
                data={
                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {
                            "tag": data,
                            "success": "Tag successfully added to meetup",
                        }
                    ],
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            response = Response(
                data={
                    "status": status.HTTP_400_BAD_REQUEST,
                    "detail": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response


# remove tag from meetup object
# meetups/1/tags/1
class AmeetupTag(APIView):
    """
    delete:
    Remove tag from meetup.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MeetingTagSerializer

    @classmethod
    @swagger_auto_schema(
        operation_description="Remove a tag from a meetup",
        operation_id="Remove a tag from a meetup.",
        request_body=MeetingTagSerializer,
        responses={
            200: MeetingTagSerializer(many=False),
            401: "Unathorized Access",
            403: "Tag is disabled",
            404: "Meetup or Tag Does not exist",
        },
    )
    def delete(cls, request, tag_id, meeting_id):
        meetingtags = get_object_or_404(
            MeetingTag, meetup=meeting_id, tag=tag_id
        )
        serializer = MeetingTagSerializer(meetingtags, many=False)

        serial_tag = serializer.data

        if not (
                request.user.is_superuser
                or (request.user.id == serial_tag["created_by"])
        ):
            return Response(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Sorry. Permission denied!",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        meetingtags.delete()
        return Response(
            data={
                "status": status.HTTP_200_OK,
                "data": [
                    {"success": "Tag successfully removed from Meet up."}
                ],
            },
            status=status.HTTP_200_OK,
        )
