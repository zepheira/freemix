from django.db.models.query_utils import Q


def check_owner(user_obj, obj):
    return user_obj.id == obj.user_id

def check_published(user_obj, obj):
    if obj.published:
        return True
    return check_owner(user_obj, obj)

class PermissionsRegistry:

    _filter_registry = {}
    _perm_registry = {}

    @classmethod
    def register_filter(cls, perm_dict):
        cls._filter_registry = dict(cls._filter_registry, **perm_dict)

    @classmethod
    def register(cls, perm, callback=None, filter=None):
        if callback:
            cls._perm_registry[perm] = callback
        if filter:
            cls._filter_registry[perm] = filter

    @classmethod
    def get_callback(cls, perm):
        return cls._perm_registry.get(perm, lambda x,y: False)

    @classmethod
    def get_filter(cls, perm):
        return cls._filter_registry[perm]



class RegistryBackend:
    supports_object_permissions=True
    supports_anonymous_user = True

    def authenticate(self, username, password):
        return None


    def has_perm(self, user_obj, perm, obj=None):
        if obj is None:
            return False
        pfunc = PermissionsRegistry.get_callback(perm)
        return pfunc(user_obj, obj)

owner_filter = lambda user: Q(user=user)

def published_query_filter(user):
    if user.is_authenticated():
        return Q(published=True)|owner_filter(user)
    return Q(published=True)

PermissionsRegistry.register('dataset.can_view', check_published, published_query_filter)
PermissionsRegistry.register('dataset.can_edit', check_owner, owner_filter)
PermissionsRegistry.register('dataset.can_delete', check_owner, owner_filter)
PermissionsRegistry.register('datasource.can_view', check_owner, owner_filter)
PermissionsRegistry.register('datasource.can_edit', check_owner, owner_filter)
PermissionsRegistry.register('datasource.can_delete', check_owner, owner_filter)
PermissionsRegistry.register('datasourcetransaction.can_view', lambda user_obj, obj: user_obj.id==obj.source.user_id)