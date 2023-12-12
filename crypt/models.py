from django.db import models

# Create your models here.
class BlowfishModel(models.Model):
	"""
		Model of Blowfish database table
		1. filename: The name of file
		2. file: The actual file that overrided after being encrypted and vice versa
		3. size: Size of file
		4. time: Processed time
		5. created:  The date and time when the document was uploaded
		6. category: Either encryption or decryption
		7. slug: Timestamp used for unique id and change the origin filename
	"""
	filename = models.CharField(max_length=256, null=True)
	file = models.FileField(upload_to='uploads/', blank=False, null=False)
	size = models.CharField(max_length=256, null=True)
	time = models.CharField(max_length=256, null=True)
	created = models.DateTimeField(auto_now_add=True)
	category = models.CharField(max_length=10, editable=False)
	slug = models.SlugField(null=True)

	def __str__(self):
		return self.slug
		