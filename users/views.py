from django.shortcuts import redirect, render, HttpResponse
from django.template import loader
from coding.settings import *
from django.core.mail import send_mail
from .models import DayTrack, Profile
from questions.models import Question
from django.contrib.auth.decorators import login_required
from django.template import loader

# Create your views here.


def index(request):
    context = {}

    if request.method == "POST":
        email = request.POST['email']
        print(email)

        try:
            profileObj = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            profileObj = None

        if profileObj is None:
            profileObj = Profile(email=email)
            profileObj.save()
            
        context['saved'] = email
        context['confirmation_link'] = request.build_absolute_uri(
            '') + f'confirm/{profileObj.id}'
        context['snooze_link'] = request.build_absolute_uri(
            '') + f'snooze/{profileObj.id}'
        context['resume_link'] = request.build_absolute_uri(
            '') + f'resume/{profileObj.id}'

        if profileObj.verified == False:

            # Sending email to activate account
            html_message = loader.render_to_string(
                'users/activate_account.html', context)

            send_mail(  
                subject = f'Activate your account',
                message = '',
                from_email = EMAIL_HOST_USER,
                recipient_list = [email],
                fail_silently=True,
                html_message=html_message)

            context['EmailSendPage'] = 'EmailSendPage'
            return render(request, 'users/index.html', context)

    return render(request, 'users/dailycoding.html', context)


def confirm(request, pk):
    context= {}
    try:
        profileObj = Profile.objects.get(id=pk)
        if profileObj is None:
            context['UserNotFound'] = 'UserNotFound'
            return render(request, 'users/index.html', context)

        profileObj.verified = True
        profileObj.save()

        # Setting the pause to 0 
        DayTrackObj = DayTrack.objects.get(profileOwner=profileObj)
        DayTrackObj.paused = 0
        DayTrackObj.save()

        context['AccountConfirmationPage'] = 'AccountConfirmationPage'

        return render(request, 'users/index.html', context)

    except Exception as e:
        context['UserNotFound'] = 'UserNotFound'
        return render(request, 'users/index.html', context)


def unsubscribe(request, pk):
    context = {}
    try:
        profileObj = Profile.objects.get(id=pk)
        if profileObj is None:
            context['UserNotFound'] = 'UserNotFound'
            return render(request, 'users/index.html', context)

        profileObj.verified = False
        profileObj.save()
        context['UnsubscribedAccount'] = 'UnsubscribedAccount'
        return render(request, 'users/index.html', context)

    except Exception as e:
        context['SomethingWentWrong'] = True
        return render(request, 'users/index.html', context)


def snooze(request, pk):
    context = {}
    DaytoNo = {'1 Day': 1, '1 Week': 7, '1 Month': 31, '3 Months': 90}
    try:
        profileObj = Profile.objects.get(id=pk)
        if profileObj is None:
            context['UserNotFound'] = 'UserNotFound'
            return render(request, 'users/index.html', context)

        DayTrackObj = DayTrack.objects.get(profileOwner=profileObj)
            
        if request.method == 'POST':
            pause_action = request.POST['action']
            if pause_action == "unsubscribe":
                return redirect(f"/unsubscribe/{pk}/")

            pauseDays = DaytoNo[pause_action]
            DayTrackObj.paused += pauseDays
            DayTrackObj.save()
            context['PausedAccount'] = pause_action
            return render(request, 'users/index.html', context)

    # Invalid URL
    except Exception:
        context['SomethingWentWrong'] = True
        return render(request, 'users/index.html', context)

    return render(request, 'users/unsubscribe.html', context)


def resume(request, pk):
    context = {}
    try:
        profileObj = Profile.objects.get(id=pk)
        if profileObj is None:
            context['UserNotFound'] = 'UserNotFound'
            return render(request, 'users/index.html', context)

        DayTrackObj = DayTrack.objects.get(profileOwner=profileObj)
        if DayTrackObj is None:
            context['UserNotFound'] = 'UserNotFound'
            return render(request, 'users/index.html', context)

        DayTrackObj.paused = 0
        DayTrackObj.save()
        context['ResumeQuestions'] = 'ResumeQuestions'
        return render(request, 'users/index.html', context)

    except Exception as e:
        context['SomethingWentWrong'] = True
        return render(request, 'users/index.html', context)


@login_required(login_url="/")
def send_question(request):
    verified_profile_Objs = Profile.objects.filter(verified = True)
    context = {}
    questions = {}
    for verified_profile_Obj in verified_profile_Objs:
        email = verified_profile_Obj.email
        DayRecord = DayTrack.objects.get(profileOwner = verified_profile_Obj)

        if DayRecord.paused > 0:
            DayRecord.paused -= 1
            DayRecord.save()
        else:
            questionNo = DayRecord.currentDay
            if questionNo <=7: 
                DayRecord.currentDay += 1
                question_obj = Question.objects.get(dayNo = questionNo)
                html_message = loader.render_to_string(
                'questions/single_question.html', {'question_object': question_obj})
                send_mail(
                    subject = f'Day #{question_obj.dayNo}',
                    message = html_message,
                    from_email = EMAIL_HOST_USER,
                    recipient_list = [email],
                    fail_silently=True,
                    html_message=html_message)
                DayRecord.save()

                # getting question 
                try:
                    QuestionObj = Question.objects.get(dayNo = questionNo)
                    questions[email] =  str(QuestionObj.dayNo) + " " +  QuestionObj.title
                except Exception as e:
                    print(e)
                    print("Question Not Found")
            else:
                questions[email] = 'Limit Over'
                # print("Thanks for subscribing, hopefully you have solved all the questions :)")

    context = {'questions': questions}
    
    return render(request, 'users/sendQuestion.html', context)