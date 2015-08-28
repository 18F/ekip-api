from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def choose_adventure_type(request):
    if 'ok_to_start' not in request.session:
        return HttpResponseRedirect(reverse('student_pass'))

    return render(
        request,
        'adventure/choose_adventure.html',
    )


def game_start(request):
    if 'ok_to_start' not in request.session:
        return HttpResponseRedirect(reverse('student_pass'))

    request.session['game_start'] = True
        
    return render(
        request,
        'adventure/start.html',
    )


def swimming_end(request):
    if 'ok_to_start' not in request.session:
        return HttpResponseRedirect(reverse('student_pass'))

    selection = request.GET.get('selection', 'ocean')

    selector = {
        'ocean': "ocean",
        'lake': 'lake',
        'river': 'river'
    }
    request.session['game_end'] = True

    return render(
        request,
        'adventure/swimming_end.html',
        {
            'activity': 'swimming',
            'selection': selector[selection],
        }
    )


def swimming(request):
    if 'ok_to_start' not in request.session:
        return HttpResponseRedirect(reverse('student_pass'))

    if request.method == 'POST':
        selection = request.POST.get('selection', 'ocean')
        return HttpResponseRedirect(
            '%s?selection=%s' % (reverse('swimming_end'), selection))
    return render(request, 'adventure/swimming.html')


def time_travel_end(request):
    if 'ok_to_start' not in request.session:
        return HttpResponseRedirect(reverse('student_pass'))

    selection = request.GET.get('selection', 'dinosaur-tracks')

    selector = {
        'mlk-house': "Martin Luther King's house",
        'ancient-drawings': 'ancient drawings',
        'dinosaur-tracks': 'dinosaur tracks'
    }
    request.session['game_end'] = True

    return render(
        request,
        'adventure/time_travel_end.html',
        {
            'activity': 'time travel',
            'selection': selector[selection],
        }
    )


def time_travel(request):
    if 'ok_to_start' not in request.session:
        return HttpResponseRedirect(reverse('student_pass'))

    if request.method == 'POST':
        selection = request.POST.get('selection', 'dinosaur-tracks')
        return HttpResponseRedirect(
            '%s?selection=%s' % (reverse('time_travel_end'), selection))
    return render(request, 'adventure/time_travel.html')


def nature_walk(request):
    if 'ok_to_start' not in request.session:
        return HttpResponseRedirect(reverse('student_pass'))

    if request.method == 'POST':
        if 'huge-mountain' in request.POST:
            return HttpResponseRedirect(
                '%s?selection=mountains' % reverse('nature_walk_end'))
        elif 'wild-animals' in request.POST:
            return HttpResponseRedirect(
                '%s?selection=animals' % reverse('nature_walk_end'))
        else:
            return HttpResponseRedirect(
                '%s?selection=plants' % reverse('nature_walk_end'))
    return render(request, 'adventure/nature_walk.html')


def nature_walk_end(request):
    if 'ok_to_start' not in request.session:
        return HttpResponseRedirect(reverse('student_pass'))

    selection = request.GET.get('selection', 'mountains')

    selector = {
        'mountains': 'huge mountains',
        'animals': 'wild animals',
        'plants': 'beautiful plants'
    }

    request.session['game_end'] = True

    return render(
        request,
        'adventure/nature_walk_end.html',
        {
            'activity': 'nature walk',
            'selection': selector[selection],
        }
    )
