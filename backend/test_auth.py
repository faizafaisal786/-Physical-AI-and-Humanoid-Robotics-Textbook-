"""
Simple authentication test script
Run: python test_auth.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Helper to print formatted response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")

def test_authentication():
    """Test complete authentication flow"""

    print("Starting Authentication Tests...")
    print(f"Base URL: {BASE_URL}")

    # Test 1: Signup
    print("\n[1] Testing Signup...")
    signup_data = {
        "email": "demo@example.com",
        "password": "SecurePass123",
        "username": "demouser",
        "full_name": "Demo User"
    }

    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    print_response("Signup Response", response)

    if response.status_code == 201:
        data = response.json()
        access_token = data["tokens"]["access_token"]
        refresh_token = data["tokens"]["refresh_token"]
        print(f"✓ Signup successful!")
        print(f"Access Token: {access_token[:30]}...")
        print(f"Refresh Token: {refresh_token[:30]}...")
    elif response.status_code == 400:
        print("✗ User already exists. Testing login instead...")

        # Test 2: Login (if signup fails because user exists)
        print("\n[2] Testing Login...")
        login_data = {
            "email": "demo@example.com",
            "password": "SecurePass123"
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print_response("Login Response", response)

        if response.status_code == 200:
            data = response.json()
            access_token = data["tokens"]["access_token"]
            refresh_token = data["tokens"]["refresh_token"]
            print(f"✓ Login successful!")
        else:
            print("✗ Login failed!")
            return
    else:
        print("✗ Signup failed!")
        return

    # Test 3: Get Profile (Protected Route)
    print("\n[3] Testing Protected Route (/me)...")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print_response("Get Profile Response", response)

    if response.status_code == 200:
        print("✓ Protected route access successful!")
    else:
        print("✗ Protected route access failed!")

    # Test 4: Get Products (Public/Optional Auth)
    print("\n[4] Testing Products Endpoint...")
    response = requests.get(f"{BASE_URL}/products?limit=5")
    print_response("Products Response", response)

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Got {len(data['data'])} products")
        print(f"Has more pages: {data['pagination']['has_next']}")
    else:
        print("✗ Products endpoint failed!")

    # Test 5: Refresh Token
    print("\n[5] Testing Token Refresh...")
    refresh_data = {"refresh_token": refresh_token}

    response = requests.post(f"{BASE_URL}/auth/refresh", json=refresh_data)
    print_response("Refresh Token Response", response)

    if response.status_code == 200:
        new_access_token = response.json()["access_token"]
        print(f"✓ Token refresh successful!")
        print(f"New Access Token: {new_access_token[:30]}...")
        access_token = new_access_token
    else:
        print("✗ Token refresh failed!")

    # Test 6: Get Sessions
    print("\n[6] Testing Get Sessions...")
    session_data = {"refresh_token": refresh_token}

    response = requests.post(f"{BASE_URL}/auth/sessions", json=session_data)
    print_response("Active Sessions Response", response)

    if response.status_code == 200:
        sessions = response.json()["sessions"]
        print(f"✓ Found {len(sessions)} active session(s)")
    else:
        print("✗ Get sessions failed!")

    # Test 7: Logout
    print("\n[7] Testing Logout...")
    logout_data = {"refresh_token": refresh_token}

    response = requests.post(f"{BASE_URL}/auth/logout", json=logout_data)
    print_response("Logout Response", response)

    if response.status_code == 200:
        print("✓ Logout successful!")
    else:
        print("✗ Logout failed!")

    # Test 8: Verify token is invalid after logout
    print("\n[8] Testing if token is invalid after logout...")
    response = requests.get(f"{BASE_URL}/me", headers=headers)

    if response.status_code == 401:
        print("✓ Token correctly invalidated after logout!")
    else:
        print("⚠ Token still valid (session may still be active)")

    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_authentication()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to server!")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: uvicorn app:app --reload")
    except Exception as e:
        print(f"\n✗ Error: {e}")
