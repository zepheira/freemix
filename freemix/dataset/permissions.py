from django.db.models.query_utils import Q


def check_owner(user_obj, obj):
    return user_obj.id == obj.owner_id

def check_published(user_obj, obj):
    if obj.published:
        return True
    return check_owner(user_obj, obj)

class FreemixPermissionsBackend:
    supports_object_permissions=True
    supports_anonymous_user = True

    _registry = {
        'dataset.can_view': check_published,
        'dataset.can_edit': check_owner,
        'dataset.can_delete': check_owner,
    }

    def authenticate(self, username, password):
        return None

    @classmethod
    def register_perms(cls, perm_dict):
        cls._registry = dict(cls._registry, **perm_dict)

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None:
            return False
        pfunc = self._registry.get(perm, lambda x,y: False)
        return pfunc(user_obj, obj)

owner_filter = lambda user: Q(owner=user)

def published_query_filter(user):
    if user.is_authenticated():
        return Q(published=True)|owner_filter(user)
    return Q(published=True)