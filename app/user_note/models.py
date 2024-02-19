from django.db import models
import logging
from app.account.models import User
from django.utils import timezone

def get_default_content():

    return {
        "note_changes": [],
    }


class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.JSONField(default=get_default_content)
    is_deleted = models.BooleanField(default=False)
    @staticmethod
    def create_notes(user, content):

        change_data = {"note_content": content, "user": user.username, "timestamp": timezone.now().isoformat()}
        content = {"note_changes": [change_data]}
        obj = Note.objects.create(owner=user, content=content)
        return obj

    @staticmethod
    def get_note_object_on_id(note_id=None):
        note_object = None
        if note_id:
            try:
                note_object = Note.objects.get(id=note_id)
            except Exception as e:
                logging.error('getting exception on get_note_object_on_id', repr(e))
        return note_object


class NoteShare(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def is_user_exists(user, note_object):
        is_exists = NoteShare.objects.filter(shared_user=user, note=note_object).exists()
        return is_exists

    @staticmethod
    def check_and_create_shared_user(users, note_object):
        objs = []
        try:
            for user in users:
                is_exists = NoteShare.objects.filter(shared_user=user, note=note_object).exists()
                if not is_exists:
                    obj = NoteShare.objects.create(shared_user=user, note=note_object)
                    objs.append(obj)
        except Exception as e:
            logging.error('getting exception on check_and_create_shared_user', repr(e))
        return objs


class CreateNoteManager:
    def __init__(self, user, requested_data):
        self.user = user
        self.requested_data = requested_data

    def save_user_note(self):
        resp_dict = dict(status=False, message="Something went wrong")
        try:
            content = self.requested_data.data.get('content', None)
            if content is not None:
                Note.create_notes(self.user, content)
                resp_dict['status'] = True
                resp_dict['message'] = "Note Created Successfully"
        except Exception as e:
            logging.error('getting exception on save_user_note', repr(e))
        return resp_dict


class GetNoteManager:
    def __init__(self, user, note_id):
        self.user = user
        self.note_id = note_id

    def get_user_note(self):
        resp_dict = dict(status=False, message="Something went wrong", data=dict())
        try:
            note_object = Note.get_note_object_on_id(self.note_id)
            if note_object is not None:
                if note_object.owner == self.user or NoteShare.is_user_exists(self.user, note_object):
                    note_content = [change['note_content'] for change in note_object.content.get('note_changes', [])]
                    resp_dict['data'] = note_content
                    resp_dict['status'] = True
                    resp_dict['message'] = "Got Note Successfully"
        except Exception as e:
            logging.error('getting exception on save_user_note', repr(e))
        return resp_dict


class ShareNoteManager:
    def __init__(self, user, requested_data):
        self.user = user
        self.requested_data = requested_data

    def share_user_note(self):
        resp_dict = dict(status=False, message="Something went wrong")
        try:
            note_id = self.requested_data.data.get('note_id', None)
            shared_users = self.requested_data.data.get('shared_users', [])
            shared_users_arr = []
            note_object = Note.get_note_object_on_id(note_id)
            if note_id is not None and len(shared_users) != 0:
                if note_object.owner == self.user:
                    for shared_user_id in shared_users:
                        shared_users_arr.append(shared_user_id)
                    NoteShare.check_and_create_shared_user(shared_users_arr, note_object)
                    resp_dict['status'] = True
                    resp_dict['message'] = "Note Access Share Successfully"
        except Exception as e:
            logging.error('getting exception on share_user_note', repr(e))
        return resp_dict


class UpdateNoteManager:
    def __init__(self, user, requested_data, note_id):
        self.user = user
        self.requested_data = requested_data
        self.note_id = note_id

    def update_user_note(self):
        resp_dict = dict(status=False, message="Something went wrong")
        try:
            content = self.requested_data.data.get('content', None)
            note_object = Note.get_note_object_on_id(self.note_id)
            if note_object is not None:
                change_data = {"note_content": content, "user": self.user.username, "timestamp": timezone.now().isoformat()}
                note_object.content["note_changes"].append(change_data)
                note_object.save()
                resp_dict['status'] = True
                resp_dict['message'] = "Note Updated Successfully"
        except Exception as e:
            logging.error('getting exception on update_user_note', repr(e))
        return resp_dict


class GetNoteVersionHistoryManager:
    def __init__(self, user, note_id):
        self.user = user
        self.note_id = note_id

    def get_user_note_history(self):
        resp_dict = dict(status=False, message="Something went wrong", data=dict())
        try:
            note_object = Note.get_note_object_on_id(self.note_id)
            if note_object is not None:
                if note_object.owner == self.user or NoteShare.is_user_exists(self.user, note_object):
                    data = note_object.content
                    resp_dict['data'] = data
                    resp_dict['status'] = True
                    resp_dict['message'] = "Got Note Successfully"
        except Exception as e:
            logging.error('getting exception on get_user_note_history', repr(e))
        return resp_dict