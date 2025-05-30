from rest_framework import serializers
from .models import Forum, ForumMembership, ForumMessage, ForumAttachment
from students.models import Student
from instructors.models import Instructor

 
class SimpleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'email', 'fullname', 'verification_status']

class SimpleInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'email', 'fullname', 'verification_status']

class ForumSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    created_by_profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = Forum
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 
                  'is_active', 'created_by_name', 'created_by_profile_picture']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.fullname or obj.created_by.email
        return "Unknown Instructor"
    
    def get_created_by_profile_picture(self, obj):
        if obj.created_by and obj.created_by.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.created_by.profile_picture.url)
            return obj.created_by.profile_picture.url
        return None

class ForumMembershipSerializer(serializers.ModelSerializer):
    student_details = SimpleStudentSerializer(source='student', read_only=True)
    
    class Meta:
        model = ForumMembership
        fields = ['id', 'forum', 'student', 'joined_at', 'is_active', 'student_details']
        read_only_fields = ['joined_at']

class ForumMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    
    class Meta:
        model = ForumMessage
        fields = ['id', 'forum', 'content', 'sender_type', 'sender_id', 'sent_at', 'sender_name', 'attachments']
        read_only_fields = ['sent_at', 'sender_name']
    
    def get_sender_name(self, obj):
        sender = obj.sender
        if obj.sender_type == 'instructor': 
            return f"{sender.fullname} (Instructor)"
        else:
            return f"{sender.fullname} (Student)"
    
    def get_attachments(self, obj):
        attachments = ForumAttachment.objects.filter(message=obj)
        return ForumAttachmentSerializer(attachments, many=True).data

class ForumAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ForumAttachment
        fields = ['id', 'message', 'forum', 'file', 'file_name', 'file_type', 'uploaded_at', 'sender_type', 'sender_id', 'file_url']
        read_only_fields = ['uploaded_at', 'file_url']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None