from sympy import cos,pi
from textwrap import wrap
import os

Board = [["  " for x in range(0,8)] for x in range(0,8)]
Board_attack_diagram = [["  " for x in range(0,8)] for x in range(0,8)]
Col = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
Row = {"1":0,"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,"8":7}
Pieces=["Q","K","R","N","B"]
Castle_Detectors=[True]*4
list,c,save=[""]*2,0,[]
Passant,Check_w,Check_d,Mate,Error = [False]*5

def spawn():
    global Board
    for x in range(0,8):
        Board[1][x]="Pw"
        Board[6][x]="Pd"

    Board[0][7]="Rw"
    Board[0][0]="Rw"
    Board[7][7]="Rd"
    Board[7][0]="Rd"

    Board[0][1]="Nw"
    Board[0][6]="Nw"
    Board[7][1]="Nd"
    Board[7][6]="Nd"

    Board[0][2]="Bw"
    Board[0][5]="Bw"
    Board[7][2]="Bd"
    Board[7][5]="Bd"

    Board[0][4]="Kw"
    Board[0][3]="Qw"
    Board[7][4]="Kd"
    Board[7][3]="Qd"
def Board_attack_refresh():
    global Board_attack_diagram,Board,Passant
    Board_attack_diagram = [["" for x in range(0,8)] for x in range(0,8)]
    for i in range(0,8):
        for j in range(0,8):
            if "w" in Board[i][j]:
                ally = "w"
                enemy = "d"
            elif "d" in Board[i][j]:
                ally = "d"
                enemy = "w"

            if Board[i][j] == "Pw":
                if i == 7:
                    continue
                if j == 0:
                    Board_attack_diagram[i+1][j+1] += "Pw"+str(i)+str(j)
                elif j == 7:
                    Board_attack_diagram[i+1][j-1] += "Pw"+str(i)+str(j)
                else:
                    Board_attack_diagram[i+1][j+1] += "Pw"+str(i)+str(j)
                    Board_attack_diagram[i+1][j-1] += "Pw"+str(i)+str(j)
                if i == 1:
                    if Board[i+1][j] == "  ":
                        Board_attack_diagram[i+1][j]+="@@"+str(i)+str(j)
                        if Board[i+2][j] == "  ":
                            Board_attack_diagram[i+2][j]+="@+"+str(i)+str(j)
                else:
                    if Board[i+1][j] == "  ":
                        Board_attack_diagram[i+1][j]+="@@"+str(i)+str(j)

            if Board[i][j] == "Pd":
                if i == 0:
                    continue
                if j == 0:
                    Board_attack_diagram[i-1][j+1] +="Pd"+str(i)+str(j)
                elif j == 7:
                    Board_attack_diagram[i-1][j-1] += "Pd"+str(i)+str(j)
                else:
                    Board_attack_diagram[i-1][j+1] += "Pd"+str(i)+str(j)
                    Board_attack_diagram[i-1][j-1] += "Pd"+str(i)+str(j)
                if i == 6:
                    if Board[i-1][j] == "  ":
                        Board_attack_diagram[i-1][j]+="**"+str(i)+str(j)
                        if Board[i-2][j] == "  ":
                            Board_attack_diagram[i-2][j]+="*+"+str(i)+str(j)
                else:
                    if Board[i-1][j] == "  ":
                        Board_attack_diagram[i-1][j]+="**"+str(i)+str(j)

            if "R" in Board[i][j]:
                for x in range(1,8):
                    if i+x <= 7:
                        if Board[i+x][j] != "  ":
                            Board_attack_diagram[i+x][j]+="R"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i+x][j]+="R"+ally+str(i)+str(j)
                for x in range(1,8):
                    if i-x>= 0:
                        if Board[i-x][j] != "  ":
                            Board_attack_diagram[i-x][j]+="R"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i-x][j]+="R"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j+x <= 7:
                        if Board[i][j+x] != "  ":
                            Board_attack_diagram[i][j+x]+="R"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i][j+x]+="R"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j-x >= 0:
                        if Board[i][j-x] != "  ":
                            Board_attack_diagram[i][j-x]+="R"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i][j-x]+="R"+ally+str(i)+str(j)

            if "B" in Board[i][j]:
                for x in range(1,8):
                    if j+x <= 7 and i+x <= 7:
                        if Board[i+x][j+x] != "  ":
                            Board_attack_diagram[i+x][j+x]+="B"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i+x][j+x]+="B"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j+x <= 7 and i-x >= 0:
                        if Board[i-x][j+x] != "  ":
                            Board_attack_diagram[i-x][j+x]+="B"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i-x][j+x]+="B"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j-x >= 0 and i-x >= 0:
                        if Board[i-x][j-x] != "  ":
                            Board_attack_diagram[i-x][j-x]+="B"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i-x][j-x]+="B"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j-x >= 0 and i+x <= 7:
                        if Board[i+x][j-x] != "  ":
                            Board_attack_diagram[i+x][j-x]+="B"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i+x][j-x]+="B"+ally+str(i)+str(j)

            if "N" in Board[i][j]:
                for x in range(0,4):
                    row = abs(2*cos(x*pi/3)-cos(x*pi))
                    col = 2*cos(x*pi/3)
                    if i+row <= 7 and 0<=j+col<=7:
                        Board_attack_diagram[i+row][j+col]+="N"+ally+str(i)+str(j)
                    if i-row >= 0 and 0<=j+col<=7:
                        Board_attack_diagram[i-row][j+col]+="N"+ally+str(i)+str(j)

            if "Q" in Board[i][j]:
                for x in range(1,8):
                    if i+x <= 7:
                        if Board[i+x][j] != "  ":
                            Board_attack_diagram[i+x][j]+="Q"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i+x][j]+="Q"+ally+str(i)+str(j)
                for x in range(1,8):
                    if i-x>= 0:
                        if Board[i-x][j] != "  ":
                            Board_attack_diagram[i-x][j]+="Q"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i-x][j]+="Q"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j+x <= 7:
                        if Board[i][j+x] != "  ":
                            Board_attack_diagram[i][j+x]+="Q"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i][j+x]+="Q"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j-x >= 0:
                        if Board[i][j-x] != "  ":
                            Board_attack_diagram[i][j-x]+="Q"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i][j-x]+="Q"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j+x <= 7 and i+x <= 7:
                        if Board[i+x][j+x] != "  ":
                            Board_attack_diagram[i+x][j+x]+="Q"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i+x][j+x]+="Q"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j+x <= 7 and i-x >= 0:
                        if Board[i-x][j+x] != "  ":
                            Board_attack_diagram[i-x][j+x]+="Q"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i-x][j+x]+="Q"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j-x >= 0 and i-x >= 0:
                        if Board[i-x][j-x] != "  ":
                            Board_attack_diagram[i-x][j-x]+="Q"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i-x][j-x]+="Q"+ally+str(i)+str(j)
                for x in range(1,8):
                    if j-x >= 0 and i+x <= 7:
                        if Board[i+x][j-x] != "  ":
                            Board_attack_diagram[i+x][j-x]+="Q"+ally+str(i)+str(j)
                            break
                        else:
                            Board_attack_diagram[i+x][j-x]+="Q"+ally+str(i)+str(j)
def king_move():
    for i in range(0,8):
        for j in range(0,8):
            if "Kw" in Board[i][j]:
                for x in range(-1,2):
                    for y in range(-1,2):
                        if 0<=i+x<=7 and 0<=j+y<=7:
                            if x==0 and y==0:
                                continue
                            if "d" in Board_attack_diagram[i+x][j+y]:
                                continue
                            else:
                                Board_attack_diagram[i+x][j+y]+="Kw"+str(i)+str(j)

            if "Kd" in Board[i][j]:
                for x in range(-1,2):
                    for y in range(-1,2):
                        if 0<=i+x<=7 and 0<=j+y<=7:
                            if x==0 and y==0:
                                continue
                            if "w" in Board_attack_diagram[i+x][j+y]:
                                continue
                            else:
                                Board_attack_diagram[i+x][j+y]+="Kd"+str(i)+str(j)
def Moviments_Normal(move,side):
    global Board,Board_attack_diagram,Passant
    if len(move)==2:
        col,row=move[0],move[1]
        able=wrap(Board_attack_diagram[Row[row]][Col[col]],4)
        if side=="w":
            for x in range(len(able)):
                if "@@" in able[x]:
                    Board[Row[row]][Col[col]]="Pw"
                    Board[int(able[x][2])][int(able[x][3])]="  "
                    Passant=False
                elif "@+" in able[x]:
                    Board[Row[row]][Col[col]]="Pw"
                    Board[int(able[x][2])][int(able[x][3])]="  "
                    Passant=True
        if side=="d":
            for x in range(len(able)):
                if "**" in able[x]:
                    Board[Row[row]][Col[col]]="Pd"
                    Board[int(able[x][2])][int(able[x][3])]="  "
                    Passant=False
                elif "*+" in able[x]:
                    Board[Row[row]][Col[col]]="Pd"
                    Board[int(able[x][2])][int(able[x][3])]="  "
                    Passant=True

    elif len(move)==3 and move!="0-0":
        piece,col,row=move[0],move[1],move[2]
        able=wrap(Board_attack_diagram[Row[row]][Col[col]],4)
        a=0
        for x in range(len(able)):
            if piece+side in able[x]:
                a+=1
        if Board[Row[row]][Col[col]]=="  " and a==1:
            for x in range(len(able)):
                if piece+side in able[x]:
                    Board[Row[row]][Col[col]] = piece+side
                    Board[int(able[x][2])][int(able[x][3])] = "  "
                    Passant = False

    elif len(move)==4:
        piece,diference,col,row=move[0],move[1],move[2],move[3]
        able=wrap(Board_attack_diagram[Row[row]][Col[col]],4)
        a=0
        for x in range(len(able)):
            if piece+side in able[x]:
                a+=1
        if Board[Row[row]][Col[col]]=="  " and a>1:
            for x in range(len(able)):
                if diference in Col:
                    b=0
                    for y in range(8):
                        if Board[y][Col[diference]]==piece+side:
                            b+=1
                    if piece+side in Board[int(able[x][2])][Col[diference]] and b==1:
                        if piece+side+able[x][2]+str(Col[diference]) in able[x]:
                            Board[Row[row]][Col[col]] = piece+side
                            Board[int(able[x][2])][int(able[x][3])] = "  "
                            Passant = False
                elif diference in Row:
                    b=0
                    for y in range(8):
                        if Board[Row[diference]][y]==piece+side:
                            b+=1
                    if piece+side in Board[Row[diference]][int(able[x][3])] and b==1:
                        if piece+side+str(Row[diference])+able[x][3] in able[x]:
                            Board[Row[row]][Col[col]] = piece+side
                            Board[int(able[x][2])][int(able[x][3])] = "  "
                            Passant = False
    elif move == "0-0":
        if side=="w":
            ene = "d"
            row = 0
            d = 1
        else:
            ene = "w"
            row = 7
            d = 2
        if Castle_Detectors[d]==True:
            if Board[row][6]=="  " and Board[row][5]=="  ":
                if ene not in Board_attack_diagram[row][6] and ene not in Board_attack_diagram[row][5]:
                    Board[row][6]="K"+side
                    Board[row][4]="  "
                    Board[row][5]="R"+side
                    Board[row][7]="  "

    elif move == "0-0-0":
        print(1)
        if side=="w":
            ene = "d"
            row = 0
            d = 0
        else:
            ene = "w"
            row = 7
            d = 3
        if Castle_Detectors[d]==True:
            if Board[row][2]=="  " and Board[row][3]=="  " and Board[row][1]=="  ":
                if ene not in Board_attack_diagram[row][2] and ene not in Board_attack_diagram[row][3]:
                    Board[row][2]="K"+side
                    Board[row][4]="  "
                    Board[row][3]="R"+side
                    Board[row][0]="  "
def Moviments_Attack(move,side):
    global Board,Board_attack_diagram,Passant
    if side=="w":
        ene="d"
    else:
        ene="w"
    if len(move)==4:
        piece,col,row=move[0],move[2],move[3]
        able=wrap(Board_attack_diagram[Row[row]][Col[col]],4)
        if piece in Col:
            piece="P"
        if piece in Pieces:
            a=0
            for x in range(len(able)):
                if piece+side in able[x]:
                    a+=1
                if a==1 and ene in Board[Row[row]][Col[col]]:
                    for x in range(len(able)):
                        if piece+side in able[x]:
                            Board[Row[row]][Col[col]] = piece+side
                            Board[int(able[x][2])][int(able[x][3])] = "  "
                            Passant = False
        else:
            if ene in Board[Row[row]][Col[col]]:
                for x in range(len(able)):
                    if piece+side in able[x]:
                        Board[Row[row]][Col[col]] = piece+side
                        Board[int(able[x][2])][Col[move[0]]] = "  "
                        Passant = False
            elif Passant==True:
                for x in range(len(able)):
                    if piece+side in able[x]:
                        if col+row == list[-2][0]+str(int(list[-2][1])+1):
                            Board[Row[row]][Col[col]] = piece+side
                            Board[Row[list[-2][1]]][Col[list[-2][0]]]="  "
                            Board[int(able[x][2])][Col[move[0]]] = "  "
                            Passant = False
                        elif col+row == list[-2][0]+str(int(list[-2][1])-1):
                            Board[Row[row]][Col[col]] = piece+side
                            Board[Row[list[-2][1]]][Col[list[-2][0]]]="  "
                            Board[int(able[x][2])][Col[move[0]]] = "  "
                            Passant = False
    elif len(move)==5:
        piece,diference,col,row=move[0],move[1],move[3],move[4]
        able=wrap(Board_attack_diagram[Row[row]][Col[col]],4)
        a=0
        for x in range(len(able)):
            if piece+side in able[x]:
                a+=1
        if ene in Board[Row[row]][Col[col]] and a>1:
            for x in range(len(able)):
                if diference in Col:
                    b=0
                    for y in range(8):
                        if Board[y][Col[diference]]==piece+side:
                            b+=1
                    if piece+side in Board[int(able[x][2])][Col[diference]] and b==1:
                        if piece+side+able[x][2]+str(Col[diference]) in able[x]:
                            Board[Row[row]][Col[col]] = piece+side
                            Board[int(able[x][2])][int(able[x][3])] = "  "
                            Passant = False
                elif diference in Row:
                    b=0
                    for y in range(8):
                        if Board[Row[diference]][y]==piece+side:
                            b+=1
                    if piece+side in Board[Row[diference]][int(able[x][3])] and b==1:
                        if piece+side+str(Row[diference])+able[x][3] in able[x]:
                            Board[Row[row]][Col[col]] = piece+side
                            Board[int(able[x][2])][int(able[x][3])] = "  "
                            Passant = False
def Detect_special_moviments(side):
    global Board,Board_attack_diagram,Castle_Detectors,list_moviments,Check_w,Check_d,Mate
    if Castle_Detectors[0]==True:
        if Board[0][0]=="  " or Board[0][4]=="  ":
            Castle_Detectors[0]= False

    if Castle_Detectors[1]==True:
        if Board[0][7]=="  " or Board[0][4]=="  ":
            Castle_Detectors[1]= False

    if Castle_Detectors[2]==True:
        if Board[7][7]=="  " or Board[7][4]=="  ":
            Castle_Detectors[2]= False

    if Castle_Detectors[3]==True:
        if Board[7][0]=="  " or Board[7][4]=="  ":
            Castle_Detectors[3]= False

    if "Pw" in Board[7] or "Pd" in Board[0]:
        for x in range(0,8):
            if Board[7][x]=="Pw":
                piece=input("Choose a piece Q,B,N,R\n")
                Board[7][x]=piece+side
            if Board[0][x]=="Pd":
                piece=input("Choose a piece Q,B,N,R\n")
                Board[0][x]=piece+side

    for i in range(8):
        for j in range(8):
            if Board[i][j]== "Kw":
                if "d" in Board_attack_diagram[i][j]:
                    Check_w=True
                    print("Check")
                    m=0
                    for x in range(-1,2):
                        for y in range(-1,2):
                            if 0<=i+x<=7 and 0<=j+y<=7:
                                if x==0 and y==0:
                                    continue
                                if "d" in Board_attack_diagram[i+x][j+y] or "w"in Board[i+x][j+y]:
                                    if "w"in Board_attack_diagram[Row[list[-1][-1]]][Col[list[-1][-2]]]:
                                        m=1
                                    else:
                                        continue
                                else:
                                    m=1
                    if m==0:
                        print("Mate")
                    Mate=True
                else:
                    Check_w=False

            if Board[i][j]== "Kd":
                if "w" in Board_attack_diagram[i][j]:
                    Check_d=True
                    print("Check")
                    m=0
                    for x in range(-1,2):
                        for y in range(-1,2):
                            if 0<=i+x<=7 and 0<=j+y<=7:
                                if x==0 and y==0:
                                    continue
                                if "w" in Board_attack_diagram[i+x][j+y] or "d"in Board[i+x][j+y]:
                                    if "d"in Board_attack_diagram[Row[list[-1][-1]]][Col[list[-1][-2]]]:
                                        m=1
                                    else:
                                        continue
                                else:
                                    m=1
                    if m==0:
                        print("Mate")
                        Mate=True
                else:
                    Check_d=False
spawn()
Board_attack_refresh()
king_move()
while True:
    save=[[Board[i][j] for j in range(0,8)]for i in range(0,8)]
    if c%2==0:
        side="w"
    else:
        side="d"
    Board_attack_refresh()
    king_move()
    move=input()
    if move == "stop":
        break

    list.append(move)
    if "x" in move:
        if move[1]=="x" or move[2]=="x":
            Moviments_Attack(move,side)
    else:
        Moviments_Normal(move,side)

    Board_attack_refresh()
    king_move()
    Detect_special_moviments(side)

    if side=="d" and Check_d==True:
        print("King dark in check")
        Board=save
    elif side=="w" and Check_w==True:
        print("King white in check")
        Board=save
    for i in range(7,-1,-1):
        print(Board[i])
    if save==Board:
        print("erro")
        continue
    if Mate==True:
        break
    c+=1
