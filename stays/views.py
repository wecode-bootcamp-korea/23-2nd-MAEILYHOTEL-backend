from django.views     import View
from django.http      import JsonResponse
from django.db.models import Sum

from stays.models    import Room

class RoomView(View):
    def get(self, request, room_id):
        if not Room.objects.filter(id = room_id).exists():
            return JsonResponse({"message":"INVALID_ID"}, status=404)
        room    = Room.objects.get(id = room_id)
        data    = {
            "name"     : room.name,
            "people"   : room.people,
            "image_url": room.image_url,
            "options"  : [{
                "name"     : option.name,
                "check_in" : option.check_in,
                "check_out": option.check_out
            } for option in room.roomoption_set.all()],
        }
        return JsonResponse(data, status=200) 
