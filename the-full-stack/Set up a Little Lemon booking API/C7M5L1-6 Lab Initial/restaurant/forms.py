from .models import Booking
from django.forms import ModelForm

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"