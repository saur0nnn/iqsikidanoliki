import pygame
import time
from pygame.locals import *
from sys import exit
import math
from collections import defaultdict

#tamashis fps
FPS=60

#feris kodebi
black=(0,0,0)
white = (255,255,255)
blue=(0,0,200)
red=(200,0,0)
green=(0,200,0)

cross=1
circle=2
empty=0

computer=1
human=2

class Player:
    '''playerebis class'''

    def __init__(self,type,sign,name):
        self.type=type
        self.sign=sign
        self.name = name

    def SetBoard(self,board):
        '''dafas aketebs sadac playeri tamashobs'''
        self.board=board

    def GetMove(self):
        pass

    #mausis click
    def MouseClick(self,cell):
        pass

    def OppositeSign(self,sign):
        '''mowinaagmdegis figuras achvenebs'''
        if sign == circle:
            return cross
        return circle

#adamianis class
class HumanPlayer(Player):
    '''motamashis class'''
    
    def __init__(self,sign,name):
        super().__init__(human,sign,name)#adamiani
        self.lastmove=-1

    def GetMove(self):
        '''egreve abrunebs motamashis sawinaagmdegod svlas'''
        if(self.lastmove != -1):
            move=self.lastmove
            self.lastmove=-1
            return move

    def MouseClick(self,cell):
        '''playeris dadebul figuris sawinaagmdegod tamashobs'''
        
        if not cell in self.board.moves:
            self.lastmove=cell


class ComputerPlayer(Player):
    '''botis class'''
    
    def __init__(self,sign,name):
        super().__init__(computer,sign,name)#bot
        self.lastmove=-1

    def GetMove(self):
        '''shemdeg svlas axorcielebs boti'''
        self.maxdepth = 100
        self.loop = 0
        val,move = self.MaxValue(-9,9)
        return move

    def GetScore(self):
        '''tamashis dasrulebis da "scoreboard" is funqcia'''
        if self.board.Draw():
            return 0
        elif self.board.GetWinner() == self.sign:
            return 1
        return -1 #meore motamashem moigo
    
    def MaxValue(self,alpha,beta):
        '''svlebis max raodenoba'''
        maxpos = None
        maxval = -9

        for move in self.board.getFreePositions():
            self.loop+=1
            self.board.Move(move,self.sign)

            if self.board.GameOver():
                newval = self.GetScore()
            else:
                newval,movepos = self.MinValue(alpha,beta)

            self.board.UndoMove()

            if newval > beta:
                return newval,move
            if newval > alpha:
                alpha = newval

            if newval > maxval:
                maxval = newval
                maxpos = move
            if newval == 1:
                break;

        return maxval,maxpos
    
    def MinValue(self,alpha,beta):
        '''minimaluri svlebis raodenoba'''
        minpos = None
        minval = 9

        for move in self.board.getFreePositions():
            self.loop+=1
            self.board.Move(move,self.OppositeSign(self.sign))

            if self.board.GameOver():
                newval = self.GetScore()
            else:
                newval,movepos = self.MaxValue(alpha,beta)

            self.board.UndoMove()

            if newval < alpha:
                return newval,move
            if newval < beta:
                beta = newval

            if newval < minval:
                minval = newval
                minpos = move
            if newval == -1:
                break;

        return minval,minpos

class BoardAnalyzer:
    '''dafis class'''

    possiblecells = [ (a,b) for a in range(0,3) for b in range(0,3)]
    alllines=[[(a,b) for a in range(0,3)]  for b in range(0,3)]+[[(b,a) for a in range(0,3)]  for b in range(0,3)]+[[(0,0),(1,1),(2,2)],[(0,2),(1,1),(2,0)]]

    def __init__(self):
        self.moves=[] #inaxavs svlebs
        self.gameover=False
        self.draw=False
        self.board=defaultdict(lambda:empty) #carieli dafa

    def getFreePositions(self):
        '''nebismier players sheudzlia gaaketos svla cariel grafashi'''
        return [x for x in self.possiblecells if not x in self.moves]

    def Move(self,position,symbol):
        '''grafashi dasmuli simbolo'''
        #tu grafa carielia sheudzlia dasvas simbolo
        if self.board[position] != empty:
            return False
        self.board[position]=symbol
        self.moves.append(position)
        self.CheckGameOver()
        return True
    
    def UndoMove(self):
        '''wina svlis shecvla'''
        if len(self.moves) == 0:
            return False
        self.board[self.moves.pop()]=empty
        #game overis shemdeg vegar svav simbolos
        self.gameover = False
        return True

    def GameOver(self):
        return self.gameover

    def Draw(self):
        return self.draw
    
    def GetWinner(self):
        '''giwers vin moigo tamashi'''
        if self.GameOver() and not self.Draw():
            return self.winner

    def CheckGameOver(self):
        '''naxulobs rodis morcheba tamasi'''
        for line in self.alllines:
            px,py,pz=line
            if self.board[px] != empty and self.board[px]==self.board[py]==self.board[pz]:
                self.gameover = True
                self.winner = self.board[px]
                self.draw=False
                break
        else:
            if len(self.moves) == 9:
                self.draw=True
                self.gameover = True
            else:
                self.gameover = False


class Board:
    '''dafa'''
    gridcolor=blue
    circlecolor=red
    crosscolor=green

    def __init__(self,boardsize=400):
        self.players=[]
        self.boardsize=boardsize
        self.gameboard=BoardAnalyzer()
        self.font = pygame.font.Font(None, 30)

    def reset(self):
        '''aresetebs dafas'''
        self.gameboard=BoardAnalyzer()
        for player in self.players:
            player.SetBoard(self.gameboard)
        #vinc agebs igebs pirvelad dawyebis sashualebas
        self.player1,self.player2=self.player2,self.player1

    def printstatus(self,screen):
        textstr=''
        if game.gameboard.GameOver():
            if game.gameboard.Draw():
                textstr="Fre. Daachiret tavidan dasawyebad."
            else:
                textstr=self.player1.name+" -ma moigo. [TAVIDAN DAWYEBA]"
        else:
            textstr=self.player1.name+" -is jeria."
        text = self.font.render(textstr, 1,(255,255,255))
        textpos = text.get_rect(centerx=screen.get_width()/2,y=self.boardsize+5)
        screen.blit(text, textpos)

    def AddPlayer(self,player):
        player.SetBoard(self.gameboard)
        self.players.append(player)
        if(len(self.players) > 1):
            self.player1=self.players[0]
            self.player2=self.players[1]

    def draw(self,screen):
        #lurji dafa
        tolerance=20
        pygame.draw.line(screen, self.gridcolor, (self.boardsize/3,tolerance), (self.boardsize/3,self.boardsize-tolerance),10)
        pygame.draw.line(screen, self.gridcolor, ((2*self.boardsize)/3,tolerance), ((2*self.boardsize)/3,self.boardsize-tolerance),10)
        pygame.draw.line(screen, self.gridcolor, (tolerance,(self.boardsize)/3), (self.boardsize-tolerance,(self.boardsize)/3),10)
        pygame.draw.line(screen, self.gridcolor, (tolerance,(2*self.boardsize)/3), (self.boardsize-tolerance,(2*self.boardsize)/3),10)

        #simboloebis daxatva
        for move in self.gameboard.moves:
            mx,my=move
            onethird=int(self.boardsize/3)

            if self.gameboard.board[move] == circle:
                #wris daxatva
                pos=mx*onethird+int(onethird/2),my*onethird+int(onethird/2)
                pygame.draw.circle(screen, self.circlecolor, pos, int(onethird/3), 10)
            elif self.gameboard.board[move] == cross:
                tl=mx*onethird+int(onethird/5),my*onethird+int(onethird/5)

                tr=(mx+1)*onethird-int(onethird/5),my*onethird+int(onethird/5)

                bl=mx*onethird+int(onethird/5),(my+1)*onethird-int(onethird/5)

                br=(mx+1)*onethird-int(onethird/5),(my+1)*onethird-int(onethird/5)

                pygame.draw.line(screen, self.crosscolor, tl, br,10)
                pygame.draw.line(screen, self.crosscolor, tr, bl,10)


    #daclickvis pozicia
    def MouseClick(self,position):
        mx,my=position
        if my < self.boardsize:
            onethird=int(self.boardsize/3)
            cx=int(math.floor(mx/onethird))
            cy=int(math.floor(my/onethird))
            cell=cx,cy
            self.player1.MouseClick(cell)
        elif self.gameboard.GameOver():
            self.reset()

    def update(self):
        #boardis ganaxleba
        if not self.gameboard.GameOver():
            nextpos=self.player1.GetMove()
            if  nextpos is not None:
                self.gameboard.Move(nextpos,self.player1.sign)
                if not self.gameboard.GameOver():
                    self.player1,self.player2=self.player2,self.player1



if(__name__ == "__main__"):
    pygame.init()
    boardsize=400
    screen = pygame.display.set_mode((boardsize,boardsize+35))
    pygame.display.set_caption('IQSIKI DA NOLIKI')
    gameover=False
    clock = pygame.time.Clock()
    game=Board()

    game.AddPlayer(ComputerPlayer(cross,"Bot"))
    game.AddPlayer(HumanPlayer(circle,"User"))

    while gameover==False:
        clock.tick(FPS)
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit();exit()
            if event.type == pygame.MOUSEBUTTONUP:
                game.MouseClick(event.pos)
        game.update()
        game.draw(screen)
        game.printstatus(screen)
        pygame.display.update()

time.sleep(30)