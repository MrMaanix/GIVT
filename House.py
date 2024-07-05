import pygame
import sys
import random

class House:
    def __init__(self, screen_size):
        self.screen_size = screen_size

        #load images
        self.house_size = (400,267)
        self.eCooking = self.load_and_scale('Images/houses/eCooking.png')
        self.EV = self.load_and_scale('Images/houses/EV.png')
        self.EV_eCooking = self.load_and_scale('Images/houses/EV-eCooking.png')
        self.EV_HP = self.load_and_scale('Images/houses/EV-HP.png')
        self.EV_HP_eCooking = self.load_and_scale('Images/houses/EV-HP-eCooking.png')
        self.EV_HP_PV = self.load_and_scale('Images/houses/EV-HP-PV.png')
        self.EV_HP_PV_eCooking = self.load_and_scale('Images/houses/EV-HP-PV-eCooking.png')
        self.EV_PV = self.load_and_scale('Images/houses/EV-PV.png')
        self.EV_PV_eCooking = self.load_and_scale('Images/houses/EV-PV-eCooking.png')
        self.HP = self.load_and_scale('Images/houses/HP.png')
        self.HP_eCooking = self.load_and_scale('Images/houses/HP-eCooking.png')
        self.HP_PV = self.load_and_scale('Images/houses/HP-PV.png')
        self.HP_PV_eCooking = self.load_and_scale('Images/houses/HP-PV-eCooking.png')
        self.PV = self.load_and_scale('Images/houses/PV.png')
        self.PV_eCooking = self.load_and_scale('Images/houses/PV-eCooking.png')
        self.NONE = self.load_and_scale('Images/houses/NONE.png')
        
        self.start_pos = (screen_size[0]/2 - 300,screen_size[1]/2-85)
        # self.start_pos = (0,0)

        self.houses = self.LCT_percentages_houses([0, 0, 0, 0])

    def load_and_scale(self, image_path):
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, self.house_size)

    def draw(self, screen, LCT_percentages):
        self.houses = self.LCT_percentages_houses(LCT_percentages)
        self.draw_houses(screen, self.houses)

    def draw_houses(self,screen,houses):
        screen.blit(houses[0], (self.start_pos[0], self.start_pos[1]))
        screen.blit(houses[1], (self.start_pos[0]- self.house_size[0]/2 +5,self.start_pos[1] + self.house_size[1]/5 - 1))
        start_pos_2 = (self.start_pos[0] + 465,self.start_pos[1] + 22)
        screen.blit(houses[2], (start_pos_2[0],start_pos_2[1]))
        screen.blit(houses[3], (start_pos_2[0]- self.house_size[0]/2 +5,start_pos_2[1] + self.house_size[1]/5 - 1))
        screen.blit(houses[4], (start_pos_2[0]- 2*self.house_size[0]/2 +5,start_pos_2[1] + 2*self.house_size[1]/5 - 1))
        screen.blit(houses[5], (start_pos_2[0]- 3*self.house_size[0]/2 +5,start_pos_2[1] + 3*self.house_size[1]/5 - 1))
        start_pos_3 = (start_pos_2[0] + 465,start_pos_2[1] + 22)
        screen.blit(houses[6], (start_pos_3[0]- self.house_size[0]/2 +5,start_pos_3[1] + self.house_size[1]/5 - 1))
        screen.blit(houses[7], (start_pos_3[0]- 2*self.house_size[0]/2 +5,start_pos_3[1] + 2*self.house_size[1]/5 - 1))
        screen.blit(houses[8], (start_pos_3[0]- 3*self.house_size[0]/2 +5,start_pos_3[1] + 3*self.house_size[1]/5 - 1))
        screen.blit(houses[9], (start_pos_3[0]- 4*self.house_size[0]/2 +5,start_pos_3[1] + 4*self.house_size[1]/5 - 1))

    def LCT_percentages_houses(self, LCT_percentages):
        # Initialize house list
        house_types = []

        percentages = [int(10*LCT_percentages[0]),int(10*LCT_percentages[1]),int(10*LCT_percentages[2]),int(10*LCT_percentages[3])]

        # Total number of houses
        total_houses = 10

        # Calculate and place houses with all four LCTs first
        num_all_LCTs = min(percentages)
        for _ in range(num_all_LCTs):
            house_types.append(self.EV_HP_PV_eCooking)
        percentages = [p - num_all_LCTs for p in percentages]
        # Calculate and place houses for remaining combinations
        def add_houses(house_image, num_houses):
            for _ in range(num_houses):
                house_types.append(house_image)

        if sum(percentages) > 0:
            num_EV_HP_PV = min(percentages[0], percentages[1], percentages[3])
            add_houses(self.EV_HP_PV, num_EV_HP_PV)
            percentages[0] -= num_EV_HP_PV
            percentages[1] -= num_EV_HP_PV
            percentages[3] -= num_EV_HP_PV

            num_EV_HP_eCooking = min(percentages[0], percentages[1], percentages[2])
            add_houses(self.EV_HP_eCooking, num_EV_HP_eCooking)
            percentages[0] -= num_EV_HP_eCooking
            percentages[1] -= num_EV_HP_eCooking
            percentages[2] -= num_EV_HP_eCooking

            num_EV_PV_eCooking = min(percentages[0], percentages[2], percentages[3])
            add_houses(self.EV_PV_eCooking, num_EV_PV_eCooking)
            percentages[0] -= num_EV_PV_eCooking
            percentages[2] -= num_EV_PV_eCooking
            percentages[3] -= num_EV_PV_eCooking

            num_HP_PV_eCooking = min(percentages[1], percentages[2], percentages[3])
            add_houses(self.HP_PV_eCooking, num_HP_PV_eCooking)
            percentages[1] -= num_HP_PV_eCooking
            percentages[2] -= num_HP_PV_eCooking
            percentages[3] -= num_HP_PV_eCooking

            num_EV_HP = min(percentages[0], percentages[1])
            add_houses(self.EV_HP, num_EV_HP)
            percentages[0] -= num_EV_HP
            percentages[1] -= num_EV_HP

            num_EV_PV = min(percentages[0], percentages[3])
            add_houses(self.EV_PV, num_EV_PV)
            percentages[0] -= num_EV_PV
            percentages[3] -= num_EV_PV

            num_EV_eCooking = min(percentages[0], percentages[2])
            add_houses(self.EV_eCooking, num_EV_eCooking)
            percentages[0] -= num_EV_eCooking
            percentages[2] -= num_EV_eCooking

            num_HP_PV = min(percentages[1], percentages[3])
            add_houses(self.HP_PV, num_HP_PV)
            percentages[1] -= num_HP_PV
            percentages[3] -= num_HP_PV

            num_HP_eCooking = min(percentages[1], percentages[2])
            add_houses(self.HP_eCooking, num_HP_eCooking)
            percentages[1] -= num_HP_eCooking
            percentages[2] -= num_HP_eCooking

            num_PV_eCooking = min(percentages[2], percentages[3])
            add_houses(self.PV_eCooking, num_PV_eCooking)
            percentages[2] -= num_PV_eCooking
            percentages[3] -= num_PV_eCooking

            num_EV = percentages[0]
            add_houses(self.EV, num_EV)
            percentages[0] -= num_EV

            num_HP = percentages[1]
            add_houses(self.HP, num_HP)
            percentages[1] -= num_HP

            num_eCooking = percentages[2]
            add_houses(self.eCooking, num_eCooking)
            percentages[2] -= num_eCooking

            num_PV = percentages[3]
            add_houses(self.PV, num_PV)
            percentages[3] -= num_PV

        # Fill the rest with NONE
        while len(house_types) < total_houses:
            house_types.append(self.NONE)

        # Shuffle the house types to distribute them randomly
        #random.shuffle(house_types)
        return house_types