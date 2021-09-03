#Importing Packages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
import cv2
import threading
import os
import numpy as np
import time
import datetime
from . import YoloDetector
from .forms import ClassForm, DeleteForm
from .models import Users, Datatable
from .serializers import cvserializer
# Create your views here.

CLASSES = 0
VIDEO_LOCATION = 0


def say(request):
    print('v', os.getcwd())
    if(request.method == 'POST'):
        form = ClassForm(request.POST)
        if form.is_valid():
            val = form.cleaned_data.get("classes_field")
            print('val', val)
            return render(request, 'hello.html', {'form': form, 'val':val})
    
    else:
        form=ClassForm()
        return render(request, 'hello.html', {'form': form})
    


class VideoCamera(object):
    
    def __init__(self):
        self.detected_classes = []
        with open(os.path.join(os.getcwd(), "cv", "coco_names.txt"), 'r') as f:
            self.classes = [w.strip() for w in f.readlines()]
        #print("Default classes: \n", self.classes)
        self.selected = {}
        global CLASSES, VIDEO_LOCATION
        for iclasses in CLASSES:
            self.selected[iclasses] = (0, 0, 255)
        print('self.selected', self.selected)
        self.detector = YoloDetector.YoloDetector(os.path.join(os.getcwd(), "cv", "yolov3-tiny.cfg"), 
            os.path.join(os.getcwd(), "cv", "yolov3-tiny.weights"), 
            self.classes)
        video_location = os.path.join(os.getcwd(), "static", VIDEO_LOCATION)
        self.video = cv2.VideoCapture(video_location)
        print('video open?', self.video.isOpened())
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):

        detections = self.detector.detect(self.frame)
        for cls, color in self.selected.items():
            if cls in detections:
                self.detected_classes.append(cls)
                for box in detections[cls]:
                    x1, y1, x2, y2 = box
                    self.frame = cv2.rectangle(self.frame, (x1, y1), (x2, y2), color, thickness=1)
                    self.frame = cv2.putText(self.frame, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)
        #cv2.imshow("detections", frame)

        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        try:
            while(self.grabbed==True):
                (self.grabbed, self.frame) = self.video.read()
                time.sleep(0.1)
        except Exception as e:
            print('Exception-update', e)
        finally:
            record = Datatable.objects.create(classes=','.join(str(e) for e in self.detected_classes), date_d=datetime.date.today())
            record.save()
            #print('datatable', Datatable.objects.all())


def gen(camera):
    try:
        while True:
            frame = camera.get_frame()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    except Exception as e:
        pass

@gzip.gzip_page
def livefe(request):

    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e: 
        print('Exception-livefe', e)

def stream(request):
    return render(request, 'streem.html')

def delete_record(val=15):
    try:
        days_ago = datetime.date.today() - datetime.timedelta(days=val)
        records = Datatable.objects.filter(date_d=days_ago)
        if(records):
            print('days_ago', days_ago)
            record = Datatable.objects.filter(date_d=days_ago).delete()
            return(True)
        else:
            print('No record is found')
            return(False)
    except Exception as e:
        print('Exception-delete_record', e)

def delete_record1(request):
    if(request.method == 'POST'):
        form1 = DeleteForm(request.POST)
        if form1.is_valid():
            val = form1.cleaned_data.get("delete_field")
            print('val', val)
            if(delete_record(val)):
                print('Deleted')
            else:
                print('Not Deleted')
            return HttpResponseRedirect("/cv/st/")
    
    else:
        return render(request, 'streem1.html', {'form': ClassForm(request), 'form1':DeleteForm()})
    


def stream1(request):
    if(request.method == 'POST'):
        form = ClassForm(request, request.POST)
        if form.is_valid():
            val = form.cleaned_data.get("classes_field")
            video_location = form.cleaned_data.get("video_location")
            #print('val', val, video_location)
            request.session.setdefault('classes_field', 'person')
            request.session['classes_field'] = val
            global CLASSES, VIDEO_LOCATION
            CLASSES = val
            VIDEO_LOCATION = video_location
            return render(request, 'streem1.html', {'form':ClassForm(request), 'form1':DeleteForm(), 'flag':True})
    else:
        return render(request, 'streem1.html', {'form': ClassForm(request), 'form1':DeleteForm()})
    

class FileUploadView1(APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request, format='mp4'):
        up_file = request.FILES['data']
        destination = open("/home/vishakraj94/project1/static/"+up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close() 

        output_name = detector(up_file.name)
        output_data = "Download the file-https://127.0.0.1:8000/static/"+output_name
        return Response(output_data, status.HTTP_201_CREATED)
