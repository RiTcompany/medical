import json
import logging
from typing import Any, Dict
from uuid import uuid4
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

import firebase_admin
from firebase_admin import credentials, auth, firestore, messaging

User = get_user_model()


def initialize_firebase():
    try:
        service_account_json = settings.GOOGLE_APPLICATION_CREDENTIALS

        if service_account_json:
            service_account_dict = json.loads(service_account_json)
            cred = credentials.Certificate(service_account_dict)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully using environment variable.")
        else:
            print("FIREBASE_SERVICE_ACCOUNT_JSON environment variable not set.")

    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")


class FirebaseService:
    @staticmethod
    def send_push_notification(fcm_token, title=None, body=None, data=None):

        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data,
                token=fcm_token,
            )

            response = messaging.send(message)
            print(f"Successfully sent message: {response}")
            return response

        except Exception as e:
            print(f"Error sending message: {e}")
            return None
