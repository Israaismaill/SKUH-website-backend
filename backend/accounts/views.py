from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import User, Appointment, Doctor, News
from .serializers import RegisterSerializer, EmailTokenObtainPairSerializer, NewsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



# --- 1. THE REGISTER VIEW (Required by your urls.py) ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# --- 2. THE APPOINTMENT VIEW ---
@csrf_exempt
@api_view(['POST'])
def create_appointment(request):
    data = request.data
    try:
        # Find the doctor in our DB by name
        doctor = Doctor.objects.get(name=data['doctorName'])
        
        # Create a reference ID if it doesn't exist
        ref_id = data.get('id', 'REF-' + str(data['patientPhone'])[-4:])

        appointment = Appointment.objects.create(
            doctor=doctor,
            reference_id=ref_id,
            patient_name=data['patientName'],
            patient_phone=data['patientPhone'],
            appointment_date=data['date'],
            reason=data.get('reason', ''),
            status='Confirmed',
            payment_status='Paid'
        )
        return Response({"message": "Saved successfully!", "ref_id": ref_id}, status=status.HTTP_201_CREATED)

    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found in database"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_doctors(request):
    doctors = Doctor.objects.all()
    from .serializers import DoctorSerializer
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_news(request):
    news = News.objects.all()
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer