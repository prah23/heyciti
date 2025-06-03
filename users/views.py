from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from tasks.models import Task, UserTask

class CreateUserAndLinkTasksView(APIView):
    """
    API endpoint to create a user and link all tasks to the user.
    """

    def post(self, request):
        soeid = request.data.get('soeid')

        # Validate SOEID
        if not soeid:
            return Response({'error': 'SOEID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get the user
        user, created = User.objects.get_or_create(soeid=soeid)

        # Link all tasks in the database to the user
        tasks = Task.objects.all()
        for task in tasks:
            UserTask.objects.get_or_create(user=user, task=task)

        if created:
            return Response({'message': f'User with SOEID {soeid} created and tasks linked successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': f'User with SOEID {soeid} already exists. Tasks linked successfully.'}, status=status.HTTP_200_OK)

class UpdateUserAvatarView(APIView):
    """
    API endpoint to update or add an avatar for a given user by SOEID.
    """

    def patch(self, request, soeid):
        # Get the user by SOEID
        try:
            user = User.objects.get(soeid=soeid)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get the avatar from the request data
        avatar = request.data.get('avatar')
        if not avatar:
            return Response({'error': 'Avatar is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's avatar
        user.avatar = avatar
        user.save()

        return Response({'message': f'Avatar updated successfully for user with SOEID {soeid}.'}, status=status.HTTP_200_OK)

class GetUserDetailsView(APIView):
    """
    API endpoint to fetch a user's details by SOEID.
    """

    def get(self, request, soeid):
        # Get the user by SOEID
        try:
            user = User.objects.get(soeid=soeid)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the response data
        user_data = {
            'soeid': user.soeid,
            'avatar': user.avatar
        }

        return Response(user_data, status=status.HTTP_200_OK)