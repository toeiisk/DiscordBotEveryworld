# import pyautogui
# import time

# def is_color_green(rgb, green_threshold=120):
#     """Check if the color is considered green."""
#     r, g, b = rgb
#     return g > green_threshold and g > r and g > b

# def move_cursor_away(safe_x, safe_y):
#     """Move the cursor to a specified safe location."""
#     pyautogui.moveTo(safe_x, safe_y)

# def click_button_if_green(button_x, button_y, safe_x, safe_y, cooldown=1.0):
#     """Click the button if it's green, then wait for it not to be green before clicking again."""
#     # Move cursor to a safe location first to avoid hover effects
#     move_cursor_away(safe_x, safe_y)
#     button_color = pyautogui.screenshot().getpixel((button_x, button_y))
#     if is_color_green(button_color):
#         pyautogui.click(button_x, button_y)
#         print(f"Clicked green button at ({button_x}, {button_y}).")
#         # Move cursor away after clicking
#         move_cursor_away(safe_x, safe_y)
#         time.sleep(cooldown)  # Wait after a click to avoid rapid re-clicks
#         # Wait for the button to not be green anymore
#         while is_color_green(pyautogui.screenshot().getpixel((button_x, button_y))):
#             time.sleep(0.5)  # Check every half second
#             move_cursor_away(safe_x, safe_y)  # Keep cursor away during checks
#         print("Button no longer green, ready for next click.")

# def autoclicker(button1_x, button1_y, button2_x, button2_y, safe_x, safe_y):
#     try:
#         print("Autoclicker started. Press CTRL+C to stop.")
#         while True:
#             click_button_if_green(button1_x, button1_y, safe_x, safe_y)
#             click_button_if_green(button2_x, button2_y, safe_x, safe_y)
#     except KeyboardInterrupt:
#         print("Autoclicker terminated.")

# # Replace these coordinates with the coordinates of your buttons and a safe position
# button1_x = 844
# button1_y = 840
# button2_x = 915
# button2_y = 841
# safe_x = 100  # Example safe coordinate X
# safe_y = 100  # Example safe coordinate Y

# autoclicker(button1_x, button1_y, button2_x, button2_y, safe_x, safe_y)

import pyautogui
import time

def is_color_green(rgb, green_threshold=120):
    """Check if the color is considered green."""
    r, g, b = rgb
    return g > green_threshold and g > r and g > b

def is_specific_grey(rgb, target_rgb=(78, 80, 88)):
    """Check if the color matches the specific grey color."""
    return rgb == target_rgb

def move_cursor_away(safe_x, safe_y):
    """Move the cursor to a specified safe location."""
    pyautogui.moveTo(safe_x, safe_y)

def click_button_if_color(button_x, button_y, safe_x, safe_y, color_check_function, cooldown=1.0):
    """Click the button if it matches the color criteria."""
    move_cursor_away(safe_x, safe_y)
    button_color = pyautogui.screenshot().getpixel((button_x, button_y))
    if color_check_function(button_color):
        pyautogui.click(button_x, button_y)
        print(f"Clicked button at ({button_x}, {button_y}) with color {button_color}.")
        move_cursor_away(safe_x, safe_y)
        time.sleep(cooldown)
        return True  # Click occurred
    return False  # No click occurred

def autoclicker(button1_x, button1_y, button2_x, button2_y, safe_x, safe_y, grey_click_delay=120, terminate_timeout=180):
    print("Autoclicker started. Press CTRL+C to stop.")
    last_green_click_time = time.time()
    last_action_time = last_green_click_time  # Track any button click
    grey_click_allowed_time = last_green_click_time + grey_click_delay  # Initiate with delay

    try:
        while True:
            current_time = time.time()
            clicked_any = False

            # Check for green button
            if click_button_if_color(button1_x, button1_y, safe_x, safe_y, is_color_green) or click_button_if_color(button2_x, button2_y, safe_x, safe_y, is_color_green):
                last_green_click_time = current_time
                grey_click_allowed_time = current_time + grey_click_delay  # Reset grey click delay
                clicked_any = True

            # Check for grey button if no green button clicked and grey click delay has passed
            elif current_time >= grey_click_allowed_time:
                if click_button_if_color(button1_x, button1_y, safe_x, safe_y, is_specific_grey) or click_button_if_color(button2_x, button2_y, safe_x, safe_y, is_specific_grey):
                    grey_click_allowed_time = current_time + grey_click_delay  # Reset grey click delay to avoid immediate re-clicks
                    clicked_any = True

            if clicked_any:
                last_action_time = current_time

            # Terminate if no interaction for a specified timeout
            if current_time - last_action_time > terminate_timeout:
                print("No buttons clicked recently. Terminating autoclicker.")
                break

    except KeyboardInterrupt:
        print("Autoclicker terminated.")

# Replace these coordinates with the coordinates of your buttons and a safe position
button1_x = 844
button1_y = 840
button2_x = 915
button2_y = 841
safe_x = 100  # Example safe coordinate X
safe_y = 100  # Example safe coordinate Y

autoclicker(button1_x, button1_y, button2_x, button2_y, safe_x, safe_y)


