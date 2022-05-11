#!/bin/python3

import math
import pygame
import serial
import json


pygame.init()

width,height=900,600

win=pygame.display.set_mode((width,height))
fps=60
pygame.display.set_caption("json map maker")

white=(255,255,255)
black =(0,0,0)

gridlist=[]

collums=16
rows=15


gridw=width/collums
gridh=height/rows

senddict={}

def find_grid(collum,row):#gives the name of a grid piece given collum and row
    name=row*collums+collum
    if name>=0 and name<=collums*rows:
        return name

class piece:

    def __init__(self,name):
        self.name=name
        self.w=gridw#these 2 are kinda useless rn
        self.h=gridh
    
        self.row=math.ceil(name/collums)-1




        #self.collum=name-(self.row)*(collums)
        self.collum=name-(self.row)*(collums)-1

        #self.x=((collums - self.collum)*gridw)
        self.x=(self.collum*gridw)

        self.y=(gridh*self.row)
        self.state=False



    def render(self):
        rect=pygame.Rect(self.x,self.y,gridw,gridh)

        if self.state:

            pygame.draw.rect(win,black,rect)
        else:
            pygame.draw.rect(win,black,rect,1)



    def findclose(self):#left right up down
        #returns indexes of the grid spaces that on the left, right, above and below
        #
        left=   find_grid(self.collum-1,self.row)
        right=  find_grid(self.collum+1,self.row)
        up=     find_grid(self.collum,self.row-1)
        down=   find_grid(self.collum,self.row+1)
        
        return(left,right,up,down)
        #this might have a problem with giving numbers that are not existant but those numbers should be ignored


    def clicked(self,x,y):#be wary this worked really fast
        if x>=self.x and x<=self.x+self.w:  
            if y>=self.y and y<=self.y+self.h:
                return True
        return False

    def changestate(self):
        self.state= not self.state








def main():
    win.fill(white)
    run=True
    runval=1
    

    for i in range(collums*rows):
        gridlist.append(i)
        gridlist[i]=piece(i+1)


    while run:
        win.fill(white)

        for i in gridlist:
            i.render()
            


        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_s:
                    send=[]
                    for i in gridlist:
                        if i.state:
                            send.append(int(i.name))#change to json save file as

                    senddict[runval]=send
                    jsend=json.dumps(senddict)
                    
                    f=open("matrixanimastionmap"+".json","w")
                    f.write(jsend)
                    f.close()
                    runval=runval+1                    



            if event.type==pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                for i in gridlist:
                    if i.clicked(mx,my):
                        print(i.name)
                        #print(i.findclose())
                        i.changestate()
    pygame.quit()





if __name__=="__main__":
    main()
