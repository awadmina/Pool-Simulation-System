import sys
import cgi
import os
import glob
import math
import phylib
import Physics
import re
import json
from datetime import datetime
import random 
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;

globalCurrentGameName = None
globalCurrentShooter = None
globalPlayerHigh = None
globalPlayerLow = None
globalBallsHighLeft = list(range(9, 16)) 
globalBallsLowLeft = list(range(1, 8)) 
globalGame = Physics.Game 
globalTable = Physics.Table
globalSvgArray = []
globalPlayer1Name = None
globalPlayer2Name = None

# http://localhost:5534/start.html  

class MyHandler(BaseHTTPRequestHandler):
    global globalCurrentGameName, globalCurrentShooter, globalPlayerHigh, globalPlayerLow, globalBallsHighLeft, globalBallsLowLeft, globalGame, globalTable, globalSvgArray

    def do_GET(self):
        global globalCurrentGameName, globalCurrentShooter, globalPlayerHigh, globalPlayerLow, globalBallsHighLeft, globalBallsLowLeft, globalGame, globalTable, globalSvgArray, globalPlayer1Name, globalPlayer2Name
        parsed = urlparse(self.path)
        
        if parsed.path in ['/start.html']:
        
            fp = open('.'+parsed.path)
            content = fp.read();

            self.send_response( 200 ); 
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
            
        elif parsed.path.startswith('/anime.js'):
       
            filepath = '.' + parsed.path  
            if os.path.isfile(filepath):
             
                with open(filepath, 'rb') as file:
                    self.send_response(200)  # OK
                    self.send_header('Content-type', 'application/javascript')
                    self.end_headers()
                    self.wfile.write(file.read())
        
        elif parsed.path in ['/animationTable']:
        
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(globalSvgArray).encode('utf-8'))  
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )   
        
    def do_POST(self):

        global globalCurrentGameName, globalCurrentShooter, globalPlayerHigh, globalPlayerLow, globalBallsHighLeft, globalBallsLowLeft, globalGame, globalTable, globalSvgArray, globalPlayer1Name, globalPlayer2Name
        
        parsed  = urlparse( self.path );
        if parsed.path in [ '/start.html' ]:
            
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   ); 
        
            globalCurrentGameName = "Game " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            globalPlayer1Name = form.getvalue('player1Name')
            globalPlayer2Name = form.getvalue('player2Name')
            
            globalTable = initTable()  
           
            globalGame = Physics.Game(gameName=globalCurrentGameName, player1Name=globalPlayer1Name, player2Name=globalPlayer2Name)

            #decide who shoots first
            globalCurrentShooter = random.choice([globalPlayer1Name, globalPlayer2Name])
            
            #generate the SVG string for the initial table
            startingSVGString = globalTable.svg()
            
            if globalCurrentShooter == globalPlayer1Name:
                globalCurrentShooter = globalPlayer2Name
            elif globalCurrentShooter == globalPlayer2Name:
                globalCurrentShooter = globalPlayer1Name

            # http://localhost:5534/start.html
            htmlContent = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>POOL TABLE GAME</title>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
                <script src="anime.js"></script> <!-- Ensure this is after jQuery -->
                <style>
                    body {{
                        background-color: #f0f0f0;
                        font-family: Arial, sans-serif;
                        text-align: center;
                    }}
                    h1, h2 {{
                        color: #336699;
                    }}
                    p {{
                        color: #555;
                    }}
                    .container {{
                        margin: 0 auto;
                        max-width: 800px;
                        padding: 20px;
                        background-color: #fff;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    .table-image {{
                        width: 100%;
                        border-radius: 50px;
                        margin-bottom: 20px;
                        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                    }}
                    .table-image + .table-image {{
                        margin-top: 20px;
                    }}
                    a {{
                        text-decoration: none;
                        color: #336699;
                        font-weight: bold;
                    }}
                    .btn {{
                        background-color: #4CAF50; /* Green */
                        border: none;
                        color: white;
                        padding: 15px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        transition-duration: 0.4s;
                        cursor: pointer;
                        border-radius: 8px;
                        box-shadow: -4px 4px #999;
                    }}
                    .btn:hover {{
                        background-color: #507963;
                        box-shadow: -2px 2px #182820;
                    }}
                    
                    table {{
                        margin: 20px auto;
                        border-collapse: collapse;
                        width: 100%;
                    }}
                    th, td {{
                        padding: 8px;
                        text-align: center;
                        border-bottom: 1px solid #ddd;
                    }}
                    th {{
                        background-color: #336699;
                        color: white;
                    }}
                    .btn {{
                        background-color: #336699;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        text-decoration: none;
                        font-size: 16px;
                    }}
                    .btn:hover {{
                        background-color: #23527c;
                    }}
                    ul {{
                        list-style-type: none;
                    }}
                    li {{
                        margin-bottom: 5px;
                        color: #555; 
                    }}
                    #svg-container {{
                    }}
                </style>
            </head>
            <body">
            <div class="container">
                <h1 style="color:#336699;">STRIKE WITH PRECISION, CONQUER THE TABLE'S MISSION!</h1>
                <p>Take aim, perfect your shot, and dominate the game!</p>
                <h2>Table:</h2>
                <!-- Player names placeholders -->
                <div id="player1Name" style="margin-bottom: 20px;">Player 1: {globalPlayer1Name}</div>
                <div id="player2Name" style="margin-bottom: 20px;">Player 2: {globalPlayer2Name}</div>
                <div id="firstShooter" style="font-weight: bold; margin-bottom: 20px;">Turn: {globalCurrentShooter}</div>
                
                <div id="svg-container">
                    {startingSVGString}
                </div>
                
            </body>
            </html>
            """
            # http://localhost:5534/start.html 
            
            self.send_response(200)  
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", str(len(htmlContent)))
            self.end_headers()
            
            self.wfile.write(bytes(htmlContent, "utf-8"))
            
        elif parsed.path == '/cueVels':
            content_length = int(self.headers['Content-Length'])  
            post_data = self.rfile.read(content_length)  
            
            data = json.loads(post_data.decode('utf-8'))  
            
            #get velocity
            velocityX = data.get('velocityX')
            velocityY = data.get('velocityY')
            
            # Update the table 
            cueBall = globalTable.cueBall(globalTable)
            if not cueBall:
                print("Error, Cue Ball not Found in cueVels post request")
                return None
            
            xPos, yPos = cueBall.obj.still_ball.pos.x, cueBall.obj.still_ball.pos.y
            
            cueBall.type = phylib.PHYLIB_ROLLING_BALL
            
            #Add the positions and velocities to the new rolling cueball
            cueBall.obj.rolling_ball.pos.x, cueBall.obj.rolling_ball.pos.y = xPos, yPos
            cueBall.obj.rolling_ball.vel.x, cueBall.obj.rolling_ball.vel.y = velocityX, velocityY    
            #Add the ball number to the new rolling ball
            cueBall.obj.rolling_ball.number = 0  
               
            speedRB = math.sqrt((velocityX * velocityX) + (velocityY * velocityY))    
            
            # Calculate acceleration
            if speedRB > Physics.VEL_EPSILON:
                cueBall.obj.rolling_ball.acc.y = ((velocityX / speedRB) * -1) * Physics.DRAG 
                cueBall.obj.rolling_ball.acc.x = ((velocityX / speedRB) * -1) * Physics.DRAG 
            else:
                cueBall.obj.rolling_ball.acc.y = 0.0
                cueBall.obj.rolling_ball.acc.x = 0.0                  
            
            globalSvgArray.append(globalTable.svg())    
            while globalTable is not None:

                newTable = globalTable.segment()
                
                if newTable is None:
                    break                
                globalSvgArray.append(newTable.svg())
                globalTable = newTable
            
            # Respond to the client
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {'status': 'success'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
                
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )             
            # http://localhost:5534/start.html     
##################################################################################################################################################################################################################

def initTable():
    table = Physics.Table()

    balls = [
                Physics.Coordinate(675, 2025), # Cue Ball White 0
                Physics.Coordinate(675, 675),  # Yellow 1
                Physics.Coordinate(645, 622),  # Blue 2
                Physics.Coordinate(614, 569),  # Red 3
                Physics.Coordinate(584, 516),  # Purple 4  
                Physics.Coordinate(797, 463),  # Orange 5
                Physics.Coordinate(614, 463),  # Green 6          
                Physics.Coordinate(706, 516),  # Brown 7
                Physics.Coordinate(675, 569),  # Black 8
                Physics.Coordinate(706, 622),  # Light Yellow 9
                Physics.Coordinate(736, 569),  # Light Blue 10
                Physics.Coordinate(767, 516),  # Pink 11
                Physics.Coordinate(553, 463),  # Medium Purple 12
                Physics.Coordinate(736, 463),  # Light Salmon 13
                Physics.Coordinate(645, 516),  # Light Green 14
                Physics.Coordinate(675, 463),  # Sandy Brown 15
                ]
         
    for ballNum in range(len(balls)):
        table += Physics.StillBall(ballNum, balls[ballNum])        
    
    return table     
####################################################################################################################################################################################################################################################################   
def resetGameTable():
    global globalCurrentGameName, globalCurrentShooter, globalPlayerHigh, globalPlayerLow, globalBallsHighLeft, globalBallsLowLeft, globalGame, globalTable, globalSvgArray, globalPlayer1Name, globalPlayer2Name
    globalCurrentGameName = None
    globalCurrentShooter = None
    globalPlayerHigh = None
    globalPlayerLow = None
    globalBallsHighLeft = list(range(9, 16))
    globalBallsLowLeft = list(range(1, 8))   
    globalGame = None
    globalTable = None
    globalSvgArray = []
    globalPlayer1Name = None
    globalPlayer2Name = None
    print("GLOBAL VARIABLES RESET")


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();

# http://localhost:5534/start.html


