from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class Index(APIView):
    """
    get:
    Welcome to Questioner route
    operation_description:welcome
    """

    @classmethod
    @swagger_auto_schema(
        operation_description="Welcome to Questioner",
        operation_id="welcome To Questioner",
        security=None,
    )
    def get(self, request):
        return Response({"The Dojos": "Welcome to Questioner."})
