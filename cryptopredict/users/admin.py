from django.contrib import admin

# Register your models here.
from users.models import users,Feedback

class usersAdmin(admin.ModelAdmin):
    search_fields = ('user', 'name')

admin.site.register(users,usersAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    # Make the fields read-only
    readonly_fields = ('user', 'feedback')  # Specify fields to display as read-only
    
    # Define the fields to be searchable
    search_fields = ('user__username', 'feedback')
    # Make the fields read-only
    readonly_fields = ('user', 'feedback')  # Specify fields to display as read-only
    def has_add_permission(self, request):
        # Allow adding feedback
        return False

    def has_change_permission(self, request, obj=None):
        # Return False to disable editing
        return False
    
admin.site.register(Feedback,FeedbackAdmin)
