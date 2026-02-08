import sys
import os
from datetime import timedelta

# Add src to path
sys.path.append(os.getcwd())

from src.auth.utils import create_access_token, decode_token
from src.config import Config

def test_tokens():
    print(f"Testing with JWT_SECRET: {Config.JWT_SECRET}")
    
    user_data = {"uid": "test-uid", "email": "test@example.com"}
    
    # 1. Test Access Token
    print("\nGenerating access token...")
    access_token = create_access_token(user_data=user_data)
    print(f"Access Token: {access_token[:20]}...")
    
    decoded_access = decode_token(access_token)
    print(f"Decoded Access: {decoded_access}")
    assert decoded_access["refresh"] is False
    
    # 2. Test Refresh Token
    print("\nGenerating refresh token...")
    refresh_token = create_access_token(user_data=user_data, refresh=True, expiry=timedelta(days=2))
    print(f"Refresh Token: {refresh_token}")
    
    decoded_refresh = decode_token(refresh_token)
    print(f"Decoded Refresh: {decoded_refresh}")
    assert decoded_refresh["refresh"] is True
    
    print("\nAll token tests passed!")

if __name__ == "__main__":
    try:
        test_tokens()
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
