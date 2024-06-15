from typing import Annotated, Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils.html import mark_safe

# Create your models here.


LEVEL_THRESHOLD = {
    "Beginner": 0,
    "Intermediate": 150,
    "Expert": 390,
    "StarLord": 199999
}


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    """Custom user model."""
    email: Annotated[models.EmailField, Any] = models.EmailField(unique=True)
    first_name: Any = models.CharField(max_length=50)
    last_name: Any = models.CharField(max_length=50)
    age: Any = models.IntegerField(null=True, blank=True)
    level: Any = models.ForeignKey('Level', null=True, on_delete=models.SET_NULL)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    scores: Any = models.IntegerField(default=0)
    is_active: Any = models.BooleanField(default=True)
    is_staff: Any = models.BooleanField(default=False)
    is_superuser: Any = models.BooleanField(default=False)
    date_joined: Any = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        return self.is_active and self.is_superuser

    def has_perm(self, perm, obj=None):
        """
        Does the user have the given permission?
        """
        return self.is_active and self.is_superuser

    def get_total_score(self):
        return Score.objects.filter(user=self).aggregate(models.Sum('score'))['score__sum'] or 0

    def get_progress_percentage(self):
        total_score = self.get_total_score()
        self.update_level()
        # print(f'total score {total_score}')
        current_level_threshold = LEVEL_THRESHOLD.get(self.level, 0)
        # print(f'current threshold {current_level_threshold}')
        next_level_threshold = self.get_next_level()
        # print(f'next level threshold {next_level_threshold}')
        if next_level_threshold == current_level_threshold:
            return 100
        progress_within_level = total_score - current_level_threshold
        # print(f'progress within level {progress_within_level}')
        level_range = next_level_threshold - current_level_threshold
        # print(f'Level range {level_range}')
        # print(f'percentage {progress_within_level/level_range}')
        percentage = (progress_within_level/level_range) * 100
        return format(percentage, '.2f')

    def get_next_level(self):
        levels = list(LEVEL_THRESHOLD.values())
        # print(f'levels {levels}')
        current_index = levels.index(LEVEL_THRESHOLD[self.level.name])
        # print(f'current index {current_index}')
        if current_index < len(levels) - 1:
            # print(f'Next Level: {levels[current_index + 1]}')
            return levels[current_index + 1]
        return levels[-1]

    def calculate_level(self, quiz_score):
        for level, threshold in sorted(LEVEL_THRESHOLD.items(), key=lambda x: x[1]):
            if quiz_score < threshold:
                break
            level = Level.objects.get(name=level)
            self.level = level

        self.save()

    def update_level(self):
        total_score = self.get_total_score()
        self.calculate_level(total_score)

    def image_tag(self):
        if self.profile_image:
            image_url = f'{settings.MEDIA_URL}{self.profile_image.name}'
            return mark_safe(f'<img src="{image_url}" width="60" />')
        else:
            return "No image provided"


class Subject(models.Model):
    """The different subjects or topics that make up the questions."""
    name: Annotated[models.CharField, Any] = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Level(models.Model):
    """The difficulty level of the questions."""
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
        ('StarLord', 'StarLord'),
    ]
    name: Annotated[models.CharField, Any] = models.CharField(
        max_length=50, choices=LEVEL_CHOICES, default="Beginner",
        null=False, unique=True)
    time_limit = models.IntegerField(default=1, help_text="Time limit for the questions in this level")

    def __str__(self):
        return self.name


class Question(models.Model):
    """The question model."""
    subject: Annotated[models.ForeignKey, Any] = models.ForeignKey(
        "Subject", null=True, on_delete=models.CASCADE)
    quiz: Annotated[models.ForeignKey, Any] = models.ForeignKey(
        "Quiz", on_delete=models.CASCADE)
    level: Annotated[models.ForeignKey, Any] = models.ForeignKey(
        'Level', null=False, on_delete=models.CASCADE)
    question_text: Annotated[models.CharField, Any] = models.CharField(
        max_length=200)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text

    class Meta:
        unique_together = [['question_text', 'quiz']]


class Option(models.Model):
    """The options for a question."""
    question: Annotated[models.ForeignKey, Any] = models.ForeignKey(
        "Question", related_name="options", on_delete=models.CASCADE)
    text: Annotated[models.CharField, Any] = models.CharField(max_length=250)
    is_correct: Annotated[models.BooleanField, Any] = models.BooleanField(
        default=False)

    def __str__(self):
        return f"{self.question} | option: {self.text} {self.is_correct}"


class Answer(models.Model):
    """The user's answer to a question."""
    user: Annotated[models.ForeignKey, Any] = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE)
    question: Annotated[models.ForeignKey, Any] = models.ForeignKey(
        "Question", on_delete=models.CASCADE)
    option: Annotated[models.ForeignKey, Any] = models.ForeignKey(
        "Option", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.question} : {self.option.is_correct}"

    class Meta:
        unique_together = [['user', 'question']]


class Score(models.Model):
    """User scores for quizzes."""
    user: Annotated[models.ForeignKey, Any] = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE)
    quiz: Annotated[models.ForeignKey, Any] = models.ForeignKey(
        "Quiz", on_delete=models.CASCADE)
    score: Annotated[models.IntegerField, Any] = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.quiz} - {self.score}"

    class Meta:
        unique_together = [['user', 'quiz']]

    @classmethod
    def create_or_update_score(cls, user, quiz, score):
        """Create or update score for a user and quiz."""
        # Check if a score with the same user and quiz exists
        existing_score = cls.objects.filter(user=user, quiz=quiz).first()
        if existing_score:
            # If a score exists, update the score
            existing_score.score = score
            existing_score.save()
        else:
            # If no score exists, create a new score
            cls.objects.create(user=user, quiz=quiz, score=score)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user, created = CustomUser.objects.get_or_create(pk=self.user.pk)
        user.update_level()


def get_default_level():
    default_level, created = Level.objects.get_or_create(
        name='Beginner',
        defaults={'time_limit': 1}
    )
    return default_level.id


class Quiz(models.Model):
    """Individual quiz."""
    title: Annotated[models.CharField, Any] = models.CharField(max_length=100)
    description: Annotated[models.TextField, Any] = models.TextField()
    level: Annotated[models.ForeignKey, Any] = models.ForeignKey(
        'Level', null=False, default=get_default_level, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.level.name}"

    class Meta:
        unique_together = [['title', 'level']]
