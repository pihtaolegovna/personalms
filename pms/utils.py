from django.utils import timezone
from django.db.models import Sum, Count
from pms.models import User, Task, UserTaskMetric


def calculate_user_metrics():
    for user in User.objects.all():
        # Получаем все завершенные задачи для пользователя
        completed_tasks = Task.objects.filter(creator=user, status='completed')

        # Подсчитываем общее время выполнения задач
        total_time = sum(
            (task.end_time - task.start_time).total_seconds() / 3600 for task in completed_tasks if
            task.end_time and task.start_time
        )
        completed_count = completed_tasks.count()

        # Подсчитываем дополнительные метрики:
        # Среднее время выполнения задач,
        # Минимальное время выполнения задачи,
        # Максимальное время выполнения задачи,
        # Процент выполненных задач, Процент задач,
        # выполненных в срок,
        # Общее время, проведенное на задачах,
        # Общее количество задач,

        average_time = (total_time / completed_count) if completed_count > 0 else 0
        min_time = min(
            (task.end_time - task.start_time).total_seconds() / 3600 for task in completed_tasks
            if task.end_time and task.start_time
        ) if completed_count > 0 else 0
        max_time = max(
            (task.end_time - task.start_time).total_seconds() / 3600 for task in completed_tasks
            if task.end_time and task.start_time
        ) if completed_count > 0 else 0

        total_tasks_count = Task.objects.filter(creator=user).count()
        completed_task_percentage = (completed_count / total_tasks_count * 100) if total_tasks_count > 0 else 0

        # Обновляем или создаем метрики
        metric, created = UserTaskMetric.objects.update_or_create(
            user=user,
            defaults={
                'total_time_hours': round(total_time),
                'completed_tasks_count': completed_count,
                'average_task_completion_time': round(average_time),
                'min_task_completion_time': round(min_time),
                'max_task_completion_time': round(max_time),
                'completed_task_percentage': round(completed_task_percentage, 2),
                'total_time_spent_on_tasks': round(total_time),  # Общее время на всех задачах
                'task_efficiency': round(completed_count / total_tasks_count * 100, 2) if total_tasks_count > 0 else 0,
                'task_revisions_count': Task.objects.filter(creator=user).exclude(status='completed').count(),
            }
        )
