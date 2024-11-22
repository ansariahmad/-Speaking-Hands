import cv2
import time
import random
import joblib
import numpy as np
import pandas as pd
import mediapipe as mp
from datetime import datetime
from django.http import JsonResponse
from django.core.mail import send_mail
from sklearn.metrics import accuracy_score
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from cvzone.HandTrackingModule import HandDetector
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import DashBoard, LoginAttempts, LoginDateTime


prediction_dict = dict()
accuracy_dict = dict()
curnt_key = 0
start = 0
prediction_dict[0] = dict()
prediction_dict[curnt_key][start] = []

id_ = 1
user_ = None
otp_code = None



accuracy_dict[0] = dict()
accuracy_dict[curnt_key][start] = None

video_data = []


svm = joblib.load("static/svm_advanced_2.pkl")
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Create your views here.
# @login_required(login_url='login')



new_user = []

def SignApp(request):
    return render(request, 'SignApp.html')

def test(request):
    return render(request, 'test.html')

def index(request):
    return render(request, 'index.html')

def logoutPage(request):
    logout(request)
    return redirect('SignApp')
    #return redirect('SignApp')

def video(request):
    return render(request, 'video.html')
    
def admin_view_predictions(request, id):
    dashboard = DashBoard.objects.filter(user_id_id=id)
    return render(request, 'user_predictions.html', {'data':dashboard})

def admin_view_login_stats(request, id):
    login_attempt = None
    logindatetime = None
    try:
        login_attempt = LoginAttempts.objects.get(id=id)
        logindatetime = LoginDateTime.objects.filter(user_id_id=id)
    except:
        return render(request, "user_login_statistics.html", {"attempt":login_attempt,
                                                            "logindatetime":logindatetime})
    return render(request, "user_login_statistics.html", {"attempt":login_attempt,
                                                            "logindatetime":logindatetime})

def verify_otp_signup(request):
    global otp_code
    global new_user
    if request.method == "POST":
        otp = int(request.POST.get("otp"))
        if otp != otp_code:
            return render (request,'otp.html', {"email" : f"{new_user[1]}", "error" : "Incorrect OTP! Check your Gmail."})
        else:
            my_user=User.objects.create_user(new_user[0],new_user[1],new_user[2])
            my_user.save()
            
            user_login = LoginAttempts(id=my_user.id, user_id_id=my_user.id, login_attempts=1)
            user_login.save()
            
            # save login date and time
            current_date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            datetime_object = datetime.strptime(current_date_time, "%Y-%m-%d %H:%M:%S")
            date = datetime_object.date()
            time_ = datetime_object.time()
            id = LoginDateTime.objects.order_by("-id").first()
            if id == None:
                id = 1
            else:
                id = int(id.id)
                id += 1
            logindatetime = LoginDateTime(id=id, user_id_id=my_user.id, login_date=date, login_time = time_)
            logindatetime.save()
            otp_code = None
            new_user = []
            return redirect('login')

    
def signup(request):
    global otp_code
    global new_user
    my_user = None
    user = None
    
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return render (request,'signup.html', {"data" : "Passwords don't match!"})
        else:
            try:
                user = User.objects.get(email=email)
                try:
                    my_user=User.objects.create_user(uname,email,pass1)
                except:
                    return render (request,'signup.html', {"data" : "This username already exists!"})
            except:
                try:
                    my_user=User.objects.create_user(uname,email,pass1)
                except:
                    return render (request,'signup.html', {"data" : "This username already exists!"})
            finally:
                if user != None:
                    if my_user != None:
                        my_user.delete()
                    return render (request,'signup.html', {"data" : "This email already exists!"})
                else:
                    if my_user != None:
                        my_user.delete()
                
            otp_code = random.randint(100000, 999999)
            send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            'speaksign8@gmail.com',
            [email],
            fail_silently=False,
        )
            new_user.extend([uname, email, pass1])
            return render (request,'otp.html', {"email" : f"{email}", "data" : " "})
            

    return render (request,'signup.html')

def admin_view(request):
    user = User.objects.all()
    return render(request, "admin.html", {'data' : user})

def admin_login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        pass1 = request.POST.get('pass')
        try:
            admin = User.objects.get(username = username)
        except:
            return render(request, "adminlogin.html", {"error": "Incorrect Username"})
        if (admin.check_password(pass1)) and (admin.is_superuser == True):
            user = User.objects.all()
            return render(request, 'admin.html', {'data': user})
        else:
            return render(request, "adminlogin.html", {"error": "Incorrect credientials!!!"})
    return render(request, "adminlogin.html")


def admin_logout(request):
    logout(request)
    return redirect('SignApp')

def login_view(request):
    global user_
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        user_=user
        if user is not None:
            if user.is_superuser == 1:
                return render (request, "login.html", {"error":"Do not try to login !!!"})
            id_ = user.id
            login_attempt = LoginAttempts.objects.get(user_id_id=id_)
            user_login = LoginAttempts(id=id_, user_id_id=id_, login_attempts=login_attempt.login_attempts+1)
            user_login.save()
            login(request,user)
            
            # save login date and time
            current_date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            datetime_object = datetime.strptime(current_date_time, "%Y-%m-%d %H:%M:%S")
            date = datetime_object.date()
            time_ = datetime_object.time()
            id = LoginDateTime.objects.order_by("-id").first()
            id = int(id.id)
            id += 1
            logindatetime = LoginDateTime(id=id, user_id_id=id_, login_date=date, login_time = time_)
            logindatetime.save()
            return redirect('SignApp')
        else:
            return render (request, "login.html", {"error":"Invalid Credientials !!!"})

    return render (request,'login.html')

@login_required
def updatepass(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            user = request.user
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('SignApp')  # Redirect to a success page or profile page
        else:
            # messages.error(request, 'Passwords do not match.')
            return render(request, "updatepass.html", {"error" : "Passwords don't match"})
    return render(request, 'updatepass.html')

def forget_password_email(request):
    global user_
    global otp_code
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email = email)
            user_ = user
        except:
            return render(request, "forgetpass-email.html", {"error" : "Email doesn't exist!"})
        otp_code = random.randint(100000, 999999)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            'speaksign8@gmail.com',
            [email],
            fail_silently=False,
        )
        return render(request, "forgetpass-otp.html")
    return render(request, "forgetpass-email.html")

def forget_password_otp(request):
    global otp_code
    if request.method == "POST":
        otp = int(request.POST['otp'])
        if otp != otp_code:
            return render(request, "forgetpass-otp.html", {"error" : "incorrect otp!"})
        return render(request, "forget-update-pass.html")
    return render(request, "forgetpass-otp.html")

def forget_updatepass(request):
    global user_
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user = user_
            user.set_password(password)
            user.save()
            user_ = None
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            return redirect('SignApp')  # Redirect to a success page or profile page
        else:
            # messages.error(request, 'Passwords do not match.')
            return render(request, "forget-update-pass.html", {"error" : "Passwords don't match"})
    return render(request, 'forget-update-pass.html')

def simple_process_frame(request):
    image_data = request.POST.get('image_data')
    image = process_image_data(image_data)
    res = predict(image)
    return JsonResponse({"first_array" : res})

def process_frame(request):
    global curnt_key
    global prediction_dict
    image_data = request.POST.get('image_data')
    image = process_image_data(image_data)
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    landmarks_list = []

    # Check if landmarks are found
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Append hand landmarks to the list
            for landmark in hand_landmarks.landmark:
                # Each landmark has x, y, and z (depth) coordinates
                x, y, z = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0]), int(landmark.z * image.shape[1])
                # x, y, z = landmark.x, landmark.y, landmark.z
                landmarks_list.append((x, y, z))
    
    res = predict(image)

    if (res != "Nothing") and (curnt_key != 0):
        
        prediction_dict[curnt_key][start].append(res)
        
        temp_len = len(prediction_dict[curnt_key][start])
        score = accuracy_score([curnt_key]*temp_len, prediction_dict[curnt_key][start])
        accuracy_dict[curnt_key][start] = score
    return JsonResponse({"first_array" : res})

def predict(img):
    detector = HandDetector(staticMode=True, detectionCon=0.7, maxHands=1)
    hands, img = detector.findHands(img, draw=False)
    if hands:
        hand = hands[0]
        if hand['type'] == "Left":
            return "Nothing"
        landmarks = preprocess(np.array(hand['lmList']).flatten())
        # pred = svm.predict(landmarks.reshape(1, -1))
        # return "Hand Found"
        res = svm.predict(landmarks.reshape(1, -1))
        return int(res[0])
    return "Nothing"

def preprocess(landmarks):
        base_x, base_y, base_z = landmarks[0], landmarks[1], landmarks[2]
        for idx, value in enumerate(landmarks):
            if idx in range(0, 62, 3):
                landmarks[idx] -= base_x
            elif idx in range(1, 62, 3):
                landmarks[idx] -= base_y
            else:
                landmarks[idx] -= base_z
        
        max_val = max(list(map(abs, landmarks)))
        landmarks = landmarks / max_val
        return landmarks

def process_image_data(image_data):
    import base64
    import numpy as np
    
    encoded_data = image_data.split(',')[1]
    decoded_data = base64.b64decode(encoded_data)
    image_array = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), -1)
    
    # Implement your image processing logic here
    # For simplicity, let's just return the first array
    return image_array

def process_button(request):
    global start
    global curnt_key
    global prediction_dict
    global accuracy_dict
    
    button = request.POST.get('button')
    current_time = time.localtime()
    start = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    curnt_key = int(button)
#  prediction_dict[curnt_key] = []
    if curnt_key not in prediction_dict:
        prediction_dict[curnt_key] = dict()
    if curnt_key not in accuracy_dict:
        accuracy_dict[curnt_key] = dict()
    
    accuracy_dict[curnt_key][start] = 0
    prediction_dict[curnt_key][start] = []
    
    return JsonResponse({"button" : button})




@require_POST
def handle_button_click(request):
    global id_
    global prediction_dict
    global accuracy_dict
    
    id_ = int(request.user.id)
    joblib.dump(prediction_dict, "static/prediction.pkl")
    joblib.dump(accuracy_dict, "static/accuracy.pkl")
    
    dates = []
    letters = []
    times = []
    total_predictions = [] 
    accuracies = []
    corrects = []
    incorrects = []

    # You can process the request here
    data = request.POST.get('clicked')
    if data == 'true':
        primary_ = 1
        if len(prediction_dict) == 1:
            response_data = {'message':'No Progress has been made.'}
        else:
            for letter in list(prediction_dict.keys())[:]:
                for time in list(prediction_dict[letter].keys()):
                    if len(prediction_dict[letter][time]) == 0:
                        del prediction_dict[letter][time]
            
            for letter in list(prediction_dict.keys())[:]:
                letters.extend([letter]*len(prediction_dict[letter]))
                for time in list(prediction_dict[letter].keys()):
                    datetime_object = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

                    # Extract date and time
                    date = datetime_object.date()
                    time_ = datetime_object.time()
            
                    times.append(time_)
                    dates.append(date)
                    total_predictions.append(len(prediction_dict[letter][time]))
                    accuracies.append(round(accuracy_dict[letter][time], 4))
                    temp = pd.Series(prediction_dict[letter][time])
                    corrects.append((temp == letter).sum())
                    incorrects.append(len(temp) - (temp == letter).sum())
                    last_record = DashBoard.objects.order_by('-id').first()
                    if last_record == None:
                        primary_ = 1
                    else:
                        primary_ = last_record.id + 1
            for idx in range(len(letters)):                
                data = None
                data = DashBoard(id=int(primary_), c_date=dates[idx], c_time=times[idx], button_pressed=letters[idx], 
                            total_predictions=total_predictions[idx], correct_predictions=corrects[idx], 
                            incorrect_predictions=incorrects[idx], accuracy=accuracies[idx], user_id_id=id_)
                primary_ += 1
                data.save()                    
            # Do something if the button was clicked
            response_data = {'message': 'Progress has been saved!'}
            
            prediction_dict = dict()
            accuracy_dict = dict()
            curnt_key = 0
            start = 0
            prediction_dict[0] = dict()
            prediction_dict[curnt_key][start] = []

            accuracy_dict[0] = dict()
            accuracy_dict[curnt_key][start] = None
    else:
        response_data = {'message': 'No click detected'}

        return JsonResponse({'status': 'failed'}, status=400)
    return JsonResponse(response_data)

def dashboard_view(request):
    data = DashBoard.objects.filter(user_id_id=request.user.id)
    return render(request, 'DashBoard.html', {'data': data})

def home(request):
    return render(request, 'home.html')