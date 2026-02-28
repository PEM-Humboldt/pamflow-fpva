from time import sleep
from rich.progress import track

# 1. Define the function you want to track
def process_data(items_to_process):
    """
    Tracks the progress of a loop using rich.progress.track.
    """
    # 2. Wrap the iterable (list, range, etc.) with track()
    for item in track(items_to_process, description="[green]Processing files..."):
        # 3. Simulate work being done
        sleep(0.1) 
        
        # You can access the item normally within the loop
        # print(f"Processed item: {item}")


if __name__ == "__main__":
    
    # Define the total number of steps/items
    TOTAL_ITEMS = 50
    data_list = range(TOTAL_ITEMS)
    
    # Run the function
    print("Starting the heavy lifting...")
    process_data(data_list)
    print("Processing complete! ✨")