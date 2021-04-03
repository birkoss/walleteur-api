from django.core.exceptions import ValidationError
from django.utils import timezone

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Person, Transaction

from core.helpers import create_error_response

from .serializers import PersonSerializer


class persons(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        persons = Person.objects.filter(user=request.user)

        serializer = PersonSerializer(data=persons, many=True)

        return Response({
            'persons': persons,
        }, status=status.HTTP_200_OK)

    # Add a new User (or an existing User) in the current playgroup
    # def post(self, request, playgroup_id, format=None):
        # playgroup = fetch_playgroup(
        #     id=playgroup_id,
        #     playgroupplayer__player=request.user,
        #     playgroupplayer__player_role__name='admin',
        # )
        # if playgroup is None:
        #     return create_error_response('invalid_playgroup')

        # serializer = AchievementSerializer(data=request.data)
        # print(request.data)
        # if serializer.is_valid():
        #     achievement = serializer.save(author=request.user)

        #     # Add the achievement to the playgroup
        #     playgroup_achievement = PlaygroupAchievement(
        #         playgroup=playgroup,
        #         achievement=achievement,
        #         points=achievement.points,
        #         author=request.user,
        #     )

        #     playgroup_achievement.save()

        #     return Response({
        #         'achievementId': playgroup_achievement.id,
        #         'status': status.HTTP_200_OK,
        #     })
        # else:
        #     print(serializer.error_messages)
        #     return create_error_response(serializer.error_messages)
