from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import Person

import face_recognition
import numpy as np
import json

@csrf_exempt
def addPerson(request):
	if request.method == "POST":
		name = request.POST.get('name')
		age = request.POST.get('age')
		parentContactNumber = request.POST.get('contact')
		address = request.POST.get('address')
		height = request.POST.get('height')
		weight = request.POST.get('weight')
		about = request.POST.get('about')
		image = request.FILES['image']

		image1 = face_recognition.load_image_file(image)
		encoded = face_recognition.face_encodings(image1)[0]

		try:
			temp = Person.objects.create(name = name, age = age, parentContactNumber = parentContactNumber, address = address, height = height, weight = weight, about = about, image = image)
			temp.save()
		except Exception as e:
			return HttpResponse(e)

		return HttpResponse('Successfully added ' + temp.name)

@csrf_exempt
def comparePerson(request):
	image = request.FILES['image']

	image_input = face_recognition.load_image_file(image)
	encoded_input = face_recognition.face_encodings(image_input)[0]
	print(encoded_input)

	matched = []

	for person in Person.objects.all():
		target_image_path = person.image.path
		target_image = face_recognition.load_image_file(target_image_path)
		encoded_target = face_recognition.face_encodings(target_image)[0]

		dic = {}

		result = face_recognition.compare_faces([encoded_target], encoded_input)
		if result[0]:
			dic['name'] = person.name
			dic['parentContactNumber'] = person.parentContactNumber
			dic['height'] = person.height
			dic['weight'] = person.weight
			dic['date_of_missing'] = person.date_of_missing
			dic['place_of_missing'] = person.place_of_missing
			dic['is_missing'] = person.is_missing
			dic['address'] = person.address
			print('Matched: ' + person.name)
			matched.append(dic)		

	return HttpResponse(json.dumps(matched))

