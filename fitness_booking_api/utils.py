import pytz

def adjust_class_time(class_obj, tz: str):
    """Convert class datetime to target timezone."""
    try:
        target = pytz.timezone(tz)
        class_obj.datetime = class_obj.datetime.astimezone(target)
    except Exception:
        pass  # fallback to original
    return class_obj
