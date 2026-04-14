from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User, News
from .models import Doctor , Appointment

# 1. The form for CREATING a user
class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# 2. The configuration for the ADMIN INTERFACE
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    
    # What to show when ADDING a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
   
    list_display = ('name', 'specialty', 'available', 'queue_length', 'next_slot')
    search_fields = ('name', 'specialty')
    list_filter = ('specialty', 'available')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('reference_id', 'patient_name', 'doctor', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date', 'doctor')
    search_fields = ('reference_id', 'patient_name', 'patient_phone')
    readonly_fields = ('reference_id', 'created_at')

    def save_model(self, request, obj, form, change):
        import random
        if not obj.reference_id:
            obj.reference_id = 'SKH-' + str(random.randint(1000, 9999))
        super().save_model(request, obj, form, change)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date')
    search_fields = ('title', 'category')