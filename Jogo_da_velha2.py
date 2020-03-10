Col={"a":0,"b":1,"c":2}
Row={"1":0,"2":1,"3":2}

class tic_tac():
    board=[[" "for i in range(3)]for j in range(3)]
    def play(self,side):
        if side%2==0:
            move="X"
        else:
            move="O"

        self.m=input()
        col,row=self.m[:2]
        if col in Col and row in Row:
            if self.board[Row[row]][Col[col]]==" ":
                self.board[Row[row]][Col[col]]=move
                return True
        else:
            print("Write like this 'a3'!")

    def print(self):
        for i in range(2,-1,-1):
            print(self.board[i])

    def win(self):
        b=self.board
        if b[0][0]==b[1][0] and b[1][0]==b[2][0] and b[0][0]==b[2][0] and b[0][0]!= " ":
            print("%s ganhou" %b[0][0])
            return True
        if b[0][1]==b[1][1] and b[1][1]==b[2][1] and b[0][1]==b[2][1] and b[0][1]!= " ":
            print("%s ganhou" %b[0][1])
            return True
        if b[0][2]==b[1][2] and b[1][2]==b[2][2] and b[0][2]==b[2][2] and b[0][2]!= " ":
            print("%s ganhou" %b[0][2])
            return True

        if b[0][0]==b[0][1] and b[0][1]==b[0][2] and b[0][2]==b[0][0] and b[0][0]!= " ":
            print("%s ganhou" %b[0][0])
            return True
        if b[1][0]==b[1][1] and b[1][1]==b[1][2] and b[1][2]==b[1][0] and b[1][0]!= " ":
            print("%s ganhou" %b[1][0])
            return True
        if b[2][0]==b[2][1] and b[2][1]==b[2][2] and b[2][2]==b[2][0] and b[2][0]!= " ":
            print("%s ganhou" %b[2][0])
            return True

        if b[0][0]==b[1][1] and b[1][1]==b[2][2] and b[0][0]==b[2][2] and b[0][0]!= " ":
            print("%s ganhou" %b[0][0])
            return True
        if b[2][0]==b[1][1] and b[1][1]==b[0][2] and b[0][2]==b[2][0] and b[2][0]!= " ":
            print("%s ganhou" %b[0][0])
            return True
c=0
while True:
    c+=1
    if tic_tac().play(c)!=True:
        print("Impossible move")
        c-=1
    tic_tac().print()
    if tic_tac().win()==True or c==9:
        break
