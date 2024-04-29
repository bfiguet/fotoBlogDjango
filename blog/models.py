from django.conf import settings
from django.db import models
from PIL import Image


class Photo(models.Model):
	image = models.ImageField(verbose_name='image')
	caption = models.CharField(max_length=128, blank=True, verbose_name='legende')
	uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)

	IMAGE_MAX_SIZE = (800, 800)

	def resize_image(self):
		image = Image.open(self.image)
		image.thumbnail(self.IMAGE_MAX_SIZE)
		image.save(self.image.path)

	#surcharger la methode save
	def save(self, *args, **kwargs): # a chaq enregistrement d'image, elle sera automatiquement redimensionne
		super().save(*args,**kwargs)
		self.resize_image()

class Blog(models.Model):
	photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
	title = models.CharField(max_length=128, verbose_name='titre')
	content = models.CharField(max_length=5000, verbose_name='contenu')
	#author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	starred = models.BooleanField(default=False)
	word_count = models.IntegerField(null=True)
	contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BlogContributor', related_name='contributions')

	def _get_word_count(self):
		return len(self.content.split(' '))
	
	def save(self, *args, **kargs):
		self.word_count = self._get_word_count()
		super().save(*args, **kargs)

class BlogContributor(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	contribution = models.CharField(max_length=255, blank=True)

	class Meta:
		unique_together = ('blog', 'contributor')
