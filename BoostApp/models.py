from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, editable=False)
    class UserRole(models.TextChoices):
        USER = 'User'
        ADVERTISER = 'Advertiser'
        BOOSTER = 'Booster'
    userRole = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default = 'User',
    )

########################
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
#########################

class Advertiser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        default='DEFAULT VALUE',
        editable=False,
    )
    advRank = models.PositiveSmallIntegerField(choices=list(zip(range(1, 11), range(1, 11))), default=1)
    advCommission = models.DecimalField(max_digits=2, decimal_places=2)
    balance = models.PositiveIntegerField(default=0)

class Booster(models.Model):
    advertiser = models.OneToOneField(
        Advertiser,
        on_delete=models.CASCADE,
        primary_key=True,
        default='DEFAULT VALUE',
        editable=False,
    )
    class ClassName(models.TextChoices):
        WARRIOR = 'Warrior'
        PALADIN = 'Paladin'
        HUNTER = 'Hunter'
        ROGUE = 'Rogue'
        PRIEST = 'Priest'
        SHAMAN = 'Shaman'
        MAGE = 'Mage'
        WARLOCK = 'Warlock'
        MONK = 'Monk'
        DRUID = 'Druid'
        DEMON_HUNTER = 'Demon Hunter' 
        DEATH_KNIGHT = 'Death Knight'
    className = models.CharField(
        max_length=12,
        choices=ClassName.choices,
    ) 

    class ArmourType(models.TextChoices):
        CLOTH = 'Cloth'
        LEATHER = 'Leather'
        MAIL = 'Mail'
        PLATE = 'Plate'
    armourType = models.CharField(
        max_length=7,
        choices=ArmourType.choices,
    )

    class Role(models.TextChoices):
        TANK = 'Tank'
        HEALER = 'Healer'
        DAMAGE = 'Damage'
    role = models.CharField(
        max_length=6,
        choices=Role.choices,
    )

class Boost(models.Model):
    boostId = models.CharField(max_length=6, primary_key=True)
    price = models.PositiveIntegerField()
    name = models.CharField(max_length=40)
    class BoostType(models.TextChoices):
        DUNGEON = 'Dungeon'
        RAID = 'Raid'
    boostType = models.CharField(
        max_length=7,
        choices=BoostType.choices,
    )
    level = models.PositiveSmallIntegerField()

class Booking(models.Model):
    bookingId = models.AutoField(primary_key=True)
    noOfBoosters = models.PositiveSmallIntegerField()
    noOfBuyers = models.PositiveSmallIntegerField()
    dateTime = models.DateTimeField()
    totalPot = models.PositiveIntegerField()
    advertiserCut = models.PositiveIntegerField()
    boosterCut = models.PositiveIntegerField()
    boost = models.ForeignKey(
        Boost,
        on_delete=models.CASCADE,
        default='DEFAULT VALUE',
    )
    completed = models.BooleanField()

class Attendance(models.Model):
    bookingId = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        default='DEFAULT VALUE',
        )
    booster = models.ForeignKey(
        Booster,
        on_delete=models.CASCADE,
        default='DEFAULT VALUE',
    )

class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)
    dateTime = models.DateTimeField()
    price = models.PositiveIntegerField()
    advertiser = models.ForeignKey(
        Advertiser,
        on_delete=models.CASCADE,
        default='DEFAULT VALUE',
    )
    buyer = models.CharField(max_length=30)

class BookingTransaction(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        primary_key=True,
        default=0,
    )
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        default='DEFAULT VALUE',
    )