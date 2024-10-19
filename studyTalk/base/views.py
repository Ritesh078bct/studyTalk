from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from .forms import RoomForm,RegistrationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User

from django.db.models import Q
# from django.http import HttpResponse
# Create your views here.

def index(request):
    rooms=Room.objects.all()
    topics=Topic.objects.all()
    messages=Message.objects.all()
    # for room in rooms:
    #     for participant in room.participants.all():
    #         print(participant)
    return render(request, 'base/index.html',{'rooms':rooms,'topics':topics,'messages':messages}) # This is the view function that will be called when the URL is visited. It will render the index.html template.

@login_required
def createRoom(request):
    if request.method == 'POST':
        form = RoomForm(request.POST,)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('index')

    else:
        form=RoomForm()
    return render(request, 'base/create-room.html',{'form':form})

@login_required
def updateRoom(request,room_id):
    # print(request)
    room = get_object_or_404(Room,pk=room_id,host=request.user)
    if request.method == "POST":
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('index')
    else:
        form=RoomForm(instance=room)
    return render(request,'base/update-room.html',{'form':form})

@login_required
def deleteRoom(request,room_id):
    room = get_object_or_404(Room,pk=room_id,host=request.user)
    if request.method == "POST":
        room.delete()
        return redirect('index')
    return render(request,'base/delete-room.html')


def registerUser(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('index')
    else:
        form=RegistrationForm()
    return render(request,'registration/register.html',{"form":form})







def search_feature(request):

    topics=Topic.objects.all()

    if request.method=="GET":
        q = request.GET.get('q') 
        rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
        return render(request, 'base/search-result.html', { 'rooms':rooms,'topics':topics})
    
    # Check if the request is a post request.
   
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        rooms = Room.objects.filter(name__contains=search_query)
        return render(request, 'base/search-result.html', {'query':search_query, 'rooms':rooms,'topics':topics})
    else:
        return render(request, 'base/search-result.html',{'topics':topics})
    


def room(request,room_id):
    room=get_object_or_404(Room, pk=room_id)
    room_messages=room.message_set.all()
    participants=room.participants.all()
    if request.method == "POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            message=request.POST.get('message')
        )
        room.participants.add(request.user)
        return redirect('room',room_id=room_id)
    else:
        pass
    context={
        'room':room,
        'messages':room_messages,
        'participants':participants
        }
    return render(request,'base/room.html',context)




@login_required
def deleteMessage(request,message_id):
    message = get_object_or_404(Message,pk=message_id,user=request.user)
    if request.method == "POST":
        message.delete()
        return redirect('room',room_id=message.room.id)
    return render(request,'base/delete-message.html')


def userProfile(request,user_id):
    # user = User.objects.get(id=user_id)
    user=get_object_or_404(User,pk=user_id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    print(user)
    context = {'feed-user': user, 'rooms': rooms,
               'messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)