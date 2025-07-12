import datetime

user_db = {}

async def is_subscribed(user_id):
    info = user_db.get(user_id)
    if not info: return False
    return info.get("sub_until", datetime.datetime(2000,1,1)) > datetime.datetime.now()

async def check_user_limit(user_id):
    info = user_db.setdefault(user_id, {"count": 0, "date": str(datetime.date.today())})
    if info["date"] != str(datetime.date.today()):
        info["count"] = 0
        info["date"] = str(datetime.date.today())
    if info["count"] >= 5:
        return False
    info["count"] += 1
    return True
