# from django.db import models
# from django.contrib.auth.models import User
# import uuid
#
#
# class EmailVerificationToken(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     token = models.UUIDField(default=uuid.uuid4)
#
#     def __str__(self):
#         return self.user.username + " - Email Verification Token"
