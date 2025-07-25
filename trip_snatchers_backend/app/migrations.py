from sqlalchemy import create_engine, text
from app.database import SQLALCHEMY_DATABASE_URL

def migrate():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Add verification columns to users table
    with engine.connect() as conn:
        # First check if the columns exist
        result = conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM pragma_table_info('users') 
            WHERE name IN ('is_verified', 'verification_token', 'verification_token_expires')
        """))
        count = result.fetchone()[0]
        
        if count < 3:  # If any of the columns are missing
            print("Adding verification columns to users table...")
            try:
                # Create new table with all columns
                conn.execute(text("""
                    CREATE TABLE users_new (
                        id INTEGER PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT UNIQUE,
                        phone TEXT,
                        country TEXT,
                        age INTEGER,
                        gender TEXT,
                        hashed_password TEXT,
                        is_verified BOOLEAN DEFAULT 0,
                        verification_token TEXT UNIQUE,
                        verification_token_expires TIMESTAMP
                    )
                """))
                
                # Copy data from old table to new table
                conn.execute(text("""
                    INSERT INTO users_new (
                        id, first_name, last_name, email, phone, country, 
                        age, gender, hashed_password
                    )
                    SELECT 
                        id, first_name, last_name, email, phone, country, 
                        age, gender, hashed_password
                    FROM users
                """))
                
                # Set existing users as verified
                conn.execute(text("""
                    UPDATE users_new 
                    SET is_verified = 1
                """))
                
                # Drop old table and rename new table
                conn.execute(text("DROP TABLE users"))
                conn.execute(text("ALTER TABLE users_new RENAME TO users"))
                
                print("Migration completed successfully!")
            except Exception as e:
                print(f"Error during migration: {str(e)}")
                raise
        else:
            print("Verification columns already exist. No migration needed.")
        
        conn.commit()

if __name__ == "__main__":
    migrate() 