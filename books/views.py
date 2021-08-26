import json

from django.views     import View
from django.http      import JsonResponse
from django.db        import transaction

from datetime        import datetime
from stays.models    import RoomOption, Room
from books.models    import Book, Payment
from users.utils     import login_decorator

class BooksView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        books = Book.objects.filter(user=user).select_related('room','room__staytype').prefetch_related('room__staytype__staytypeimage_set').order_by('-created_at')[:5]
        data = [{
            "stay_id"  : book.room.staytype.id,
            "stay_name": book.room.staytype.name,
            "stay_img" : book.room.staytype.staytypeimage_set.all()[0].image_url,
            "room_id"  : book.room.id,
            "room_name": book.room.name,
            "check_in" : book.check_in,
            "check_out": book.check_out,
            "status"   : "이용완료" if book.status == True else "이용예정"
        } for book in books]
        return JsonResponse({"data":data}, status=200)

    @login_decorator
    @transaction.atomic
    def post(self, request):
        try:
            data        = json.loads(request.body)
            user        = request.user
            check_in    = data.get('CheckIn')
            check_out   = data.get('CheckOut')
            room_option = data.get('RoomOption')
            room_id     = data.get('Room')
            price       = data.get('Price')

            if not (check_in or check_out):
                return JsonResponse({"message":"INVALID_DATE"}, status = 400)
            
            if not price:
                return JsonResponse({"message":"Not_Exist_Price"}, status = 400)

            if not RoomOption.objects.filter(name=room_option, room_id=room_id).exists():
                return JsonResponse({"message":"INVALID_RoomOption"}, status=404)

            if not Room.objects.filter(id=room_id).exists():
                return JsonResponse({"message":"INVALID_Room_ID"}, status=404)

            check_in    = datetime.strptime(check_in, '%Y-%m-%d')
            check_out   = datetime.strptime(check_out, '%Y-%m-%d')
            room_option = RoomOption.objects.get(name=room_option,room_id=room_id)

            if check_in > check_out:
                return JsonResponse({"message":"INVALID_DATE"}, status = 400)
            
            book = Book.objects.create(
                check_in          = check_in,
                check_out         = check_out,
                room_id           = room_id,
                room_option       = room_option,
                user              = user
            )
            
            Payment.objects.create(book = book, amount = price)
            
            user.point -= price
            user.save()
            
            return JsonResponse({"message":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

