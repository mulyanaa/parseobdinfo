import csv

print("Enter the hex value: ")
hex_value = input()
# Example input 
# "0x1E3F9801420014800000101000"
# 0xD83F8017A019A01540D8000"

# Convert hex to binary
binary_value = bin(int(hex_value, 16))[2:].zfill(32)  # Ensure 32-bit representation

# Define the lookup table for OBD-II PIDs from a CSV file
def load_pid_table_from_csv(file_path):
    pid_table = {}
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            pid_hex_value = row.get('PID (hex)', '').strip()
            pid_name = row.get('Name', 'Unknown').strip()
            if pid_hex_value:
                try:
                    pid_hex = int(pid_hex_value, 16)
                    pid_table[pid_hex] = pid_name
                except ValueError:
                    print(f"Skipping invalid PID (hex) value: {pid_hex_value}")
    return pid_table

# Load the PID table (update the path as needed)
pid_table_file = 'obd2-pid-table-service-01.csv'
obd2_pid_table = load_pid_table_from_csv(pid_table_file)

# Display supported PIDs based on the binary message
print("Index (Hex) | Binary Bit | Supported PID")
print("------------|------------|-------------------------------")
for index, bit in enumerate(binary_value, start=1):
    hex_index = index  # Convert index to hex (1-based index for PIDs)
    pid_description = obd2_pid_table.get(hex_index, "Unknown PID")
    supported = "Yes" if bit == '1' else "No"
    print(f"{hex_index:03X}        | {bit}          | {supported} - {pid_description}")
