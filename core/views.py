from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import Person
from django.core.files.base import ContentFile

import face_recognition
import numpy as np
import json
import base64
from tempfile import TemporaryFile


@csrf_exempt
def addPerson(request):
	if request.method == "POST":
		name = request.POST.get('name')
		age = request.POST.get('age')
		fathersName = request.POST.get('father')
		nearest_police_station = request.POST.get('nearest_police_station')
		complexion = request.POST.get('complexion')
		parentContactNumber = request.POST.get('contact')
		address = request.POST.get('address')
		height = request.POST.get('height')
		weight = request.POST.get('weight')
		image = base64.b64decode(request.POST.get('image')) #request.FILES['image'].encode()))
		place_of_missing = request.POST.get('place_of_missing')

		try:
			temp = Person.objects.create(name = name, age = age, parentContactNumber = parentContactNumber, address = address, height = height, weight = weight, place_of_missing = place_of_missing, fathersName = fathersName, nearest_police_station= nearest_police_station, complexion=complexion)
			temp.image.save('absc.jpeg', ContentFile(image))
			print(type(ContentFile(image)))
			temp.save()
		except Exception as e:
			return HttpResponse(e)

		return HttpResponse('Successfully added ' + temp.name)

@csrf_exempt
def comparePerson(request):
	from django.core.files.uploadedfile import InMemoryUploadedFile
	from io import BytesIO

	data = base64.b64decode(request.POST.get('image'))
	print('data type ', type(data))
	buf = BytesIO(data)
	buf.seek(0, 2)
	image = InMemoryUploadedFile(buf, "image", "some_filename.png", None, buf.tell(), None)
	
	image_input = face_recognition.load_image_file(image)
	encoded_input = face_recognition.face_encodings(image_input)[0]

	matched = []

	for person in Person.objects.all():
		target_image_path = person.image.path
		target_image = face_recognition.load_image_file(target_image_path)
		encoded_target = face_recognition.face_encodings(target_image)[0]

		dic = {}

		result = face_recognition.compare_faces([encoded_target], encoded_input)
		if result[0]:
			dic['name'] = person.name
			dic['image_url'] = person.image.url
			dic['father_name'] = person.fathersName
			dic['contact'] = person.parentContactNumber
			dic['age'] = person.age
			dic['nearest_police_station'] = person.nearest_police_station
			dic['date_of_missing'] = person.date_of_missing
			dic['place_of_missing'] = person.place_of_missing
			dic['height'] = person.height
			dic['weight'] = person.weight
			dic['complexion'] = person.complexion
			dic['address'] = person.address
			#print('Matched: ' + person.name)
			matched.append(dic)		
		final = dict()
		if len(matched) > 0:
			final['status'] = 'matched'
			final['children'] = matched
		else:
			final['status'] = 'not found'
	return HttpResponse(json.dumps(final))

