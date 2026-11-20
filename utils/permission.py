from models import RolePermission  # or your actual model import

def has_permission(role_name, permission_name):
    return RolePermission.query.filter(
        RolePermission.role.has(role_name=role_name),  # relationship filter
        RolePermission.permission.has(action_name = permission_name)  # relationship filter
    ).first() is not None