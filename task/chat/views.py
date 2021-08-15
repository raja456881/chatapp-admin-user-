from django.shortcuts import render
# Create your views here.

def room(request, username):
    try:
        user=request.user
        return render(request, 'chat/index.html', {
            'room_name':"username"
            })
    except:
        return render(request, 'chat/index.html')