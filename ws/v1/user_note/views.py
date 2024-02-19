from rest_framework.views import APIView
from django.http import JsonResponse
import logging
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.user_note.models import (CreateNoteManager,GetNoteManager,
                                  ShareNoteManager, UpdateNoteManager,
                                  GetNoteVersionHistoryManager)


class CreateNote(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            user = request.user
            create_note_manager = CreateNoteManager(user, request)
            save_user_history_resp = create_note_manager.save_user_note()
            resp_dict['status'] = save_user_history_resp['status']
            resp_dict['message'] = save_user_history_resp['message']
        except Exception as e:
            logging.error('getting exception on CreateNote', repr(e))
        return JsonResponse(resp_dict, status=200)


class GetNote(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, note_id):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            user = request.user
            get_note_manager = GetNoteManager(user, note_id)
            get_note_manager_resp = get_note_manager.get_user_note()
            resp_dict['data'] = get_note_manager_resp['data']
            resp_dict['status'] = get_note_manager_resp['status']
            resp_dict['message'] = get_note_manager_resp['message']
        except Exception as e:
            logging.error('getting exception on GetNote', repr(e))
        return JsonResponse(resp_dict, status=200)


class ShareNote(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            user = request.user
            share_note_manager = ShareNoteManager(user, request)
            share_note_manager_resp = share_note_manager.share_user_note()
            resp_dict['status'] = share_note_manager_resp['status']
            resp_dict['message'] = share_note_manager_resp['message']
        except Exception as e:
            logging.error('getting exception on ShareNote', repr(e))
        return JsonResponse(resp_dict, status=200)


class UpdateNote(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, note_id):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            user = request.user
            update_note_manager = UpdateNoteManager(user, request, note_id)
            update_note_manager_resp = update_note_manager.update_user_note()
            resp_dict['status'] = update_note_manager_resp['status']
            resp_dict['message'] = update_note_manager_resp['message']
        except Exception as e:
            logging.error('getting exception on UpdateNote', repr(e))
        return JsonResponse(resp_dict, status=200)


class GetNoteVersionHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, note_id):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            user = request.user
            get_note_version_history_manager = GetNoteVersionHistoryManager(user, note_id)
            get_note_version_history_manager_resp = get_note_version_history_manager.get_user_note_history()
            resp_dict['data'] = get_note_version_history_manager_resp['data']
            resp_dict['status'] = get_note_version_history_manager_resp['status']
            resp_dict['message'] = get_note_version_history_manager_resp['message']
        except Exception as e:
            logging.error('getting exception on GetNoteVersionHistory', repr(e))
        return JsonResponse(resp_dict, status=200)