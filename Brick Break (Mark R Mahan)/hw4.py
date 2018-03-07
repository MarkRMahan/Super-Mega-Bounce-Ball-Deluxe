"""
Author: Mark R. Mahan
Trace folder: Mahan07//HW//hw4
File name: hw4.py
INSTRUCTIONS:
    Win the game by getting the ball to destroy all 40 blocks on the screen, lose the game by letting the ball hit the bottom of the canvas until all 5 lives are depleted
    Use the left and right arrow keys to move the paddle left and right (Just pressing once is the only requirement)
    Use the down arrow key in order to stop the paddle from moving
    Once the game has been won or lost, use the 'e' key to exit the game
    
DESCRIPTION:
A Paddle and Bouncing Ball Game that includes features such as:
 1) Unique pixel images used for the ball, the blocks, the losing image, and the winning image
 2) A slightly different canvas for the bouncing ball and paddle because I felt as though this new canvas would be more aesthetically pleasing to the player
 3) A bouncing ball that bounces off the canvas's borders, the 40 blocks and all 4 of their corners, and the paddle's top and its left and right top corners
   (The ball is intended to go through the paddle if it hits the canvas's bottom/is traveling north
 4) Everytime the ball bounces, there is a chance that the ball's speed/angle will change
 5) A smaller paddle to move around since a bigger, blocky paddle in a smaller canvas would not look as good
    (Move the paddle using the left and right arrow keys, stop it using the down arrow key)
 6) Everytime the paddle is allowed to move against a canvas wall, it decreases in size unless the paddle is 30 pixels wide
 7) If the paddle is less than its original size (80 pixels wide), it increases in size if the ball bounces off the paddle
 8) A white line/box under the paddle to show it's path of movement
 9) Everytime the game is started, the 40 blocks' colors will be randomized
 10) An exit button, assigned to 'e', that will close the game once the player has won/lost
 11) Upon winning, the ball is reset to its original location and a "You Win!" image is displayed
 12) Upon losing, the ball is reset to its original location and a "Game Over" image is displayed
 13) Lives are displayed at the top of the screen and are depleted when the ball hits the bottom of the canvas

I hope you enjoy the game!
"""

from tkinter import *
from tkinter import font
import random

class BallGame(Frame):
    '''Class that creates a bouncing ball game'''
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Super Mega Ball Bounce Deluxe") #Creates unique title
        self.grid()
        
        
        # Canvas
        self.height = 500 #Canvas Height
        self.width = 600 #Canvas Width
        self.canvas = Canvas(self, height = 500, width = 600, bg = "gray")
        self.canvas.grid(row = 1, column = 0)
        
        
        # Ball Category
        self.diameter = 20 #Ball diameter
        self.ball_top_L = 10 #Tracks top-left of the ball (X-axis)
        self.ball_top_R = self.ball_top_L + 20 #Tracks top-right (X-axis)
        self.ball_bot_R = 150 #Tracks bot-right (Y-axis)
        self.ball_mid = 20 #Tracks middle of the ball (X-axis)
        self.ball_mid_Y = 140 #Tracks the middle using Y-axis
        self.h_direction = "east" #Ball starts out going east
        self.v_direction = "south" #Ball starts out going south
        self.bImage = PhotoImage(file = "game_ball.jpg") #Ball Image
        self.bImage = self.bImage.subsample(15, 15) #Uses only every Xth and Yth pixel of the Ball Image
        self.canvas.create_image(self.ball_top_L, self.ball_bot_R - 20, #The Ball
                                 image = self.bImage,
                                 anchor = "nw", tags = "8bit")
        
        
        # Coordinates/Speed
        self.dx = 1 #Determines pixels per movement (X-axis)
        self.dy = 1 #Determines pixels per movement (Y-axis)
        self.x_cord = 50 #X coordinate for the blocks
        self.y_cord = 10 #Y coordinate for the blocks
        
        
        # Lives/Game_Over/Game_Options
        self.Won = False
        self.Life_num = 5 #Number of lives
        self.L_font = font.Font(family = "Impact", size = 20) #Font used for the Lives
        self.lives = Label(self, font = self.L_font, #Displays lives
                           text = "Lives: " + str(self.Life_num))
        
        self.lives.grid(row = 0, column = 0)
        self.Game_Over = PhotoImage(file = "game_over.jpg") #Game over image
        self.You_Win = PhotoImage(file = "you_win.jpg") #"You win" image
        self.canvas.bind("<KeyPress-e>", self.Exit) #Exits button for when the game is won or lost
        
        
        # Paddle Category
        self.pad_topL = 160 #Tracks paddle's leftside
        self.pad_botR = 240 #Tracks paddle's rightside
        self.pad_height = 115 #The height of the paddle + the 105 pixels inbetween the paddle and bottom screen
        self.P = "" #Used for paddle movement and lack thereof
        self.paddle_line1 = 387 #Top of the paddle's travel line
        self.paddle_line2 = 393 #Bottom of the paddle's travel line
        self.canvas.create_rectangle(0, self.paddle_line1, #Paddle line (White line under paddle)
                                     600, self.paddle_line2,
                                     fill = "white")
        self.canvas.bind("<KeyPress-Left>", self.MovePL) #Button to start left movement
        self.canvas.bind("<KeyPress-Right>", self.MovePR) #Button to start right movement
        self.canvas.bind("<KeyPress-Down>", self.Stop) #Stops the paddle
        self.canvas.focus_set()
        self.decrease = 0 #Used when paddle is moving left or right against a wall
        paddle = self.canvas.create_rectangle( #The Paddle (80 pixels wide)
            self.pad_topL, 385, self.pad_botR,
            395, tags = "paddle", fill = "black")
        
        
        # Blocks Category
        # These are all the blocks used and all are subsampled in order to fit the screen
        self.blue = PhotoImage(file = "Blocks\\blue.jpg")
        self.blue = self.blue.subsample(5,5)
        self.green = PhotoImage(file = "Blocks\\green.jpg")
        self.green = self.green.subsample(5,5)
        self.orange = PhotoImage(file = "Blocks\\orange.jpg")
        self.orange = self.orange.subsample(5,5)
        self.pink = PhotoImage(file = "Blocks\\pink.jpg")
        self.pink = self.pink.subsample(5,5)
        self.purple = PhotoImage(file = "Blocks\\purple.jpg")
        self.purple = self.purple.subsample(5,5)
        self.red = PhotoImage(file = "Blocks\\red.jpg")
        self.red = self.red.subsample(5,5)
        self.yellow = PhotoImage(file = "Blocks\\yellow.jpg")
        self.yellow = self.yellow.subsample(5,5)
        self.color_list = [self.green, self.orange, self.pink, self.purple,
                           self.red, self.yellow, self.blue] #A list of the colored blocks
        self.block_list = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #List of blocks 1-40 in which the "block" will be set to 0 if the block is destroyed
                           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        
 
        self.Create_Lvl1()#Creates lvl 1
        self.Bounce()#Starts the ball
        
        
    def Bounce(self):
        while True:
            if self.GameWon():#Checks if you have won the game
                break
            self.Lvl1()#Allows the ball to hit the blocks
            top_pad = self.height - self.pad_height + 1
            self.MovePaddle() # Checks to see if the paddle needs moving
            
            if self.h_direction == "east": #Going East
                # Uses dx to keep the variables tracking the ball
                self.ball_top_L += self.dx
                self.ball_top_R += self.dx
                self.ball_mid += self.dx
                if self.ball_top_L >= self.width - self.diameter + 1: #Checks if the ball has reached the right side of the canvas (The +1 is just to make the ball bounce better)
                    self.ball_top_L = self.width - self.diameter + 1
                    self.ChangeDirection_H() #Changes the h_direction to west
                    self.dx = self.SpeedChange() #Changes the horizontal speed if the value returned is different than the current speed
                
            else: #Going West
                # Tracks the ball using dx
                self.ball_top_L -= self.dx
                self.ball_top_R -= self.dx
                self.ball_mid -= self.dx
                if self.ball_top_L <= 0: #Checks if the ball has reached the left side of the canvas
                    self.ball_top_L = 0
                    self.ChangeDirection_H() #Changes h_direction to east
                    self.dx = self.SpeedChange() #Changes X's speed
                
            if self.v_direction == "south": #Going South
                # Tracks the ball using dy
                self.ball_bot_R += self.dy
                self.ball_mid_Y += self.dy
                if self.ball_bot_R >= self.height: #Checks if the ball has hit the bottom of the canvas
                    self.ball_bot_R = self.height
                    self.ChangeDirection_V() #Changes the v_direction to north
                    self.dy = self.SpeedChange() #Changes the 
                    if self.LifeLost() == True: #Takes lives away and ends the game if 0 lives
                        break #Stops the game
                    
                if self.ball_bot_R >= top_pad: #Checks if the ball has hit the paddle
                    if self.ball_bot_R <= self.paddle_line2 and self.paddle_line1 <= self.ball_bot_R: #Makes sure the ball won't bounce strangely under the paddle
                        
                        if self.pad_topL <= self.ball_top_R and self.ball_top_R <= self.pad_topL + 10 \
                           and self.h_direction == "east" or self.pad_botR - 10 <= self.ball_top_L and \
                           self.ball_top_L <= self.pad_botR and self.h_direction == "west": #Checks if the ball has reached the top left or top right corner of the paddle
                            self.ChangeDirection_H() #Changes the h_direction
                            
                        if self.pad_topL < self.ball_top_L and self.ball_top_L < self.pad_botR or \
                           self.pad_topL < self.ball_top_R and self.ball_top_R < self.pad_botR or \
                           self.pad_topL <= self.ball_mid and self.ball_mid <= self.pad_botR: #Checks if the ball has hit the paddle
                            self.ball_bot_R = top_pad
                            self.ChangeDirection_V() #Changes v_direction
                            self.Increase() #Increases the paddle size if the paddle has decreased in size from it's original length
                            self.dy = self.SpeedChange() #Changes vertical speed
                
            else: #Going North
                # Tracks the ball using dy
                self.ball_bot_R -= self.dy
                self.ball_mid_Y -= self.dy
                if self.ball_bot_R <= self.diameter: #Checks if the ball has reached the top of the canvas
                    self.ball_bot_R = self.diameter + 1
                    self.ChangeDirection_V() #Changes v_direction to south
                    self.dy = self.SpeedChange() #Changes Y's speed
                    
            self.Remake_Ball() #Recreates the ball using new coordinates
            self.canvas.after(6) #Delays the next loop for 6 milliseconds
            self.canvas.update() #Updates the canvas
            

    def Remake_Ball(self):
        '''Remakes the ball at the new coordinates'''
        self.canvas.delete("8bit") #Deletes the old ball image
        self.canvas.create_image(self.ball_top_L, self.ball_bot_R - 20, #The Ball
                                 image = self.bImage,
                                 anchor = "nw", tags = "8bit")

    def Create_Lvl1(self):
        '''Creates the 4 rows of 10 blocks'''
        block_num = 0
        for row in range(4): #Used to make 4 rows
            self.y_cord += 25 #Moves the blocks down another row
            for i in range(2):#Loops to create 5 blocks twice to make 1 row
                random.shuffle(self.color_list) #Shuffles the colored blocks
                color = 0
                for block in self.color_list: #Creates a row of 5 colored blocks from the shuffled color_list
                    block_num += 1 #Allows there to be 40 unique blocks with different tags
                    new_block = self.canvas.create_image(self.x_cord, #Makes the new block
                                            self.y_cord,
                                            image = self.color_list[color],
                                            anchor = "nw",
                                            tags = "block" + str(block_num))
                    self.x_cord += 50 #Changes the coordinate so that the next time the ball is made it'll be to the right of the previous block
                    color += 1
                    if self.x_cord == 550: #Stops the loop once the row has 10 blocks
                        break
            self.x_cord = 50 #Resets to create lower row of blocks
        

    def Block_Bounce(self, block_num, x1, x2, x3, x4, x5, x6):
        '''Allows the interaction between the ball and the block'''
        #Block_num is the number that was assigned to the block
        # (x1,x2) X-coordinates left of the block  |  (x3,x4) X-coordinates on which the block lies upon  |  (x5,x6) X-coordinates right of the block
        if self.block_list[block_num - 1] == 1: #Checks if the block is "deleted" (I just set the value to 0 to "delete" it)
            pos = self.canvas.coords("block" + str(block_num)) #Used to refer to the block's positioning (Anchor in the top left)
            
            if x1 <= self.ball_mid and self.ball_mid <= x2: #Left of the block
                if self.ball_top_L >= pos[0] - self.diameter and self.ball_mid_Y <= \
                   pos[1] + 30 and self.ball_mid_Y >= pos[1]: #Checks if the ball has touched the left side of the block
                    self.ball_top_L = pos[0] - self.diameter
                    self.block_list[block_num - 1] = 0 #Sets the block's value in block_list to 0 which means the block is deleted
                    self.h_direction = "west"
                    self.canvas.delete("block" + str(block_num)) #Deletes the block
                if self.ball_bot_R >= pos[1] and self.ball_bot_R < pos[1]+ 12:
                    if self.ball_top_L >= pos[0] - self.diameter and \
                        self.ball_top_L < pos[0] - 10: #Bounces back if the ball hits the top left corner
                        self.block_list[block_num - 1] = 0
                        self.h_direction = "west"
                        self.v_direction = "north"
                        self.canvas.delete("block" + str(block_num))
                if self.ball_bot_R <= pos[1] + 45 and self.ball_bot_R > pos[1] + 35:
                    if self.ball_top_L >= pos[0] - self.diameter and \
                        self.ball_top_L < pos[0] - 10: #Bounces back if the ball hits the bot left corner
                        self.block_list[block_num - 1] = 0
                        self.h_direction = "west"
                        self.v_direction = "south"
                        self.canvas.delete("block" + str(block_num))
                        
            if x3 <= self.ball_mid and self.ball_mid <= x4: #Ball is under/over the Column of the block
                if self.ball_bot_R >= pos[1] and self.ball_bot_R < pos[1] + 12: #Checks if the ball hit the top of the block
                    self.ball_bot_R = pos[1]
                    self.block_list[block_num - 1] = 0 #Sets the block's value in block_list to 0 which means the block is deleted
                    self.v_direction = "north"
                    self.canvas.delete("block" + str(block_num)) #Deletes the block
                if self.ball_bot_R <= pos[1] + 45 and self.ball_bot_R > pos[1] + 40: #Checks if the ball hit the bottom of the block
                    self.ball_bot_R = pos[1] + 45
                    self.block_list[block_num - 1] = 0
                    self.v_direction = "south"
                    self.canvas.delete("block" + str(block_num))
                    
            if x5 <= self.ball_mid and self.ball_mid <= x6: #Right of the block
                if self.ball_top_L <= pos[0] + 50 and self.ball_mid_Y <= \
                   pos[1] + 30 and self.ball_mid_Y >= pos[1]: #Checks if the ball has hit the right side of the block
                    self.ball_top_L = pos[0] + 50
                    self.block_list[block_num - 1] = 0 #Sets the block's value in block_list to 0 which means the block is deleted
                    self.h_direction = "east"
                    self.canvas.delete("block" + str(block_num)) #Deletes the block
                if self.ball_bot_R >= pos[1] and self.ball_bot_R < pos[1]+ 12:
                    if self.ball_top_L >= pos[0] + 50 and \
                        self.ball_top_L < pos[0] + 40: #Bounces back if it hits the top right corner
                        self.block_list[block_num - 1] = 0
                        self.h_direction = "east"
                        self.v_direction = "north"
                        self.canvas.delete("block" + str(block_num))
                if self.ball_bot_R <= pos[1] + 45 and self.ball_bot_R > pos[1] + 35:
                    if self.ball_top_L >= pos[0] + 50 and \
                        self.ball_top_L < pos[0] + 40: #Bounces back from the bot right corner
                        self.block_list[block_num - 1] = 0
                        self.h_direction = "east"
                        self.v_direction = "south"
                        self.canvas.delete("block" + str(block_num))
                        
                    
    def Lvl1(self):
        '''Sets how the ball will interact with each block'''
        #Row 1 of blocks
        self.Block_Bounce(1, 0, 49, 50, 99, 100, 149)
        self.Block_Bounce(2, 50, 99, 100, 149, 150, 199)
        self.Block_Bounce(3, 100, 149, 150, 199, 200, 249)
        self.Block_Bounce(4, 150, 199, 200, 249, 250, 299)
        self.Block_Bounce(5, 200, 249, 250, 299, 300, 349)
        self.Block_Bounce(6, 250, 299, 300, 349, 350, 399)
        self.Block_Bounce(7, 300, 349, 350, 399, 400, 449)
        self.Block_Bounce(8, 350, 399, 400, 449, 450, 499)
        self.Block_Bounce(9, 400, 449, 450, 499, 500, 549)
        self.Block_Bounce(10, 450, 499, 500, 549, 550, 599)
        #Row 2 of blocks
        self.Block_Bounce(11, 0, 49, 50, 99, 100, 149)
        self.Block_Bounce(12, 50, 99, 100, 149, 150, 199)
        self.Block_Bounce(13, 100, 149, 150, 199, 200, 249)
        self.Block_Bounce(14, 150, 199, 200, 249, 250, 299)
        self.Block_Bounce(15, 200, 249, 250, 299, 300, 349)
        self.Block_Bounce(16, 250, 299, 300, 349, 350, 399)
        self.Block_Bounce(17, 300, 349, 350, 399, 400, 449)
        self.Block_Bounce(18, 350, 399, 400, 449, 450, 499)
        self.Block_Bounce(19, 400, 449, 450, 499, 500, 549)
        self.Block_Bounce(20, 450, 499, 500, 549, 550, 599)
        #Row 3 of blocks
        self.Block_Bounce(21, 0, 49, 50, 99, 100, 149)
        self.Block_Bounce(22, 50, 99, 100, 149, 150, 199)
        self.Block_Bounce(23, 100, 149, 150, 199, 200, 249)
        self.Block_Bounce(24, 150, 199, 200, 249, 250, 299)
        self.Block_Bounce(25, 200, 249, 250, 299, 300, 349)
        self.Block_Bounce(26, 250, 299, 300, 349, 350, 399)
        self.Block_Bounce(27, 300, 349, 350, 399, 400, 449)
        self.Block_Bounce(28, 350, 399, 400, 449, 450, 499)
        self.Block_Bounce(29, 400, 449, 450, 499, 500, 549)
        self.Block_Bounce(30, 450, 499, 500, 549, 550, 599)
        #Row 4 of blocks
        self.Block_Bounce(31, 0, 49, 50, 99, 100, 149)
        self.Block_Bounce(32, 50, 99, 100, 149, 150, 199)
        self.Block_Bounce(33, 100, 149, 150, 199, 200, 249)
        self.Block_Bounce(34, 150, 199, 200, 249, 250, 299)
        self.Block_Bounce(35, 200, 249, 250, 299, 300, 349)
        self.Block_Bounce(36, 250, 299, 300, 349, 350, 399)
        self.Block_Bounce(37, 300, 349, 350, 399, 400, 449)
        self.Block_Bounce(38, 350, 399, 400, 449, 450, 499)
        self.Block_Bounce(39, 400, 449, 450, 499, 500, 549)
        self.Block_Bounce(40, 450, 499, 500, 549, 550, 599)
        
    def ChangeDirection_H(self): #Changes the h_direction when called
        if self.h_direction == "east":
            self.h_direction = "west"
        else:
            self.h_direction = "east"

    def ChangeDirection_V(self): #Changes the v_direction when called
        if self.v_direction == "south":
            self.v_direction = "north"
        else:
            self.v_direction = "south"

    def SpeedChange(self): #Used to change the speed of dx or dy
        speeds = [1, 2]
        random.shuffle(speeds)
        new_speed = speeds.pop()
        return new_speed

    def Increase(self): #Increases the size of the paddle if the paddle's size has decreased
        if self.pad_botR - self.pad_topL < 80:
            self.decrease -= 5 #Makes sure that if the paddle has increased, it won't increase more if it touches the left or right of the screen
            self.canvas.delete("paddle")
            self.pad_topL -= 5
            self.pad_botR += 5
            paddle = self.canvas.create_rectangle( #Recreates the increased paddle
                    self.pad_topL, 385, self.pad_botR,
                    395, tags = "paddle", fill = "black")
            
    def Exit(self, event): #Allows for the exitting of the game if the game is won or lost
        if self.Life_num == 0 or self.Won: #Checks if the player has won or lost
            self.master.destroy()
        
    def MovePaddle(self):
        '''Moves the paddle left or right depending on self.P'''
        if self.P == "Left":
            self.canvas.delete("paddle")
            self.pad_topL -= 3
            self.pad_botR -= 3
            if self.pad_topL <= 0: #Checks if the paddle is at the canvas's left
                self.pad_topL = 0
                self.pad_botR = 80 - self.decrease #Decreases the paddle's right side value
                if self.decrease <= 50: #Keeps the paddle to be at least 30 pixels
                    self.decrease += 1
            paddle = self.canvas.create_rectangle( #Recreates the new paddle
                    self.pad_topL, 385, self.pad_botR,
                    395, tags = "paddle", fill = "black")
            
        if self.P == "Right":
            self.canvas.delete("paddle")
            self.pad_topL += 3
            self.pad_botR += 3
            if self.pad_botR >= self.width:#Checks if the paddle is at the canvas's right
                self.pad_botR = self.width
                self.pad_topL = self.width - 80 + self.decrease #Decreases the paddle's left side value
                if self.decrease <= 50: #Keeps the paddle to be at least 30 pixels
                    self.decrease += 1
            paddle = self.canvas.create_rectangle( #Recreates the new paddle
                    self.pad_topL, 385, self.pad_botR,
                    395, tags = "paddle", fill = "black")

    def Stop(self, event):
        '''Changes self.P in order to stop the paddle in place'''
        self.P = ""

    def MovePL(self, event):
        '''Changes self.P to move the paddle left'''
        self.P = "Left"

    def MovePR(self, event):
        '''Changes self.P to move the paddle right'''
        self.P = "Right"

    def GameWon(self):
        result = 0
        for block in self.block_list:
            result += block #Adds the value's in block_list to result
        if result == 0: #Checks if result was 0 due to there being no 1 values in block_list
            self.Won = True
            self.ball_top_L = 10
            self.ball_bot_R = 150
            self.Remake_Ball() #Places the ball back in its starting position
            self.canvas.create_image(110, 300, image = self.You_Win, #Creates the winning image
                                 anchor = "nw", tags = "Won")
        return self.Won
        

    def LifeLost(self):
        game_over = False
        self.Life_num -= 1 #Takes one life away
        self.lives = Label(self, font = self.L_font, text = "Lives: " + str(self.Life_num)) #Redisplays lives
        self.lives.grid(row = 0, column = 0)
        if self.Life_num == 0: #Checks if there is 0 lives remaining
            game_over = True
            self.ball_top_L = 10
            self.ball_bot_R = 150
            self.Remake_Ball() #Places the ball back in its starting position
            self.canvas.create_image(100, 300, image = self.Game_Over, #Creates the losing image
                                 anchor = "nw", tags = "Over")
        return game_over

    
        
                
def main():
    BallGame().mainloop() #Begins the game

main()
