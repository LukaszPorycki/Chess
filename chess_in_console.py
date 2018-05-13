import sys
import os
import numpy as np

class Figure():
    Field = [["  " for j in range(8)] for i in range(8)]

    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        self.firstMove=True
        self.doesnt_move = True
        if color==1:
            Figure.Field[x][y] = 'W'
        else:
            Figure.Field[x][y] = 'B'

    def print_possible_moves(self):
        print([action for action in self.possible()])

    def move(self,x,y):
        possible_moves = [action for action in self.possible()]
        self.firstMove=False
        #only_moves = [(x,y) for x,y,z in self.possible()]
        if (x,y,'m') in possible_moves or (x,y,'b') in possible_moves:
            name = Figure.Field[self.x][self.y]
            Figure.Field[self.x][self.y] = '  '
            self.x=x
            self.y=y
            Figure.Field[x][y]=name
        else:
            print("This move is inpossible")
        return possible_moves

    def out_of_range(self,x,y):
        scope = range(8)
        if x in scope and y in scope:
            return True
        else:
            return False

    def possible(self):
        pass

    def is_beat_possible(self,x,y):
        if Figure.Field[self.x][self.y][0]==Figure.Field[x][y][0]:
            #print(Figure.Field[self.y][self.x][0],Figure.Field[y][x][0])
            return False
        else:
            return True

    @staticmethod
    def get_field():
        return Figure.Field

class Pawns(Figure):
    def __init__(self,x,y,color):
        Figure.__init__(self,x,y,color)
        Figure.Field[x][y]+='P'

    def possible(self):
        x=self.x
        y=self.y
        try:
            if self.out_of_range(x-1,y) and Figure.Field[x-1][y]=='  ':
                if self.firstMove:
                    #self.firstMove = False
                    if self.out_of_range(x - 2, y) and Figure.Field[x - 2][y] == '  ':
                        yield (x - 2, y, "m")
                    yield (x - 1, y, "m")
                else:
                    yield (x-1,y,"m")
            if self.out_of_range(x-1,y-1) and Figure.Field[x-1][y-1] !='  ':
                if self.is_beat_possible(x -1, y -1):
                    yield (x-1,y-1,"b")

            if self.out_of_range(x -1,y + 1) and Figure.Field[x - 1][y + 1]!='  ':
                if self.is_beat_possible(x -1, y +1):
                    yield (x -1, y +1,"b")
        except Exception as e:
            print(e)

class WhitePawn(Figure):
    def __init__(self,x,y,color):
        Figure.__init__(self,x,y,color)
        Figure.Field[x][y]='WP'

    def possible(self):
        x=self.x
        y=self.y
        try:
            if self.out_of_range(x+1,y) and Figure.Field[x+1][y] == '  ':
                if self.firstMove:
                    #self.firstMove = False
                    if self.out_of_range(x + 2, y) and Figure.Field[x + 2][y] == '  ':
                        yield (x + 2, y, "m")
                    yield (x + 1, y, "m")
                else:
                    yield (x + 1, y, "m")
            if self.out_of_range(x+1,y+1) and Figure.Field[x+1][y+1]!='  ':
                if self.is_beat_possible(x + 1, y + 1):
                    yield (x+1,y+1,"b")
            if self.out_of_range(x + 1, y - 1) and Figure.Field[x + 1][y - 1] != '  ':
                if self.is_beat_possible(x + 1, y -1):
                    yield (x + 1, y - 1,"b")
        except Exception as e:
            print(e)

class Rooks(Figure):
    def __init__(self,x,y,color):

        Figure.__init__(self,x,y,color)
        Figure.Field[x][y]+='R'

    def possible(self):
        beat_flag_x = True
        beat_flag_y = True
        x = self.x
        y = self.y
        stop_up = 7
        stop_down = -7
        stop_left = -7
        stop_right = 7
        tab = [i for i in range(-7, 0)]
        tab.reverse()
        iterator = tab + [i for i in range(1, 8)]
        try:
            for move in iterator:
                # if beat_flag_y:
                if move <= stop_up and move >= stop_down:
                    if self.out_of_range(x + move, y ) and Figure.Field[x + move][y ] == '  ':
                        yield (x + move, y, "m")
                    if self.out_of_range(x + move, y ) and Figure.Field[x + move][y ]!= '  ':
                        if self.is_beat_possible(x+move,y):
                            yield (x + move, y , "b")
                        if move < 0:
                            stop_down = move
                        else:
                            stop_up = move
                if move <= stop_right and move >= stop_left:
                    if self.out_of_range(x, y + move) and Figure.Field[x ][y + move] == '  ':
                        yield (x , y + move, "m")
                    if self.out_of_range(x, y + move) and Figure.Field[x ][y + move] != '  ' :
                        if self.is_beat_possible(x,y+move):
                            yield (x , y+move, "b")
                        if move < 0:
                            stop_left = move
                        else:
                            stop_right = move
        except:
            pass

    def move(self, x, y):
        possible_moves = [action for action in self.possible()]
        self.firstMove = False
        # only_moves = [(x,y) for x,y,z in self.possible()]
        if (x, y, 'm') in possible_moves or (x, y, 'b') in possible_moves:
            name = Figure.Field[self.x][self.y]
            Figure.Field[self.x][self.y] = '  '
            self.x = x
            self.y = y
            Figure.Field[x][y] = name
            self.doesnt_move = False
        else:
            print("This move is inpossible")
        return possible_moves

class Khnights(Figure):
    def __init__(self,x,y,color):

        Figure.__init__(self,x,y,color)
        Figure.Field[x][y]+='k'

    def possible(self):
        x=self.x
        y=self.y

        for move_y in [i for i in range(-2,3) if i !=0]:
            for move_x in [i for i in range(-2,3) if i !=0]:
                try:
                    if(abs(move_x)!=abs(move_y)):
                        if self.out_of_range(x+move_x,y + move_y) and Figure.Field[x+move_x][y + move_y] == '  ':
                            yield (x + move_x,y + move_y,"m")
                        if self.out_of_range(x+move_x,y + move_y) and Figure.Field[x+move_x][y + move_y] != '  ':
                            if self.is_beat_possible(x+move_x,y+move_y):
                                yield (x+move_x, y + move_y,"b")
                except Exception as error:
                    print(error)
                    pass

class Bishops(Figure):

    def __init__(self, x, y,color):

        Figure.__init__(self, x, y,color)
        Figure.Field[x][y]+='B'

    def possible(self):
        beat_flag_x = True
        beat_flag_y = True
        x=self.x
        y=self.y
        stop_up=7
        stop_down=-7
        stop_left=-7
        stop_right=7
        tab = [i for i in range(-7,0)]

        tab.reverse()
        iterator =tab+ [i for i in range(1, 8)]
        try:
            for move in  iterator:
                #if beat_flag_y:
                if move<= stop_up and move>=stop_down:
                    if self.out_of_range(x+move,y + move) and Figure.Field[x+move][y + move] == '  ':
                        yield (x+move,y + move, "m")
                    if self.out_of_range(x + move, y + move) and Figure.Field[x + move][y + move] != '  ':
                        if self.is_beat_possible(x + move, y + move):
                            #print('HALLLLLLLLOOOOOOOO!!!!!!!!!!!!!!!!!!')
                            yield (x + move, y + move, "b")
                        if move<0:
                            stop_down = move
                        else:
                            stop_up= move
                if move <= stop_right and move >= stop_left:
                    if self.out_of_range(x + move, y - move) and Figure.Field[x + move][y - move] == '  ':
                        yield (x + move, y - move, "m")
                    if self.out_of_range(x + move, y - move) and Figure.Field[x + move][y - move] != '  ':
                        if self.is_beat_possible(x + move, y - move):
                            yield (x + move, y - move, "b")
                        if move < 0:
                            stop_left = move
                        else:
                            stop_right = move
        except:
            pass

class Quen(Rooks,Bishops):

    def __init__(self, x, y,color):
        Figure.__init__(self,x,y,color)

        Figure.Field[x][y]+='Q'


    def print_possible_moves(self):
        actions = [action for action in Rooks.possible(self)] + [action for action in Bishops.possible(self)]
        print(actions)

    def possible(self):
        actions = [action for action in Rooks.possible(self)] + [action for action in Bishops.possible(self)]
        for action in actions:
            yield action

    def move(self,x,y):
        possible_moves = [action for action in Rooks.possible(self)] + [action for action in Bishops.possible(self)]
        if (x, y, 'm') in possible_moves or (x,y,'b') in possible_moves:
            name = Figure.Field[self.x][self.y]
            Figure.Field[self.x][self.y] = '  '
            self.x = x
            self.y = y
            Figure.Field[x][y] = name
        else:
            print("This move is impossible")
        return possible_moves

class King(Figure):

    def __init__(self, x, y,color):
        Figure.__init__(self, x, y,color)
        Figure.Field[x][y]+='K'


    def possible(self):
        x=self.x
        y=self.y
        for i in range(-1,2):
            for j in range(-1,2):
                try:
                    if (i,j)!=(0,0):
                        if self.out_of_range(x+j,y + i) and Figure.Field[x+j][y +i] == '  ':
                            yield (x+j,y + i, "m")
                except Exception as error:
                    print(error)
                    pass
    def move(self,x,y):
        possible_moves = [action for action in self.possible()]
        self.firstMove=False
        #only_moves = [(x,y) for x,y,z in self.possible()]
        if (x,y,'m') in possible_moves or (x,y,'b') in possible_moves:
            print(self.x,self.y,'check')
            name = Figure.Field[self.x][self.y]
            Figure.Field[self.x][self.y] = '  '
            self.x=x
            self.y=y
            Figure.Field[x][y]=name
            self.doesnt_move=False
        else:
            print("This move is inpossible")
        return possible_moves

    def move_site(self,site):
        if site=='l':

            yield (self.x,self.y-1)
        else:
            yield (self.x, self.y + 1)

class Game():
    def __init__(self):
        self.black={}
        figure=Figure(1,1,1)
        Blackpavn = [Pawns(1,i,2) for i in range(8)]
        Whitepavn = [WhitePawn(6, i, 1) for i in range(8)]
        Blackrooks=[Rooks(0,0,2),Rooks(0,7,2)]
        Whiterooks = [Rooks(7, 0, 1), Rooks(7, 7, 1)]
        Blackkhnights=[Khnights(0,1,2),Khnights(0,6,2)]
        Whitekhnights = [Khnights(7, 1, 1), Khnights(7, 6, 1)]
        Blackbishops=[Bishops(0,2,2),Bishops(0,5,2)]
        Whitebishops = [Bishops(7, 2, 1), Bishops(7, 5, 1)]
        BlackKing=King(0,4,2)
        WhiteKing=King(7,4,1)
        BlackQuean=Quen(0,3,2)
        WhiteQuean=Quen(7,3,1)


        self.abreviations = dict(zip(['BP','BR','Bk','BB','BQ','BK','WP','WR','Wk','WB','WQ','WK'],[Blackpavn,Blackrooks,Blackkhnights,Blackbishops,BlackQuean,BlackKing,Whitepavn,Whiterooks,Whitekhnights,Whitebishops,WhiteQuean,WhiteKing]))
        print(self.abreviations)

    def draw(self):
        for i in range(16):
            for j in range(16):
                if i%2==0:
                    if(j%2==0):
                        fig=Figure.Field[int(i/2)][int(j/2)]
                        sys.stdout.write(' '+str(fig))
                    else:
                        sys.stdout.write('|')
                else:
                    sys.stdout.write('--')
            sys.stdout.write('\n')

    def game(self):
        for i in range(100):
            good=True
            while good:
                try:
                    if i%2==0:
                        print('White player turn: ')
                    else:
                        print('Black player turn')
                    firstplayer= input('Choose Pawn: ')
                    pion=firstplayer[0:2]
                    try:
                        which = firstplayer[2]
                        print("You choose : "+which)
                        print(pion)
                        self.abreviations[pion][int(which)].print_possible_moves()
                    except Exception as error:
                        print(error)
                        self.abreviations[pion].print_possible_moves()
                        pass
                    firstplayer = input('choose field: ')
                    x_where,y_where=firstplayer[0:2]
                    print('y :' + str(x_where)+'x: '+str(y_where))
                    try:
                        print(self.abreviations[pion][int(which)].move(int(x_where),int(y_where)))
                    except:
                        print(self.abreviations[pion].move(int(x_where), int(y_where)))
                    self.draw()
                except Exception as e:
                    print('You are wrong, try again!')
                    continue
                good=False

















