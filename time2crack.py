import subprocess
import re
import platform

def get_character_set():
    print("Select the characters to include in your password:")
    print("1) Letters (a-z, A-Z)")
    print("2) Numbers (0-9)")
    print("3) Special Characters (!@#$%^&*)")
    print("4) Letters and Numbers")
    print("5) Letters, Numbers, and Special Characters")
    print("6) Custom Set (you specify the characters)")

    choice = input("Enter your choice (1-6): ")
    if choice == "1":
        return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    elif choice == "2":
        return "0123456789"
    elif choice == "3":
        return "!@#$%^&*"
    elif choice == "4":
        return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    elif choice == "5":
        return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    elif choice == "6":
        return input("Enter your custom characters: ")
    else:
        print("Invalid choice. Please try again.")
        return get_character_set()

def calculate_combinations(characters):
    total_characters = len(characters)
    while True:
        length = input("Enter the desired password length: ")
        if length.isdigit():
            length = int(length)
            break
        print("Invalid input. Please enter a positive integer.")

    combinations = total_characters ** length
    print("\nSelected character set:", characters)
    print("Number of characters in set:", total_characters)
    print("Password length:", length)
    print("Total possible combinations:", combinations, "\n")
    return combinations

def get_device_selection():
    print("Fetching device information...")
    try:
        if platform.system() == "Windows":
            # Command to invoke the hashcat PowerShell function
            command = 'powershell -Command "hashcat -I"'
        else:
            # Standard command for non-Windows systems
            command = ["hashcat", "-I"]

        result = subprocess.run(
            command if platform.system() != "Windows" else ["powershell", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=(platform.system() == "Windows")  # Use shell only on Windows
        )

        if result.returncode != 0:
            print("Error fetching device information:", result.stderr)
            return None

        # print("Hashcat Device Info:\n", result.stdout)

        # Parse device information from the output
        devices = []
        lines = result.stdout.splitlines()
        current_device = {}
        for line in lines:
            if "Backend Device ID" in line:
                if current_device:
                    devices.append(current_device)
                current_device = {"ID": line.split("#")[-1].strip()}
            elif "Type...........:" in line:
                current_device["Type"] = line.split(":")[-1].strip()
            elif "Name...........:" in line:
                current_device["Name"] = line.split(":")[-1].strip()
        if current_device:
            devices.append(current_device)

        # Display the devices and let the user select one
        print("\nAvailable devices:")
        for i, device in enumerate(devices, 1):
            print(f"{i}) {device['Type']}: {device['Name']}")

        while True:
            try:
                choice = int(input("\nSelect a device by entering the number: "))
                if 1 <= choice <= len(devices):
                    selected_device = devices[choice - 1]
                    print(f"Selected device: {selected_device['Type']} - {selected_device['Name']}")
                    return selected_device["ID"]
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    except FileNotFoundError:
        print("Hashcat is not installed or not in PATH.")
        return None

def run_hashcat_benchmark(mode, device_id):
    print(f"Running hashcat benchmark for mode {mode} on device {device_id}...")
    try:
        if platform.system() == "Windows":
            # Command to invoke the hashcat PowerShell function
            command = f'powershell -Command "hashcat -b -d {device_id} -m {mode}"'
            print(command)
        else:
            # Standard command for non-Windows systems
            command = ["hashcat", "-b", "-d", device_id, "-m", mode]
            print(command)

        result = subprocess.run(
            command if platform.system() != "Windows" else ["powershell", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=(platform.system() == "Windows")  # Use shell only on Windows
        )

        if result.returncode != 0:
            print("Error running hashcat:", result.stderr)
            return None

        print("Hashcat Output:\n", result.stdout)

        match = re.search(r"Speed\.#1.*?:\s*([\d.]+)\s*([a-zA-Z/]+)", result.stdout)
        if match:
            hash_rate = match.group(1) + " " + match.group(2)
            print(f"Benchmark completed. Detected hash rate: {hash_rate}")
            return hash_rate
        else:
            print("Could not parse hash rate from hashcat output. Please check the output above.")
            return None
    except FileNotFoundError:
        print("Hashcat is not installed or not in PATH.")
        return None

def process_hash_rate(hash_rate):
    match = re.match(r"([\d.]+)\s*([a-zA-Z/]+)", hash_rate)
    if not match:
        print("Unknown format. Please use H/s, kH/s, or MH/s.")
        return None

    rate_number, unit = match.groups()
    rate_number = float(rate_number)

    if unit == "MH/s":
        return int(rate_number * 1e6)
    elif unit == "kH/s":
        return int(rate_number * 1e3)
    elif unit == "H/s":
        return int(rate_number)
    else:
        print("Unknown unit. Please use H/s, kH/s, or MH/s.")
        return None

def calculate_cracking_time(combinations, hash_rate):
    if not hash_rate or combinations == 0:
        print("Error: Combinations or hash rate not properly calculated.")
        return

    time_seconds = int(combinations / hash_rate)

    years = time_seconds // (365 * 24 * 3600)
    remaining_seconds = time_seconds % (365 * 24 * 3600)
    months = remaining_seconds // (30 * 24 * 3600)
    remaining_seconds %= (30 * 24 * 3600)
    days = remaining_seconds // (24 * 3600)
    remaining_seconds %= (24 * 3600)
    hours = remaining_seconds // 3600
    remaining_seconds %= 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    print("\nEstimated time to crack:")
    if years > 0:
        print(f"{years} years, {months} months, {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds")
    elif months > 0:
        print(f"{months} months, {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds")
    elif days > 0:
        print(f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds")
    else:
        print(f"{hours} hours, {minutes} minutes, and {seconds} seconds")

def get_hash_type():
    print("Select the hash type:")
    print("1) MD5 (-m 0)")
    print("2) SHA1 (-m 100)")
    print("3) SHA256 (-m 1400)")
    print("4) NTLM (-m 1000)")
    print("5) bcrypt (-m 3200)")

    choice = input("Enter your choice (1-5): ")
    hash_modes = {
        "1": ("MD5", "0"),
        "2": ("SHA1", "100"),
        "3": ("SHA256", "1400"),
        "4": ("NTLM", "1000"),
        "5": ("bcrypt", "3200")
    }

    if choice in hash_modes:
        return hash_modes[choice]
    else:
        print("Invalid choice. Please try again.")
        return get_hash_type()

def main():
    print("Welcome to Time2Crack, The Password Brute-Force Time Calculator!")
    characters = get_character_set()
    combinations = calculate_combinations(characters)
    device_id = get_device_selection()
    if not device_id:
        print("Device selection failed. Exiting.")
        return
    hash_type, mode = get_hash_type()
    hash_rate_input = run_hashcat_benchmark(mode, device_id)
    if not hash_rate_input:
        print("Could not obtain hash rate. Exiting.")
        return
    hash_rate = process_hash_rate(hash_rate_input)
    if hash_rate:
        print(f"Hash rate in hashes per second: {hash_rate}")
        calculate_cracking_time(combinations, hash_rate)

if __name__ == "__main__":
    main()
