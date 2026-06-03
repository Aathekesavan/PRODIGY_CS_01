#!/usr/bin/env python3
"""
Caesar Cipher Tool - A premium Command Line Interface for encrypting,
decrypting, and brute-forcing Caesar ciphers.

Created for PRODIGY_CS_01.
"""

import sys
import textwrap
from colorama import init, Fore, Back, Style

# Initialize colorama for colored terminal output (autoreset will reset colors after each print)
init(autoreset=True)

class CaesarCipher:
    """Core cryptographic operations for Caesar Cipher."""

    @staticmethod
    def encrypt(text: str, shift: int, shift_numbers: bool = False) -> str:
        """
        Encrypts the text by shifting alphabetic characters.
        
        Args:
            text: The plaintext to encrypt.
            shift: The shift value (can be positive, negative, or large).
            shift_numbers: If True, also shifts numeric characters (0-9) by the shift value.
            
        Returns:
            The encrypted ciphertext.
        """
        result = []
        alpha_shift = shift % 26
        num_shift = shift % 10

        for char in text:
            if char.isalpha():
                # Determine start ASCII code depending on case
                start = ord('A') if char.isupper() else ord('a')
                # Calculate new character
                shifted_char = chr(start + (ord(char) - start + alpha_shift) % 26)
                result.append(shifted_char)
            elif char.isdigit() and shift_numbers:
                # Shift numbers if requested
                shifted_digit = chr(ord('0') + (ord(char) - ord('0') + num_shift) % 10)
                result.append(shifted_digit)
            else:
                # Spaces, punctuation, and other characters remain unchanged
                result.append(char)

        return "".join(result)

    @classmethod
    def decrypt(cls, text: str, shift: int, shift_numbers: bool = False) -> str:
        """
        Decrypts the text by applying a negative shift.
        
        Args:
            text: The ciphertext to decrypt.
            shift: The shift value.
            shift_numbers: If True, also decrypts numeric characters (0-9).
            
        Returns:
            The decrypted plaintext.
        """
        return cls.encrypt(text, -shift, shift_numbers)

    @classmethod
    def brute_force(cls, text: str, shift_numbers: bool = False) -> dict:
        """
        Decrypts the text using all possible shifts (1 to 25).
        
        Args:
            text: The ciphertext to brute-force.
            shift_numbers: If True, also decodes numeric shifts.
            
        Returns:
            A dictionary mapping shift key (1-25) to decrypted text.
        """
        results = {}
        for shift in range(1, 26):
            results[shift] = cls.decrypt(text, shift, shift_numbers)
        return results


class CipherCLI:
    """Clean and interactive Command Line Interface."""

    def __init__(self):
        self.cipher = CaesarCipher()
        self.shift_numbers_setting = False  # Keep standard alphabet-only shift by default

    def print_banner(self):
        """Prints a stylized CLI banner."""
        banner_lines = [
            r"   ______                                    ______  _         _                 ",
            r"  / ____/____ _ ___   _____ ____ _ _____    / ____/ (_) ____  / /_   ___   _____ ",
            r" / /    / __ `// _ \ / ___// __ `// ___/   / /     / / / __ \/ __ \ / _ \ / ___/ ",
            r"/ /___ / /_/ //  __/(__  )/ /_/ // /      / /___  / / / /_/ / / / //  __// /     ",
            r"\____/ \__,_/ \___//____/ \__,_//_/       \____/ /_/ / .___/_/ /_/ \___//_/      ",
            r"                                                    /_/                          "
        ]
        
        print("\n" + Fore.CYAN + Style.BRIGHT + "=" * 80)
        # Apply a subtle vertical color gradient to the banner
        colors = [Fore.CYAN, Fore.CYAN, Fore.BLUE, Fore.BLUE, Fore.MAGENTA, Fore.MAGENTA]
        for line, color in zip(banner_lines, colors):
            print(color + Style.BRIGHT + line)
        print(Fore.CYAN + Style.BRIGHT + "=" * 80)
        print(Fore.YELLOW + "  🔒 Pure Python Caesar Cipher Tool | Shift Letters, Numbers & Special Characters")
        print(Fore.CYAN + Style.BRIGHT + "=" * 80 + "\n")

    def get_validated_input(self, prompt: str, validator=None, error_msg: str = "Invalid input.") -> str:
        """Helper to get and validate user input recursively or via loop."""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print(Fore.RED + "⚠️  Input cannot be empty. Please try again.")
                    continue
                if validator:
                    if validator(user_input):
                        return user_input
                    else:
                        print(Fore.RED + f"⚠️  {error_msg}")
                else:
                    return user_input
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n\n👋 Operation cancelled by user. Returning to main menu...")
                raise
            except Exception as e:
                print(Fore.RED + f"⚠️  Error: {e}")

    def get_shift_value(self) -> int:
        """Gets a validated integer shift value from the user."""
        def is_int(val):
            try:
                int(val)
                return True
            except ValueError:
                return False

        shift_str = self.get_validated_input(
            prompt=Fore.GREEN + "👉 Enter shift key (integer, e.g. 3): ",
            validator=is_int,
            error_msg="Shift key must be a valid integer. Please try again."
        )
        return int(shift_str)

    def print_side_by_side(self, original: str, processed: str, mode_label: str, col_width: int = 37):
        """Displays original vs processed text side-by-side in a beautiful table."""
        orig_lines = original.splitlines()
        proc_lines = processed.splitlines()
        
        orig_wrapped = []
        proc_wrapped = []
        
        # Ensure we wrap and match heights line by line
        for o_line, p_line in zip(orig_lines, proc_lines):
            o_sub = textwrap.wrap(o_line, width=col_width) or [""]
            p_sub = textwrap.wrap(p_line, width=col_width) or [""]
            
            # Pad to match heights
            max_len = max(len(o_sub), len(p_sub))
            o_sub += [""] * (max_len - len(o_sub))
            p_sub += [""] * (max_len - len(p_sub))
            
            orig_wrapped.extend(o_sub)
            proc_wrapped.extend(p_sub)
            
        # Draw the table borders and headers
        border_col = Fore.BLUE + Style.BRIGHT
        text_col = Fore.WHITE
        header_col = Fore.CYAN + Style.BRIGHT
        
        top_border = border_col + "┌" + "─" * (col_width + 2) + "┬" + "─" * (col_width + 2) + "┐"
        headers = border_col + "│ " + header_col + "ORIGINAL TEXT".ljust(col_width) + border_col + " │ " + header_col + mode_label.ljust(col_width) + border_col + " │"
        divider = border_col + "├" + "─" * (col_width + 2) + "┼" + "─" * (col_width + 2) + "┤"
        bottom_border = border_col + "└" + "─" * (col_width + 2) + "┴" + "─" * (col_width + 2) + "┘"
        
        print("\n" + top_border)
        print(headers)
        print(divider)
        
        for o_part, p_part in zip(orig_wrapped, proc_wrapped):
            print(border_col + "│ " + text_col + o_part.ljust(col_width) + border_col + " │ " + text_col + p_part.ljust(col_width) + border_col + " │")
            
        print(bottom_border + "\n")

    def display_brute_force(self, original_text: str, brute_results: dict):
        """Displays brute force decryption results in a clean formatted grid."""
        border_col = Fore.BLUE + Style.BRIGHT
        text_col = Fore.WHITE
        header_col = Fore.CYAN + Style.BRIGHT
        
        col_shift_w = 7
        col_text_w = 68
        
        top_border = border_col + "┌" + "─" * (col_shift_w + 2) + "┬" + "─" * (col_text_w + 2) + "┐"
        headers = border_col + "│ " + header_col + "SHIFT".center(col_shift_w) + border_col + " │ " + header_col + "DECRYPTED PREVIEW".ljust(col_text_w) + border_col + " │"
        divider = border_col + "├" + "─" * (col_shift_w + 2) + "┼" + "─" * (col_text_w + 2) + "┤"
        bottom_border = border_col + "└" + "─" * (col_shift_w + 2) + "┴" + "─" * (col_text_w + 2) + "┘"
        
        print(Fore.YELLOW + Style.BRIGHT + "\n🔍 Running Brute-Force Decryption (Trying all 25 possible shifts):")
        print(top_border)
        print(headers)
        print(divider)
        
        for shift, decrypted in brute_results.items():
            # Standardize multi-line or long outputs to one neat line for preview
            cleaned_text = " ".join(decrypted.splitlines())
            if len(cleaned_text) > col_text_w:
                preview = cleaned_text[:col_text_w - 3] + "..."
            else:
                preview = cleaned_text.ljust(col_text_w)
                
            shift_str = f"Key {shift:02d}".center(col_shift_w)
            # Highlight likely shifts if possible, or just standard colors
            print(border_col + "│ " + Fore.GREEN + shift_str + border_col + " │ " + text_col + preview + border_col + " │")
            
        print(bottom_border + "\n")

    def run(self):
        """Main CLI loop."""
        self.print_banner()
        
        while True:
            print(Fore.CYAN + Style.BRIGHT + "--- MAIN MENU ---")
            print(Fore.WHITE + "1. " + Fore.GREEN + "🔑 Encrypt Text")
            print(Fore.WHITE + "2. " + Fore.GREEN + "🔓 Decrypt Text")
            print(Fore.WHITE + "3. " + Fore.GREEN + "💥 Brute-Force Decrypt")
            print(Fore.WHITE + "4. " + Fore.GREEN + "⚙️  Toggle Shift Numbers (Current: " + (Fore.YELLOW + "ENABLED" if self.shift_numbers_setting else Fore.RED + "DISABLED") + Fore.GREEN + ")")
            print(Fore.WHITE + "5. " + Fore.RED + "❌ Exit")
            print(Fore.CYAN + Style.BRIGHT + "-" * 17)
            
            try:
                choice = input(Fore.GREEN + "👉 Select option (1-5): ").strip()
                
                if choice == '1':
                    print(Fore.YELLOW + "\n--- Encryption Mode ---")
                    text = self.get_validated_input(Fore.GREEN + "📝 Enter message to encrypt: ")
                    shift = self.get_shift_value()
                    encrypted = self.cipher.encrypt(text, shift, self.shift_numbers_setting)
                    self.print_side_by_side(text, encrypted, f"ENCRYPTED (Shift {shift})")
                    
                elif choice == '2':
                    print(Fore.YELLOW + "\n--- Decryption Mode ---")
                    text = self.get_validated_input(Fore.GREEN + "📝 Enter message to decrypt: ")
                    shift = self.get_shift_value()
                    decrypted = self.cipher.decrypt(text, shift, self.shift_numbers_setting)
                    self.print_side_by_side(text, decrypted, f"DECRYPTED (Shift {shift})")
                    
                elif choice == '3':
                    print(Fore.YELLOW + "\n--- Brute-Force Mode ---")
                    text = self.get_validated_input(Fore.GREEN + "📝 Enter message to brute-force: ")
                    brute_results = self.cipher.brute_force(text, self.shift_numbers_setting)
                    self.display_brute_force(text, brute_results)
                    
                elif choice == '4':
                    self.shift_numbers_setting = not self.shift_numbers_setting
                    status = "ENABLED" if self.shift_numbers_setting else "DISABLED"
                    color = Fore.YELLOW if self.shift_numbers_setting else Fore.RED
                    print(Fore.GREEN + f"\n✔️  Numeric shift setting changed! Digits shift is now {color}{status}.\n")
                    
                elif choice == '5':
                    print(Fore.CYAN + "\n👋 Thank you for using Caesar Cipher tool. Goodbye!")
                    break
                else:
                    print(Fore.RED + "⚠️  Invalid option. Please enter a number between 1 and 5.\n")
                    
            except KeyboardInterrupt:
                # Graceful handling of Ctrl+C
                print(Fore.YELLOW + "\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(Fore.RED + f"\n⚠️  An unexpected error occurred: {e}\n")


if __name__ == "__main__":
    cli = CipherCLI()
    cli.run()
