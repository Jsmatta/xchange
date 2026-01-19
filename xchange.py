#!/usr/bin/env python3

import os
import sys
from typing import Dict
import requests
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

# ==============================================================================
# CONSTANTS
# ==============================================================================

API_URL = "https://api.fxratesapi.com/latest"
SUPPORTED_EXCHANGES = [
    "ADA", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARB", "ARS", "AUD", "AWG", "AZN",
    "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BNB", "BND", "BOB", "BRL", "BSD",
    "BTC", "BTN", "BWP", "BYN", "BYR", "BZD", "CAD", "CDF", "CHF", "CLF", "CLP", "CNY",
    "COP", "CRC", "CUC", "CUP", "CVE", "CZK", "DAI", "DJF", "DKK", "DOP", "DOT", "DZD",
    "EGP", "ERN", "ETB", "ETH", "EUR", "FJD", "FKP", "GBP", "GEL", "GGP", "GHS", "GIP",
    "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "IMP",
    "INR", "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF",
    "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LTC", "LTL",
    "LVL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRO", "MUR", "MVR",
    "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "OP",
    "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF",
    "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLL", "SOL", "SOS", "SRD", "STD",
    "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS",
    "UAH", "UGX", "USD", "UYU", "UZS", "VEF", "VND", "VUV", "WST", "XAF", "XAG", "XAU",
    "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XRP", "YER", "ZAR", "ZMK", "ZMW", "ZWL"
]

# ==============================================================================
# UI DECORATION FUNCTIONS
# ==============================================================================

def create_box(text: str, width: int = 60, color: str = Fore.CYAN, border_color: str = Fore.YELLOW) -> str:
    """
    Create a decorative box around text with colored borders.

    Args:
        text: The text to display inside the box
        width: Minimum width of the box
        color: Text color
        border_color: Border color

    Returns:
        Formatted box string
    """
    lines = text.split('\n')
    box_width = max(width, max(len(line) for line in lines) + 4)

    result = []
    # Top border
    result.append(f"{border_color}╔{'═' * (box_width - 2)}╗{Style.RESET_ALL}")

    # Content lines
    for line in lines:
        padding = box_width - len(line) - 3
        result.append(f"{border_color}║{Style.RESET_ALL} {color}{line}{' ' * padding}{border_color}║{Style.RESET_ALL}")

    # Bottom border
    result.append(f"{border_color}╚{'═' * (box_width - 2)}╝{Style.RESET_ALL}")

    return '\n'.join(result)


def create_header(title: str, subtitle: str = "") -> str:
    """
    Create a formatted header box for the application.

    Args:
        title: Main title text
        subtitle: Optional subtitle text

    Returns:
        Formatted header string
    """
    header_text = f"{Fore.WHITE}{Style.BRIGHT}{'═' * 20} {title} {'═' * 20}{Style.RESET_ALL}"
    if subtitle:
        header_text += f"\n{Fore.CYAN}{subtitle}{Style.RESET_ALL}"
    return create_box(header_text, width=70, color=Fore.WHITE, border_color=Fore.BLUE)


def create_success_box(text: str) -> str:
    """Create a green success message box."""
    return create_box(f"SUCCESS: {Fore.GREEN}{text}{Style.RESET_ALL}", width=50, color=Fore.GREEN, border_color=Fore.GREEN)


def create_error_box(text: str) -> str:
    """Create a red error message box."""
    return create_box(f"ERROR: {Fore.RED}{text}{Style.RESET_ALL}", width=50, color=Fore.RED, border_color=Fore.RED)


def create_info_box(text: str) -> str:
    """Create a blue info message box."""
    return create_box(f"INFO: {Fore.BLUE}{text}{Style.RESET_ALL}", width=50, color=Fore.BLUE, border_color=Fore.BLUE)


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_colored_input(prompt: str) -> str:
    """
    Get user input with colored prompt.

    Args:
        prompt: The prompt text to display

    Returns:
        User input string
    """
    return input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}").strip()


# ==============================================================================
# BUSINESS LOGIC FUNCTIONS
# ==============================================================================

def fetch_exchange_rates() -> Dict[str, float]:
    """
    Fetch current exchange rates from the API.

    Returns:
        Dictionary of currency exchange rates

    Raises:
        SystemExit: If API request fails
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        api_response = response.json()
        rates = api_response.get("rates", {})

        if not rates:
            print(create_error_box("No exchange rates data received from API"))
            sys.exit(1)

        return rates

    except requests.RequestException as e:
        print(create_error_box(f"Error fetching data from API: {str(e)}"))
        sys.exit(1)
    except ValueError as e:
        print(create_error_box(f"Error parsing API response: {str(e)}"))
        sys.exit(1)


def validate_currency(currency: str) -> bool:
    """
    Validate if a currency code is supported.

    Args:
        currency: Currency code to validate

    Returns:
        True if currency is supported, False otherwise
    """
    return currency.upper() in SUPPORTED_EXCHANGES


def convert_currency(amount: float, from_currency: str, to_currency: str, rates: Dict[str, float]) -> float:
    """
    Convert an amount from one currency to another.

    Args:
        amount: Amount to convert
        from_currency: Source currency code
        to_currency: Target currency code
        rates: Dictionary of exchange rates

    Returns:
        Converted amount

    Raises:
        SystemExit: If currency validation fails
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if not validate_currency(from_currency) or not validate_currency(to_currency):
        print(create_error_box("Unsupported currency"))
        sys.exit(1)

    try:
        from_rate = rates[from_currency]
        to_rate = rates[to_currency]

        if from_rate == 0:
            print(create_error_box(f"Exchange rate for {from_currency} is not available"))
            sys.exit(1)

        converted_amount = (amount / from_rate) * to_rate
        return converted_amount

    except KeyError as e:
        print(create_error_box(f"Exchange rate not available for currency: {str(e)}"))
        sys.exit(1)
    except ZeroDivisionError:
        print(create_error_box("Invalid exchange rate (division by zero)"))
        sys.exit(1)


def format_conversion_result(amount: float, from_currency: str, to_currency: str, converted_amount: float) -> str:
    """
    Format the conversion result for display.

    Args:
        amount: Original amount
        from_currency: Source currency
        to_currency: Target currency
        converted_amount: Converted amount

    Returns:
        Formatted result string
    """
    return f"{Fore.YELLOW}{amount} {from_currency}{Style.RESET_ALL} {Fore.WHITE}is equal to{Style.RESET_ALL} {Fore.GREEN}{converted_amount:.2f} {to_currency}{Style.RESET_ALL}"


# ==============================================================================
# MAIN APPLICATION LOGIC
# ==============================================================================

def display_conversion_result(amount: float, from_currency: str, to_currency: str, converted_amount: float) -> None:
    """
    Display the conversion result in a decorated box.

    Args:
        amount: Original amount
        from_currency: Source currency
        to_currency: Target currency
        converted_amount: Converted amount
    """
    result_text = format_conversion_result(amount, from_currency, to_currency, converted_amount)
    print(create_success_box(result_text))


def handle_user_exit() -> None:
    """Handle graceful user exit with goodbye message."""
    print(create_header(" GOODBYE! ", "Thank you for using Currency Converter"))
    sys.exit(0)


def get_user_amount() -> float:
    """
    Get and validate amount from user.

    Returns:
        Validated amount as float

    Raises:
        ValueError: If input is not a valid number
    """
    amount_input = get_colored_input("Enter amount to convert: ")
    return float(amount_input)


def run_conversion_loop(rates: Dict[str, float]) -> None:
    """
    Main interactive loop for currency conversion.

    Args:
        rates: Dictionary of exchange rates
    """
    while True:
        clear_screen()
        print(create_header("CURRENCY CONVERTER", "Real-time exchange rates powered by fxratesapi.com"))
        print(f"\n{Fore.CYAN}(Type 'exit' to quit){Style.RESET_ALL}\n")

        # Get source currency
        from_currency_input = get_colored_input("Enter source currency (e.g., USD): ")
        if from_currency_input.lower() == "exit":
            handle_user_exit()

        # Get target currency
        to_currency_input = get_colored_input("Enter target currency (e.g., EUR): ")
        if to_currency_input.lower() == "exit":
            handle_user_exit()

        # Get amount and validate
        try:
            amount = get_user_amount()
        except ValueError:
            print(create_error_box("Invalid amount. Please enter a number."))
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            continue

        # Perform conversion and display result
        converted_amount = convert_currency(amount, from_currency_input, to_currency_input, rates)
        display_conversion_result(amount, from_currency_input.upper(), to_currency_input.upper(), converted_amount)

        # Wait for user before continuing
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")


def main() -> None:
    """
    Main entry point for the currency converter application.
    """
    try:
        # Fetch exchange rates once at startup
        print(create_info_box("Fetching latest exchange rates..."))
        rates = fetch_exchange_rates()

        # Start the interactive conversion loop
        run_conversion_loop(rates)

    except KeyboardInterrupt:
        print(create_info_box("Operation cancelled by user"))
        handle_user_exit()
    except Exception as e:
        print(create_error_box(f"Unexpected error: {str(e)}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
