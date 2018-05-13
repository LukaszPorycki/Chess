from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QApplication, QGraphicsItem, QGraphicsPixmapItem,QMessageBox
from chess_in_console import Figure,Pawns,WhitePawn,Rooks,Bishops,Quen,King,Khnights
import sys
import socket  # Import socket module


class Piece(QGraphicsItem):
    id=0
    SelectedItem=None
    scene = None
    size = None
    turn = 1
    color = 1
    listening = False
    good = False
    firstMove = True

    def __init__(self, pixmap,x,y,width,height,figure,site='l',IsMoovable = True):
        super(QGraphicsItem, self).__init__()
        self.id = Piece.id
        self.pixmap = pixmap
        self.x = x
        self.y = y
        self.xP=x
        self.yP=y
        self.figure = figure
        self.background=False
        self.site = site
        if IsMoovable:
            self.setFlags(QGraphicsItem.ItemIsSelectable)
        #self.text=QString()
        self.rectF = QtCore.QRectF(self.x,self.y,width,height)
        Piece.id += 1
        #print(Piece.id)

    def paint(self, painter, QStyleOptionGraphicsItem, widget = None):
        painter.drawPixmap(self.x,self.y,self.pixmap)
        pass
    # def paint_rec(self, painter, QStyleOptionGraphicsItem, widget = None):
    #     painter.fillRect(self.x, self.y, Piece.size, Piece.size, QtCore.Qt.black)

    def boundingRect(self):
        return self.rectF

    def mousePressEvent(self, event):
        #print(event.pos().x(),event.pos().y())
        #print(QGraphicsSceneMouseEvent.pos().x(),QPoint(QGraphicsSceneMouseEvent.pos().y()))
        #print(event.scenePos().x(),event.scenePos().y())
        if(Piece.turn==self.figure.color):
            try:
                ##############
               # if not Piece.firstMove:

                ##############
                self.setSelected(True)
                #self.setPos(0,0)
                Piece.SelectedItem=self
                #print(Piece.SelectedItem==self)
                possibleMoves = [[move[0]*Piece.size,move[1]*Piece.size] for move in self.figure.possible() if move[0]>=0 and move[1]>=0 and move[0]<8 and move[1]<8]# if move[2]!='b']
                print(possibleMoves,'look here!')
                #print(possibleMoves)
                #print(Piece.scene)
                if len([cast for cast in self.Castling(self.figure.color)])!=0:
                    for cast in self.Castling(self.figure.color):
                        Piece.scene.addItem(cast)
                        ChooseablePiece.add(cast)

                #[print(pos[1], pos[0], Piece.size)for pos in possibleMoves]
                #[Piece.scene.addItem(Piece(QPixmap("./whiterook.png").scaled(Piece.size,Piece.size), pos[1],pos[0],Piece.size,Piece.size,None)) for pos in possibleMoves]
                for pos in possibleMoves:
                    #print(pos)
                    field=ChooseablePiece( float(pos[1]), float(pos[0]), float(Piece.size), float(Piece.size),self.figure,Piece.scene,Piece.size,self)
                    Piece.scene.addItem(field)
                    ChooseablePiece.add(field)
            except Exception as e:
                print(e)
            #self.scene.addItem(Piece(QPixmap("./whiterook.png").scaled(self.field, self.field), 0, 0, self.field, self.field,Whiterooks[0]))
            # Piece.SelectedItem.x=10
            Piece.change_turn()
        else:
            pass
    def setCoords(self,x,y):
        self.xP=x
        self.yP=y

    def Castling(self,color):
        print('hallo')
        rooks = [figure for figure in self.scene.items() if isinstance(figure.figure,Rooks) and not isinstance(figure.figure,Quen) ]
        print(rooks)
        WhiteRooks = [rook for rook in rooks if rook.figure.color == 1]
        BlackRooks = [rook for rook in rooks if rook.figure.color == 2]
        if color == 1:
            rooks=WhiteRooks
        else:
            rooks=BlackRooks
        if isinstance(self.figure,King) :
                for rook in rooks:
                    if rook.figure.doesnt_move and self.figure.doesnt_move:
                        for rookPos in rook.figure.possible():
                            if rook.site == 'l':
                                if [rookPos[0],rookPos[1]] in [[kingpos[0],kingpos[1]]for kingpos in self.figure.possible()]:
                                    yield CastlingPiece(rook.x,rook.y,Piece.size,Piece.size,self,rook,Piece.scene,Piece.size,'l')
                            else:
                                if [rookPos[0], rookPos[1]] in [[kingpos[0], kingpos[1]] for kingpos in self.figure.possible()]:
                                    yield CastlingPiece(rook.x,rook.y,Piece.size,Piece.size,self,rook,Piece.scene,Piece.size,'r')
        else:
            pass

    @staticmethod
    def change_turn():
        if Piece.turn == 1:
            Piece.turn = 2
        else :
            Piece.turn = 1
    @staticmethod
    def addGlobalScene(scene):
        Piece.scene = scene
    @staticmethod
    def addGlobalSize(size):
        Piece.size =size

class Background(Piece):
    def init(self,pixmap,x,y,width,height,figure):
        Piece.__init__(self,pixmap,x,y,width,height,figure,site='l',IsMoovable = True)
        self.background=True

    def mousePressEvent(self, event):
        pass

class CastlingPiece(QGraphicsItem):
    def __init__(self,x,y,width,height,king,rook,scene,size,site):
        super(QGraphicsItem,self).__init__()
        self.x=x
        self.y=y
        self.xP=x
        self.yP=y
        self.king=king
        print(self.king.figure.x,self.king.figure.y)
        self.rook=rook
        self.scene=scene
        self.size=size
        self.site=site
        self.rectF = QtCore.QRectF(self.x, self.y, width, height)

    def boundingRect(self):
        return self.rectF

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # painter.drawPixmap(self.x,self.y,self.pixmap)
            painter.fillRect(self.x, self.y, Piece.size, Piece.size, QtCore.Qt.red)
    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
        try:
            temp=self.rook.figure.Field[self.rook.figure.x][self.rook.figure.y]
            self.rook.figure.Field[self.rook.figure.x][self.rook.figure.y] = '  '
            positions=[pos for pos in self.king.figure.move_site(self.site)]
            for pos in positions:
                print(self.king.figure.x)
                self.king.figure.Field[pos[0]][pos[1]]=self.king.figure.Field[self.king.figure.x][self.king.figure.y]

                self.king.figure.Field[self.king.figure.x][self.king.figure.y]=temp
                self.rook.figure.x=self.king.figure.x
                self.rook.figure.y=self.king.figure.y
                self.king.figure.x=pos[0]
                self.king.figure.y=pos[1]

                print('ok?')
                if self.site=='l':
                    self.rook.moveBy(self.king.xP-self.rook.xP,self.king.yP-self.rook.yP)
                    self.king.moveBy(-self.size, 0)
                    self.rook.setCoords(self.king.xP,self.king.yP)
                    print(pos[1],'elo')
                    self.king.setCoords(pos[1]*self.size,pos[0]*self.size)

                else:
                    self.rook.moveBy(self.king.xP - self.rook.xP, self.king.yP - self.rook.yP)
                    self.king.moveBy(self.size, 0)
                    print(pos[1],pos[0],'elohere')
                    self.rook.setCoords(self.king.xP, self.king.yP)
                    self.king.setCoords(pos[1] * self.size, pos[0] * self.size)
            ChooseablePiece.clear()
        except Exception as e:
            print(e)
class ChooseablePiece(QGraphicsItem):
    szach = 0
    szach_mat = False
    not_choosed_fields=[]
    def __init__(self,x,y,width,height,figure,scene,size,relatedPiece):
        super(QGraphicsItem, self).__init__()
        self.relatedPiece=relatedPiece
        #print(x,y,width,height)
        self.x=x
        self.y=y
        self.xP=x
        self.yP=y
        self.figure=figure
        self.scene=scene
        self.size=size
        self.rectF = QtCore.QRectF(self.x, self.y, width, height)
        pass

    def boundingRect(self):
        return self.rectF

    def mousePressEvent(self, event):
        flag=False
        try:

            #self.scene.removeItem(self)
            item_from_this_place = [item for item in self.scene.items() if item.xP==self.x and item.yP==self.y ]
            piece_from_this_place=[item for item in item_from_this_place if isinstance(item,Piece)]
            #print(ChooseablePiece.not_choosed_fields)
            if len(piece_from_this_place)!=0:
                #print(piece_from_this_place,"It's here")
                for piece in piece_from_this_place:

                    if piece.background:
                        #print(piece,'Whats going on?')
                        pass
                    else:
                        #print('I remove :',piece)
                        #Figure.Field[piece.figure.x][piece.figure.y]='  '
                        self.figure.move(int(piece.yP / self.size), int(piece.xP / self.size))
                        self.relatedPiece.moveBy(piece.xP - self.relatedPiece.xP, piece.yP - self.relatedPiece.yP)
                        self.relatedPiece.setCoords(piece.xP,piece.yP)
                        self.scene.removeItem(piece)
            else:
                self.figure.move(int(self.y / self.size), int(self.x / self.size))
                #print(self.x-self.relatedPiece.x,self.y-self.relatedPiece.y)
                print(self.x-self.relatedPiece.xP,self.y-self.relatedPiece.yP)
                self.relatedPiece.moveBy(self.x-self.relatedPiece.xP,self.y-self.relatedPiece.yP)
                # self.relatedPiece.x=self.x
                # self.relatedPiece.y=self.y
                self.relatedPiece.setCoords(self.x,self.y)
                #print(self.relatedPiece.x,self.relatedPiece.y)
                #print([item for item in self.scene.items() if item.xP == self.x and item.yP == self.x])
            ChooseablePiece.clear()
            self.draw()
            # dialog=TextItemDlg('soema')
            # dialog.exec_()

            #MyFirstScene.showMessage("It's working")
            self.szach_mat()
            if ChooseablePiece.szach!=0:
                MyFirstScene.showMessage("SZACH")
                print(ChooseablePiece.szach)
            if ChooseablePiece.szach==2:
                MyFirstScene.showMessage("Szach Mat")

            print(self.relatedPiece.figure.firstMove)


            ###################################
            Client.send()
            ##################################3

        except Exception as e:
            print(e)
    #
    #
    # def send(self):
    #
    #     #relatedpiece.figure
    #     # zmiana pozycji , bicie
    #     beat_figure_id=
    #     changed_figure_id=
    #     changed_figure_actual_position=
    # def get_recived_changes(self):
    #     data=recive.Get_changes()
    #
    #
    #     changes=data.split(',')
    #     beat_figure_id=changes[0],
    #     changed_figure_id=changes[1]
    #     changed_x=int(changes[2])
    #     changed_y=int(changes[3])
    #     changed_figure=[figure for figure in self.scene.items() if figure.id == changed_figure_id]
    #     if beat_figure_id !='':
    #         beated_figure = [figure for figure in self.scene.items() if figure.id == beat_figure_id]
    #         beated_figure[0].figure.Field[beated_figure[0].figure.x][beated_figure[0].figure.y]='  '
    #         self.scene.removeItem(beated_figure[0])
    #     changed_figure[0].moveBy(self.x - changed_x*self.size,self.y-changed_y*self.size )
    #     changed_figure[0].figure.move(changed_x,changed_y)
    #     changed_figure[0].setCoords(changed_x*self.size,changed_y*self.size)

    def szach_mat(self):

        kings = [figure.figure for figure in self.scene.items() if isinstance(figure.figure,King)]
        WhiteKing = None
        BlackKing = None
        for king in kings:
            if king.color == 1:
                WhiteKing = king
            else:
                BlackKing = king

        for figure in self.scene.items():
            if (not isinstance(figure,Background)) and (not isinstance(figure,ChooseablePiece)):
                possibleMoves = [move for move in figure.figure.possible()]
                BlackKingMoves=[BlackKing.x,BlackKing.y]
                WhiteKingMoves = [WhiteKing.x,WhiteKing.y]
                for possibleMove in possibleMoves:
                    if [possibleMove[0],possibleMove[1]] == BlackKingMoves or [possibleMove[0],possibleMove[1]] == WhiteKingMoves:
                        ChooseablePiece.szach +=1
                        return 0
        ChooseablePiece.szach=0

    def paint(self, painter, QStyleOptionGraphicsItem, widget = None):
        # painter.drawPixmap(self.x,self.y,self.pixmap)
        if self.figure.color==1:
            painter.fillRect(self.x, self.y, Piece.size,Piece.size, QtCore.Qt.white)
        else:
            painter.fillRect(self.x, self.y, Piece.size, Piece.size, QtCore.Qt.black)

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

    @staticmethod
    def clear():
        for field in ChooseablePiece.not_choosed_fields:
            Piece.scene.removeItem(field)
        ChooseablePiece.not_choosed_fields=[]
    @staticmethod
    def add(field):
        ChooseablePiece.not_choosed_fields.append(field)


class Client(QtCore.QThread):
    data = None
    socket = None
    def __init__(self,):# scene):
        QtCore.QThread.__init__(self)
        #self.scene = scene
        Client.socket = socket.socket()


    def run(self):
        try:
            host = self.socket.gethostname()
            port = 60000
            Client.socket.connect((host,port))
            #listening for initial settings
            #Client.socket.send('Init')
            feedback = Client.socket.recv(1024)
            feedback=feedback.split('|')
            Piece.color = int(feedback[0])
            Piece.good = bool(feedback[1])
            Piece.firstMove=bool(feedback[2])
            Piece.listening = bool(feedback[3])
        except Exception as e:
            print(e)
        while True:
            if not Piece.firstMove:
                Client.makeChanges()
            if Piece.listening:
                Piece.listening=False
                data=Client.socket.recv(1024)
                Piece.good = True
                Client.data = data
                Piece.listening = False
            else:
                pass

    @staticmethod
    def send(cId,bId,x,y):
        data = cId+'|'+bId+'|'+x+'|'+y
        Client.socket.send(data)
        Piece.listening = True
        Piece.good = False

    @staticmethod
    def makeChanges():
        cId, bId, x, y = Client.getData()
        cId = int(cId)
        try:
            bId = int(bId)
        except:
            pass
        x = int(x)
        y = int(y)
        changed = [figure for figure in Piece.scene.items() if figure.id == cId]
        if bId != 'not':
            beated = [figure for figure in Piece.scene.items() if figure.id == bId]
            self.figure.Field[x][y] = '  '
            Piece.scene.removeItem(beated[0])
        changed[0].moveBy(pos[0] * Piece.size - changed[0].xP, pos[1] - changed[0].yP)
        changed[0].setCoords(pos[0] * Piece.size, pos[1] * Piece.size)
        changed[0].figure.Field[x][y] = changed[0].figure.Field[changed[0].figure.x][changed[0].figure.y]


    @staticmethod
    def getData():
        data = Client.data.split('|')
        changeId,beatedId,posX,posY = data
        return [changeId,beatedId,posX,posY]






    # @staticmethod
    # def WhiteTurn():
    #

# class recive(QtCore.QThread):
#     data
#     def __init__(self,scene):
#         QtCore.QThread.__init__(self)
#         self.scene = scene
#
#     def run(self):
#
#         s = socket.socket()  # Create a socket object
#         host = socket.gethostname()  # Get local machine name
#         port = 60000  # Reserve a port for your service.
#
#         s.connect((host, port))
#         s.send("Hello server!")
#
#
#         while True:
#             print('receiving data...')
#             data = s.recv(1024)
#             print('data=%s', (data))
#             if not data:
#                 break
#             # write data to a file
#
#         print('Successfully get the file')
#         s.close()
#         print('connection closed')
#
    # class recive(QtCore.QThread):
    #
    #     def __init__(self, scene):
    #         QtCore.QThread.__init__(self)
    #         self.scene = scene
    #
    #     def run(self):
    #         print(self.scene.selectedItems())

    # s = socket.socket()  # Create a socket object
    # host = socket.gethostname()  # Get local machine name
    # port = 60000  # Reserve a port for your service.
    #
    # s.connect((host, port))
    # s.send("Hello server!")
    # #
    # # with open('received_file', 'wb') as f:
    # #     print
    # #     'file opened'
    # while True:
    #     print('receiving data...')
    #     data = s.recv(1024)
    #     print('data=%s', (data))
    #     if not data:
    #         break
    #     # write data to a file
    #     # f.write(data)
    #
    # # f.close()
    # print('Successfully get the file')
    # s.close()
    # print('connection closed')

    # while True:
    #     conn, addr = s.accept()  # Establish connection with client.
    #     print
    #     'Got connection from', addr
    #     data = conn.recv(1024)
    #     print('Server received', repr(data))
    #
    #     filename = 'mytext.txt'
    #     f = open(filename, 'rb')
    #     l = f.read(1024)
    #     while (l):
    #         conn.send(l)
    #         print('Sent ', repr(l))
    #         l = f.read(1024)
    #     f.close()
    #
    #     print('Done sending')
    #     conn.send('Thank you for connecting')
    #     conn.close()


class scene(QGraphicsScene):

    def __init__(self,parent=None):
        super(scene,self).__init__(parent)


    # def mousePressEvent(self,event):
    #     print(self.selectedItems())

    # def selectedItems(self):
    #     items = self.selectedItems()
    #     if len(items)==1:
    #         print("is selected")
    #         return items[0]
    #     return None

class MyFirstScene(QWidget):
    mainWindow=None
    def __init__(self):
        QWidget.__init__(self)
        MyFirstScene.mainWindow = self
        self.scene=scene(self)
        self.setGeometry(100,100,400,400)
        self.background=QPixmap("./chessboard.png")
        self.bg_height=self.background.height()
        self.bg_width=self.background.width()
        self.field=self.bg_width/8


        #self.background=QPixmap("./chessboard.png")
        #self.scene.drawBackground(painter.drawPixmap)
        #self.scene.addText("Hello, world!")
        figure = Figure(1, 1, 1)
        Blackpavn = [Pawns(6, i, 2) for i in range(8)]
        Whitepavn = [WhitePawn(1, i, 1) for i in range(8)]
        Blackrooks = [Rooks(7, 0, 2), Rooks(7, 7, 2)]
        Whiterooks = [Rooks(0, 0, 1), Rooks(0, 7, 1)]
        Blackkhnights = [Khnights(7, 1, 2), Khnights(7, 6, 2)]
        Whitekhnights = [Khnights(0, 1, 1), Khnights(0, 6, 1)]
        Blackbishops = [Bishops(7, 2, 2), Bishops(7, 5, 2)]
        Whitebishops = [Bishops(0, 2, 1), Bishops(0, 5, 1)]
        BlackKing = King(7, 4, 2)
        WhiteKing = King(0, 4, 1)
        BlackQuean = Quen(7, 3, 2)
        WhiteQuean = Quen(0, 3, 1)
        Piece.addGlobalScene(self.scene)
        Piece.addGlobalSize(self.field)

        self.scene.addItem(Background(self.background,0,0,self.bg_width,self.bg_height,False))
        self.scene.addItem(Piece(QPixmap("./whiterook.png").scaled(self.field,self.field), 0, 0,self.field,self.field,Whiterooks[0]))
        self.scene.addItem(Piece(QPixmap("./whiterook.png").scaled(self.field,self.field), self.field*7, 0,self.field,self.field,Whiterooks[1],site='r'))
        self.scene.addItem(Piece(QPixmap("./whiteknight.png").scaled(self.field,self.field), self.field, 0,self.field,self.field,Whitekhnights[0]))
        self.scene.addItem(Piece(QPixmap("./whiteknight.png").scaled(self.field,self.field), self.field*6, 0,self.field,self.field,Whitekhnights[1]))
        self.scene.addItem(Piece(QPixmap("./whitebishop.png").scaled(self.field,self.field), self.field*2, 0,self.field,self.field,Whitebishops[0]))
        self.scene.addItem(Piece(QPixmap("./whitebishop.png").scaled(self.field,self.field), self.field*5, 0,self.field,self.field,Whitebishops[1]))
        self.scene.addItem(Piece(QPixmap("./whitequean.png").scaled(self.field,self.field), self.field*3, 0,self.field,self.field,WhiteQuean))
        self.scene.addItem(Piece(QPixmap("./Chessking.png").scaled(self.field,self.field), self.field*4, 0,self.field,self.field,WhiteKing))
        [self.scene.addItem(Piece(QPixmap("./whitepawn.png").scaled(self.field,self.field), self.field*i, self.field,self.field,self.field,pawn)) for i,pawn in enumerate(Whitepavn)]
        self.scene.addItem(Piece(QPixmap("./blackrook.png").scaled(self.field, self.field), 0, self.field*7, self.field, self.field,Blackrooks[0]))
        self.scene.addItem(Piece(QPixmap("./blackrook.png").scaled(self.field, self.field), self.field * 7, self.field*7, self.field, self.field,Blackrooks[1],site='r'))
        self.scene.addItem(Piece(QPixmap("./blackknight.png").scaled(self.field, self.field), self.field, self.field*7, self.field, self.field,Blackkhnights[0]))
        self.scene.addItem(Piece(QPixmap("./blackknight.png").scaled(self.field, self.field), self.field * 6, self.field*7, self.field,self.field,Blackkhnights[1]))
        self.scene.addItem(Piece(QPixmap("./blackbishop.png").scaled(self.field, self.field), self.field * 2, self.field*7, self.field,self.field,Blackbishops[0]))
        self.scene.addItem(Piece(QPixmap("./blackbishop.png").scaled(self.field, self.field), self.field * 5, self.field*7, self.field,self.field,Blackbishops[1]))
        self.scene.addItem(Piece(QPixmap("./blackquean.png").scaled(self.field, self.field), self.field * 3, self.field*7, self.field,self.field,BlackQuean))
        self.scene.addItem(Piece(QPixmap("./blackking.png").scaled(self.field, self.field), self.field * 4, self.field*7, self.field, self.field,BlackKing))
        [self.scene.addItem(Piece(QPixmap("./blackpawn.png").scaled(self.field, self.field), self.field * i, self.field*6, self.field,self.field,pawn)) for i,pawn in enumerate(Blackpavn)]
        #self.scene.addItem(Piece(QPixmap("./Chessking.png").scaled(self.bg_width / 8, self.bg_height / 8), 0, 0))
        #height=QPixmap("./Chessking.png").height()
        #item=self.selectedItems()
        #print(QGraphicsScene.selectedItems(self.scene))
        self.view = QGraphicsView(self.scene, self)
        #self.view.setBackgroundBrush(self.background)
        # selected=selectedThread(self.scene)
        # selected.start()
        #self.scene.selectedItems()
        self.view.scene().update()
        self.show()
        # try:
        #     client = Client()
        #     client.start()
        # except Exception as e:
        #     print(e)

    @staticmethod
    def showMessage(string):
        QMessageBox.question(MyFirstScene.mainWindow, string, None)





if __name__ == "__main__":
    app=QApplication(sys.argv)
    firstScene = MyFirstScene()
    sys.exit(app.exec_())