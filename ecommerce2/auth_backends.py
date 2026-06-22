from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from users.models import Profile 

class KeycloakOIDCBackend(OIDCAuthenticationBackend):

    def create_user(self, claims):
        user = super().create_user(claims)
        self.update_user_roles(user, claims)
        self.sync_profile(user, claims)
        return user
    
    def update_user(self, user, claims):
        self.update_user_roles(user, claims)
        self.sync_profile(user, claims)
        return user

    def update_user_roles(self, user, claims):
        roles = claims.get('realm_access', {}).get('roles', [])

        if 'admin_role' in roles:
            user.is_superuser = True
            user.is_staff = True

        elif 'staff_role' in roles:
            user.is_staff = True
            user.is_superuser = False

        user.save()
    def sync_profile(self, user, claims):
        phone = claims.get("phone_number")

        if phone:
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = phone
            profile.save()

    def get_username(self, claims):
        return claims.get('email')
