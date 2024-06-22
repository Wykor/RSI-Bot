from models import AlertChannel
import sqlalchemy

def add_alert_channel(session, channel_id):
    alert_channel = AlertChannel(channel_id)
    try:
        session.add(alert_channel)
        session.commit()
        return True
    # except the object already exists
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        return False