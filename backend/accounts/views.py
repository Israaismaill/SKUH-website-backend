from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import User, Appointment, Doctor, News
from .serializers import RegisterSerializer, EmailTokenObtainPairSerializer, NewsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


# --- 1. THE REGISTER VIEW (Required by your urls.py) ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_verified = False
        user.save()

        # Generate verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build verification link
        verify_url = f"{settings.FRONTEND_URL}/verify-email?uid={uid}&token={token}"

        # Send email
        send_mail(
            subject='Verify your email - SKUH Hospital',
            message=f'''
Hello {user.first_name},

Thank you for registering with Souad Kafafi University Hospital.

Please click the link below to verify your email address:

{verify_url}

If you did not register, please ignore this email.

Best regards,
SKUH Hospital Team
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

@api_view(['GET'])
def verify_email(request):
    uid = request.GET.get('uid')
    token = request.GET.get('token')

    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except Exception:
        return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

    if default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        return Response({'message': 'Email verified successfully!'})
    else:
        return Response({'error': 'Link expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)

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
    
@api_view(['POST'])
def create_doctor(request):
    from .serializers import DoctorSerializer
    serializer = DoctorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_doctor(request, pk):
    from .serializers import DoctorSerializer
    try:
        doctor = Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DoctorSerializer(doctor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_doctor(request, pk):
    try:
        doctor = Doctor.objects.get(pk=pk)
        doctor.delete()
        return Response({'message': 'Deleted successfully'})
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_appointments(request):
    from .serializers import AppointmentSerializer
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


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