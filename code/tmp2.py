import time
import os
import pickle
import numpy as np
import csv
import random
"""
The template of the script for the machine learning process in game pingpong
"""
filename = os.path.abspath('final_KNNP2.sav')
model = pickle.load(open(filename, 'rb'))

class MLPlay:
    def __init__(self, side):
        """
        Constructor
        @param side A string "1P" or "2P" indicates that the MLPlay is used by 
               which side.
        """
        self.ball_served = False
        self.side = "2P"
        self.ServePosition = random.randrange(20,180, 5) #亂數5的倍數 發球座標
        
    def update(self, scene_info):
        Mode = "KNN" #KNN or RULE

        # if Mode == "RULE":
        #     # Make the caller to invoke reset() for the next round.
        #     #print(scene_info)
        #     if scene_info["status"] != "GAME_ALIVE":
        #         return "RESET"

        #     if not self.ball_served:
        #         self.ball_served = True
        #         return "SERVE_TO_LEFT"
        #     else: 
        #         #print(scene_info)
        #         BallCoordinate_Now = scene_info["ball"]
        #         ball_speed = scene_info["ball_speed"]
        #         BallCoordinate_Last = (BallCoordinate_Now[0] + ball_speed[0] , BallCoordinate_Now[1] + ball_speed[1])
        #         PlatformX = scene_info["platform_2P"][0] + 20
        #         # PlatformY = scene_info["platform_2P"][1] + 20
        #         # PlatformX_1P = scene_info["platform_1P"][0] + 20
        #         # PlatformY_1P = scene_info["platform_1P"][1] + 20
        #         # Frame = scene_info["frame"]
        #         aid = 0

        #         if BallCoordinate_Now[0] - BallCoordinate_Last[0] != 0:
        #             aid = BallCoordinate_Now[0] + ((BallCoordinate_Now[1] - 80) / ball_speed[1] * ball_speed[0] * -1)

        #         if aid < 0:
        #             aid = -aid
        #         elif aid > 195:
        #             aid = aid - 195
        #             aid = 195 - aid

        #         # CSV_Read_2P.doWrite(BallCoordinate_Now[0], BallCoordinate_Now[1], m, ball_speed[0], ball_speed[1], PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM)
        #         # # ball_speed[1] > 0 up    ball_speed[1] < 0 down up
        #         if ball_speed[1] < 0 and BallCoordinate_Now[1] <=80+abs(ball_speed[0]):
        #             if ball_speed[0]>0:
        #                 return "MOVE_RIGHT"
        #             else:
        #                 return "MOVE_LEFT"

        #         elif ball_speed[1] < 0 and PlatformX > (aid//5)*5 :
        #             return "MOVE_LEFT"
        #         elif ball_speed[1] < 0 and PlatformX < (aid//5)*5 :
        #             return "MOVE_RIGHT"

        #         elif ball_speed[1] > 0 and PlatformX < 100 :
        #             return "MOVE_RIGHT"

        #         elif ball_speed[1] > 0 and PlatformX > 100 :
        #             return "MOVE_LEFT"
                    
        #         elif ball_speed[1] > 0 and PlatformX == 100 :
        #             return "NONE"
        #         else :
        #             return "NONE"

        if Mode == "KNN":
            
            if scene_info["status"] != "GAME_ALIVE":
                return "RESET"
                
            if not self.ball_served:
                self.ball_served = True
                return "SERVE_TO_LEFT"
            else:
                BallCoordinate_Now = scene_info["ball"]
                ball_speed = scene_info["ball_speed"]
                PlatformX_2P = scene_info["platform_2P"][0] + 20
                PlatformY_2P = scene_info["platform_2P"][1] + 20
                # PlatformX_1P = scene_info["platform_1P"][0] + 20
                # PlatformY_1P = scene_info["platform_1P"][1] + 20             

                input = []
                inp_temp = np.array([PlatformX_2P, PlatformY_2P, BallCoordinate_Now[0], BallCoordinate_Now[1], ball_speed[0], ball_speed[1]])

                input = inp_temp[np.newaxis, :]
                   
                move = model.predict(input)
                # print("input>>> ", move)
                if move < 0:
                    return "MOVE_LEFT"
                elif move > 0:
                    return "MOVE_RIGHT"
                else:
                    return "None"

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False