from django.shortcuts import render
from .models import users_collection, train_collection, booking_collection
from .forms import LoginForm, RegisterForm, TrainSearchForm, NewTrainForm, BookTrainForm
import bson

def landing(request):
    error = ""
    trains = []
    trainSearch = False
    trainLen = 0
    if request.method == 'POST':
        form = TrainSearchForm(request.POST)
        if form.is_valid():
            originStation = form.cleaned_data['originStation']
            destinationStation = form.cleaned_data['destinationStation']
            journeyDate = form.cleaned_data['journeyDate']

            trains = [t for t in train_collection.find({"originStation": originStation, "destinationStation": destinationStation})]
            for t in trains:
                t['id'] = str(t['_id'])
            trainLen = len(trains)
            trainSearch = True
            
        else:
            form = TrainSearchForm()
            error = 'Invalid form data. Please try again.'
    else:
        form = TrainSearchForm()
    return render(request, 'landing.html', {"form": form, "trains": trains, "trainLen": trainLen, "trainSearch": trainSearch, "error": error})

def login(request):
    error=''
    data = {}
    isLogged = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                data = users_collection.find_one({'email': email})
                if data.get('password') == password:
                    data['userId'] = str(data['_id'])
                    isLogged = True
                
                else:
                    form = LoginForm()
                    error = 'Wrong credientials. Please try again.'
                    
            except:
                form = LoginForm()
                error = 'User not found!! Please try again.'
        else:
            form = LoginForm()
            error = 'Wrong credientials. Please try again.'
    else:
        form = LoginForm()
    
    context = {'form': form, 'isLogged': isLogged, 'data': data, 'error': error}
    return render(request, 'login.html', context)



def register(request):
    error=''
    data = {}
    isLogged = False
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            usertype = form.cleaned_data['usertype']

            user = {"username": username, "email": email, "password": password, "usertype": usertype}
            result = users_collection.insert_one(user)
            isLogged = True
            data = {
            'userId': str(result.inserted_id),
            'username': username,
            'email': email,
            'password': password,
            'usertype': usertype
            }
            
        else:
            form = RegisterForm()
            error = 'Invalid form data. Please try again.'
    else:
        form = RegisterForm()
    
    context = {'form': form, 'isLogged': isLogged, 'data': data, 'error': error}
    return render(request, 'register.html', context)



def loadBookTrain(request, trainId):
    return render(request, 'user/loadBookTrain.html', {"trainId": trainId})

def bookTrain(request, trainId, userId):
    success = False
    error = ''
    print(userId)  # This is for debugging to ensure you're receiving the correct userId
    
    # Fetch the train information
    train = train_collection.find_one({"_id": bson.ObjectId(trainId)})

    # Fetch the user based on userId
    user = users_collection.find_one({"_id": bson.ObjectId(userId)})
    
    # If user is not found, you can handle the error
    if not user:
        error = "User not found."
        return render(request, 'user/bookTrain.html', {"error": error})
    
    if request.method == 'POST':
        form = BookTrainForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mobile = form.cleaned_data['mobile']
            passengersCount = form.cleaned_data['passengersCount']
            journeyDate = str(form.cleaned_data['journeyDate'])
            coachType = form.cleaned_data['coachType']

            coachPrices = {
                '1A': 4,
                '2A': 3,
                '3A': 2,
                'SL': 1
            }

            # Calculate the total price
            totalPrice = int(coachPrices[coachType]) * int(passengersCount)

            # Get train details again (may not be necessary if already fetched above)
            trainData = train_collection.find_one({"_id": bson.ObjectId(trainId)})
            
            trainName = trainData['trainName']
            trainNumber = trainData['trainNumber']
            StartStation = trainData['originStation']
            destinationStation = trainData['destinationStation']
            bookingStatus = "confirmed"

            # Prepare the booking information
            booking = {
                "email": email,
                "mobile": mobile,
                "passengersCount": passengersCount,
                "journeyDate": journeyDate,
                "coachType": coachType,
                "totalPrice": totalPrice,
                "user": user,  # The user object fetched earlier
                "userId": userId,
                "trainName": trainName,
                "trainNumber": trainNumber,
                "StartStation": StartStation,
                "destinationStation": destinationStation,
                "bookingStatus": bookingStatus
            }
            
            # Insert the booking into the database
            result = booking_collection.insert_one(booking)
            success = True
            
        else:
            form = BookTrainForm()
            error = 'Invalid form data. Please try again.'
    else:
        form = BookTrainForm()

    return render(request, 'user/bookTrain.html', {
        "train": train,
        "form": form,
        "success": success,
        "error": error
    })

def loadBookings(request):
    return render(request, 'user/loadBookings.html')

def bookings(request, id):
    bookings = [b for b in booking_collection.find({"userId": id})]
    print(bookings)
    for b in bookings:
        b['id'] = str(b['_id'])
    return render(request, 'user/bookings.html', {"bookings":bookings})

def cancelUserTicket(request, id):
    success = False
    booking = booking_collection.update_one({"_id": bson.ObjectId(id)}, {"$set": {"bookingStatus": "Cancelled"}})
    success = True
    return render(request, 'user/cancel-booking.html', {"success":success})


def cancelTicket(request, id):
    success = False
    booking = booking_collection.update_one({"_id": bson.ObjectId(id)}, {"$set": {"bookingStatus": "Cancelled"}})
    success = True
    return render(request, 'admin/cancel-booking.html', {"success":success})

def admin(request):
    users = [u for u in users_collection.find()]
    usersCount = len(users)

    trains = [t for t in train_collection.find()]
    trainsCount = len(trains)

    bookings = [b for b in booking_collection.find()]
    bookingsCount = len(bookings)

    return render(request, 'admin/admin.html', {"usersCount": usersCount, "trainsCount": trainsCount, "bookingsCount":bookingsCount})

def allBookings(request):
    bookings = [b for b in booking_collection.find()]
    for b in bookings:
        b['id'] = str(b['_id'])
    return render(request, 'admin/allBookings.html', {"bookings":bookings})

def allUsers(request):
    users = [u for u in users_collection.find()]
    for u in users:
        u['id'] = str(u['_id'])
    return render(request, 'admin/allUsers.html', {"users": users})

def allTrains(request):
    trains = [t for t in train_collection.find()]
    for t in trains:
        t['id'] = str(t['_id'])
    return render(request, 'admin/allTrains.html', {"trains": trains})

def newTrain(request):
    success = False
    if request.method == 'POST':
        form = NewTrainForm(request.POST)
        if form.is_valid():
            trainNumber = form.cleaned_data['trainNumber']
            trainName = form.cleaned_data['trainName']
            originStation = form.cleaned_data['originStation']
            destinationStation = form.cleaned_data['destinationStation']
            totalSeats = form.cleaned_data['totalSeats']
            basePrice = form.cleaned_data['basePrice']
            departureTime = str(form.cleaned_data['departureTime'])
            arrivalTime = str(form.cleaned_data['arrivalTime'])

            train = {"trainNumber": trainNumber, "trainName": trainName, "originStation": originStation, "destinationStation": destinationStation, 
                    "totalSeats": totalSeats, "basePrice": basePrice, "departureTime": departureTime, "arrivalTime": arrivalTime}
            result = train_collection.insert_one(train)
   
            success = True
            
        else:
            form = NewTrainForm()
            error = 'Invalid form data. Please try again.'
    else:
        form = NewTrainForm()
    return render(request, 'admin/newTrain.html', {"form":form, "success": success})

def editTrain(request, id):
    success = False
    error = ''
    train = train_collection.find_one({"_id": bson.ObjectId(id)})
    if request.method == 'POST':
        form = NewTrainForm(request.POST)
        if form.is_valid():
            object_id = bson.ObjectId(id)

            trainNumber = form.cleaned_data['trainNumber']
            trainName = form.cleaned_data['trainName']
            originStation = form.cleaned_data['originStation']
            destinationStation = form.cleaned_data['destinationStation']
            totalSeats = form.cleaned_data['totalSeats']
            basePrice = form.cleaned_data['basePrice']
            departureTime = str(form.cleaned_data['departureTime'])
            arrivalTime = str(form.cleaned_data['arrivalTime'])

            train_collection.update_one({"_id": object_id}, {"$set": {"trainNumber": trainNumber, "trainName": trainName, "originStation": originStation, "destinationStation": destinationStation, 
                    "totalSeats": totalSeats, "basePrice": basePrice, "departureTime": departureTime, "arrivalTime": arrivalTime}})
            success = True
  
            
        else:
            form = NewTrainForm()
            print("erroruu")
            success = False
            error = 'Invalid form data. Please try again.'
    else:
        object_id = bson.ObjectId(id)
        train = train_collection.find_one({'_id': object_id})
        if train is None:
            error = "Error in fetching train!!"
            form = NewTrainForm()
        else:
            form = NewTrainForm(initial={
                            "trainNumber": train['trainNumber'], 
                            "trainName": train['trainName'], 
                            "originStation": train['originStation'], 
                            "destinationStation": train['destinationStation'], 
                            "totalSeats": train['totalSeats'],
                            "basePrice": train['basePrice'], 
                            "departureTime": train['departureTime'], 
                            "arrivalTime": train['arrivalTime']
                        })
    
    context = {'form': form, 'success': success, 'error': error}
    return render(request, 'admin/editTrain.html', context)