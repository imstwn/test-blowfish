import os

def ValidateFile(value):
	ext = os.path.splitext(value.name)[1]
	valid_extensions = ['.txt', '.csv', '.py', '.ipynb', '.html', '.css', '.js', '.sql']
	if ext.lower() in valid_extensions:
		return True