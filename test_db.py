import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

database_url = os.getenv("DATABASE_URL")
print(f"📡 Testing connection to cloud database...")
print(f"   URL: {database_url[:60]}...")
print()

try:
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print("✅ Connection successful!")
        print(f"📊 PostgreSQL: {version.split(',')[0]}")
        
        result = conn.execute(text("""
            SELECT count(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """))
        table_count = result.fetchone()[0]
        print(f"📋 Tables: {table_count}")
        
        result = conn.execute(text("SELECT count(*) FROM users;"))
        user_count = result.fetchone()[0]
        print(f"👥 Users: {user_count}")
        
        result = conn.execute(text("SELECT count(*) FROM menu_items;"))
        menu_count = result.fetchone()[0]
        print(f"🍔 Menu items: {menu_count}")
        
        result = conn.execute(text("SELECT count(*) FROM orders;"))
        order_count = result.fetchone()[0]
        print(f"📦 Orders: {order_count}")
        
        print()
        print("🎉 Cloud database is working perfectly!")
        
except Exception as e:
    print(f"❌ Connection failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
