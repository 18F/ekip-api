from django.shortcuts import render, get_object_or_404

def main_landing(request):
    return render(
        request, 
        'main_landing.html',
        {}
    )

def get_your_pass(request):
    return render(
        request, 
        'get_your_pass.html',
        {}
    )

def plan_your_trip(request):
    return render(
        request, 
        'plan_your_trip.html',
        {}
    )


def student_pass(request):
    return render(
        request, 
        'student_pass.html',
        {}
    )

def educator_passes(request):
    return render(
        request, 
        'educator_passes.html',
        {}
    )


def learn(request):
    return render(
        request, 
        'learn.html',
        {}
    )

