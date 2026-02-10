import subprocess
import json

def run_subfinder(domain):
    try:
        # Run subfinder command
        result = subprocess.run(['subfinder', '-d', domain, '-silent'], capture_output=True, text=True)
        # Check if the command was successful
        if result.returncode == 0:
            return result.stdout.splitlines()
        else:
            print(f"Error running subfinder: {result.stderr}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def save_to_file(subdomains, filename):
    with open(filename, 'w') as file:
        for subdomain in subdomains:
            file.write(subdomain + '\n')

def main():
    domains = ['sites.google.be', 'indse.be']
    for domain in domains:
        print(f"Searching for subdomains of {domain}...")
        subdomains = run_subfinder(domain)
        if subdomains:
            print(f"Found {len(subdomains)} subdomains for {domain}")
            save_to_file(subdomains, f"{domain}_subdomains.txt")
        else:
            print(f"No subdomains found for {domain}")

if __name__ == "__main__":
    main()
