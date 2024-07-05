import pygame
import sys

class Interface:
    def __init__(self, screen_size, position, shared_state):
        self.screen_size = screen_size
        self.position = position

        #share state
        self.shared_state = shared_state
       
        # Define colors
        self.border_color = (0, 0, 0) 
        self.rect_fill = (211, 211,211)
        #self.slider_colors = [(70, 130, 180), (72, 209, 204), (47, 79, 79), (255, 127, 80)]  # Different slider colors 
        self.slider_colors = [(0, 18, 61), (70, 172, 187), (74, 100, 125), (84, 150, 199)]  # Different slider colors 	
        self.slider_bg_color = (220, 220, 220)  # Light grey for background
        self.circle_color = (255, 255, 255)  # White 

        # Load images
        self.images = [
            pygame.image.load('Images\EV_icon_2.svg'),
            pygame.image.load('Images\HP_icon.svg'),
            pygame.image.load('Images\eCooking_icon_2.svg'),
            pygame.image.load('Images\solar_icon_2.svg')
        ]
        self.images[0] = pygame.transform.scale(self.images[0], (75, 75))
        self.images[1] = pygame.transform.scale(self.images[1], (80, 80))
        self.images[2] = pygame.transform.scale(self.images[2], (850, 850))
        self.images[3] = pygame.transform.scale(self.images[3], (115, 115))


        # Define rectangle
        self.rect_width = self.screen_size[0]/4.5
        self.rect_height = self.screen_size[1]/2.5
        self.rect = pygame.Rect(position[0], position[1], self.rect_width, self.rect_height)
        self.border_radius = 20
        self.border_width = 2

        # Slider positions and sizes
        sliders_pos_x = 80
        sliders_pos_y = 90
        self.slider_rects = [
            pygame.Rect(self.position[0]+ sliders_pos_x, self.position[1] + sliders_pos_y + 0*(self.rect_height-sliders_pos_y)/4, (self.rect_width-sliders_pos_x)-20, 10),
            pygame.Rect(self.position[0]+ sliders_pos_x, self.position[1] + sliders_pos_y + 1*(self.rect_height-sliders_pos_y)/4, (self.rect_width-sliders_pos_x)-20, 10),
            pygame.Rect(self.position[0]+ sliders_pos_x, self.position[1] + sliders_pos_y + 2*(self.rect_height-sliders_pos_y)/4, (self.rect_width-sliders_pos_x)-20, 10),
            pygame.Rect(self.position[0]+ sliders_pos_x, self.position[1] + sliders_pos_y + 3*(self.rect_height-sliders_pos_y)/4, (self.rect_width-sliders_pos_x)-20, 10),
        ]
        self.circle_radius = 10
        self.slider_values = [0.1, 0.2, 0.4, 0.3]  #start positions
        self.left_arrow = pygame.image.load('Images/left_arrow.png')
        self.right_arrow = pygame.image.load('Images/right_arrow.png')
        self.left_arrow = pygame.transform.smoothscale(self.left_arrow, (25,25))
        self.right_arrow = pygame.transform.smoothscale(self.right_arrow, (25,25))

        # Font
        self.font = pygame.font.SysFont(None, 36)
        self.amount_font = pygame.font.SysFont(None, 24)
        self.title_text_1 = self.font.render('Aantal Apparaten', True, (0, 0, 0))

        # Weather buttons
        weatherblock_height = 100
        self.weather_rect = pygame.Rect(self.position[0], self.position[1] + self.rect_height + 10, self.rect_width, weatherblock_height)
        self.sunny_rect = pygame.Rect(self.weather_rect.x + 15, self.weather_rect.y + 40, (self.rect_width-45)/2, weatherblock_height/2)
        self.cloudy_rect = pygame.Rect(self.weather_rect.x + (self.rect_width-45)/2 + 30, self.weather_rect.y + 40, (self.rect_width-45)/2, weatherblock_height/2)
        self.sunny_active = True
        self.cloudy_active = False

        self.button_backgroundcolor = (240,240,240)

        # Weather font and icons
        self.weather_font = pygame.font.SysFont(None, 30)
        self.weather_title_text = self.font.render('Weer', True, (0, 0, 0))
        weather_icon_size = (30, 30)
        self.sunny_icon = pygame.image.load('Images/sunny_icon_2.png')
        self.cloudy_icon = pygame.image.load('Images/cloudy_icon_2.png')
        self.sunny_icon = pygame.transform.smoothscale(self.sunny_icon, weather_icon_size)
        self.cloudy_icon = pygame.transform.smoothscale(self.cloudy_icon, weather_icon_size)

         # Schedule slider
        scheduleblock_height = 200
        self.schedule_rect = pygame.Rect(self.position[0], self.position[1] + self.rect_height + 10 + weatherblock_height + 10, self.rect_width, scheduleblock_height)
        self.schedule_bar_pos = (self.schedule_rect.x + 10, self.schedule_rect.y + 100)
        self.schedule_bar = pygame.Rect(self.schedule_bar_pos[0], self.schedule_bar_pos[1], self.schedule_rect.width - 20, 20)
        self.bracket_width = self.schedule_bar.width/3
        self.schedule_positions = {
            "morning": self.schedule_bar.x,
            "afternoon": self.schedule_bar.x + (self.bracket_width),
            "evening": self.schedule_bar.x + 2*self.bracket_width
        }
        self.car_position = self.schedule_positions["evening"]
        self.heat_pump_position = self.schedule_positions["evening"]
        self.car_rect = pygame.Rect(self.car_position, self.schedule_bar.y - 70, self.bracket_width, 50)
        self.heat_pump_rect = pygame.Rect(self.heat_pump_position, self.schedule_bar.y + 40, self.bracket_width, 50)
        self.car_icon = pygame.image.load('Images/EV_icon_2.svg')
        self.heat_pump_icon = pygame.image.load('Images/HP_icon.svg')
        self.car_icon = pygame.transform.smoothscale(self.car_icon, (60, 60))
        self.heat_pump_icon = pygame.transform.smoothscale(self.heat_pump_icon, (60, 60))
        self.dark_sun = pygame.image.load('Images/dark_sun_icon.svg')
        self.dark_moon = pygame.image.load('Images/dark_moon_icon.svg')
        self.dark_sun = pygame.transform.smoothscale(self.dark_sun, (245,245))
        self.dark_moon = pygame.transform.smoothscale(self.dark_moon, (350,350))

        self.active_slider = None  # Track which slider is being moved
        self.EV_schedule_pos = 3  # (default to evening)
        self.HP_schedule_pos = 3  # (default to evening)
        
        #scenario buttons
        scenarioblock_height = 50
        self.best_scenario_rect = pygame.Rect(self.position[0], self.position[1] + self.rect_height + 10 + weatherblock_height + 10 + scheduleblock_height + 10\
                                         , (self.rect_width -10)/2, scenarioblock_height)
        self.worst_scenario_rect = pygame.Rect(self.position[0] + (self.rect_width -10)/2 + 10, self.position[1] + self.rect_height + 10 + weatherblock_height + 10 + scheduleblock_height + 10\
                                         , (self.rect_width -10)/2, scenarioblock_height)
        self.scenario_font = pygame.font.SysFont(None, 24)

    def draw(self, screen):
        self.lctPenetrations(screen)
        self.draw_weather_block(screen)
        self.draw_schedule_block(screen)
        self.draw_scenario_blocks(screen)

    def lctPenetrations(self,screen):
        # draw rectangle
        pygame.draw.rect(screen, self.rect_fill, self.rect, int(self.border_width + self.rect_width), self.border_radius)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width, self.border_radius)

        # List of texts for each slider
        slider_texts = ["Elektrische Auto", "Warmtepomp", "Elektrisch Koken", "Zonnepaneel"]

        #draw sliders
        # Draw sliders and icons
        for i, slider in enumerate(self.slider_rects):

            # Draw slider background
            pygame.draw.rect(screen, self.slider_bg_color, slider)

            # Draw slider fill
            fill_rect = pygame.Rect(slider.x, slider.y, slider.width * self.slider_values[i], slider.height)
            pygame.draw.rect(screen, self.slider_colors[i], fill_rect)

            # Draw slider circle
            circle_x = slider.x + int(slider.width * self.slider_values[i])
            circle_y = slider.y + slider.height // 2
            pygame.draw.circle(screen, self.circle_color, (circle_x, circle_y), self.circle_radius)

            # Draw percentage text
            amount = int(self.slider_values[i] * 100)
            amount_text = self.amount_font.render(f'{amount}%', True, (0, 0, 0))
            screen.blit(amount_text, (slider.x, slider.y + 15))

            # draw icons
            screen.blit(self.images[i], (slider.x - 65, slider.y -20))

            # Draw text above slider
            text_surface = self.amount_font.render(slider_texts[i], True, (0, 0, 0))
            screen.blit(text_surface, (slider.x, slider.y - 20))  # Adjust the y-offset to place the text above the slider
        
        # Draw title
        screen.blit(self.title_text_1, (self.rect_width // 2 - self.title_text_1.get_width() // 2, self.position[1] + 20))

    def draw_weather_block(self, screen):
        # Draw weather block background
        pygame.draw.rect(screen, self.rect_fill, self.weather_rect, border_radius=20)
        pygame.draw.rect(screen, self.border_color, self.weather_rect, self.border_width, border_radius=20)

        # Draw title
        screen.blit(self.weather_title_text, (self.weather_rect.x + self.weather_rect.width // 2 - self.weather_title_text.get_width() // 2, self.weather_rect.y + 10))

        # Draw Sunny button
        sunny_bg_color = self.button_backgroundcolor if not self.sunny_active else (173, 216, 230)
        pygame.draw.rect(screen, sunny_bg_color, self.sunny_rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, self.sunny_rect, self.border_width, border_radius=10)
        screen.blit(self.sunny_icon, (self.sunny_rect.x + 10, self.sunny_rect.y + 10))
        sunny_text = self.weather_font.render('Zonnig', True, (0, 0, 0))
        screen.blit(sunny_text, (self.sunny_rect.x + 50, self.sunny_rect.y + 12))

        # Draw Cloudy button
        cloudy_bg_color = self.button_backgroundcolor if not self.cloudy_active else (173, 216, 230)
        pygame.draw.rect(screen, cloudy_bg_color, self.cloudy_rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, self.cloudy_rect, self.border_width, border_radius=10)
        screen.blit(self.cloudy_icon, (self.cloudy_rect.x + 10, self.cloudy_rect.y + 10))
        cloudy_text = self.weather_font.render('Bewolkt', True, (0, 0, 0))
        screen.blit(cloudy_text, (self.cloudy_rect.x + 50, self.cloudy_rect.y + 12))

    def draw_schedule_block(self, screen):
        # Draw schedule block background
        pygame.draw.rect(screen, self.rect_fill, self.schedule_rect, border_radius=20)
        pygame.draw.rect(screen, self.border_color, self.schedule_rect, self.border_width, border_radius=20)

        # Draw title
        schedule_title = self.font.render('Dagplanning', True, (0, 0, 0))
        screen.blit(schedule_title, (self.schedule_rect.x + self.schedule_rect.width // 2 - schedule_title.get_width() // 2, self.schedule_rect.y + 10))

        # Draw schedule bar
        pygame.draw.rect(screen, (120, 120, 120), (self.schedule_bar[0],self.schedule_bar[1],self.schedule_bar[2]/4,self.schedule_bar[3]))
        pygame.draw.rect(screen, (169, 169, 169), (self.schedule_bar[0]+1*self.schedule_bar[2]/4,self.schedule_bar[1],self.schedule_bar[2]/4,self.schedule_bar[3]))
        pygame.draw.rect(screen, (169, 169, 169), (self.schedule_bar[0]+2*self.schedule_bar[2]/4 -1,self.schedule_bar[1],self.schedule_bar[2]/4 +2,self.schedule_bar[3])) #some patching up
        pygame.draw.rect(screen, (120, 120, 120), (self.schedule_bar[0]+3*self.schedule_bar[2]/4,self.schedule_bar[1],self.schedule_bar[2]/4 +2,self.schedule_bar[3]))

        #draw dark sun and moon in bar
        screen.blit(self.dark_sun, (self.schedule_bar[0]+1*self.schedule_bar[2]/4 + 2, self.schedule_bar[1]))
        screen.blit(self.dark_moon, (self.schedule_bar[0]+3*self.schedule_bar[2]/4 + 2, self.schedule_bar[1]))

        # Draw car icon and bracket
        screen.blit(self.car_icon, (self.car_rect.x + self.bracket_width/2 - self.car_rect.width/4, self.car_rect.y + 5))
        car_color = self.slider_colors[0]
        pygame.draw.line(screen, car_color, (self.car_rect.x, self.car_rect.y + self.car_rect.height), (self.car_rect.x + self.bracket_width, self.car_rect.y + self.car_rect.height), 2)
        pygame.draw.line(screen, car_color, (self.car_rect.x, self.car_rect.y + self.car_rect.height), (self.car_rect.x, self.car_rect.y + self.car_rect.height + 15), 2)
        pygame.draw.line(screen, car_color, (self.car_rect.x + self.bracket_width, self.car_rect.y + self.car_rect.height), (self.car_rect.x + self.bracket_width, self.car_rect.y + self.car_rect.height + 15), 2)
        screen.blit(self.left_arrow, (self.car_rect.x, self.car_rect.y + 17))
        screen.blit(self.right_arrow, (self.car_rect.x + self.bracket_width - 35, self.car_rect.y + 17))

        
        # Draw heat pump icon and bracket 
        screen.blit(self.heat_pump_icon, (self.heat_pump_rect.x + self.bracket_width/2 - self.heat_pump_rect.width/4 + 3, self.heat_pump_rect.y + 5))
        HP_color = self.slider_colors[1]
        pygame.draw.line(screen, HP_color, (self.heat_pump_rect.x, self.heat_pump_rect.y), (self.heat_pump_rect.x + self.bracket_width, self.heat_pump_rect.y), 2)
        pygame.draw.line(screen, HP_color, (self.heat_pump_rect.x, self.heat_pump_rect.y), (self.heat_pump_rect.x, self.heat_pump_rect.y -15), 2)
        pygame.draw.line(screen, HP_color, (self.heat_pump_rect.x + self.bracket_width, self.heat_pump_rect.y), (self.heat_pump_rect.x + self.bracket_width, self.heat_pump_rect.y -15), 2)
        screen.blit(self.left_arrow, (self.heat_pump_rect.x, self.heat_pump_rect.y + 12))
        screen.blit(self.right_arrow, (self.heat_pump_rect.x + self.bracket_width - 35, self.heat_pump_rect.y + 12))


    def draw_scenario_blocks(self, screen):
        # Draw best case scenario
        pygame.draw.rect(screen, self.button_backgroundcolor, self.best_scenario_rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, self.best_scenario_rect, self.border_width, border_radius=10)
        # Draw title
        best_scenario_title = self.scenario_font.render('Beste Scenario', True, (0, 0, 0))
        screen.blit(best_scenario_title, (self.best_scenario_rect.x + self.best_scenario_rect.width / 2 - best_scenario_title.get_width() / 2, self.best_scenario_rect.y+ self.best_scenario_rect.height/2 - best_scenario_title.get_height() / 2))

        # Draw worst case scenario
        pygame.draw.rect(screen, self.button_backgroundcolor, self.worst_scenario_rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, self.worst_scenario_rect, self.border_width, border_radius=10)
        # Draw title
        worst_scenario_title = self.scenario_font.render('Slechtste Scenario', True, (0, 0, 0))
        screen.blit(worst_scenario_title, (self.worst_scenario_rect.x + self.worst_scenario_rect.width / 2 - worst_scenario_title.get_width() / 2, self.worst_scenario_rect.y + self.worst_scenario_rect.height/2 - worst_scenario_title.get_height() / 2))

    def update_sliders(self, mouse_pos):
        if self.active_slider is not None:
            if isinstance(self.active_slider, int):
                slider = self.slider_rects[self.active_slider]
                relative_x = mouse_pos[0] - slider.x
                new_value = max(0, min(1, relative_x / slider.width))
                self.slider_values[self.active_slider] = round(new_value * 10) / 10  # Round to nearest 0.1
            elif self.active_slider == 'car':
                new_position = max(self.schedule_bar.x, min(self.schedule_bar.x + 2* self.bracket_width, mouse_pos[0]))
                self.car_rect.x = new_position
                if new_position <=75:
                    self.EV_schedule_pos = 1
                elif new_position >= 188:
                    self.EV_schedule_pos = 3
                else:
                    self.EV_schedule_pos = 2
            elif self.active_slider == 'heat_pump':
                new_position = max(self.schedule_bar.x, min(self.schedule_bar.x + 2* self.bracket_width, mouse_pos[0]))
                self.heat_pump_rect.x = new_position
                if new_position <=75:
                    self.HP_schedule_pos = 1
                elif new_position >= 188:
                    self.HP_schedule_pos = 3
                else:
                    self.HP_schedule_pos = 2

    def get_EV_schedule_pos(self):
        return self.EV_schedule_pos
    
    def get_HP_schedule_pos(self):
        return self.HP_schedule_pos
    
    def get_weather(self):
        if self.sunny_active:
            return 1
        else:
            return 0

    def get_percentages(self):
        return self.slider_values
    
    def get_weather(self):
        return self.sunny_active
    
    def get_PV_slider(self):
        return self.slider_values[3]
    
    def get_eCooking_slider(self):
        return self.slider_values[2]
    
    def get_EV_slider(self):
        return self.slider_values[0]
    
    def get_HP_slider(self):
        return self.slider_values[1]

    def handle_mouse_down(self, mouse_pos):
        for i, slider in enumerate(self.slider_rects):
            circle_x = slider.x + int(slider.width * self.slider_values[i])
            circle_y = slider.y + slider.height // 2
            distance = ((mouse_pos[0] - circle_x) ** 2 + (mouse_pos[1] - circle_y) ** 2) ** 0.5
            if distance <= self.circle_radius:
                self.active_slider = i
                self.shared_state.set_state("devices")
                return
        if self.sunny_rect.collidepoint(mouse_pos):
            self.sunny_active = True
            self.cloudy_active = False
            self.shared_state.set_state("weather")
        elif self.cloudy_rect.collidepoint(mouse_pos):
            self.sunny_active = False
            self.cloudy_active = True
            self.shared_state.set_state("weather")
        elif self.car_rect.collidepoint(mouse_pos):
            self.active_slider = "car"
            self.shared_state.set_state("schedule")
        elif self.heat_pump_rect.collidepoint(mouse_pos):
            self.active_slider = "heat_pump"
            self.shared_state.set_state("schedule")
        elif self.best_scenario_rect.collidepoint(mouse_pos):
            self.slider_values = [0.9, 0.8, 0.9, 1]
            self.HP_schedule_pos, self.EV_schedule_pos = 2 , 2
            self.car_rect.x, self.heat_pump_rect.x = 132 , 132
            self.sunny_active = 1
            self.cloudy_active = 0
            self.shared_state.set_state("best case")
        elif self.worst_scenario_rect.collidepoint(mouse_pos):
            self.slider_values = [1, 0.9, 0.8, 0.9]
            self.HP_schedule_pos, self.EV_schedule_pos = 3 , 3
            self.car_rect.x, self.heat_pump_rect.x = 243 , 243
            self.cloudy_active = 0
            self.sunny_active = 1
            self.shared_state.set_state("worst case")
        #print(mouse_pos[0],mouse_pos[1])

    def handle_mouse_up(self):
        if self.active_slider in ['car', 'heat_pump']:
            closest_position = self.find_closest_position(self.active_slider)
            if self.active_slider == 'car':
                self.car_position = closest_position
                self.car_rect.x = closest_position
            elif self.active_slider == 'heat_pump':
                self.heat_pump_position = closest_position
                self.heat_pump_rect.x = closest_position
        self.active_slider = None

    def find_closest_position(self, slider_type):
        if slider_type == 'car':
            current_x = self.car_rect.x
        elif slider_type == 'heat_pump':
            current_x = self.heat_pump_rect.x

        closest_position = min(self.schedule_positions.values(), key=lambda pos: abs(pos - current_x))
        return closest_position