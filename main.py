import pygame
import sys
from Interface import Interface
from Neighborhood import Neighborhood
from SharedState import SharedState

def create_visualization():
    # Initialize Pygame
    pygame.init()

    # Check if initialization was successful
    if not pygame.get_init():
        print("Failed to initialize Pygame")
        sys.exit()

    # Set up the display
    screen_size = 1600, 900
    #screen = pygame.display.set_mode(screen_size, display=1)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN, display=0)
    game_icon = pygame.image.load('Images\power pole.png')
    pygame.display.set_icon(game_icon)
    pygame.display.set_caption("Wat is Mijn Impact op het Grid?")

    # Init classes
    shared_state = SharedState()
    interface = Interface(screen_size, (10,10), shared_state)
    neighborhood = Neighborhood(screen_size,interface.get_percentages(), shared_state)

    # Define colors
    background_color = (229, 237, 248)  # Light blue

    # Main loop
    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    interface.handle_mouse_down(event.pos)
                    neighborhood.handle_events(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    interface.handle_mouse_up()
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:  # Left mouse button is pressed
                        interface.update_sliders(event.pos)

        except Exception as e:
            print(e)

        # Fill the background
        screen.fill(background_color)
        neighborhood.draw(screen, interface.get_percentages(),interface.get_weather())
        neighborhood.update_power_profile(interface.get_PV_slider(), interface.get_eCooking_slider(),\
                                          interface.get_EV_slider(), interface.get_HP_slider(), interface.get_weather(),\
                                            interface.get_EV_schedule_pos(), interface.get_HP_schedule_pos())
        interface.draw(screen)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        create_visualization()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()