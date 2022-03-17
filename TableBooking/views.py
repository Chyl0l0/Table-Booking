import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import RoomForm, BookingForm
from .models import Room, Table, Booking
# Create your views here.
from django.db.models import Q
from django.views.generic.list import ListView
from django.contrib.admin.views.decorators import staff_member_required

room_form = None
booking_form = None


def index(request):
    return render(request, 'TableBooking/index.html')


@staff_member_required
def create_room(request):
    form = RoomForm()
    context = {'form': form}
    global room_form
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room_form = form
            return redirect('create-layout')
    return render(request, 'TableBooking/create_room.html', context)


@staff_member_required
def create_layout(request):
    global room_form

    if room_form is None:
        return redirect('create-layout')

    rows = room_form.cleaned_data['rows']
    cols = room_form.cleaned_data['columns']

    context = {'rows': range(rows), 'cols': range(cols)}

    if request.method == 'POST':
        seat_list = []
        for pos, data in request.POST.items():
            seats = 0
            try:
                seats = int(data)
            except ValueError:
                continue
            if seats > 0:
                x, y = pos.split('_')
                seat_list.append((int(x), int(y), seats))
        print(room_form)
        room = Room(rows=rows, columns=cols, tables_number=len(seat_list),
                    date_from=room_form.cleaned_data['date_from'], date_to=room_form.cleaned_data['date_to'])
        room.save()
        for x, y, seats in seat_list:
            Table(room=room, seats_number=seats, x_pos=x, y_pos=y).save()
        return redirect('index')

    return render(request, 'TableBooking/create_layout.html', context)


@login_required
def create_booking(request):
    form = BookingForm()
    context = {'form': form}
    global booking_form
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_form = form
            return redirect('select-table')
    return render(request, 'TableBooking/create_booking.html', context)


@login_required
def select_table(request):
    def gen_tables(x, y):
        print(bookings)

        for t in q_tables:
            if t.x_pos == x and t.y_pos == y:
                if t in tables:
                    return x, y, t.seats_number, 'reserved'
                else:
                    return x, y, t.seats_number, 'free'
        return x, y, 0, 'unavailable'
    global booking_form

    lst_tables =[]
    date = booking_form.cleaned_data['date']
    duration = booking_form.cleaned_data['duration']
    time = booking_form.cleaned_data['time']
    timeTo = (datetime.datetime.combine(date,time) + datetime.timedelta(hours=duration)).time()
    room = Room.objects.filter(date_from__lte= date, date_to__gte= date)[0]
    rows = room.rows
    cols = room.columns
    print(room)
    q_tables = Table.objects.filter(room=room)
    print(q_tables)
    bookings = Booking.objects.filter(Q(table__in=q_tables) & Q(date=date) & (Q(time__lt=time) & Q(timeTo__gt=time) |
                                                                              Q(time__lt=timeTo) & Q(timeTo__gt=timeTo) |
                                                                              Q(time__gt=time) & Q(timeTo__lt=timeTo)
                                                                              ))
    tables = [b.table for b in bookings]
    for i in range(rows):
        for j in range(cols):
            lst_tables.append(gen_tables(i, j))
    context = {'rows': rows, 'cols': cols, 'tables': lst_tables}
    if request.method == 'POST':
        print(request.POST)
        if 'radAnswer' in request.POST:
            x, y = request.POST.get('radAnswer').split('_')
            Booking(user=request.user, table=q_tables.filter(x_pos=x,y_pos=y)[0], date=date, time=time, timeTo=timeTo, duration=duration).save()
            return redirect('index')
    return render(request, 'TableBooking/select_table.html', context)



class UserBookings(ListView):
    context_object_name = 'user_bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class TodayBookings(ListView):
    template_name = 'TableBooking/today_bookings.html'
    context_object_name = 'today_bookings'

    def get_queryset(self):
        return Booking.objects.filter(date=datetime.date.today())
