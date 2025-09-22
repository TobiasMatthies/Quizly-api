from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class IsAuthenticatedFromCookie(BasePermission):
    """
    Custom permission class to check if the user is authenticated
    via a JWT access token stored in an HTTPOnly cookie.
    """
    def has_permission(self, request, view):
        jwt_authenticator = JWTAuthentication()

        try:
            validated_token = jwt_authenticator.get_validated_token(request.COOKIES.get('access_token'))
            user = jwt_authenticator.get_user(validated_token)

            request.user = user

            return user is not None and user.is_authenticated

        except (InvalidToken, TokenError):
            return False
        except Exception:
            return False

class IsQuizOwner(BasePermission):
    """
    Checks if the user is the owner of the quiz
    """

    def has_object_permission(self, request, view, obj):
        jwt_authenticator = JWTAuthentication()

        try:
            validated_token = jwt_authenticator.get_validated_token(request.COOKIES.get('access_token'))
            user = jwt_authenticator.get_user(validated_token)

            return obj.user == user

        except (InvalidToken, TokenError):
            return False
        except Exception:
            return False
