import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Watchlist(Base):
    __tablename__ = 'watchlists'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    ticker = Column(String(10), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

class SearchHistory(Base):
    __tablename__ = 'search_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    ticker = Column(String(10), nullable=False)
    searched_at = Column(DateTime, default=datetime.utcnow)

class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    default_ticker = Column(String(10), default='AAPL')
    default_period = Column(String(10), default='1y')
    theme = Column(String(10), default='dark')
    show_ma50 = Column(Boolean, default=True)
    show_ma200 = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Database:
    def __init__(self, db_path='stock_analysis.db'):
        """Initialize database connection and create tables if they don't exist."""
        try:
            self.db_path = db_path
            self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
            Base.metadata.create_all(self.engine)
            
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def add_to_watchlist(self, user_id, ticker):
        """Add a ticker to user's watchlist if it doesn't already exist."""
        try:
            # Check if ticker already exists in watchlist
            existing = self.session.query(Watchlist).filter_by(
                user_id=user_id, ticker=ticker
            ).first()
            
            if not existing:
                watchlist_item = Watchlist(user_id=user_id, ticker=ticker)
                self.session.add(watchlist_item)
                self.session.commit()
                logger.info(f"Added {ticker} to watchlist for user {user_id}")
                return True
            else:
                logger.info(f"{ticker} already in watchlist for user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding to watchlist: {e}")
            self.session.rollback()
            return False
    
    def remove_from_watchlist(self, user_id, ticker):
        """Remove a ticker from user's watchlist."""
        try:
            watchlist_item = self.session.query(Watchlist).filter_by(
                user_id=user_id, ticker=ticker
            ).first()
            
            if watchlist_item:
                self.session.delete(watchlist_item)
                self.session.commit()
                logger.info(f"Removed {ticker} from watchlist for user {user_id}")
                return True
            else:
                logger.info(f"{ticker} not found in watchlist for user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error removing from watchlist: {e}")
            self.session.rollback()
            return False
    
    def get_watchlist(self, user_id):
        """Get user's watchlist."""
        try:
            watchlist_items = self.session.query(Watchlist).filter_by(
                user_id=user_id
            ).order_by(Watchlist.added_at.desc()).all()
            
            return [item.ticker for item in watchlist_items]
            
        except Exception as e:
            logger.error(f"Error getting watchlist: {e}")
            return []
    
    def add_to_search_history(self, user_id, ticker):
        """Add a ticker to search history."""
        try:
            # Remove existing entry for this ticker to avoid duplicates
            self.session.query(SearchHistory).filter_by(
                user_id=user_id, ticker=ticker
            ).delete()
            
            # Add new entry
            search_item = SearchHistory(user_id=user_id, ticker=ticker)
            self.session.add(search_item)
            
            # Keep only the 6 most recent searches
            recent_searches = self.session.query(SearchHistory).filter_by(
                user_id=user_id
            ).order_by(SearchHistory.searched_at.desc()).all()
            
            if len(recent_searches) > 6:
                for old_search in recent_searches[6:]:
                    self.session.delete(old_search)
            
            self.session.commit()
            logger.info(f"Added {ticker} to search history for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error adding to search history: {e}")
            self.session.rollback()
    
    def get_recent_searches(self, user_id):
        """Get user's recent searches (last 6 unique searches)."""
        try:
            recent_searches = self.session.query(SearchHistory).filter_by(
                user_id=user_id
            ).order_by(SearchHistory.searched_at.desc()).limit(6).all()
            
            return [item.ticker for item in recent_searches]
            
        except Exception as e:
            logger.error(f"Error getting recent searches: {e}")
            return []
    
    def get_user_preferences(self, user_id):
        """Get user preferences."""
        try:
            prefs = self.session.query(UserPreferences).filter_by(
                user_id=user_id
            ).first()
            
            if prefs:
                return {
                    'default_ticker': prefs.default_ticker,
                    'default_period': prefs.default_period,
                    'theme': prefs.theme,
                    'show_ma50': prefs.show_ma50,
                    'show_ma200': prefs.show_ma200
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return None
    
    def update_user_preferences(self, user_id, preferences):
        """Update user preferences."""
        try:
            prefs = self.session.query(UserPreferences).filter_by(
                user_id=user_id
            ).first()
            
            if prefs:
                # Update existing preferences
                prefs.default_ticker = preferences.get('default_ticker', prefs.default_ticker)
                prefs.default_period = preferences.get('default_period', prefs.default_period)
                prefs.theme = preferences.get('theme', prefs.theme)
                prefs.show_ma50 = preferences.get('show_ma50', prefs.show_ma50)
                prefs.show_ma200 = preferences.get('show_ma200', prefs.show_ma200)
            else:
                # Create new preferences
                prefs = UserPreferences(
                    user_id=user_id,
                    default_ticker=preferences.get('default_ticker', 'AAPL'),
                    default_period=preferences.get('default_period', '1y'),
                    theme=preferences.get('theme', 'dark'),
                    show_ma50=preferences.get('show_ma50', True),
                    show_ma200=preferences.get('show_ma200', True)
                )
                self.session.add(prefs)
            
            self.session.commit()
            logger.info(f"Updated preferences for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating user preferences: {e}")
            self.session.rollback()
            return False
    
    def close(self):
        """Close database connection."""
        try:
            self.session.close()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database: {e}")

def init_db():
    """Initialize database with default data if needed."""
    try:
        db = Database()
        logger.info("Database initialization completed")
        return db
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return None
