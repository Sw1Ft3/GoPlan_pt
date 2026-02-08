from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Schedule, Event
import json


def index(request):
    """Главная страница со списком расписаний"""
    try:
        schedules = Schedule.objects.all()
    except Exception as e:
        # Если таблица еще не создана, показываем пустой список
        schedules = []
        messages.warning(request, 'База данных не инициализирована. Выполните: py manage.py migrate')
    return render(request, 'schedules/index.html', {'schedules': schedules})


def schedule_detail(request, schedule_id):
    """Детальная страница расписания"""
    schedule = get_object_or_404(Schedule, id=schedule_id)
    events = schedule.events.all()
    
    # Группируем события по дням недели
    days_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    events_by_day = {}
    for day in days_order:
        events_by_day[day] = events.filter(day_of_week=day)
    
    return render(request, 'schedules/schedule_detail.html', {
        'schedule': schedule,
        'events_by_day': events_by_day,
        'days_order': days_order,
    })


def create_schedule(request):
    """Создание нового расписания"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        
        if title:
            schedule = Schedule.objects.create(title=title, description=description)
            messages.success(request, 'Расписание успешно создано!')
            return redirect('schedule_detail', schedule_id=schedule.id)
        else:
            messages.error(request, 'Название расписания обязательно!')
    
    return redirect('index')


def delete_schedule(request, schedule_id):
    """Удаление расписания"""
    if request.method == 'POST':
        schedule = get_object_or_404(Schedule, id=schedule_id)
        schedule.delete()
        messages.success(request, 'Расписание удалено!')
    return redirect('index')


def create_event(request, schedule_id):
    """Создание нового события"""
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        day_of_week = request.POST.get('day_of_week')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        color = request.POST.get('color', '#3b82f6')
        
        if title and day_of_week and start_time and end_time:
            Event.objects.create(
                schedule=schedule,
                title=title,
                description=description,
                day_of_week=day_of_week,
                start_time=start_time,
                end_time=end_time,
                color=color
            )
            messages.success(request, 'Событие успешно добавлено!')
        else:
            messages.error(request, 'Заполните все обязательные поля!')
    
    return redirect('schedule_detail', schedule_id=schedule_id)


def delete_event(request, event_id):
    """Удаление события"""
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        schedule_id = event.schedule.id
        event.delete()
        messages.success(request, 'Событие удалено!')
        return redirect('schedule_detail', schedule_id=schedule_id)
    return redirect('index')


def edit_event(request, event_id):
    """Редактирование события"""
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.title = request.POST.get('title', event.title)
        event.description = request.POST.get('description', event.description)
        event.day_of_week = request.POST.get('day_of_week', event.day_of_week)
        event.start_time = request.POST.get('start_time', event.start_time)
        event.end_time = request.POST.get('end_time', event.end_time)
        event.color = request.POST.get('color', event.color)
        event.save()
        messages.success(request, 'Событие обновлено!')
        return redirect('schedule_detail', schedule_id=event.schedule.id)
    
    return redirect('schedule_detail', schedule_id=event.schedule.id)
