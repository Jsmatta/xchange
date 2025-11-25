import requests
import sys

# constants
API_URL = "https://api.fxratesapi.com/latest"
SUPPORTED_EXCHANGES = ["ADA", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARB", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BNB", "BND", "BOB", "BRL", "BSD", "BTC", "BTN", "BWP", "BYN", "BYR", "BZD", "CAD", "CDF", "CHF", "CLF", "CLP", "CNY", "COP", "CRC", "CUC", "CUP", "CVE", "CZK", "DAI", "DJF", "DKK", "DOP", "DOT", "DZD", "EGP", "ERN", "ETB", "ETH", "EUR", "FJD", "FKP", "GBP", "GEL", "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LTC", "LTL", "LVL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRO", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "OP", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLL", "SOL", "SOS", "SRD", "STD", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VEF", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XRP", "YER", "ZAR", "ZMK", "ZMW", "ZWL"]

# fetch data from API
def fetch_data():
    response = requests.get(API_URL) # GET request
    if response.status_code == 200:
        api_response = response.json()
        # Extract the 'rates' key from the API response its a dictionary of currency rates inside another dictionary
        return api_response.get("rates", {})
    
    else: # error
        print("Error fetching data from API")
        sys.exit(1)

# convert currency
def convert_currency(amount, from_currency, to_currency, data):
    if from_currency not in SUPPORTED_EXCHANGES or to_currency not in SUPPORTED_EXCHANGES:
        print("Unsupported currency")
        sys.exit(1)
    
    from_rate = data[from_currency] 
    to_rate = data[to_currency]
    
    converted_amount = (amount / from_rate) * to_rate
    return converted_amount

#displaying the results
def display_results(amount, from_currency, to_currency, converted_amount):
    print(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")

def main():
    # Fetch data once from the API
    data = fetch_data()
    
    # Loop for continuous currency conversion until user exits
    while True:
        print("\n--- Currency Converter ---")
        print("(Type 'exit' to quit)")
        
        # Get input from user
        from_currency_input = input("Enter source currency (e.g., USD): ").strip()
        
        # Check if user wants to exit
        if from_currency_input.lower() == "exit":
            print("Goodbye!")
            sys.exit(0)
        
        # Convert to uppercase to match supported exchanges
        from_currency = from_currency_input.upper()
        
        # Get destination currency
        to_currency_input = input("Enter target currency (e.g., EUR): ").strip()
        
        # Check if user wants to exit
        if to_currency_input.lower() == "exit":
            print("Goodbye!")
            sys.exit(0)
        
        # Convert to uppercase to match supported exchanges
        to_currency = to_currency_input.upper()
        
        # Get amount to convert
        try:
            amount = float(input("Enter amount to convert: ").strip())
        except ValueError:
            print("Invalid amount. Please enter a number.")
            continue
        
        # Convert and display results
        converted_amount = convert_currency(amount, from_currency, to_currency, data)
        display_results(amount, from_currency, to_currency, converted_amount)

if __name__ == "__main__":
    main()