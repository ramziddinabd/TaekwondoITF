from django.db import models
import random

# Create your models here.

class Team(models.Model):
    REGION_CHOICES = [
        ('ANDIJON', 'andijon'),
        ('BUXORO', 'buxoro'),
        ('FARGONA', 'fargona'),
        ('JIZZAX', 'jizzax'),
        ('XORAZM', 'xorazm'),
        ('NAMANGAN', 'namangan'),
        ('NAVOIY', 'navoiy'),
        ('QASHQADARYO', 'qashqadaryo'),
        ('SAMARQAND', 'samarqand'),
        ('SIRDARYO', 'sirdaryo'),
        ('SURXONDARYO', 'surxondaryo'),
        ('QORAQALPOGISTON', 'qoraqalpogiston'),
        ('TOSHKENT_REG', 'toshkent_reg'),
        ('TOSHKENT_CITY', 'toshkent_city'),
        
    ]
    region = models.CharField(
        max_length=18,
        choices=REGION_CHOICES, 
    )
    name = models.CharField(max_length=200, null=True)
    coach = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class MatchType(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Member(models.Model):
    GENDER_CHOICES = [
        ('M', 'male'),
        ('F', 'female')
    ]
    
    full_name = models.CharField(max_length=200, null=True)
    birth_date = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES, 
    )
    weight = models.IntegerField(default=0, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.full_name

class Tournament(models.Model):
    GENDER_CHOICES = [
        ('M', 'male'),
        ('F', 'female')
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES, 
    )
    min_birth_date = models.DateField()
    max_birth_date = models.DateField()
    min_weight = models.IntegerField(default=0, null=True, blank=True)
    max_weight = models.IntegerField(default=0, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, blank=True, null=True)
    match_type = models.ForeignKey(MatchType, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.match_type) + " | " + str(self.level) 
    

    def generate_members(self):
        tournament_members = Member.objects.filter(
            gender__exact=self.gender, 
            birth_date__gte=self.min_birth_date,
            birth_date__lte=self.max_birth_date,
            weight__gte=self.min_weight,
            weight__lte=self.max_weight,
            level__exact=self.level,     
        )

        return tournament_members

class Match(models.Model):
    first_member = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True, related_name='first_member')
    second_member = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True, related_name='second_member')
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, blank=True, null=True)
    
    def generate_matches(self, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)
        tournament_members = list(tournament.generate_members())
        matches = []

        for _ in range(round(len(tournament_members) / 2)):        
            random.shuffle(tournament_members)
            first_member = tournament_members.pop()

            if tournament_members:
                random.shuffle(tournament_members)
                second_member = tournament_members.pop()

            if second_member and (first_member.team == second_member.team):
                continue

            matches.append([first_member, second_member])
            first_member, second_member = None, None

        for match in matches:
            self.objects.create(first_member=match[0], second_member=match[1], tournament=tournament)

        return matches
            


        
         




    


    

