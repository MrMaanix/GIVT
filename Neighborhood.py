import pygame
import sys
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
from House import House

class Neighborhood:
    def __init__(self, screen_size, slider_percentages, shared_state):
        self.screen_size = screen_size
    
        #share state
        self.shared_state = shared_state

        # Define colors
        self.ellipse_fill = (144, 201, 204)

        self.count = 0 # temporary fix

        # Define ground
        self.ground_ellipse = (self.screen_size[0]/6, self.screen_size[1]/2+35, self.screen_size[0]*5/6+20, self.screen_size[1]/2-40)
        self.ground_transformer_ellipse = (self.screen_size[0]-150, self.screen_size[1]/2 - 30, self.screen_size[0]/4, self.screen_size[1]/6-30)

        # load transformer grid station
        self.transformer = pygame.image.load('Images\Transformer house and grid pole.png')
        self.transformer = pygame.transform.smoothscale(self.transformer, (200,200))

        #define houses
        self.houses = House(screen_size)

         # Load data
        self.PV_generation_cloudy = pd.read_csv('Data\PV_generation_cloudy.csv', header=None)
        self.PV_generation_sunny = pd.read_csv('Data\PV_generation_sunny.csv', header=None)
        self.eCooking_demand = pd.read_csv('Data\eCooking_demand.csv', header=None)
        self.Baseload = pd.read_csv('Data\Baseload.csv', header=None)
        self.EV_demand = pd.read_csv('Data\EV_demand.csv', header=None)
        self.HP_demand = pd.read_csv('Data\HP_demand.csv', header=None)

        # toggle between graphs
        self.graph_toggle = 0   # 0 = capacity bar, 1 =power profile
        self.prev_toggle = 0   
        self.graph_button_pos = (1450,10)
        self.graph_button_rect = pygame.Rect(self.graph_button_pos[0], self.graph_button_pos[1], 140,50)
        self.graph_text_CB = "  Klik hier voor\nvermogensprofiel"
        self.graph_text_PP = "  Klik hier voor\n  capaciteitsbalk"
        self.graph_button_font = pygame.font.SysFont(None, 23)
        self.button_backgroundcolor = (240, 240, 240)
        self.power_profile_pos = (self.screen_size[0]/2+100, 10)
        self.power_profile_hitbox_rect = pygame.Rect(self.power_profile_pos[0], self.power_profile_pos[1], 540,360)
        
        # Initialize power profile
        self.power_profile = None

        # Previous slider values
        self.prev_PV_percentage = None
        self.prev_eCooking_percentage = None
        self.prev_EV_percentage = None
        self.prev_HP_percentage = None
        self.prev_EV_schedule = 3           # 3 = evening, 2 = afternoon, 1 = morning
        self.prev_HP_schedule = 3           # 3 = evening, 2 = afternoon, 1 = morning

        #weather
        weather_icon_size = (90, 90)
        self.sunny_icon = pygame.image.load('Images/sunny_icon_2.png')
        self.cloudy_icon = pygame.image.load('Images/cloudy_icon_2.png')
        self.sunny_icon = pygame.transform.smoothscale(self.sunny_icon, weather_icon_size)
        self.cloudy_icon = pygame.transform.smoothscale(self.cloudy_icon, weather_icon_size)
        self.prev_weather = 1               # 1 = sunny, 0 = cloudy

        # Define capacity bar properties
        self.capacitybar_width = 150
        self.capacitybar_height = 360
        self.capacitybar_pos = (screen_size[0] - self.capacitybar_width - 160, 10)
        self.capacitybar_rect = pygame.Rect(self.capacitybar_pos[0], self.capacitybar_pos[1], self.capacitybar_width, self.capacitybar_height)
        self.bar_rect = pygame.Rect(self.capacitybar_pos[0], self.capacitybar_pos[1], self.capacitybar_width, self.capacitybar_height)
        self.capacitybar_backgroundcolor = (220, 220, 220)  # Light grey for background
        self.border_radius = 20
        self.border_width = 2
        #the bar itself
        self.bar_color = (25, 150, 111) # bar start color green
        self.bar_width = 60
        self.bar_height = 290
        self.bar_pos = (self.capacitybar_pos[0] + 80, self.capacitybar_pos[1] + 60)
        self.bar_rect = pygame.Rect(self.bar_pos[0], self.bar_pos[1], self.bar_width, self.bar_height)
        self.green_bar_height = 50

        # Create the graph surface
        self.graph_surface = self.update_graph()
        self.update_power_profile(slider_percentages[3], slider_percentages[2], slider_percentages[0], slider_percentages[1], 1, 3, 3)

        #make textbox
        self.textbox_rect = pygame.Rect(390, 110, 480, 190)
        self.textbox_font = pygame.font.SysFont(None, 24)
        self.textbox_button_rect = pygame.Rect(self.textbox_rect.x, self.textbox_rect.y, 17,17)
        self.textbutton = True

        #load alert icon
        self.red_alert_icon = pygame.image.load('Images/red-alert-icon.png')
        self.red_alert_icon = pygame.transform.smoothscale(self.red_alert_icon, (60,60))
        #alarm edge
        self.alarm_border_width = 5
        self.alarm_border = pygame.Rect(0, 0, screen_size[0], screen_size[1])

    def draw(self, screen,LCT_percentages, weather_status):
        self.neighborhood(screen)
        self.houses.draw(screen, LCT_percentages)
        self.weather(screen, weather_status)
        self.draw_graphs(screen)
        self.draw_textbox(screen)

    def neighborhood(self,screen):
        # draw main ellipse
        pygame.draw.ellipse(screen, self.ellipse_fill, self.ground_ellipse)

        #draw transformer ellipse and grid
        pygame.draw.ellipse(screen, self.ellipse_fill, self.ground_transformer_ellipse)
        screen.blit(self.transformer, (self.screen_size[0]-163,self.screen_size[1]/3+15))

        #draw cables
        cable_color = (150,150,150)
        # Define start and end points
        start_pos_1 = (722, 377)
        end_pos_1 = (1064, 426)
        # Draw the hanging cable
        self.draw_hanging_cable(screen, start_pos_1, end_pos_1, -10, cable_color, 1)

        # Define start and end points
        start_pos_2 = (1188, 399)
        end_pos_2 = (1510, 459)
        # Draw the hanging cable
        self.draw_hanging_cable(screen, start_pos_2, end_pos_2, -20, cable_color, 1)

        # Define start and end points
        start_pos_3 = (1456, 473)
        end_pos_3 = (1094, 434)
        # Draw the hanging cable
        self.draw_hanging_cable(screen, start_pos_3, end_pos_3, -10, cable_color, 1)

        #draw transformer cone
        pygame.draw.polygon(screen, (0,0,0), ((1490,450), (1345,363), (1410,363)))
        
    def draw_hanging_cable(self, screen, start_pos, end_pos, sag, color, width):
        # Number of segments to divide the cable into
        segments = 100
        
        # Calculate the distance between the start and end points
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        # Generate points along the curve
        points = []
        for i in range(segments + 1):
            t = i / segments
            x = start_pos[0] + t * dx
            y = start_pos[1] + t * dy - sag * math.sin(t * math.pi)
            points.append((x, y))
    
        # Draw lines between the generated points
        for i in range(segments):
            pygame.draw.line(screen, color, points[i], points[i + 1], width)

    def weather(self, screen, weather_code):
        weather_pos = (self.textbox_rect.x + self.textbox_rect.width/2 - 45 ,10)
        if weather_code == True:
            screen.blit(self.sunny_icon, weather_pos)
        else:
            screen.blit(self.cloudy_icon, weather_pos)

    def draw_graphs(self, screen):
        # draw graph button
        pygame.draw.rect(screen, self.button_backgroundcolor, self.graph_button_rect, 0, 10)
        pygame.draw.rect(screen, (0,0,0), self.graph_button_rect, self.border_width, 10)
        #pygame.draw.line(screen, (0,0,0), (self.graph_button_pos[0] + self.border_width +2, self.graph_button_pos[1] + 15), (self.graph_button_pos[0] - self.border_width -3 +30, self.graph_button_pos[1] + 15), 3)

        # Switch between graphs
        if self.graph_toggle == 0:
            self.draw_capacity_bar(screen)
            #draw the plus
            #pygame.draw.line(screen, (0,0,0), (self.graph_button_pos[0] + 14 ,self.graph_button_pos[1] + self.border_width +2), (self.graph_button_pos[0] + 14, self.graph_button_pos[1] - self.border_width -3 +30), 3)
            text = self.graph_text_CB
        else:
            self.draw_power_profile(screen)
            text = self.graph_text_PP

        #display text in button
        max_width = self.graph_button_rect.width - 5  # Padding for text within the rectangle
        lines = self.wrap_text(text, self.graph_button_font, max_width)

        x_offset, y_offset = 6, 8
        for line in lines:
            graphbutton_text = self.graph_button_font.render(line, True, (0, 0, 0))
            screen.blit(graphbutton_text, (self.graph_button_rect.x + x_offset, self.graph_button_rect.y + y_offset))
            y_offset += self.graph_button_font.get_height() + 3        

        max_value = self.power_profile.max().max()
        if max_value >= 55:
            screen.blit(self.red_alert_icon, (1490,385))
            pygame.draw.rect(screen, (226,27,27), self.alarm_border, self.alarm_border_width)
        
    def draw_capacity_bar(self, screen):
        # draw rectangle
        border_curve = 0
        pygame.draw.rect(screen, self.capacitybar_backgroundcolor, self.capacitybar_rect, int(self.capacitybar_width/2), border_curve)
        pygame.draw.rect(screen, (0,0,0), self.capacitybar_rect, self.border_width, border_curve)    
        
        # draw the bar
        pygame.draw.rect(screen, (0,0,0), self.bar_rect, self.border_width, border_curve)        
        
        # Draw the percentage lines and text
        font = pygame.font.SysFont(None, 24)
        for i in range(0, 101, 25):
            y_pos = self.bar_pos[1] + self.bar_height * (1 - i / 120) -5
            text = font.render(f"{i}%", True, (0, 0, 0))
            text_width = text.get_width()
            screen.blit(text, (self.bar_pos[0] - text_width - 5, y_pos - 10))

        green_bar_rect = pygame.Rect(
            self.bar_pos[0] + self.border_width,  # Adjusted position within the bar
            self.bar_pos[1] + (self.bar_height - self.green_bar_height - self.border_width +1),
            self.bar_width - 2*self.border_width,  # Adjusted width within the bar
            self.green_bar_height
        )

        pygame.draw.rect(screen, self.bar_color, green_bar_rect, 0 ,border_curve)
        pygame.draw.line(screen,(0,0,0), (self.capacitybar_pos[0]+80,109), (self.capacitybar_pos[0]+138,109),2)
        # Draw the title
        title_font = pygame.font.SysFont(None, 36)
        title_text = title_font.render("Capaciteit", True, (0, 0, 0))
        screen.blit(title_text, (self.capacitybar_pos[0] + self.capacitybar_width / 2 - title_text.get_width() / 2, self.capacitybar_pos[1] + 10))
        
    def draw_textbox(self, screen):
        #draw button
        pygame.draw.rect(screen, (211, 211, 211), self.textbox_button_rect, 0, 3)
        pygame.draw.rect(screen,(0, 0, 0), self.textbox_button_rect, 1, 3)
        textbox_button_text_font = pygame.font.SysFont(None, 24)
        textbox_button_text = textbox_button_text_font.render("i", True, (0, 0, 0))
        screen.blit(textbox_button_text, (self.textbox_button_rect.x + self.textbox_button_rect.width / 2 - textbox_button_text.get_width() / 2, \
                                          self.textbox_button_rect.y + self.textbox_button_rect.height / 2 - textbox_button_text.get_height() / 2 + 1))

        if self.textbutton:
            shape_surf = pygame.Surface(pygame.Rect(self.textbox_rect).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, (0, 0, 0, 20), shape_surf.get_rect(), 0, 3)
            screen.blit(shape_surf, self.textbox_rect)
            
             # Choose which text based on shared state
            state = self.shared_state.get_state()
            if state == "default":
                text = "Deze visualisatie helpt om een idee te krijgen van de impact die elektrische aparaten hebben op het elektriciteits netwerk.\n\nProbeer het aantal apparaten, het weer en de dagplanning aan te passen en zie de verandering, of klik op een van de twee toekomst scenarios als voorbeeld.\n\nHet doel is om de vermogenspieken, zowel omhoog als omlaag, zo klein mogelijk te houden voor een gebalanceerd netwerk, en daarbij niet over de maximale capaciteit te gaan."
            elif state == "best case":
                text = "Dit is een goed toekomst scenario. Ondanks dat er veel apparaten zullen zijn is het verbruik-gedrag veranderd.\n\nHet meeste verbruik van de auto en de warmtepomp zijn naar de middag verschoven om gebruik te maken van de zonne-energie. Op een zonnige dag zorg dit voor een goede balans tussen energie opwek en vraag.\n\nToch is de auto niet vaak thuis in de middag, probeer de auto eens naar de ochtend te verschuiven."
            elif state == "worst case":
                text = "Dit is een slecht toekomst scenario. De vraag naar elekticiteit is enorm gestegen en het verbruik gedrag is hetzelfde gebleven als nu. Hierdoor is alle elektriciteitsvraag geconcentreerd in de avond, wanneer mensen koken, verwarmen, auto opladen en de zon afwezig is.\n\nDe avond piek is zo hoog dat het elektriciteitsstation het niet aankan en uit zal vallen, waardoor de stroom ook uitvalt. Ook is er een negatieve middag piek door een overschot aan opwek, waardoor het netwerk erg uit balans is."
            elif state == "weather":
                text = "Het weer kan veel invloed hebben op de opwek van zonnepanelen. Op een bewolkte dag neemt de opwek flink af, en elke wolk voor de zon zal zorgen voor een tijdelijk stop van opgewekte energie.\n\nIn het vermogensprofiel zie je dit terug in de 2 pieken vergeleken met de vloeiende boog van een volledig zonnige dag."
            elif state == "devices":
                text = "Hoe meer apparaten er in de wijk zijn, hoe groter de vraag naar elektriciteit.\n\nDe elektrische auto, warmtepomp en elektrische kook apparaten (zoals fornuis, oven, magnetron en waterkoker) vragen veel vermogen. De zonnepanelen wekken juist veel vermogen op.\n\nHet aantal apparaten zal in de komende jaren flink stijgen, hoe moeten we daar mee omgaan?"
            elif state == "schedule":
                #text = "De planning van apparaten met veel vermogen, zoals de elektrische auto en warmtepomp, heeft veel impact op het elektriciteits netwerk.\n\nOmdat er savonds ook al gekookt wordt, de lampen en wasmachine aangaan wil je het liefst de auto en warmtepomp op een ander moment van de dag opladen/ gebruiken.\n\nProbeer ze eens te verschuiven naar de ochtend of de middag en kijk naar het vermogensprofiel."
                text = "De planning van apparaten met veel vermogen, zoals de elektrische auto en warmtepomp, heeft veel impact op het elektriciteits netwerk.\n\nOmdat er savonds ook al gekookt wordt, de lampen en wasmachine aangaan wil je het liefst de auto en warmtepomp op een ander moment van de dag opladen/ gebruiken.\n\nProbeer ze eens te verschuiven naar de ochtend of de middag en kijk naar het vermogensprofiel."
            elif state == "graphs":
                text = "Deze tool laat twee verschillende grafieken zijn, gemeten over de hele wijk:\nDe capaciteitsbalk laat alleen de hoogst behaalde vermogenspiek van de hele dag zien, vergeleken met de maximale capacitieit van het netwerk. Als de piek hoger is dan de maximale capaciteit zal de stroom uitvallen in de hele wijk.\n\nHet vermogensprofiel laat de vermogensvraag over de hele dag zien, en geeft zo meer detail. In de middag daalt het vermogen door de opwek van zonnepanelen, en de vraag zal stijgen op momenten wanneer de auto en warmtepomp worden gebruikt."
            # Display Text
            max_width = self.textbox_rect.width - 40  # Padding for text within the rectangle
            lines = self.wrap_text(text, self.textbox_font, max_width)

            y_offset, x_offset= 20, 20
            for line in lines:
                textbox_text = self.textbox_font.render(line, True, (0, 0, 0))
                screen.blit(textbox_text, (self.textbox_rect.x + x_offset, self.textbox_rect.y + y_offset))
                y_offset += self.textbox_font.get_height() + 3
            self.textbox_rect.height = y_offset + 20
        else:
            None

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            if '\n' in word:
                subwords = word.split('\n')
                for subword in subwords[:-1]:
                    current_line.append(subword)
                    lines.append(' '.join(current_line))
                    current_line = []
                current_line.append(subwords[-1])
            else:
                current_line.append(word)
                text_width, _ = font.size(' '.join(current_line))
                if text_width > max_width:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]

        lines.append(' '.join(current_line))
        return lines

    def update_power_profile(self, PV_percentage, eCooking_percentage, EV_percentage, HP_percentage, weather, EV_schedule, HP_schedule):
        # Check if the slider values have changed
        if (self.prev_PV_percentage != PV_percentage) or (self.prev_eCooking_percentage != eCooking_percentage)\
            or (self.prev_EV_percentage != EV_percentage) or (self.prev_HP_percentage != HP_percentage) or (self.prev_weather != weather)\
                or (self.prev_HP_schedule != HP_schedule) or (self.prev_EV_schedule != EV_schedule) or (self.graph_toggle != self.prev_toggle):
                
                # Adjust data based on slider percentages
                adjusted_baseload = self.Baseload*2
                adjusted_eCooking = self.eCooking_demand * (eCooking_percentage*2)
                adjusted_EV = self.EV_demand * (EV_percentage*2)
                adjusted_HP = self.HP_demand * (HP_percentage*2)

                #check for sunny cloudy
                if weather == 1:                # 1 = sunny, 2 = cloudy
                    adjusted_PV = self.PV_generation_sunny * (PV_percentage*2)
                    self.prev_weather = 1
                else:
                    adjusted_PV = self.PV_generation_cloudy * (PV_percentage*2)
                    self.prev_weather = 0

                #check for schedule shift
                adjusted_EV = self.adjust_demand(1, EV_schedule, adjusted_EV)
                adjusted_HP = self.adjust_demand(2, HP_schedule, adjusted_HP)

                # Combine data to create the power profile
                self.power_profile = adjusted_PV + adjusted_eCooking + adjusted_EV + adjusted_HP  + adjusted_baseload

                # Save the combined data to a new CSV file
                self.power_profile.to_csv('Data/power_profile.csv', header=False, index=False)

                # Update previous slider values
                self.prev_PV_percentage = PV_percentage
                self.prev_eCooking_percentage = eCooking_percentage
                self.prev_EV_percentage = EV_percentage
                self.prev_HP_percentage = HP_percentage

                # Update the graph
                if self.count == 0:
                    self.graph_surface = self.update_graph()            #temporary fix for one time graph loading after startup
                    self.count = 1
                if self.graph_toggle == 0:
                    self.green_bar_height = self.update_capacity_bar()
                    self.prev_toggle = 0
                else:
                    # Update the graph
                    self.graph_surface = self.update_graph()
                    self.prev_toggle = 1
                

    def adjust_demand(self, demand_type, schedule_pos, demand_data):
        if demand_type == 1:
            slider = schedule_pos
        else:
            slider = schedule_pos

        if slider == 1:    # morning
            shift_value = 960
        elif slider == 2:  # afternoon
            shift_value = 480
        elif slider == 3:  # evening
            shift_value = 0

        # Shift the data and update the previous time
        adjusted_demand = self.shift_data(demand_data, shift_value)
        if demand_type == 1:
            self.prev_EV_schedule = slider
        else:
            self.prev_HP_schedule = slider

        return adjusted_demand

    def shift_data(self, data, shift_value):
        if shift_value == 0:
            return data

        shifted_data = data.shift(-shift_value, fill_value=0)
        return shifted_data
    
    def update_capacity_bar(self):
        min_height = 35
        max_height = self.bar_height - self.border_width - 2   #fine tuning
        reference_max_value = 55
        yellow_value = 39
        orange_value = 47.5
        reference_height = 250
        
        power_profile_data = self.power_profile

        max_value = power_profile_data.max().max()

        if max_value < yellow_value:
            self.bar_color = (25, 150, 111)
        elif yellow_value < max_value < orange_value:
            self.bar_color = (255, 222, 89)
        elif orange_value < max_value < reference_max_value:
            self.bar_color = (250, 96, 57)
        elif max_value > reference_max_value:
            self.bar_color = (226,27,27)
            


        # Calculate the green bar height
        green_bar_height = min_height + (max_value / reference_max_value) * (reference_height - min_height)
        # Ensure the green bar height does not exceed the maximum limit
        green_bar_height = min(green_bar_height, max_height)

        return green_bar_height


    def update_graph(self):
        if self.power_profile is not None:
            # Plot the power profile data
            fig, ax = plt.subplots(figsize=(6, 4), dpi=90)
            ax.plot(self.power_profile)
            ax.set_title('Vermogensprofiel')
            ax.set_xlabel('Tijd (uren)')
            ax.set_ylabel('Vermogen (kW)')

            # Create time labels for x-axis
            time_labels = [f'{hour:02d}:00' for hour in range(0, 25, 3)]  # Labels every 2 hours from 00:00 to 00:00
            ax.set_xticks([i * 60 for i in range(0, 25, 3)])  # 1440 data points (one for each minute in a day)
            ax.set_xticklabels(time_labels)

            # Set y-axis limits
            ax.set_ylim([-45, 75])

            # Draw a static red line at y=55
            ax.axhline(y=55, color='red', linestyle='--', linewidth=2)

            # Display "100%" text right of the red line
            ax.text(1.01, 55, "100%", color='black', fontsize=12, ha='left', va='center', transform=ax.get_yaxis_transform())

            # Add a small black border around the graph
            fig.patch.set_edgecolor('black')
            fig.patch.set_linewidth(1.5)

            # Convert the Matplotlib figure to a Pygame image
            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()

            size = canvas.get_width_height()
            graph_surface = pygame.image.fromstring(raw_data, size, "RGB")
            plt.close(fig)

            return graph_surface

    def draw_power_profile(self, screen):
        # Display the pre-created graph surface
        if self.graph_surface:
            screen.blit(self.graph_surface, (self.power_profile_pos[0], self.power_profile_pos[1]))
        else:
            print("fault")

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.graph_button_rect.collidepoint(event.pos):
                state = "graphs"
                if self.graph_toggle == 0:
                    self.graph_toggle = 1
                elif self.graph_toggle == 1:
                    self.graph_toggle = 0
            if self.textbox_button_rect.collidepoint(event.pos):
                if self.textbutton:
                    self.textbutton = False
                elif not self.textbutton:
                    self.textbutton = True
            if self.capacitybar_rect.collidepoint(event.pos) and self.graph_toggle == 0:
                state = "graphs"
            if self.power_profile_hitbox_rect.collidepoint(event.pos) and self.graph_toggle == 1:
                state = "graphs"

        # Update state through the shared state object
        self.shared_state.set_state(state)

