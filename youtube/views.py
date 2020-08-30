from django.shortcuts import render
from pytube import *
from .models import Links
from django.http import HttpResponseRedirect

http = ""
file_size = 0
percentage = 0


def home(request):
    total_links = Links.objects.all()
    return render(request, 'content.html', {"total_links": total_links})


def add_links(request):
    #getting the url
    global http
    http = request.POST["content"]

    #working with pytube
    ob = YouTube(http)
    rex = ob.streams.filter(progressive=True)


    #storing in the database
    for x in rex:
        Links.objects.create(link=x)

    return HttpResponseRedirect('/')


#percentage calculator
def progress(stream, chunk, bytes_remaining):
    global percentage
    #gets the percentage of the file that has been downloaded
    file_downloaded = file_size-bytes_remaining
    per = file_downloaded/file_size*100
    percentage = "{}".format(round(per))
    print(percentage)


#downloader
def downloader(request, pl):
    global file_size
    steam = Links.objects.get(id=pl).link
    ob = YouTube(http, on_progress_callback=progress)
    rex = ob.streams
    rex = list(rex)

    mylist = []

    for x in rex:
        if str(x) in steam:
            mylist.append(x)

    #download location
    download_loc = r"C:\Users\chand\Downloads"

    trex = mylist[0]

    file_size = trex.filesize

    trex.download(download_loc)

    Links.objects.all().delete()

    return HttpResponseRedirect("/")

    
