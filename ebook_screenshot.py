import pyautogui
import time
import os
import ctypes
import shutil
from datetime import datetime
from PIL import Image

def screenshot_ebook(num_pages, page_flip_key="right", delay_between_pages=2, screenshot_region=None):
    """
    Automatically takes screenshots of an ebook and flips pages with hidden cursor.
    
    Parameters:
    - num_pages: Number of pages to capture
    - page_flip_key: Keyboard key to press to flip the page (default: right arrow)
    - delay_between_pages: Time in seconds to wait between page flips
    - screenshot_region: Optional tuple (left, top, width, height) for partial screen capture
    
    Returns:
    - folder_name: The path where screenshots are saved
    """
    # Create folder for screenshots with timestamp
    folder_name = f"ebook_screenshots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(folder_name, exist_ok=True)
    
    print("Starting screenshot process in 5 seconds...")
    print("Switch to your e-book reader and position the first page")
    time.sleep(5)
    
    # Focus on the ebook window by clicking
    if screenshot_region:
        center_x = screenshot_region[0] + screenshot_region[2] // 2
        center_y = screenshot_region[1] + screenshot_region[3] // 2
        print(f"Clicking at position ({center_x}, {center_y}) to ensure focus")
        pyautogui.click(x=center_x, y=center_y)
    else:
        # Click in the center of the main screen
        screen_width, screen_height = pyautogui.size()
        print(f"Clicking at position ({screen_width//2}, {screen_height//2}) to ensure focus")
        pyautogui.click(x=screen_width//2, y=screen_height//2)
    
    # Give a moment for the click to register
    time.sleep(1)
    
    # Move mouse to a safe position (not in a corner)
    screen_width, screen_height = pyautogui.size()
    pyautogui.moveTo(screen_width // 4, screen_height // 4)
    
    # Hide cursor using ctypes (Windows specific)
    try:
        ctypes.windll.user32.ShowCursor(False)
        cursor_hidden = True
        print("Cursor hidden successfully")
    except Exception as e:
        cursor_hidden = False
        print(f"Could not hide cursor: {e}")
        print("Continuing with visible cursor...")
    
    try:
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
                # Refocus every 10 pages by clicking, then moving mouse away again
                if page_num % 10 == 0:
                    if screenshot_region:
                        pyautogui.click(x=screenshot_region[0] + screenshot_region[2] // 2, 
                                       y=screenshot_region[1] + screenshot_region[3] // 2)
                    else:
                        screen_width, screen_height = pyautogui.size()
                        pyautogui.click(x=screen_width//2, y=screen_height//2)
                        
                    # Move mouse to a safe position again
                    pyautogui.moveTo(screen_width // 4, screen_height // 4)
                    time.sleep(0.5)
                    
                # Flip to next page
                pyautogui.press(page_flip_key)
                print(f"Flipped to next page")
                time.sleep(delay_between_pages)  # Wait for page to load
    finally:
        # Always show cursor again when script ends or fails
        if cursor_hidden:
            try:
                ctypes.windll.user32.ShowCursor(True)
                print("Cursor visibility restored")
            except Exception as e:
                print(f"Warning: Could not restore cursor visibility: {e}")
                print("You may need to restart your application or system if cursor remains hidden")
    
    return folder_name

def create_pdf_from_images(folder_path, output_pdf_name):
    """
    Create a PDF from all images in a folder.
    
    Parameters:
    - folder_path: Path to folder containing images
    - output_pdf_name: Name for the output PDF file
    
    Returns:
    - success: Boolean indicating if PDF creation was successful
    """
    try:
        # Get all image files and sort them numerically
        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        image_files.sort()  # This will sort by filename, so page_0001.png comes before page_0002.png
        
        if not image_files:
            print("No images found in the folder.")
            return False
        
        # Open the first image to get dimensions
        first_image_path = os.path.join(folder_path, image_files[0])
        first_image = Image.open(first_image_path)
        
        # Convert all images to RGB (required for PDF)
        images = []
        for img_file in image_files:
            img_path = os.path.join(folder_path, img_file)
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)
        
        # Save the PDF
        if images:
            first_image = images[0]
            first_image.save(
                output_pdf_name,
                save_all=True,
                append_images=images[1:],
                resolution=100.0,
                quality=95
            )
            print(f"PDF created successfully: {output_pdf_name}")
            return True
        else:
            print("No valid images to convert to PDF.")
            return False
    
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False

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
    
    # Set default delay to 2.0 seconds
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
    print("- Will hide cursor during screenshot process")
    
    print("\nIMPORTANT: After pressing 'y' to start, IMMEDIATELY switch to your")
    print("e-book window/monitor if you haven't already done so!")
    
    proceed = input("\nReady to start? Make sure your e-book is open and ready on the first page. (y/n): ")
    
    if proceed.lower() == 'y':
        # Take screenshots
        screenshots_folder = screenshot_ebook(num_pages, page_flip_key, delay, region)
        print(f"\nScreenshots captured! All saved to folder: {os.path.abspath(screenshots_folder)}")
        
        # Ask if user wants to compile to PDF
        compile_to_pdf = input("\nWould you like to compile these screenshots into a PDF? (y/n): ").lower() == 'y'
        
        if compile_to_pdf:
            # Get a name for the PDF
            default_pdf_name = f"ebook_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf_name = input(f"Enter PDF filename (default: {default_pdf_name}): ") or default_pdf_name
            
            # Ensure PDF has .pdf extension
            if not pdf_name.lower().endswith('.pdf'):
                pdf_name += '.pdf'
            
            # Create the PDF
            pdf_success = create_pdf_from_images(screenshots_folder, pdf_name)
            
            if pdf_success:
                # Ask if user wants to delete the screenshots folder
                delete_folder = input("\nPDF created successfully. Delete the screenshots folder? (y/n): ").lower() == 'y'
                
                if delete_folder:
                    try:
                        shutil.rmtree(screenshots_folder)
                        print(f"Screenshots folder deleted: {screenshots_folder}")
                    except Exception as e:
                        print(f"Error deleting folder: {e}")
                        print(f"You may need to delete it manually: {os.path.abspath(screenshots_folder)}")
                
                print(f"\nPDF saved to: {os.path.abspath(pdf_name)}")
        
        print("\nThank you for using the E-book Screenshot Tool. Have a nice day!")
    else:
        print("Operation cancelled. Have a nice day!")
