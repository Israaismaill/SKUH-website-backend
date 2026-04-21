from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer, UserSerializer # This imports the file you just made!
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment, Doctor
from django.views.decorators.csrf import csrf_exempt


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Or set to IsAdminUser if you want to restrict it
    serializer_class = UserSerializer
@csrf_exempt
@api_view(['POST'])
def create_appointment(request):
    data = request.data
    try:
        # 1. Find the doctor in our DB by name
        doctor = Doctor.objects.get(name=data['doctorName'])
        
        # 2. Create the appointment in the DB
        appointment = Appointment.objects.create(
            doctor=doctor,
            reference_id=data['id'],
            patient_name=data['patientName'],
            patient_phone=data['patientPhone'],
            appointment_date=data['date'],
            reason=data.get('reason', ''),
            status='Confirmed',
            payment_status='Paid'
        )
        return Response({"message": "Saved successfully!"}, status=status.HTTP_201_CREATED)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)