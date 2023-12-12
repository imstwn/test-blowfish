from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files import File
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .forms import BlowfishForm
from .models import BlowfishModel
from .blowfish import Blowfish
from .validators import *

from datetime import datetime
from pathlib import Path

import os, time

# Create your views here.
def Dashboard(request):
	totallt_f, encrypt_f, decrypt_f = 0, 0, 0
	totalpt = BlowfishModel.objects.all()
	count = BlowfishModel.objects.count()
	num = 7 if count > 7 else count
	recents = BlowfishModel.objects.all().order_by('-created')[:num]
	encrypt = BlowfishModel.objects.filter(category='encrypt')
	decrypt = BlowfishModel.objects.filter(category='decrypt')
	if count != 0:
		totallt_f = totalpt.latest('slug')
		encrypt_f = encrypt.latest('slug')
		decrypt_f = decrypt.latest('slug')
	context = {
		'title': 'Dashboard',
		'totalpt': totalpt,
		'recents': recents,
		'encrypt': encrypt,
		'decrypt': decrypt,
		'totallt_f': totallt_f,
		'encrypt_f': encrypt_f,
		'decrypt_f': decrypt_f,
	}
	return render(request, 'dashboard.html', context)

def Encrypt(request):
	file_content, message, label = None, None, None
	encrypt = []

	if request.method == 'POST':
		form = BlowfishForm(request.POST or None, request.FILES)
		if form.is_valid():
			file = form.cleaned_data.get('file')
			key = form.cleaned_data.get('key')

			if ValidateFile(file):
				updated = Filename(file.name)
				file.name = updated[1]

				BlowfishModel.objects.create(
					filename = updated[1],
					file = file,
					category='encrypt',
					slug = updated[0]
				)
				try:
					start = time.time()
					blowfish = Blowfish(GenerateKey(key))
					with file.open('r') as f:
						content = File(f)
						while True:
							file_content = content.read(1)
							if not file_content:
								break
							encrypt.append(blowfish.encryption(ord(file_content)))
					content.closed

					upd = BlowfishModel.objects.get(slug=updated[0])
					with upd.file.open('w') as newf:
						for i in encrypt:
							newf.write(str(i) + "\n" )
					end = time.time()
					upd.size = upd.file.size
					upd.time = (end - start) * 10 ** 3
					upd.save()

					messages.success(request, 'Successfully Encrypted!')

				except Exception as e:
					messages.error(request, 'Encrypt failed: {}'.format(e))

				context = {
					'title': 'Encrypt',
					'file': upd,
				}
				
				return render(request, 'encrypt.html', context)
			else:
				messages.error(request, 'Only text/* file type allowed')
	else:
		form = BlowfishForm()
	
	context = {
		'title': 'Encrypt',
		'form': form,
	}
	return render(request, 'encrypt.html', context)

def Decrypt(request):
	file_content, message, label = None, None, None
	decrypt = []

	if request.method == 'POST':
		form = BlowfishForm(request.POST or None, request.FILES)
		if form.is_valid():
			file = form.cleaned_data.get('file')
			key = form.cleaned_data.get('key')

			if ValidateFile(file):

				updated = Filename(file.name)
				file.name = updated[1]

				BlowfishModel.objects.create(
					filename = updated[1],
					file = file,
					category='decrypt',
					slug = updated[0]
				)

				try:
					start = time.time()
					blowfish = Blowfish(GenerateKey(key))
					with file.open('r') as f:
						for line in f:
							num = line.decode('utf-8').strip()
							decrypt.append(int(num))

					decrypt = [blowfish.decryption(i) for i in decrypt]
					decrypt = [chr(i) for i in decrypt]

					upd = BlowfishModel.objects.get(slug=updated[0])
					with upd.file.open('w') as newf:
						newf.write(''.join(decrypt))
					end = time.time()
					upd.size = upd.file.size
					upd.time = (end - start) * 10 ** 3
					upd.save()

					messages.success(request, 'Successfully Decrypted!')

				except Exception as e:
					upd = BlowfishModel.objects.get(slug=updated[0])
					messages.success(request, 'Successfully Decrypted!')
					# message = 'Decrypt failed: ' + str(e)
					# label = 'danger'

				context = {
					'title': 'Decrypt',
					'file': upd,
				}
				return render(request, 'decrypt.html', context)
			else:
				messages.error(request, 'Only text/* file type allowed')
	else:
		form = BlowfishForm

		context = {
			'title': 'Decrypt',
			'form': form,
		}
	return render(request, 'decrypt.html', context)

def Manage(request):
	crypt = BlowfishModel.objects.all()
	context = {
		'title': 'Manage',
		'crypt': crypt,
	}

	return render(request, 'manage.html', context)

def ManageFile(request, slug):
	file = BlowfishModel.objects.get(slug=slug)
	context = {
		'title': 'Manage - {}'.format(slug),
		'file': file,
	}
	return render(request, 'file.html', context)

def Test(request):
	sbox, rnd = [], []
	keys = 'key'
	keygen = GenerateKey(keys)
	blowfish = Blowfish(keygen)
	result = blowfish.encryption_detail(ord('D'))
	for sbx in result[2]:
		sbox.append(sbx)
	for i in result[3]:
		rnd.append(i[2:])
	print(result[-1])
	context = {
		'title': 'Blowfish Encryption Algorithm',
		'keys': keys,
		'keygen': keygen,
		'resultkey': result[0],
		'resultsub': result[1],
		'resultsbx1': sbox[0],'resultsbx2': sbox[1],'resultsbx3': sbox[2],'resultsbx4': sbox[3],
		'round': rnd,
		'postprocess': (bin(result[-1])[2:],result[-1]),
	}
	return render(request, 'step.html', context)

def DeleteFile(request, slug):
	file = BlowfishModel.objects.get(slug=slug)
	file.delete()
	return redirect('manage')

def GenerateKey(key):
	key = key * ((14 // len(key)) + 1)
	key = [ord(i) for i in key[:14]]
	return key

def Filename(current):
	time = datetime.now()
	time = time.strftime("%Y%m%d%H%M%S")
	stamp = time, f'{time}-{current}'
	return stamp

def DownloadFile(request, slug):
    file = BlowfishModel.objects.get(slug=slug)
    response = HttpResponse(file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{file.filename}"'
    return response