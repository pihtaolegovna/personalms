from django.db.models import Sum
from .models import EmployeeKPI, User
from django.db.models import Count
from pms.models import UserTaskMetric
from django.shortcuts import render
from .models import Department, Task, EmployeeDepartment
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def departments_view(request):
    departments = Department.objects.filter(is_hidden=False)
    employees = User.objects.filter(is_hidden=False)

    context = {
        'departments': departments,
        'employees': employees,
    }
    return render(request, 'departments_view.html', {'departments': departments})


@login_required
def department_tasks(request, department_id):
    user_in_department = EmployeeDepartment.objects.filter(
        user=request.user,
        department_id=department_id,
        is_hidden=False
    ).exists()

    user = request.user
    employee_department = EmployeeDepartment.objects.filter(user=user, employee_department_id=department_id)

    tasks = Task.objects.filter(department_id=department_id)

    if not user_in_department:
        return render(request, '404.html')
    context = {
        'tasks': tasks,
        'user': user,
        'employee_department': employee_department,
    }
    return render(request, 'tasks_view.html', context)


@login_required
def metrics_view(request):
    daily_metrics = (
        EmployeeKPI.objects
        .select_related('user', 'kpi_metric', 'department')
        .values(
            'measurement_date__date',
            'user__name',
            'user__second_name',
            'user__profile_photo',
            'user__position',
            'kpi_metric__metric_name',
            'multiplier'
        )
        .annotate(total_value=Sum('metric_value'))
    )

    total_value = daily_metrics.aggregate(total=Sum('total_value'))['total'] or 0
    users = User.objects.all()
    return render(request, 'Metrics.html', {
        'daily_metrics': daily_metrics,
        'total_value': total_value,
        'users': users,
    })


def user_metrics_view(request):
    metrics = UserTaskMetric.objects.all()
    return render(request, 'user_metrics.html', {'metrics': metrics})
