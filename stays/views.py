from django.views     import View
from django.http      import JsonResponse
from django.db.models import Sum

from stays.models    import Staytype, RoomOption

class StayView(View):
    def get(self, request, stay_id):
        if not Staytype.objects.filter(id = stay_id).exists():
            return JsonResponse({"message":"INVALID_ID"}, status=404)
            
        stay = Staytype.objects.get(id = stay_id)
        room = RoomOption.objects.filter(name='숙박', room__staytype=stay)
        data = {
            "category"   : stay.category.name,
            "name"       : stay.name,
            "images"     : [stayimage.image_url for stayimage in stay.staytypeimage_set.all()],
            "total_rooms": stay.room_set.all().aggregate(total_rooms=Sum('quantity'))['total_rooms'],
            "facilities" : [facility.name for facility in stay.facility.all()],
            "address"    : stay.address,
            "long"       : stay.longitude,
            "lat"        : stay.latitude,
            "description": stay.description,
            "check_in"   : room[0].check_in,
            "check_out"  : room[0].check_out
        }
        return JsonResponse(data, status=200)