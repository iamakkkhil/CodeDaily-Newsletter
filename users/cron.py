from django.core.mail import send_mail
from users.models import DayTrack, Profile
from questions.models import Question
from coding.settings import *
from django.template import loader


def send_daily_question():
    verified_profile_Objs = Profile.objects.filter(verified = True)
    host_url = 'http://127.0.0.1:8000/''https://iamakkkhil.pythonanywhere.com/'

    for verified_profile_Obj in verified_profile_Objs:
        email = verified_profile_Obj.email
        DayRecord = DayTrack.objects.get(profileOwner = verified_profile_Obj)
        if DayRecord.paused > 0:
            DayRecord.paused -= 1
            DayRecord.save()
        else:
            questionNo = DayRecord.currentDay 
            snooze = host_url + f'snooze/{verified_profile_Obj.id}'

            if questionNo <=7: 
                DayRecord.currentDay += 1
                
                question_obj = Question.objects.get(dayNo = questionNo)

                report = host_url + f'questions/report/{question_obj.dayNo}'

                html_message = loader.render_to_string(
                'questions/QuestionsTemplate.html', {'question_object': question_obj, 'snooze': snooze, 'report':report})
                send_mail(
                    subject = f'Day #{question_obj.dayNo}',
                    message = html_message,
                    from_email = EMAIL_HOST_USER,
                    recipient_list = [email],
                    fail_silently=True,
                    html_message=html_message)

                DayRecord.save()

            elif questionNo == 8:
                DayRecord.currentDay += 1
                html_message = loader.render_to_string(
                'questions/congratsEmail.html', {'snooze': snooze})
                send_mail(
                    subject = f'🎉 #7DaysofCode Completed!',
                    message = html_message,
                    from_email = EMAIL_HOST_USER,
                    recipient_list = [email],
                    fail_silently=True,
                    html_message=html_message)

                DayRecord.save()