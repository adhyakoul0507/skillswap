from firebase_config import firebase_auth

def test_setup():
    """Test Firebase setup"""
    print("🔥 Testing Firebase Setup")
    print("=" * 40)
    
    # Initialize Firebase
    if not firebase_auth.initialize():
        print("❌ Firebase initialization failed")
        return False
    
    # Test database connection
    print("\n🧪 Testing database...")
    try:
        # Write test data
        firebase_auth.db.collection('test').document('test1').set({
            'message': 'Hello Firebase!',
            'timestamp': firebase_auth.db.SERVER_TIMESTAMP
        })
        
        # Read test data
        doc = firebase_auth.db.collection('test').document('test1').get()
        if doc.exists:
            print("✅ Database working - can read/write data")
        else:
            print("❌ Database test failed")
            return False
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    # Test authentication
    print("\n🧪 Testing authentication...")
    test_email = "test@skillswap.com"
    test_password = "test123456"
    
    # Try registration
    result = firebase_auth.register_user(test_email, test_password, "Test User")
    if result['success']:
        print("✅ User registration working")
        
        # Try login
        login_result = firebase_auth.login_user(test_email, test_password)
        if login_result['success']:
            print("✅ User login working")
            print(f"   User profile: {login_result['profile']['name']}")
        else:
            print(f"❌ Login failed: {login_result['error']}")
            return False
            
    else:
        if "EMAIL_EXISTS" in result['error']:
            print("✅ Authentication working (user already exists)")
            
            # Try login with existing user
            login_result = firebase_auth.login_user(test_email, test_password)
            if login_result['success']:
                print("✅ Login with existing user working")
            else:
                print(f"❌ Login failed: {login_result['error']}")
                return False
        else:
            print(f"❌ Registration failed: {result['error']}")
            return False
    
    print("\n🎉 All tests passed! Firebase is ready!")
    return True

if __name__ == "__main__":
    test_setup()
