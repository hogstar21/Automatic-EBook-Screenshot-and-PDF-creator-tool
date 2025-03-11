import pyautogui
import time
import os
from datetime import datetime

def screenshot_ebook(num_pages, page_flip_key="right", delay_between_pages=2, screenshot_region=None):
    """
    Automatically takes screenshots of an ebook and flips pages.
    
    Parameters:
    - num_pages: Number of pages to capture
    - page_flip_key: Keyboard key to press to flip the page (default: right arrow)
    - delay_between_pages: Time in seconds to wait between page flips
    - screenshot_region: Optional tuple (left, top, width, height) for partial screen capture
    """
    # Create folder for screenshots with timestamp
    folder_name = f"ebook_screenshots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(folder_name, exist_ok=True)
    
    print("Starting screenshot process in 5 seconds...")
    print("Switch to your e-book reader and position the first page")
    time.sleep(5)
    
    for page_num in range(1, num_pages + 1):
        # Take screenshot
        screenshot_path = os.path.join(folder_name, f"page_{page_num:04d}.png")
        
        if screenshot_region:
            screenshot = pyautogui.screenshot(region=screenshot_region)
        else:
            screenshot = pyautogui.screenshot()
            
        screenshot.save(screenshot_path)
        print(f"Captured page {page_num}/{num_pages}")
        
        # Don't flip after the last page
        if page_num < num_pages:
            # Flip to next page
            pyautogui.press(page_flip_key)
            print(f"Flipped to next page")
            time.sleep(delay_between_pages)  # Wait for page to load

if __name__ == "__main__":
    print("E-book Screenshot Tool")
    print("======================")
    
    # Get user input
    num_pages = int(input("Enter number of pages to capture: "))
    
    # Ask if user wants to use a region
    use_region = input("Do you want to capture only a specific region of the screen? (y/n): ").lower() == 'y'
    region = None
    
    if use_region:
        print("Move your mouse to the top-left corner of the region and press Enter")
        input("Press Enter when ready...")
        top_left = pyautogui.position()
        
        print("Now move your mouse to the bottom-right corner of the region and press Enter")
        input("Press Enter when ready...")
        bottom_right = pyautogui.position()
        
        region = (top_left.x, top_left.y, bottom_right.x - top_left.x, bottom_right.y - top_left.y)
        print(f"Region set to: {region}")
    
    # Ask for page flip key
    page_flip_key = input("Enter key to use for page flip (default is 'right' arrow): ") or "right"
    
    # Ask for delay
    try:
        delay = float(input("Enter delay between page flips in seconds (default is 2.0): ") or "2.0")
    except ValueError:
        delay = 2.0
    
    # Confirm before starting
    print("\nSettings:")
    print(f"- Will capture {num_pages} pages")
    print(f"- Using '{page_flip_key}' key to flip pages")
    print(f"- Waiting {delay} seconds between flips")
    if region:
        print(f"- Capturing region: {region}")
    else:
        print("- Capturing full screen")
    
    proceed = input("\nReady to start? Make sure your e-book is open and ready on the first page. (y/n): ")
    
    if proceed.lower() == 'y':
        screenshot_ebook(num_pages, page_flip_key, delay, region)
        print(f"\nCompleted! All screenshots saved to folder: {os.path.abspath(folder_name)}")
    else:
        print("Operation cancelled.")