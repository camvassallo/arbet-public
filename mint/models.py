from django.db import models


# Create your models here.
class Token(models.Model):
    bet = models.OneToOneField('sportsbook.Bet', null=True, blank=True, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    mint_status = models.CharField(max_length=20, default='PENDING')
    art = models.ImageField(upload_to='token_art', blank=True)
    