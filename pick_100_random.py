import random

# Define the input and output filenames
file_categories = {
    "normie.txt": "normies_random.txt",
    "casual.txt": "casuals_random.txt",
    "gamer.txt": "gamers_random.txt"
}

def select_random_ids(input_file, output_file, num_ids=100):
    try:
        with open(input_file, "r") as f:
            ids = list(set(f.readlines()))
        
        if len(ids) < num_ids:
            print(f"Not enough unique IDs in {input_file}. Only {len(ids)} unique IDs available.")
            num_ids = len(ids)
        
        selected_ids = random.sample(ids, num_ids)
        
        with open(output_file, "w") as f:
            f.writelines(selected_ids)
        
        print(f"Successfully wrote {num_ids} unique random IDs to {output_file}")
    
    except Exception as e:
        print(f"An error occurred with file {input_file}: {e}")

for input_file, output_file in file_categories.items():
    select_random_ids(input_file, output_file)
