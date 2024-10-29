from django.contrib import admin
from .models import User, Position, Department, Task, TaskEmployee, KPI_Metric, TaskKPI, EmployeeKPI, EmployeeDepartment


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'name', 'second_name', 'third_name', 'position', 'is_active', 'is_staff', 'is_hidden')


class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_id', 'name', 'is_hidden')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'name', 'level', 'head_department', 'is_hidden')


from django.contrib import admin
from .models import Task, Department  # Import your Task and Department models


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'task_id', 'title', 'description', 'creator', 'creation_time', 'reviewer',
        'review_time', 'assigner', 'assign_time', 'start_time', 'end_time',
        'status', 'last_modified', 'is_hidden'
    )

    list_filter = ('department_id',)

class TaskEmployeeAdmin(admin.ModelAdmin):
    list_display = ('task_employee_id', 'user', 'task', 'time_added', 'is_hidden')


class KPI_MetricAdmin(admin.ModelAdmin):
    list_display = ('kpi_metric_id', 'metric_name', 'description', 'measurement_method', 'is_hidden')


class TaskKPIAdmin(admin.ModelAdmin):
    list_display = ('task_kpi_id', 'task', 'kpi_metric', 'weight', 'is_hidden')


class EmployeeKPIAdmin(admin.ModelAdmin):
    list_display = ('employee_kpi_id', 'kpi_metric', 'user', 'department', 'metric_value', 'measurement_date', 'is_hidden')


class EmployeeDepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'employee_department_id', 'department', 'user', 'can_review',
        'can_approve', 'can_assign_approver', 'can_assign_executors',
        'can_assign_reviewer', 'can_create_tasks', 'can_return_to_work',
        'can_return_to_review', 'is_hidden'
    )


# Register your models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskEmployee, TaskEmployeeAdmin)
admin.site.register(KPI_Metric, KPI_MetricAdmin)
admin.site.register(TaskKPI, TaskKPIAdmin)
admin.site.register(EmployeeKPI, EmployeeKPIAdmin)
admin.site.register(EmployeeDepartment, EmployeeDepartmentAdmin)