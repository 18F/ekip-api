from django.shortcuts import render


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
