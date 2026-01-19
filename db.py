"""
FB Manager Pro - Database Module
SQLite database for storing profiles, pages, schedules, etc.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / "data" / "fb_manager.db"


def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Profiles table (synced from Hidemium)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            name TEXT,
            folder_name TEXT,
            platform TEXT DEFAULT 'windows',
            status TEXT DEFAULT 'stopped',
            note TEXT,
            fb_account TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Pages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_uuid TEXT NOT NULL,
            page_id TEXT NOT NULL,
            page_name TEXT,
            page_url TEXT,
            category TEXT,
            follower_count INTEGER DEFAULT 0,
            role TEXT DEFAULT 'admin',
            note TEXT,
            is_selected INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(profile_uuid, page_id)
        )
    """)
    
    # Reel schedules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reel_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_uuid TEXT NOT NULL,
            page_id INTEGER,
            page_name TEXT,
            video_path TEXT NOT NULL,
            cover_path TEXT,
            caption TEXT,
            hashtags TEXT,
            scheduled_time TIMESTAMP NOT NULL,
            delay_min INTEGER DEFAULT 30,
            delay_max INTEGER DEFAULT 60,
            status TEXT DEFAULT 'pending',
            reel_url TEXT,
            error_message TEXT,
            executed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Groups table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_uuid TEXT NOT NULL,
            group_id TEXT NOT NULL,
            group_name TEXT,
            group_url TEXT,
            member_count INTEGER DEFAULT 0,
            is_selected INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(profile_uuid, group_id)
        )
    """)
    
    # Posts history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_uuid TEXT NOT NULL,
            target_type TEXT NOT NULL,
            target_id TEXT,
            target_name TEXT,
            content TEXT,
            media_paths TEXT,
            post_url TEXT,
            status TEXT DEFAULT 'pending',
            error_message TEXT,
            posted_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Content templates table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            content TEXT,
            hashtags TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Scripts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            script_data TEXT,
            is_active INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"[DB] Database initialized at {DB_PATH}")


# ========== PROFILE OPERATIONS ==========

def save_profile(profile: Dict) -> Dict:
    """Save or update a profile"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO profiles (uuid, name, folder_name, platform, status, note, fb_account)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(uuid) DO UPDATE SET
                name = excluded.name,
                folder_name = excluded.folder_name,
                platform = excluded.platform,
                status = excluded.status,
                note = excluded.note,
                fb_account = excluded.fb_account,
                updated_at = CURRENT_TIMESTAMP
        """, (
            profile.get('uuid'),
            profile.get('name'),
            profile.get('folder_name'),
            profile.get('platform', 'windows'),
            profile.get('status', 'stopped'),
            profile.get('note'),
            profile.get('fb_account')
        ))
        conn.commit()
        return {"id": cursor.lastrowid, "success": True}
    except Exception as e:
        print(f"[DB] Error saving profile: {e}")
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def get_profiles(folder_name: Optional[str] = None) -> List[Dict]:
    """Get all profiles, optionally filtered by folder"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if folder_name:
        cursor.execute("SELECT * FROM profiles WHERE folder_name = ? ORDER BY name", (folder_name,))
    else:
        cursor.execute("SELECT * FROM profiles ORDER BY name")
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_profile_by_uuid(uuid: str) -> Optional[Dict]:
    """Get a single profile by UUID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE uuid = ?", (uuid,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_profile_status(uuid: str, status: str):
    """Update profile running status"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE profiles SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE uuid = ?
    """, (status, uuid))
    conn.commit()
    conn.close()


def sync_profiles(profiles_from_api: List[Dict]):
    """Sync profiles from Hidemium API"""
    for profile in profiles_from_api:
        save_profile(profile)
    print(f"[DB] Synced {len(profiles_from_api)} profiles")


# ========== PAGE OPERATIONS ==========

def save_page(page: Dict) -> Dict:
    """Save or update a page"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO pages (profile_uuid, page_id, page_name, page_url, category, follower_count, role, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(profile_uuid, page_id) DO UPDATE SET
                page_name = excluded.page_name,
                page_url = excluded.page_url,
                category = excluded.category,
                follower_count = excluded.follower_count,
                role = excluded.role,
                note = excluded.note,
                updated_at = CURRENT_TIMESTAMP
        """, (
            page.get('profile_uuid'),
            page.get('page_id'),
            page.get('page_name'),
            page.get('page_url'),
            page.get('category'),
            page.get('follower_count', 0),
            page.get('role', 'admin'),
            page.get('note')
        ))
        conn.commit()
        result_id = cursor.lastrowid
        print(f"[DB] Saved page: {page.get('page_name')} (ID: {result_id})")
        return {"id": result_id, "success": True}
    except Exception as e:
        print(f"[DB] Error saving page: {e}")
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def get_pages(profile_uuid: Optional[str] = None) -> List[Dict]:
    """Get pages, optionally filtered by profile"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if profile_uuid:
        cursor.execute("SELECT * FROM pages WHERE profile_uuid = ? ORDER BY page_name", (profile_uuid,))
    else:
        cursor.execute("SELECT * FROM pages ORDER BY page_name")
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def sync_pages(profile_uuid: str, pages_from_scan: List[Dict]):
    """Sync pages from browser scan"""
    saved_count = 0
    for page in pages_from_scan:
        page['profile_uuid'] = profile_uuid
        result = save_page(page)
        if result.get('success'):
            saved_count += 1
    print(f"[DB] sync_pages completed: {saved_count}/{len(pages_from_scan)} pages saved")
    return saved_count


# ========== REEL SCHEDULE OPERATIONS ==========

def save_reel_schedule(schedule: Dict) -> Dict:
    """Save a reel schedule"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO reel_schedules 
            (profile_uuid, page_id, page_name, video_path, cover_path, caption, hashtags, scheduled_time, delay_min, delay_max, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            schedule.get('profile_uuid'),
            schedule.get('page_id'),
            schedule.get('page_name'),
            schedule.get('video_path'),
            schedule.get('cover_path'),
            schedule.get('caption'),
            schedule.get('hashtags'),
            schedule.get('scheduled_time'),
            schedule.get('delay_min', 30),
            schedule.get('delay_max', 60),
            schedule.get('status', 'pending')
        ))
        conn.commit()
        return {"id": cursor.lastrowid, "success": True}
    except Exception as e:
        print(f"[DB] Error saving reel schedule: {e}")
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def get_pending_reel_schedules() -> List[Dict]:
    """Get pending reel schedules"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM reel_schedules 
        WHERE status = 'pending' AND scheduled_time <= datetime('now')
        ORDER BY scheduled_time
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_reel_schedule_status(schedule_id: int, status: str, reel_url: str = None, error: str = None):
    """Update reel schedule status"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE reel_schedules 
        SET status = ?, reel_url = ?, error_message = ?, executed_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (status, reel_url, error, schedule_id))
    conn.commit()
    conn.close()


# Initialize database on import
init_database()
