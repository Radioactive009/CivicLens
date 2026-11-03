from .models import AuditLog

def log_activity(user, action, resource_type, resource_id=None, metadata=None):
    try:
        AuditLog.objects.create(
            user=user if user and user.is_authenticated else None,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id is not None else None,
            metadata=metadata or {}
        )
    except Exception as e:
        # Avoid crashing core request on logging error
        pass

