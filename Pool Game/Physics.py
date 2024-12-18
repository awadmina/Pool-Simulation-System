import phylib;
import sqlite3;
import os;
import math;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

#added
FRAME_RATE = 0.01;

# add more here
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""
FOOTER = """</svg>\n"""

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];


################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here

    def svg(self):
        return """ <circle id="%s_Ball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (BALL_COLOURS[self.obj.still_ball.number], self.obj.still_ball.pos.x,
                                                                       self.obj.still_ball.pos.y,
                                                                       BALL_RADIUS,
                                                                       BALL_COLOURS[self.obj.still_ball.number])

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """
    def __init__( self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;

    def svg(self):
         return """ <circle id="%s_Ball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (BALL_COLOURS[self.obj.rolling_ball.number], self.obj.rolling_ball.pos.x,
                                                                       self.obj.rolling_ball.pos.y,
                                                                       BALL_RADIUS,
                                                                       BALL_COLOURS[self.obj.rolling_ball.number])

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """
    def __init__( self, pos):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE_BALL, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;

    def svg(self):
        return f'<circle cx="{self.obj.hole.pos.x}" cy="{self.obj.hole.pos.y}" r="{HOLE_RADIUS}" fill="black" />'


class HCushion(phylib.phylib_object):
    """
    Python HCushion class.
    """
    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCushion_BALL, 
                                       None, 
                                       None, None, None, 
                                       None, 0.0 );
      
        # this converts the phylib_object into a HCushion class
        self.__class__ = HCushion;


    def svg(self):
        y = self.obj.hcushion.y  # Access y-coordinate directly

        # Determine cushion type based on y-coordinate
        if y == 0:
            yStr = "-25"  # Top cushion
        elif y == TABLE_LENGTH:
            yStr = "2700"  # Bottom cushion
            
        return f'<rect width="1400" height="25" x="-25" y="{yStr}" fill="darkgreen" />'

class VCushion(phylib.phylib_object):
    """
    Python VCushion class.
    """
    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCushion_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, None );
      
        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;
    
    def svg(self):
        x = self.obj.vcushion.x  # Access x-coordinate directly

        # Determine cushion type based on x-coordinate
        if x == 0:
            xStr = "-25"  # Left cushion
        elif x == TABLE_WIDTH:
            xStr = "1350"  # Right cushion

        return f'<rect width="25" height="2750" x="{xStr}" y="-25" fill="darkgreen" />'


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        """
        Returns SVG code for the entire table, including all objects.
        """
        svgStrg = HEADER

        #loop through all objects in the table and create their svg file then its sent through the method
        for obj in self:
            if obj:
                svgStrg += obj.svg();
                
        svgStrg += FOOTER
        return svgStrg

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;

            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                      Coordinate( ball.obj.still_ball.pos.x,
                                                  ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;

        # return table
        return new;
    
    def cueBall(self, table):
        for ball in table:
            
            #If its a rolling or still ball and it's number is 0
            if (isinstance(ball, StillBall) or isinstance(ball, RollingBall)) and (ball.obj.still_ball.number == 0 or ball.obj.rolling_ball.number == 0):
                    return ball
        return None

    def initTable(self):

        balls = [
                Coordinate(675, 2025), # Cue Ball (White) 0
                Coordinate(675, 675),  # Yellow 1
                Coordinate(645, 622),  # Blue 2
                Coordinate(614, 569),  # Red 3
                Coordinate(584, 516),  # Purple 4  
                Coordinate(797, 463),  # Orange 5
                Coordinate(614, 463),  # Green   6          
                Coordinate(706, 516),  # Brown 7
                Coordinate(675, 569),  # Black  8
                Coordinate(706, 622),  # Light Yellow 9
                Coordinate(736, 569),  # Light Blue 10
                Coordinate(767, 516),  # Pink 11
                Coordinate(553, 463),  # Medium Purple 12
                Coordinate(736, 463),  # Light Salmon 13
                Coordinate(645, 516),  # Light Green 14
                Coordinate(675, 463),  # Sandy Brown 15
        ]

        for i in range(len(balls)):
            self += StillBall(i, balls[i])

        return self

class Database():


    def __init__( self, reset=False ):

        self.conn = None
        if reset and os.path.exists("phylib.db"):
            os.remove("phylib.db")
        
        self.conn = sqlite3.connect("phylib.db")
        self.cursor = self.conn.cursor()

    def createDB(self):
        
        # Create the BALL table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS BALL
                        ( BALLID    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        BALLNO   INTEGER NOT NULL,
                        XPOS  FLOAT NOT NULL,
                        YPOS    FLOAT NOT NULL,
                        XVEL    FLOAT,
                        YVEL    FLOAT
                        )""")

        # Create the TTABLE table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS TTABLE
                        ( TABLEID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        TIME   FLOAT NOT NULL
                        )""")

        # Create the BALLTABLE table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS BALLTABLE
                        ( BALLID INTEGER NOT NULL,
                        TABLEID INTEGER NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES BALL(BALLID),
                        FOREIGN KEY (TABLEID) REFERENCES TTABLE(TABLEID)
                        )""")

        # Create the SHOT table 
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS SHOT
                        ( SHOTID    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        PLAYERID    INTEGER NOT NULL,
                        GAMEID    INTEGER NOT NULL,
                        FOREIGN KEY (PLAYERID) REFERENCES PLAYER(PLAYERID),
                        FOREIGN KEY (GAMEID) REFERENCES GAME(GAMEID)
                        )""")

        # Create the TABLESHOT table 
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS TABLESHOT
                        ( TABLEID   INTEGER NOT NULL,
                        SHOTID   INTEGER NOT NULL,
                        FOREIGN KEY (TABLEID) REFERENCES TTABLE(TABLEID),
                        FOREIGN KEY (SHOTID) REFERENCES SHOT(SHOTID)
                        )""")

        # Create the GAME table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS GAME
                        ( GAMEID    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMENAME   VARCHAR(64) NOT NULL
                        )""")

        # Create the PLAYER table 
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS PLAYER
                        ( PLAYERID    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMEID   INTEGER NOT NULL,
                        PLAYERNAME  VARCHAR(64) NOT NULL,
                        FOREIGN KEY (GAMEID) REFERENCES GAME(GAMEID)
                        )""")

    def readTable(self, tableID):
        self.conn = sqlite3.connect("phylib.db")
        self.cursor = self.conn.cursor()

        tableID_adjusted = tableID + 1  
        try:
            print("Reading table with ID:", tableID_adjusted)
            # self.conn = sqlite3.connect("phylib.db")  
            # self.cursor = self.conn.cursor()  
         
        
            self.cursor.execute("""
                SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, 
                    Ball.XVEL, Ball.YVEL, TTable.TIME
                FROM Ball
                INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                INNER JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
                WHERE BallTable.TABLEID = ?
            """, (tableID_adjusted,))

            rows = self.cursor.fetchall()

            if not rows:
                return None 

            table = Table()
            table.time = rows[0][6] 

            for row in rows:
                ball_id, ball_no, xpos, ypos, xvel, yvel = row[:6]

                if xvel is None or yvel is None:  
                    ball = StillBall(ball_no, Coordinate(xpos, ypos))
                else:  
                    
                    vel = math.sqrt(xvel*xvel + yvel*yvel)
                    if (vel > VEL_EPSILON):
                        xacc = (-1*xvel) / vel * DRAG
                        yacc = (-1*yvel) / vel * DRAG
                        acc = Coordinate(xacc, yacc)
                    else:
                        acc = Coordinate(0.0, 0.0)
                    ball = RollingBall(ball_no, Coordinate(xpos, ypos), Coordinate(xvel, yvel), acc)

                table += ball  
            print("Table read successfully:", table)
            return table

        except sqlite3.Error as e:
            print(f"Error reading table: {e}")
            return None  

        finally:
            self.cursor.close()  
            self.conn.commit()    


    def writeTable(self, table):
           
            try:
                self.conn = sqlite3.connect("phylib.db")  
                self.cursor = self.conn.cursor() 
                
    
                self.cursor.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
                table_id = self.cursor.lastrowid 

                for ball in table:
                    if isinstance(ball, StillBall) or isinstance(ball, RollingBall):
                        if isinstance(ball, StillBall):
                            self.cursor.execute("""
                                INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                                VALUES (?, ?, ?, 0.0, 0.0)
                            """, (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y))
                        else:
                            self.cursor.execute("""
                                INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                                VALUES (?, ?, ?, ?, ?)
                            """, (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))

                        ball_id = self.cursor.lastrowid
                        self.cursor.execute("""
                            INSERT INTO BallTable (BALLID, TABLEID) 
                            VALUES (?, ?)
                        """, (ball_id, table_id))
                return table_id - 1
            
            
            except sqlite3.Error as e:
                print(f"Error writing table: {e}")
                return None  
            
            finally:
                self.cursor.close() 
                self.conn.commit()

    def close(self):
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error committing changes: {e}")

        finally:
            self.conn.close()

        
    def getGame(self, gameID):
           
            try:
                self.cursor.execute("""
                    SELECT Game.GAMENAME, Player1.PLAYERNAME as player1Name, Player2.PLAYERNAME as player2Name,
                    Player1.PLAYERID as player1ID, Player2.PLAYERID as player2ID
                    FROM Game 
                    INNER JOIN Player Player1 ON Game.GAMEID = Player1.GAMEID
                    INNER JOIN Player Player2 ON Game.GAMEID = Player2.GAMEID
                    WHERE Game.GAMEID = ?
                """, (gameID,))

                row = self.cursor.fetchone()
                if row:
                    return dict(zip(['gameName', 'player1Name', 'player2Name', 'player1ID', 'player2ID'], row))
                else:
                    return None

            except sqlite3.Error as e:
                print(f"Error retrieving game data: {e}")
                return None

            finally:
                self.cursor.close()
                self.conn.commit()

    # def setGame(self, gameName, player1Name, player2Name):
    #     self.conn = sqlite3.connect("phylib.db")
    #     self.cursor = self.conn.cursor()

    #     try:
    #         with self.conn:  


    #            self.cursor.execute("SELECT * from PLAYER")
    #            rows = self.cursor.fetchall()
       
    #            column_names = [description[0] for description in self.cursor.description]
    #            print("\t".join(column_names))

    #            for row in rows:
    #               print("\t".join(map(str, row)))
    #               print('--------------------------')
    #            self.cursor.execute("INSERT INTO GAME (GAMENAME) VALUES (?)", (gameName,))
    #            game_id = self.cursor.lastrowid

    #            self.cursor.execute("INSERT INTO PLAYER (GAMEID, PLAYERNAME) VALUES (?, ?)", (game_id, player1Name))
    #            self.cursor.execute("INSERT INTO PLAYER (GAMEID, PLAYERNAME) VALUES (?, ?)", (game_id, player2Name))
    #            return game_id

    #     except sqlite3.Error as e:
    #         print(f"Error creating new game: {e}")
    #         raise  

    #     finally:
    #         self.cursor.close()
    #         self.conn.commit()

    def setGame(self, gameName, player1Name=None, player2Name=None):
        self.conn = sqlite3.connect("phylib.db")
        self.cursor = self.conn.cursor()

        try:
            with self.conn:
                self.cursor.execute("INSERT INTO GAME (GAMENAME) VALUES (?)", (gameName,))
                game_id = self.cursor.lastrowid

                if player1Name is not None:
                    self.cursor.execute("INSERT INTO PLAYER (GAMEID, PLAYERNAME) VALUES (?, ?)", (game_id, player1Name))
                if player2Name is not None:
                    self.cursor.execute("INSERT INTO PLAYER (GAMEID, PLAYERNAME) VALUES (?, ?)", (game_id, player2Name))

                return game_id

        except sqlite3.Error as e:
            print(f"Error creating new game: {e}")
            raise

        finally:
            self.cursor.close()
            self.conn.commit()

    
    def get_player_id(self, gameName, playerName):
        try:
            self.conn = sqlite3.connect("phylib.db")
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                SELECT PLAYER.PLAYERID
                FROM PLAYER
                INNER JOIN GAME ON PLAYER.GAMEID = GAME.GAMEID
                WHERE GAME.GAMENAME = ? AND PLAYER.PLAYERNAME = ?
            """, (gameName, playerName))

            row = self.cursor.fetchone()
            if row:
                return row[0]
            else:
                return None 
        except sqlite3.Error as e:
            print(f"Error retrieving player ID: {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.commit()
   

    def newShot(self, gameName, playerID):
        try:
            self.conn = sqlite3.connect("phylib.db")
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
            SELECT GAMEID
            FROM GAME
            WHERE GAMENAME = ?
            """, (gameName,))
            row = self.cursor.fetchone()
            if row:
                gameID = row[0]
            else:
                gameID = None
            
            if gameID is not None:
                self.cursor.execute("""
                INSERT INTO Shot (PLAYERID, GAMEID) 
                VALUES (?, ?)
                """, (playerID, gameID))
                return self.cursor.lastrowid 
            else:
                print("Error: Game not found.")
                return None

        except sqlite3.Error as e:
            print(f"Error recording new shot: {e}")
            return None

        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.commit()

    def recordTableShot(self, shotID, tableID):
        try:
            self.conn = sqlite3.connect("phylib.db")
            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                INSERT INTO TableShot (SHOTID, TABLEID) 
                VALUES (?, ?)
            """, (shotID, tableID))

            # self.conn.commit() 

        except sqlite3.Error as e:
            print(f"Error recording TableShot association: {e}")
            return None

        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.commit()

    def lastTableID(self):
        try:
            self.conn = sqlite3.connect("phylib.db")
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT MAX(TABLEID) FROM TTable")
            row = self.cursor.fetchone()
            
            if row and row[0] is not None:
                return row[0]
            else:
                return None

        except sqlite3.Error as e:
            print(f"Error getting last TABLEID: {e}")
            return None

        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.commit()
        
    def printTable(self):
        # self.openDB()
        table_names = ['BALL', 'TTABLE', 'BALLTABLE', 'SHOT', 'TABLESHOT', 'GAME', 'PLAYER']
        for table in table_names:
            self.cursor.execute(f'SELECT * from {table}')
            print(f"\nTable name: {table}")
            rows = self.cursor.fetchall()
        
            column_names = [description[0] for description in self.cursor.description]
            print("\t".join(column_names))

            for row in rows:
                print("\t".join(map(str, row)))
            print('--------------------------')

    def resetDB(self):
        # self.cursor.execute("DROP TABLE IF EXISTS BALLTABLE")  
        # self.cursor.execute("DROP TABLE IF EXISTS SHOT")       
        # self.cursor.execute("DROP TABLE IF EXISTS TABLESHOT")  
        # self.cursor.execute("DROP TABLE IF EXISTS BALL")       
        # self.cursor.execute("DROP TABLE IF EXISTS TTABLE") 
        # self.cursor.execute("DROP TABLE IF EXISTS PLAYER")   
        # self.cursor.execute("DROP TABLE IF EXISTS GAME")
        if os.path.exists("phylib.db"):
            os.remove("phylib.db")


class Game():
    
        def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):

            self.conn = sqlite3.connect("phylib.db")
            self.cursor = self.conn.cursor()
            self.db = Database()
            self.db.createDB()

            if gameID is not None:
                gameData = self.db.getGame(gameID)
                    
                if gameData: 
                    self.gameID, self.gameName, self.player1ID, self.player1Name, self.player2ID, self.player2Name
                else:
                    raise ValueError("gameID not found")
                        
            elif isinstance(gameName, str) and isinstance(player1Name, str) and isinstance(player2Name, str):
                self.gameID = self.db.setGame(gameName, player1Name, player2Name)
                self.gameName = gameName
                self.player1Name = player1Name
                self.player2Name = player2Name

                if not self.gameID: 
                    raise ValueError("gameID not found") 
                
            else:
                raise TypeError("Error in Game Class Constructor Parameters")
            
            # if gameID is not None and gameName is None and player1Name is None and player2Name is None: 
            #     print("IN FIRST CONSTRUCTOR")
    
            #     self.gameID1 = self.gameID + 1
            #     gameData = self.db.getGame(gameID1)
            
            #     if gameData: 
            #         self.gameName, self.player1ID, self.player1Name, self.player2ID, self.player2Name = gameData
                
            #     else:
            #         raise ValueError("gameID not found")
                
                
            # elif gameID is None and isinstance(gameName, str) and (player1Name, str) and (player2Name, str):
            #     # self.gameID = self.db.setGame(gameName, player1Name, player2Name)
            #     # self.gameID1 = self.gameID + 1
            #     self.gameID = None  #Will be set after inserting into database
            #     self.gameName = gameName
            #     self.player1Name = player1Name
            #     self.player2Name = player2Name
            #     self.db.setGame(gameName, player1Name, player2Name)



            
        def shoot(self, gameName, playerName, table, xvel, yvel):
            playerID = self.db.get_player_id(gameName, playerName)
            
            if playerID is None:
                print(f"Player {playerName} not found in game {gameName}.")
                return None

            shotID = self.db.newShot(gameName, playerID)
            if shotID is None:
                print("Failed to record the shot.")
                return None

            cue_ball = None
            
            # Search for the cue ball (ball number 0) among all balls on the table
            for ball in table:
                if isinstance(ball, StillBall) or isinstance(ball, RollingBall):
                    if ball.obj.still_ball.number == 0 or ball.obj.rolling_ball.number == 0:
                        cue_ball = ball
     
            # cueBall = table.cueBall(table)
        
            if not cueBall:
                print("Error, Cue Ball not Found")
                return None
            
                
            xPos, yPos = cueBall.obj.still_ball.pos.x, cueBall.obj.still_ball.pos.y
            
            cueBall.type = phylib.PHYLIB_ROLLING_BALL
            cueBall.obj.rolling_ball.pos.x = xPos
            cueBall.obj.rolling_ball.pos.y = yPos
            cueBall.obj.rolling_ball.vel.x = xvel
            cueBall.obj.rolling_ball.vel.y = yvel
            cueBall.obj.rolling_ball.acc.x = 0.0
            cueBall.obj.rolling_ball.acc.y = 0.0
            cueBall.obj.rolling_ball.number = 0  
                

            speed = phylib.phylib_length(cueBall.obj.rolling_ball.vel)
            if speed > VEL_EPSILON:
                cueBall.obj.rolling_ball.acc.x = -cueBall.obj.rolling_ball.acc.x / speed * DRAG
                cueBall.obj.rolling_ball.acc.y = -cueBall.obj.rolling_ball.acc.y / speed * DRAG

     
            initial_time = table.time
            segment = table.segment()
        
            while segment is not None:
                
                
                segment_length = segment.time - initial_time
                frames = int(segment_length / FRAME_RATE)

                for frame in range(frames):
                    frame_time = frame * FRAME_RATE
                    new_table = table.roll(frame_time)
                    new_table.time = initial_time + frame_time
                    table_id = self.db.writeTable(new_table)
                    self.db.recordTableShot(shotID, table_id)

                initial_time = segment.time
                table = segment
                segment = segment.segment()
                
            return shotID

            
         
            