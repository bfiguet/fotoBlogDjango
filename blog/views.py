from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import models, forms

@login_required
def photo_upload(request):
	form = forms.PhotoForm()
	if request.method == 'POST':
		form = forms.PhotoForm(request.POST, request.FILES)
		if form.is_valid():
			photo = form.save(commit=False) #for not save in bd
			#set the uploader to the user before saving the model
			photo.uploader = request.user
			photo.save()
			return redirect('home')
	return render(request, 'blog/photo_upload.html', context={'form':form})

@login_required
def home(request):
	photos = models.Photo.objects.all()
	return render(request, 'blog/home.html', context={'photos': photos})