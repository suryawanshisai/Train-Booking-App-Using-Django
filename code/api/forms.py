from django import forms

USER_TYPE={
        ('admin', 'admin'),
        ('user', 'user'),
    }

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})) 
    usertype = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'placeholder': 'Choose user type'}))

class LoginForm(forms.Form): 
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

# <option value="">Chennai Central</option>
#                     <option value="Banglore">Banglore Majestic</option>
#                     <option value="Hyderabad">Hyderabad Central</option>
#                     <option value="Mumbai">Mumbai</option>
#                     <option value="Indore">Indore</option>
#                     <option value="Delhi">Delhi</option>
#                     <option value="Pune">Pune</option>
#                     <option value="Trivendrum">Trivendrum</option>
#                     <option value="Bhopal">Bhopal</option>
#                     <option value="Kolkata">Kolkata</option>
#                     <option value="varanasi">varanasi</option>
#                     <option value="Jaipur">Jaipur</option>

stations = {
    ('Chennai', 'Chennai'),
    ('Bangalore', 'Bangalore'),
    ('Hyderabad', 'Hyderabad'),
    ('Mumbai', 'Mumbai'),
    ('Indore', 'Indore'),
    ('Delhi', 'Delhi'),
    ('Pune', 'Pune'),
    ('Trivendrum', 'Trivendrum'),
    ('Bhopal', 'Bhopal'),
    ('Kolkata', 'Kolkata'),
    ('varanasi', 'varanasi'),
    ('Jaipur', 'Jaipur'),
}


class TrainSearchForm(forms.Form):
    originStation = forms.ChoiceField(choices=stations, widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'placeholder': 'Choose user type'}))
    destinationStation = forms.ChoiceField(choices=stations, widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'placeholder': 'Choose user type'}))
    journeyDate = forms.DateField( widget=forms.DateInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'type':"date"}))


class NewTrainForm(forms.Form):
    trainNumber = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    trainName = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    originStation = forms.ChoiceField(choices=stations, widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'placeholder': 'Choose user type'}))
    destinationStation = forms.ChoiceField(choices=stations, widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'placeholder': 'Choose user type'}))
    totalSeats = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    basePrice = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    departureTime = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'type': 'time'}))
    arrivalTime = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'type': 'time'}))

coaches = {
    ('1A', '1A'),
    ('2A', '2A'),
    ('3A', '3A'),
    ('SL', 'SL'),
}

class BookTrainForm(forms.Form):
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    mobile = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    passengersCount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    journeyDate = forms.DateField( widget=forms.DateInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'type':"date"}))
    coachType = forms.ChoiceField(choices=coaches, widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-3', 'placeholder': 'Choose user type'}))


