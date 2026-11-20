from app import app, db
from models.role import Role
from models.permission import Permission
from models.role_permission import RolePermission

def seed_roles_and_permissions():
    with app.app_context():
        try:
            # Seed Roles
            roles = {
                'student': 'Can submit code and view feedback',
                'instructor': 'Can upload assignments and grade',
                'admin': 'Full access to platform settings'
            }

            for role_name, description in roles.items():
                if not Role.query.filter_by(role_name=role_name).first():
                    db.session.add(Role(role_name=role_name, description=description))

            db.session.commit()

            # Seed Permissions
            permissions = [
                {'action_name': 'submit_code', 'resource': 'CodeSpace', 'description': 'Allows code submission'},
                {'action_name': 'view_grades', 'resource': 'Gradebook', 'description': 'Allows viewing own grades'},
                {'action_name': 'upload_assignment', 'resource': 'AssignmentManager', 'description': 'Allows instructors to upload assignments'}
            ]

            for perm in permissions:
                if not Permission.query.filter_by(action_name=perm['action_name']).first():
                    db.session.add(Permission(**perm))

            db.session.commit()

            # Map Permissions to Roles
            role_map = {
                'student': ['submit_code', 'view_grades'],
                'instructor': ['upload_assignment']
            }

            for role_name, actions in role_map.items():
                role = Role.query.filter_by(role_name=role_name).first()
                for action in actions:
                    permission = Permission.query.filter_by(action_name=action).first()
                    if role and permission:
                        existing = RolePermission.query.filter_by(
                            role_id=role.role_id,
                            permission_id=permission.permission_id
                        ).first()
                        if not existing:
                            db.session.add(RolePermission(
                                role_id=role.role_id,
                                permission_id=permission.permission_id
                            ))

            db.session.commit()
            print("✅ Roles and permissions seeded successfully.")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Error seeding data: {e}")

if __name__ == "__main__":
    seed_roles_and_permissions()