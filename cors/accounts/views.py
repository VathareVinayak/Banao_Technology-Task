from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignupForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Profile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type'],
                profile_picture=form.cleaned_data.get('profile_picture'),
                address_line1=form.cleaned_data['address_line1'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode'],
            )
            
            # Check if client expects JSON (API call) or regular browser form POST
            if request.headers.get('Accept') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'detail': 'User created successfully'}, status=201)
            else:
                # Redirect to login page after successful form submission in browser
                return HttpResponseRedirect('/accounts/login/')
        else:
            # Return errors as JSON for API or show form with errors in browser
            if request.headers.get('Accept') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return render(request, 'accounts/signup.html', {'form': form})
    # For GET request render form as usual
    form = UserSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            profile = Profile.objects.get(user=user)
            if request.headers.get('Accept') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'detail': 'Login successful',
                    'user_type': profile.user_type,
                    'username': user.username,
                })
            else:
                if profile.user_type == 'patient':
                    return redirect('patient_dashboard')
                else:
                    return redirect('doctor_dashboard')
        else:
            error_msg = "Invalid username or password"
            if request.headers.get('Accept') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': error_msg}, status=400)
            else:
                return render(request, 'accounts/login.html', {'error': error_msg})
    return render(request, 'accounts/login.html')


@login_required
def patient_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/patient_dashboard.html', {'profile': profile})

@login_required
def doctor_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/doctor_dashboard.html', {'profile': profile})

def logout_view(request):
    logout(request)
    return redirect('login')
