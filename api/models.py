from sqlalchemy import Column, Integer, String, Date, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# -----------------------------
# fct_messages Table
# -----------------------------
class FctMessage(Base):
    __tablename__ = 'fct_messages'

    message_id = Column(String, primary_key=True)
    date_id = Column(Date)
    channel_id = Column(String)
    has_media = Column(Boolean)
    media_type = Column(String)
    image_path = Column(String)

# -----------------------------
# fct_image_detections Table
# -----------------------------
class FctImageDetection(Base):
    __tablename__ = 'yolo_detections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String)  # FK to fct_messages.message_id
    detected_object_class = Column(String)
    confidence_score = Column(Float)
    channel_name = Column(String)
    image_file = Column(String)

# -----------------------------
# dim_channels Table
# -----------------------------
class DimChannel(Base):
    __tablename__ = 'dim_channels'

    channel_id = Column(String, primary_key=True)
    channel_name = Column(String)

# -----------------------------
# dim_dates Table
# -----------------------------
class DimDate(Base):
    __tablename__ = 'dim_dates'

    date_id = Column(Date, primary_key=True)
    day_of_week = Column(String)
    month = Column(String)
    year = Column(Integer)
