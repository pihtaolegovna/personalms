from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)

    email = models.EmailField(unique=True)
    name = models.TextField()
    second_name = models.TextField()
    third_name = models.TextField(null=True, blank=True)
    position = models.ForeignKey("Position", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    profile_photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'second_name', 'third_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.name} {self.second_name}"


class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    name = models.TextField()
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.TextField()
    level = models.IntegerField()
    head_department = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('created', 'Создано'),
        ('reviewing', 'Согласуется'),
        ('assigning', 'Утверждается'),
        ('assigned', 'Утверждено'),
        ('in_work', 'В работе'),
        ('completed', 'Выполнено'),
    ]

    task_id = models.AutoField(primary_key=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)

    title = models.TextField()  # Only required field
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, related_name="created_tasks", on_delete=models.SET_NULL, null=True, blank=True)
    creation_time = models.DateTimeField(null=True, blank=True)
    reviewer = models.ForeignKey(User, related_name="reviewed_tasks", on_delete=models.SET_NULL, null=True, blank=True)
    review_time = models.DateTimeField(null=True, blank=True)
    assigner = models.ForeignKey(User, related_name="assigned_tasks", on_delete=models.SET_NULL, null=True, blank=True)
    assign_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    due_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    last_modified = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} (Creator ID: {self.creator.user_id if self.creation_time else 'None'})"

    def get_status_display_name(self):
        return dict(self.STATUS_CHOICES).get(self.status, "Unknown")

@receiver(pre_save, sender=Task)
def set_time_fields_on_assignment(sender, instance, **kwargs):
    if instance.creator and not instance.creation_time:
        instance.creation_time = timezone.now()
    if instance.reviewer and not instance.review_time:
        instance.review_time = timezone.now()
    if instance.assigner and not instance.assign_time:
        instance.assign_time = timezone.now()

class TaskEmployee(models.Model):
    task_employee_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time_added = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.task}"

@receiver(post_save, sender=TaskEmployee)
def update_task_last_modified(sender, instance, **kwargs):
    instance.task.last_modified = timezone.now()
    instance.task.save()

class KPI_Metric(models.Model):
    kpi_metric_id = models.AutoField(primary_key=True)
    metric_name = models.TextField()
    description = models.TextField()
    measurement_method = models.TextField()
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.metric_name

class TaskKPI(models.Model):
    task_kpi_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    kpi_metric = models.ForeignKey(KPI_Metric, on_delete=models.CASCADE)
    weight = models.IntegerField()
    multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task} - {self.kpi_metric}"

class EmployeeKPI(models.Model):
    employee_kpi_id = models.AutoField(primary_key=True)
    kpi_metric = models.ForeignKey(KPI_Metric, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    metric_value = models.IntegerField()
    measurement_date = models.DateTimeField()
    multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.kpi_metric}"

class EmployeeDepartment(models.Model):
    employee_department_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_review = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)
    can_assign_approver = models.BooleanField(default=False)
    can_assign_executors = models.BooleanField(default=False)
    can_assign_reviewer = models.BooleanField(default=False)
    can_create_tasks = models.BooleanField(default=False)
    can_return_to_work = models.BooleanField(default=False)
    can_return_to_review = models.BooleanField(default=False)
    can_assign_metrics = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.department}"

class UserTaskMetric(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_time_hours = models.FloatField()
    completed_tasks_count = models.IntegerField()
    average_task_completion_time = models.FloatField(default=0)
    min_task_completion_time = models.FloatField(default=0)
    max_task_completion_time = models.FloatField(default=0)
    completed_task_percentage = models.FloatField(default=0)
    on_time_completion_percentage = models.FloatField(default=0)
    high_priority_tasks_count = models.IntegerField(default=0)
    task_efficiency = models.FloatField(default=0)
    task_revisions_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - Метрики задач"

# Высчет метрики времени, потраченного на задачу + общее количество
@receiver(post_save, sender=Task)
def update_user_task_metrics(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.end_time:
        time_taken = (instance.end_time - instance.start_time).total_seconds() / 3600
        time_taken = round(time_taken)

        user_metric, created = UserTaskMetric.objects.get_or_create(user=instance.creator)

        user_metric.completed_tasks_count += 1
        user_metric.total_time_hours += time_taken
        user_metric.save()