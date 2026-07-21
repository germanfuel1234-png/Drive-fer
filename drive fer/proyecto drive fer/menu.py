"""
Interactive Menu for Gmail Account Selection with OAuth
Provides a user-friendly interface to authenticate and configure Gmail accounts
"""

import logging
import os
import json
import webbrowser
from pathlib import Path
from typing import Optional, List, Dict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger(__name__)


class GmailAccountSelector:
    """Manages Gmail account selection and OAuth authentication"""
    
    # OAuth scopes
    SCOPES = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/gmail.readonly'
    ]
    
    def __init__(self, config_file: str = ".gmail_accounts.json"):
        """
        Initialize the Gmail Account Selector
        
        Args:
            config_file: Path to store saved Gmail accounts configuration
        """
        self.config_file = config_file
        self.accounts: List[Dict] = []
        self.token_dir = ".gmail_tokens"
        self._ensure_token_dir()
        self._load_accounts()
    
    def _ensure_token_dir(self):
        """Ensure token directory exists"""
        if not os.path.exists(self.token_dir):
            os.makedirs(self.token_dir)
    
    def _load_accounts(self):
        """Load saved Gmail accounts from configuration file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.accounts = json.load(f)
                logger.info(f"Loaded {len(self.accounts)} saved Gmail accounts")
            except Exception as e:
                logger.error(f"Error loading accounts: {e}")
                self.accounts = []
        else:
            self.accounts = []
    
    def _save_accounts(self):
        """Save Gmail accounts to configuration file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.accounts, f, indent=2)
            logger.info(f"Saved {len(self.accounts)} Gmail accounts")
        except Exception as e:
            logger.error(f"Error saving accounts: {e}")
    
    def _get_token_path(self, email: str) -> str:
        """Get token file path for an email"""
        # Clean email for filename (replace @ and .)
        clean_email = email.replace('@', '_').replace('.', '_')
        return os.path.join(self.token_dir, f"{clean_email}_token.json")
    
    def _oauth_authenticate(self, email: str, name: str) -> bool:
        """
        Authenticate using OAuth2 flow with browser
        
        Args:
            email: Email to associate with (for display)
            name: Account name/description
            
        Returns:
            True if authentication successful, False otherwise
        """
        print("\n" + "="*60)
        print("🔐 GOOGLE OAUTH AUTHENTICATION")
        print("="*60 + "\n")
        
        print("📋 Próximos pasos:")
        print("  1. Se abrirá tu navegador")
        print("  2. Inicia sesión con tu cuenta de Gmail")
        print("  3. Autoriza el acceso a Drive, Sheets y Gmail")
        print("  4. Vuelve a esta ventana\n")
        
        input("🔹 Presiona Enter para continuar...")
        
        try:
            # Crear flujo OAuth
            # Nota: Esto requiere que tengas credentials.json de Google Cloud
            # Por ahora, intentaremos con el flujo interactivo
            
            print("\n🔄 Abriendo navegador para autenticación...\n")
            
            # Crear flow (sin archivo de credenciales, solo con datos básicos)
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                scopes=self.SCOPES,
                redirect_uri='http://localhost:8080/'
            )
            
            # Run local server para OAuth callback
            creds = flow.run_local_server(port=8080, open_browser=True)
            
            # Guardar token
            token_path = self._get_token_path(email)
            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())
            
            print(f"\n✅ Autenticación exitosa para {email}")
            
            # Crear cuenta
            account = {
                "email": email,
                "name": name,
                "token_path": token_path,
                "created_at": self._get_timestamp(),
                "auth_method": "oauth"
            }
            
            self.accounts.append(account)
            self._save_accounts()
            
            return True
            
        except FileNotFoundError:
            print("\n❌ Error: No se encontró 'credentials.json'")
            print("   Necesitas descargar credenciales de Google Cloud Console")
            print("   Ver documentación en OAUTH_SETUP.md")
            return False
        except Exception as e:
            print(f"\n❌ Error en autenticación: {e}")
            return False
    
    def display_menu(self) -> Dict[str, str]:
        """
        Display interactive menu to select Gmail account
        
        Returns:
            Dictionary with selected account information
        """
        print("\n" + "="*60)
        print("📧 GMAIL ACCOUNT SELECTOR")
        print("="*60 + "\n")
        
        # Show saved accounts
        if self.accounts:
            print("📌 SAVED ACCOUNTS:")
            for i, account in enumerate(self.accounts, 1):
                status = "✅" if os.path.exists(account.get('token_path', '')) else "⚠️"
                print(f"  {i}. {status} {account.get('email', 'Unknown')} ({account.get('name', 'No name')})")
            print(f"  {len(self.accounts) + 1}. ➕ Add New Account")
            print(f"  {len(self.accounts) + 2}. ❌ Exit\n")
            
            choice = self._get_menu_choice(len(self.accounts) + 2)
            
            if choice == len(self.accounts) + 1:
                return self._add_new_account()
            elif choice == len(self.accounts) + 2:
                print("\n❌ Exiting...\n")
                exit()
            else:
                selected = self.accounts[choice - 1]
                print(f"\n✅ Selected: {selected['email']}\n")
                return selected
        else:
            print("📌 NO SAVED ACCOUNTS FOUND")
            print("  1. ➕ Add New Account")
            print("  2. ❌ Exit\n")
            
            choice = self._get_menu_choice(2)
            
            if choice == 1:
                return self._add_new_account()
            else:
                print("\n❌ Exiting...\n")
                exit()
    
    def _get_menu_choice(self, max_option: int) -> int:
        """
        Get valid menu choice from user
        
        Args:
            max_option: Maximum valid option number
            
        Returns:
            Valid choice as integer
        """
        while True:
            try:
                choice = int(input("🔹 Enter your choice: ").strip())
                if 1 <= choice <= max_option:
                    return choice
                else:
                    print(f"❌ Please enter a number between 1 and {max_option}")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
    
    def _add_new_account(self) -> Dict[str, str]:
        """
        Interactively add a new Gmail account via OAuth
        
        Returns:
            Dictionary with new account information
        """
        print("\n" + "="*60)
        print("➕ ADD NEW GMAIL ACCOUNT")
        print("="*60 + "\n")
        
        # Get email
        email = self._get_input("Enter your Gmail address: ", validate_email=True)
        
        # Get account name/description
        name = self._get_input("Enter account name/description (e.g., 'Work', 'Personal'): ")
        
        # Authenticate via OAuth
        if self._oauth_authenticate(email, name):
            return {
                "email": email,
                "name": name,
                "token_path": self._get_token_path(email),
                "created_at": self._get_timestamp(),
                "auth_method": "oauth"
            }
        else:
            print("\n❌ Could not add account. Please try again.\n")
            return {}
    
    def _get_input(self, prompt: str, validate_email: bool = False) -> str:
        """
        Get validated input from user
        
        Args:
            prompt: Input prompt text
            validate_email: Whether to validate email format
            
        Returns:
            Valid user input
        """
        while True:
            value = input(f"🔹 {prompt}").strip()
            
            if not value:
                print("❌ Input cannot be empty. Please try again.")
                continue
            
            if validate_email:
                if '@' in value and '.' in value and 'gmail' in value.lower():
                    return value
                else:
                    print("❌ Please enter a valid Gmail address (example: user@gmail.com)")
                    continue
            
            return value
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def manage_accounts(self):
        """
        Manage saved accounts (view, delete, edit)
        """
        while True:
            print("\n" + "="*60)
            print("⚙️ MANAGE ACCOUNTS")
            print("="*60 + "\n")
            
            if not self.accounts:
                print("📌 No saved accounts")
                break
            
            for i, account in enumerate(self.accounts, 1):
                status = "✅" if os.path.exists(account.get('token_path', '')) else "⚠️"
                print(f"  {i}. {status} {account['email']} - {account['name']}")
            
            print(f"  {len(self.accounts) + 1}. Back\n")
            
            choice = self._get_menu_choice(len(self.accounts) + 1)
            
            if choice == len(self.accounts) + 1:
                break
            else:
                account = self.accounts[choice - 1]
                self._manage_single_account(account, choice - 1)
    
    def _manage_single_account(self, account: Dict, index: int):
        """
        Manage a single account
        
        Args:
            account: Account dictionary
            index: Account index in list
        """
        print(f"\n📧 {account['email']}")
        print("  1. Delete")
        print("  2. View Details")
        print("  3. Re-authenticate")
        print("  4. Back\n")
        
        choice = self._get_menu_choice(4)
        
        if choice == 1:
            confirm = input("⚠️ Are you sure? (y/n): ").strip().lower()
            if confirm == 'y':
                # Delete token file
                token_path = account.get('token_path', '')
                if os.path.exists(token_path):
                    os.remove(token_path)
                del self.accounts[index]
                self._save_accounts()
                print("✅ Account deleted")
        elif choice == 2:
            print("\n📋 ACCOUNT DETAILS:")
            for key, value in account.items():
                if key != 'token_path':  # Don't show token path
                    print(f"  {key}: {value}")
        elif choice == 3:
            print("\n🔄 Re-authenticating...")
            if self._oauth_authenticate(account['email'], account['name']):
                self.accounts[index] = {
                    "email": account['email'],
                    "name": account['name'],
                    "token_path": self._get_token_path(account['email']),
                    "created_at": account.get('created_at'),
                    "auth_method": "oauth"
                }
                self._save_accounts()
                print("✅ Account re-authenticated")


def select_gmail_account() -> Dict[str, str]:
    """
    Main function to select Gmail account
    
    Returns:
        Dictionary with selected account information
    """
    selector = GmailAccountSelector()
    return selector.display_menu()


if __name__ == "__main__":
    # Test the menu
    logging.basicConfig(level=logging.INFO)
    account = select_gmail_account()
    print(f"\n✅ Using account: {account['email']}")
