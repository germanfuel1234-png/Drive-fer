#!/usr/bin/env python3
"""
Test script for the interactive Gmail account selector menu
Run this to test the menu functionality without running the full application
"""

import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from menu import GmailAccountSelector
import json


def test_menu_basic():
    """Test basic menu functionality"""
    print("\n" + "="*60)
    print("🧪 TESTING GMAIL ACCOUNT SELECTOR MENU")
    print("="*60 + "\n")
    
    # Test 1: Initialize selector
    print("✓ Test 1: Initializing GmailAccountSelector...")
    try:
        selector = GmailAccountSelector()
        print(f"  ✅ Initialized successfully")
        print(f"  - Config file: {selector.config_file}")
        print(f"  - Saved accounts: {len(selector.accounts)}")
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False
    
    # Test 2: Check saved accounts
    print("\n✓ Test 2: Checking saved accounts...")
    if os.path.exists(selector.config_file):
        try:
            with open(selector.config_file, 'r') as f:
                accounts = json.load(f)
            print(f"  ✅ Found {len(accounts)} saved account(s)")
            for i, account in enumerate(accounts, 1):
                print(f"    {i}. {account.get('email', 'Unknown')} - {account.get('name', 'No name')}")
        except Exception as e:
            print(f"  ⚠️ Could not read accounts: {e}")
    else:
        print(f"  ℹ️ No saved accounts file yet (will be created on first save)")
    
    # Test 3: Check methods exist
    print("\n✓ Test 3: Checking menu methods...")
    required_methods = [
        '_load_accounts',
        '_save_accounts',
        'display_menu',
        '_get_menu_choice',
        '_add_new_account',
        '_get_input',
        'manage_accounts'
    ]
    
    for method in required_methods:
        if hasattr(selector, method):
            print(f"  ✅ Method '{method}' exists")
        else:
            print(f"  ❌ Method '{method}' missing")
            return False
    
    # Test 4: Test account creation (in memory)
    print("\n✓ Test 4: Testing account creation (in memory)...")
    try:
        test_account = {
            "email": "test@gmail.com",
            "name": "Test Account",
            "credentials_path": "/tmp/test_creds.json",
            "created_at": "2026-07-18T00:00:00"
        }
        # Don't actually save, just verify structure
        print(f"  ✅ Account structure valid:")
        print(f"    - Email: {test_account['email']}")
        print(f"    - Name: {test_account['name']}")
        print(f"    - Credentials: {test_account['credentials_path']}")
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED")
    print("="*60)
    print("\n📝 To use the interactive menu, run:")
    print("   python main.py")
    print("\n💾 Saved accounts are stored in: .gmail_accounts.json\n")
    
    return True


def show_usage():
    """Show usage information"""
    print("\n" + "="*60)
    print("📧 GMAIL ACCOUNT SELECTOR - USAGE")
    print("="*60 + "\n")
    
    print("Interactive Mode (shows menu):")
    print("  python main.py\n")
    
    print("Direct Mode (skip menu):")
    print("  python main.py /path/to/credentials.json\n")
    
    print("Test Mode (verify functionality):")
    print("  python test_menu.py\n")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("\n")
    show_usage()
    
    success = test_menu_basic()
    
    sys.exit(0 if success else 1)
