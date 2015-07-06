from django.shortcuts import render, get_object_or_404

def main_landing(request):
    return render(
        request, 
        'main_landing.html',
        {
        }
    )
