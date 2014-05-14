from .models import User

from flask.ext.login import current_user
from flask.ext.principal import RoleNeed, UserNeed, Permission, identity_changed


def load_user(user_id):
    return User.query.get(user_id)


@identity_changed.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if getattr(current_user, 'is_admin', False):
        identity.provides.add(RoleNeed('admin'))


admin_permission = Permission(RoleNeed('admin'))
