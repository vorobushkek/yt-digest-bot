from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model for storing Telegram user data"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(10), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="user")
    digests = relationship("Digest", back_populates="user")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class YouTubeChannel(Base):
    """YouTube channel model"""
    __tablename__ = "youtube_channels"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String(255), unique=True, nullable=False, index=True)  # YouTube channel ID
    channel_name = Column(String(255), nullable=False)
    channel_handle = Column(String(255), nullable=True)  # @handle
    description = Column(Text, nullable=True)
    subscriber_count = Column(Integer, nullable=True)
    video_count = Column(Integer, nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    last_checked = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    videos = relationship("Video", back_populates="channel")
    subscriptions = relationship("Subscription", back_populates="channel")
    
    def __repr__(self):
        return f"<YouTubeChannel(channel_id={self.channel_id}, name={self.channel_name})>"


class Video(Base):
    """YouTube video model"""
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String(255), unique=True, nullable=False, index=True)  # YouTube video ID
    channel_id = Column(Integer, ForeignKey("youtube_channels.id"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(String(50), nullable=True)  # PT4M13S format
    view_count = Column(Integer, nullable=True)
    like_count = Column(Integer, nullable=True)
    comment_count = Column(Integer, nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=False)
    is_processed = Column(Boolean, default=False)  # For digest processing
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    channel = relationship("YouTubeChannel", back_populates="videos")
    digest_videos = relationship("DigestVideo", back_populates="video")
    
    # Indexes for better performance
    __table_args__ = (
        Index("idx_video_channel_published", "channel_id", "published_at"),
        Index("idx_video_processed", "is_processed", "published_at"),
    )
    
    def __repr__(self):
        return f"<Video(video_id={self.video_id}, title={self.title[:50]}...)>"


class Subscription(Base):
    """User subscription to YouTube channels"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel_id = Column(Integer, ForeignKey("youtube_channels.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    digest_frequency = Column(String(20), default="daily")  # daily, weekly, monthly
    last_digest_sent = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    channel = relationship("YouTubeChannel", back_populates="subscriptions")
    
    # Unique constraint to prevent duplicate subscriptions
    __table_args__ = (
        Index("idx_user_channel_subscription", "user_id", "channel_id", unique=True),
    )
    
    def __repr__(self):
        return f"<Subscription(user_id={self.user_id}, channel_id={self.channel_id})>"


class Digest(Base):
    """Digest model for storing generated digests"""
    __tablename__ = "digests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)  # Generated digest content
    digest_type = Column(String(20), default="channel")  # channel, custom, etc.
    status = Column(String(20), default="generated")  # generated, sent, failed
    video_count = Column(Integer, default=0)
    date_from = Column(DateTime(timezone=True), nullable=True)
    date_to = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="digests")
    digest_videos = relationship("DigestVideo", back_populates="digest")
    
    def __repr__(self):
        return f"<Digest(id={self.id}, user_id={self.user_id}, title={self.title[:30]}...)>"


class DigestVideo(Base):
    """Many-to-many relationship between Digests and Videos"""
    __tablename__ = "digest_videos"
    
    id = Column(Integer, primary_key=True, index=True)
    digest_id = Column(Integer, ForeignKey("digests.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    order_in_digest = Column(Integer, default=0)  # Order of video in digest
    summary = Column(Text, nullable=True)  # AI-generated summary for this video
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    digest = relationship("Digest", back_populates="digest_videos")
    video = relationship("Video", back_populates="digest_videos")
    
    # Unique constraint
    __table_args__ = (
        Index("idx_digest_video_unique", "digest_id", "video_id", unique=True),
    )
    
    def __repr__(self):
        return f"<DigestVideo(digest_id={self.digest_id}, video_id={self.video_id})>"


# Database utility functions
def create_tables(engine):
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def drop_tables(engine):
    """Drop all tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
