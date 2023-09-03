from django.contrib import admin

from .models import Category, Task


class CategoryAdmin(admin.ModelAdmin):
    """ Category admin model. """

    list_display = (
        'id',
        'name',
        'get_tasks_count',
    )
    list_editable = (
        'name',
    )
    search_fields = (
        'name',
    )

    @admin.display(description='Tasks count')
    def get_tasks_count(self, obj):
        return obj.tasks.count()


class TaskAdmin(admin.ModelAdmin):
    """ Task admin model. """

    list_display = (
        'id',
        'title',
        'created_at',
        'due_date',
        'category',
        'user',
    )
    list_editable = (
        'title',
        'due_date',
    )
    list_filter = (
        'created_at',
        'due_date',
    )
    search_fields = (
        'title',
        'category__name',
        'user__username',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Task, TaskAdmin)
