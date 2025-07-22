import django_filters
from django_filters import rest_framework as filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(filters.FilterSet):
    # Filter by sender user id
    sender = django_filters.NumberFilter(field_name='sender__id', lookup_expr='exact')
    
    # Filter by conversation participant user id (messages in conversations with this participant)
    participant = django_filters.NumberFilter(method='filter_by_participant')

    # Filter messages within a date/time range (created_at assumed to be datetime field)
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'participant', 'created_after', 'created_before']

    def filter_by_participant(self, queryset, name, value):
        """
        Filter messages where the conversation includes participant with user id = value
        """
        return queryset.filter(conversation__participants__id=value)
