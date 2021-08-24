
from django.views     import View
from django.http      import JsonResponse

from books.models    import Book
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
            "check_out": book.check_out
        } for book in books]
        return JsonResponse({"data":data}, status=200)

        