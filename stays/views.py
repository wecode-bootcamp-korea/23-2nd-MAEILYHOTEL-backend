from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q, F, Count, Sum, Min, Case, When, Subquery, OuterRef

from datetime        import datetime, timedelta
from stays.models    import Staytype, RoomOption
from books.models    import Book

class StaytypeListView(View):
    def get(self, request):
        category_id = request.GET.get('category', None)
        location    = request.GET.get('location', None)
        check_in    = request.GET.get('CheckIn', None)
        check_out   = request.GET.get('CheckOut', None)

        if not (check_in and check_out):
            return JsonResponse({"message":"INVALID_DATE"}, status = 400)

        check_in  = datetime.strptime(check_in, '%Y-%m-%d')
        check_out = datetime.strptime(check_out, '%Y-%m-%d')

        q = Q()

        if category_id:
            q &= Q(category = category_id) 

        if location:
            q &= Q(address__icontains = location) 

        stays = Staytype.objects.filter(q)

        if check_in and check_out:
            q1 = Q(room__book__check_in__range = [check_in, check_out])
            q2 = Q(room__book__check_out__range = [check_in, check_out])
            q3 = Q(room__book__check_in__lte = check_in, room__book__check_out__gte = check_out)

            stays = Staytype.objects.filter(q).prefetch_related('room_set', 'room_set__book_set').annotate(
                total_room_count = Sum('room__quantity'), 
                booked_room_count = Subquery(
                    Staytype.objects.annotate(booked_count = Count('room__book__id', filter = (q1|q2|q3))).filter(pk = OuterRef('pk')).values('booked_count')
                    ), 
                    is_available = Case(
                        When(total_room_count__gt = F('booked_room_count'), then = True), 
                        default = False
                    )
            ).exclude(is_available = False)   
        
        response = {
                "staylist" : [{
                    "id"        : stay.id,
                    "name"      : stay.name,
                    "image_url" : stay.staytypeimage_set.all()[0].image_url,
                    "price"     : int(RoomOption.objects.filter(room__staytype__id = stay.id).aggregate(price=Min('price'))['price'])
                } for stay in stays]
            }
        
        return JsonResponse(response, status = 200)

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

class StayCalendarView(View):
    def get(self, request, stay_id):
        if not Staytype.objects.filter(id = stay_id).exists():
            return JsonResponse({"message":"INVALID_ID"}, status=404)

        today       = request.GET.get('Date')

        if not today:
            return JsonResponse({"message":"INVALID_DATE"}, status = 400)
            
        today       = datetime.strptime(today, '%Y-%m-%d').date()
        after_month = today + timedelta(days=30)
        q1          = Q(check_in__gte=today) & Q(check_in__lte=after_month)
        q2          = Q(check_out__gte=today) & Q(check_out__lte=after_month)
        q3          = Q(check_in__lt=today,check_out__gt=after_month)
        stay      = Staytype.objects.filter(id=stay_id).annotate(quantity = Sum('room__quantity'))[0]
        min_price = RoomOption.objects.filter(room__staytype=stay).aggregate(min=Min('price'))['min']
        date_list = [today + timedelta(i) for i in range(30)]
        books     = Book.objects.filter(room__staytype=stay, room_option__name='숙박').filter(q1|q2|q3)
        result    = {}
        for date in date_list:
            price       = min_price
            books_count = 0
            for book in books:
                if book.check_in < date and book.check_out > date:
                    books_count += 1

            price    = Staytype.get_discount_one_price(price=price, date=date)
            date     = str(date)
            quantity = stay.quantity - books_count

            result[date] = {
                'price'   : round(price,-2),
                'quantity': quantity
                }
        return JsonResponse({'result' : result}, status=200)
