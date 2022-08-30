from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
	name = models.CharField(max_length=32)

	class Meta():
		db_table = 'Chat'

	def __str__(self) -> str:
		return self.name

class Messages(models.Model):
	message = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

	class Meta():
		db_table = 'Messages'

	def __str__(self) -> str:
		return self.message

class ActiveUsers(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

	class Meta():
		db_table = "ActiveUsers"
		
	def __str__(self):
		return f"User {self.user} in the chat - {self.chat}"