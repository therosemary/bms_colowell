# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from accounts.models import DingtalkInfo


class DingtalkUseridAuthBackend(object):
    """User-defined authenticate backend for the report"""
    
    def authenticate(self, request, userid=None):
        try:
            dingtalk_info = DingtalkInfo.objects.get(userid=userid)
            login_user = User.objects.get(pk=dingtalk_info.bms_user_id)
        except DingtalkInfo.DoesNotExist:
            return None
        return login_user
    
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user
