from models import AlertChannel, RelativeStrengthIndex
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

def get_latest_rsi(session, symbol):
    return session.query(RelativeStrengthIndex).filter_by(symbol=symbol).order_by(RelativeStrengthIndex.latest_bar_close_at.desc()).first()

def create_rsi(session, symbol, rsi, latest_bar_close_at):
    rsi_obj = RelativeStrengthIndex(symbol, rsi, latest_bar_close_at)
    session.add(rsi_obj)
    session.commit()
    return rsi_obj