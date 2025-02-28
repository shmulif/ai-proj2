#==============================
# Matthew Glennon, Shmuel Feld, Aban Khan, Sai Vemula, Jose Salgado, Camryn Keller
# CSC645: Computer Graphics
#   Fall 2024
# Description:
#   This program creates a fully interactive 3D room, with textured walls/floor/ceiling
#   The player may also interact with the lights, pool table, as well as the pair of dice
#   on the corner table
#   
#==============================
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from utils import Point
from camera import Camera
from materials import *
from components import *
from collision import Collision
from light import Light
import select
import sys
import re
import random

# Window settings
window_dimensions = (1200, 800)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Room dimensions
ROOM_WIDTH = 20.0
ROOM_HEIGHT = 15.0
ROOM_DEPTH = 20.0

# Camera settings
CAM_ANGLE = 60.0
CAM_NEAR = 0.01
CAM_FAR = 1000.0
INITIAL_EYE = Point(0, 5.67, 8)
INITIAL_LOOK_ANGLE = 0

# List for collision boxes
collisionList = []

# States for connect four
all_states = [
    [
        ['-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-']
    ]
]
current_state_index = 0




class Room:

    # pool shooting variables
    in_shooting_mode = False
    shooting_angle = 0

    # Animation frames
    global_frame = 0 # Used to keep track of time
    dice_frame = 0
    initial_dice_frame = 0
    hanging_light_frame = 0
    initial_hanging_light_frame = 0

    # animation booleans
    animate_dice = False
    animate_hanging_light = False

    # Other spotlight variables
    swing_factor = 0
    spot_light_is_enabled = False
    spotlight_state = {
            "current_intensity": 0.5,  # Default starting intensity
            "target_intensity": 0.5   # Default target intensity
        }
    
    # Picture boolean
    show_picture = False

    def __init__(self):
        pygame.init()
        pygame.display.set_mode(window_dimensions, pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()
        
        self.camera = Camera(CAM_ANGLE, window_dimensions[0]/window_dimensions[1], CAM_NEAR, CAM_FAR, 
                           INITIAL_EYE, INITIAL_LOOK_ANGLE)
        
        self.init_gl()
        
        # Light states
        self.light_states = {
            'red': True,
            'green': True,
            'blue': True,
            'spotlight': True,
            'lamp': True,
            'flashlight': True
        }
        
        self.running = True

    def should_we_show_picture(self):
        # Iterate through the light states
        for light_name, this_light_is_on in self.light_states.items(): 
            # Ignore the flashlight and check other lights
            if light_name != 'flashlight' and this_light_is_on:
                return False  # If any non-flashlight light is on, don't show the picture
        
        # If no non-flashlight lights are on, show the picture
        return True

    def init_gl(self):
        """Initialize OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glEnable(GL_TEXTURE_2D)
        
        # Set up basic lighting
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)
        glEnable(GL_LIGHT3) # Red and intially disabled
        glEnable(GL_LIGHT4) # Green and intially disabled
        glEnable(GL_LIGHT5) # Blue and intially disabled
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 100.0)
        

    def handle_input(self):
        global all_states, current_state_index
        """Handle keyboard and mouse input"""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.KEYDOWN:  # Listen for key presses
                if event.key == pygame.K_m:
                    if current_state_index < len(all_states) - 1:
                        current_state_index += 1
                        # print(current_state_index)

                elif event.key == pygame.K_b:
                    if current_state_index > 0:
                        current_state_index -= 1
                        # print(current_state_index)
            
        
                elif event.key == pygame.K_r: # Reset Camera to starting point
                    self.camera.eye.x = 0
                    self.camera.eye.y = 5.67
                    self.camera.eye.z = 8
                    # Reset collision point to match the camera's position
                    self.camera.collisionPoint.x = self.camera.eye.x
                    self.camera.collisionPoint.y = self.camera.eye.y
                    self.camera.collisionPoint.z = self.camera.eye.z
                elif event.key == pygame.K_t:  # Reset Vertical Camera position
                    self.camera.heightAngle = INITIAL_LOOK_ANGLE

                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    light_index = event.key - pygame.K_0
                    self.toggle_light(light_index)
                elif event.key == pygame.K_h: # Prints to console help message
                    Components.help_message()

        keys = pygame.key.get_pressed()
        moveBack = False
        if keys[pygame.K_w]:
            self.camera.slideCollision(0,0,-0.1) #First move collision box
            #Check and see if a collision occurs with objects, if so flag it
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            #Check and see if wall collision occurs, if so flag it
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True

            #On collision, move collider back onto the player, do not move forward
            if moveBack == True:
                self.camera.slideCollision(0,0,.1)
            else:
                self.camera.slide(0, 0, -0.1)

        if keys[pygame.K_s]:
            self.camera.slideCollision(0,0,0.1) #First move collision box
            #Check and see if a collision occurs with objects, if so flag it
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            #Check and see if wall collision occurs, if so flag it
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True

            #On collision, move collider back onto the player, do not move forward
            if moveBack == True:
                self.camera.slideCollision(0,0,-.1)
            else:
                self.camera.slide(0, 0, 0.1)
        if keys[pygame.K_a]:
            self.camera.slideCollision(-.1,0,0)
            #Check and see if a collision occurs with objects, if so flag it
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            #Check and see if wall collision occurs, if so flag it
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True

            #On collision, move collider back onto the player, do not move forward
            if moveBack == True:
                self.camera.slideCollision(.1,0,0)
            else:
                self.camera.slide(-.1, 0, 0)
        if keys[pygame.K_d]:
            
            self.camera.slideCollision(.1,0,0)
            #Check and see if a collision occurs with objects, if so flag it
            for i in range(len(collisionList)):
                if collisionList[i].pointInside(self.camera.collisionPoint):
                    moveBack = True
            #Check and see if wall collision occurs, if so flag it
            if self.camera.collisionPoint.x < .2 -ROOM_WIDTH/2 or self.camera.collisionPoint.x > -.2 + ROOM_WIDTH/2 or self.camera.collisionPoint.z < .2 -ROOM_DEPTH/2 or self.camera.collisionPoint.z > -.2 + ROOM_DEPTH/2:
                moveBack = True

            #On collision, move collider back onto the player, do not move forward
            if moveBack == True:
                self.camera.slideCollision(-.1,0,0)
            else:
                self.camera.slide(.1, 0, 0)
        #Camera turning functions!
        if keys[pygame.K_LEFT]:
            self.camera.turn(1)
        if keys[pygame.K_RIGHT]:
            self.camera.turn(-1) 
        if keys[pygame.K_DOWN]:
            self.camera.rise(-1)
        if keys[pygame.K_UP]:
            self.camera.rise(1)  

        #Pool table control functions 
        if keys[pygame.K_p]:
            if Room.toggleHold != True:
                Room.in_shooting_mode = not Room.in_shooting_mode
                Room.toggleHold = True
        else:
            Room.toggleHold = False
        if keys[pygame.K_j] and Room.in_shooting_mode:
            Room.shooting_angle += 1
        if keys[pygame.K_l] and Room.in_shooting_mode:
            Room.shooting_angle -= 1
        if keys[pygame.K_SPACE] and Room.in_shooting_mode:
            Room.in_shooting_mode = False
            Components.shoot_cue(Room.shooting_angle)
                 
        #Dice control key
        if keys[pygame.K_x]:
                Room.initial_dice_frame =  Room.global_frame
                Room.animate_dice = True
        #Hanging light control key
        if keys[pygame.K_c]:
            Room.animate_hanging_light = not Room.animate_hanging_light

    #Function sets the animation frames of the room for the dice and light
    def animate(self):

        Room.global_frame += 1

        if Room.animate_dice:
            Room.dice_frame += 1
            if Room.global_frame - Room.initial_dice_frame > 200:
                Room.animate_dice = False
        
        if Room.animate_hanging_light:
            Room.swing_factor = 8
            Room.hanging_light_frame += 1
        else:
            if 0 < Room.swing_factor:
                Room.hanging_light_frame += 1
                Room.swing_factor -= 0.03
            else:
                Room.hanging_light_frame = 0
                    
    #Light orientation method
    def setup_lights(self):

        # Extra light
        extra_light = Light(
                light_num=GL_LIGHT6,
                position=[6, 4, 6, 1],
                diffuse=[1.0, 1.0, 1.0, 1.0],
                specular=[1.0, 1.0, 1.0, 1.0]
            )
        extra_light.enable()
        # self.draw_light_indicator([6, 4, 6], [1.0, 1.0, 1.0]) 

        # Red Light
        if self.light_states['red']:
            red_light = Light(
                light_num=GL_LIGHT0,
                position=[-5, ROOM_HEIGHT - 0.1, -5, 1],
                diffuse=[1.0, 0.0, 0.0, 1.0],
                specular=[1.0, 0.0, 0.0, 1.0]
            )
            red_light.enable()
            self.draw_light_indicator([-5, ROOM_HEIGHT - 0.1, -5], [1.0, 0.0, 0.0])  # Red sphere
        else:
            glDisable(GL_LIGHT0)

        # Green Light
        if self.light_states['green']:
            green_light = Light(
                light_num=GL_LIGHT1,
                position=[5, ROOM_HEIGHT - 0.1, -5, 1],
                diffuse=[0.0, 1.0, 0.0, 1.0],
                specular=[0.0, 1.0, 0.0, 1.0]
            )
            green_light.enable()
            self.draw_light_indicator([5, ROOM_HEIGHT - 0.1, -5], [0.0, 1.0, 0.0])  # Green sphere
        else:
            glDisable(GL_LIGHT1)

        # Blue Light
        if self.light_states['blue']:
            blue_light = Light(
                light_num=GL_LIGHT2,
                position=[0, ROOM_HEIGHT - 0.1, 5, 1],
                diffuse=[0.0, 0.0, 1.0, 1.0],
                specular=[0.0, 0.0, 1.0, 1.0]
            )
            blue_light.enable()
            self.draw_light_indicator([0, ROOM_HEIGHT - 0.1, 5], [0.0, 0.0, 1.0])  # Blue sphere
        else:
            glDisable(GL_LIGHT2)

        # Spotlight
         # Spotlight
        if self.light_states['spotlight']:
            self.spot_light_is_enabled = True
        else:
            self.spot_light_is_enabled = False

        # Desk Lamp
        if self.light_states['lamp']:
            desk_lamp = Light(
                light_num=GL_LIGHT4,
                position=[-ROOM_WIDTH / 2 + 1.3, 5.25, -ROOM_DEPTH / 2 + 1.3, 1],
                diffuse=[0.75, 0.75, 0.75, 1.0],
                specular=[0.75, 0.75, 0.75, 1.0],
                attenuation={"constant": 1.0, "linear": 0.1, "quadratic": 0.0},
                spot_direction=[0, -1, 0],
                spot_cutoff=70.0,
                spot_exponent=1.0
            )
            desk_lamp.enable()
            self.draw_light_indicator([-ROOM_WIDTH / 2 + 1.3, 5.25, -ROOM_DEPTH / 2 + 1.3], [1.0, 1.0, 0.0])  # Yellow sphere
        else:
            glDisable(GL_LIGHT4)

        # Flashlight
        if self.light_states['flashlight']:
            light_num = GL_LIGHT5
            Light.place_flashlight(light_num)
        else:
            glDisable(GL_LIGHT5)


    #Draws the sphere which represents each light
    def draw_light_indicator(self, position, color):
        """
        Draw a self-illuminated sphere at the specified position.
        :param position: The [x, y, z] position of the sphere.
        :param color: The [r, g, b] color of the sphere.
        """
        glPushMatrix()
        glDisable(GL_LIGHTING)  # Disable lighting for the sphere
        glColor3f(*color)  # Set the color of the sphere
        glTranslatef(position[0], position[1], position[2])
        gluSphere(gluNewQuadric(), 0.2, 16, 16)  # Draw a small sphere
        glEnable(GL_LIGHTING)  # Re-enable lighting
        glPopMatrix()

    #Light toggling
    def toggle_light(self, index):
        """Toggle specific light based on index"""
        light_names = ['red', 'green', 'blue', 'spotlight', 'lamp', 'flashlight']
        if index < len(light_names):
            self.light_states[light_names[index]] = not self.light_states[light_names[index]]


    def draw_room(self):
        """Draw the room with textured walls, floor, and ceiling"""
        
        # Set the material to be combined with the textures
        Materials.set_material(GL_FRONT, Materials.BRIGHT_WHITE)
        
        # Floor with checkerboard texture (20 x 20)
        Textures.set_texture(Textures.checkerboard_floor_name)

        BasicShapes.draw_plane_with_grid(ROOM_WIDTH, ROOM_DEPTH, 30, 30)


        # Walls
        Textures.set_texture(Textures.wall_name)
        
        # Back wall
        glPushMatrix()
        glTranslate(0,ROOM_HEIGHT/2,ROOM_DEPTH/2) # Move back and up
        glRotate(270, 1,0,0)
        glRotate(180, 0,1,0)
        BasicShapes.draw_plane_with_grid(ROOM_DEPTH, ROOM_HEIGHT,30,30)
        glPopMatrix()

        # Front wall
        glPushMatrix()
        glTranslate(0,ROOM_HEIGHT/2,-ROOM_DEPTH/2) # Move forward and up
        glRotate(90,1,0,0)
        BasicShapes.draw_plane_with_grid(ROOM_DEPTH, ROOM_HEIGHT,30,30)
        glPopMatrix()

        # Right wall
        glPushMatrix()
        glRotate(90,0,1,0)
        glTranslate(0,ROOM_HEIGHT/2,ROOM_DEPTH/2)
        glRotate(270, 1,0,0)
        glRotate(180, 0,1,0)
        BasicShapes.draw_plane_with_grid(ROOM_DEPTH, ROOM_HEIGHT,30,30)
        glPopMatrix()


        # Left wall
        glPushMatrix()
        glRotate(90,0,1,0)
        glTranslate(0,ROOM_HEIGHT/2,-ROOM_DEPTH/2)
        glRotate(90,1,0,0)
        BasicShapes.draw_plane_with_grid(ROOM_DEPTH, ROOM_HEIGHT,30,30)
        glPopMatrix()

        # Ceiling
        glPushMatrix()
        glTranslate(0, ROOM_HEIGHT, 0) # Move up
        glRotate(180,0,0,1)
        BasicShapes.draw_plane_with_grid(ROOM_WIDTH, ROOM_DEPTH,30,30)
        glPopMatrix()

    def draw_components(self):
        global all_states, current_state_index

        Components.draw_table_with_trim()
        collisionList.append(Collision(8,4,0,0)) #Create collision box for pool table

        # Draw connect four
        glPushMatrix()  
        glTranslatef(0, 3, 0)  # Move up from the ground
        Components.draw_connect_four_scene(all_states[current_state_index])
        glPopMatrix()

        # Place the corner table in the bottom-left corner
        glPushMatrix()  # Save current transformation matrix
        glTranslatef(-ROOM_WIDTH/2 + 1.3, 0, -ROOM_DEPTH/2 + 1.3)  # Move to corner
        Components.draw_table_with_lamp(2, 2, Room.dice_frame)  # Draw table
        collisionList.append(Collision(2,2,-ROOM_WIDTH/2 +1.3,-ROOM_DEPTH/2 + 1.3)) #Create collision box for table
        glPopMatrix()  # Restore previous transformation matrix

        # Draw a ball around the top of the lamp
        glPushMatrix()  # Save current transformation matrix
        glTranslatef(0, ROOM_HEIGHT - 0.4, 0)  # Move to Center
        Materials.set_material(GL_FRONT_AND_BACK, Materials.RUBBER_BUMPER)
        BasicShapes.draw_sphere(0.2)
        glPopMatrix()  # Restore previous transformation matrix

        glPushMatrix()  # Save current transformation matrix
        glTranslatef(0 , ROOM_HEIGHT - 6, 0)  # Move to ceiling
        hanging_light_equation = Room.swing_factor * math.sin(0.03 * Room.hanging_light_frame)
        Components.draw_animated_hanging_spotlight(hanging_light_equation, self.spot_light_is_enabled, self.global_frame)
        glPopMatrix()  # Restore previous transformation matrix

        if self.show_picture or True:
            # Add a frame to the back wall
            glPushMatrix()
            glTranslatef(0, ROOM_HEIGHT / 2, -ROOM_DEPTH / 2 + 0.25)  # Center frame on the back wall and move out a little
            glRotatef(90, 0, 0, -1)  # Rotate 90 degrees clockwise around the Z-axis
            glTranslate(-1,0,0) # Move up
            glTranslate(0,3.5,0) # Move to the right
            Components.draw_framed_picture(3, 1.2, 3)  # Frame size: 3x3   
            glPopMatrix()



    def display(self):

        """Main display function"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        

        self.camera.setProjection()
        self.camera.placeCamera()
        
        self.setup_lights()
        self.show_picture = self.should_we_show_picture()
        self.animate()
        
        self.draw_room()
        self.draw_components()
        
        pygame.display.flip()

    def parse_turns(self, input_str):
        # Split the input string into turns based on 'Current turn' separator
        turns = input_str.split('Current turn:')
        
        board_list = []
        
        for turn in turns[1:]:  # Skip the first empty element due to split
            # Extract the board, which is between the 'Current turn' and the next
            # 'Current turn' or end of the string
            board_str = turn.strip().split('\n')[1:]  # Remove the "Current turn" label and empty line
            board = []

            for row in board_str:
                board.append([cell if cell != '-' else '-' for cell in row.split()])
            
            board_list.append(board)
        
        return board_list
    def parse_grids(self, input_text):
        global all_states  # Declare the use of the global array

        # Split input text into parts based on 'Current turn:' (indicating a new section/grid)
        grid_sections = re.split(r'Current turn:.*?Enter column \(1-7\):', input_text, flags=re.DOTALL)
        
        for section in grid_sections:
            # Process only the sections that have a valid grid (non-empty sections)
            if section.strip():
                grid_lines = []
                for line in section.split("\n"):
                    # Match lines that only contain valid grid characters
                    if re.match(r"^[-XO\s]+$", line):
                        grid_lines.append(line.strip())
                
                # Convert grid lines into a 2D array and append to global all_states array
                grid = [list(line.replace(" ", "")) for line in grid_lines]
                all_states.append(grid)  # Append each grid to the global all_states array

    def get_connect_four_one_time_input(self):
        global all_states, current_state_index

        # print(sys.argv[1])

        all_states = self.parse_turns(sys.argv[1])
        current_state_index = 0

    def get_connect_four_input(self):
        global all_states, current_state_index

        input_buffer = ""  # Initialize a buffer to store the entire input

        # print("Waiting for input...")

        # Check if input is available from stdin
        readable, _, _ = select.select([sys.stdin], [], [], 0)  # Non-blocking check

        if readable:
            while True:
                chunk = sys.stdin.read(1)  # Read 1 byte at a time
                if chunk == "":  # End of input stream (EOF)
                    break
                input_buffer += chunk  # Accumulate input into buffer

                # Check if the delimiter is encountered
                if "Enter column (1-7):" or "wins!" in input_buffer:
                    break

            # Now we have the complete input in input_buffer
            if input_buffer:
                print(f"Received full input: \n{input_buffer}")
                self.parse_grids(input_buffer)
                # self.process_game_input(input_buffer)
            else:
                print("Received empty input.")

                # all_states = self.parse_turns()
                # current_state_index = 0

        

    def run(self):
        Components.initialize()
        """Set up Pool Balls"""
        Components.config_balls()
        """Main game loop""" 

        # self.get_connect_four_input()

        while self.running:
            self.handle_input()
            self.get_connect_four_input()
            self.display()
            self.clock.tick(FPS)


def main():
    room = Room()
    room.run()
    pygame.quit()


if __name__ == "__main__":
    main()