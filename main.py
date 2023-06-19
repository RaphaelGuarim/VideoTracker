import cv2
import json
import torch
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True, trust_repo='check')
from tracker import ObjectTracker

#------ Json Extraction ------#

def read_json(file_path):
    with open('./config/conf.json', 'r') as json_file:
        conf = json.load(json_file)
        line_coords = conf['line_coo']
        video_path = conf['video_path']
        return line_coords,video_path
    
#------ Video Play ------#

def play_video(video_path,coo):
    video = cv2.VideoCapture(video_path)
    # Line points
    pt1 = (coo[0][0], coo[0][1])
    pt2 = (coo[1][0], coo[1][1])
    tracker = ObjectTracker()
    # Counter initialisation
    up=0
    down = 0
    
    while True : 
        _ , frame = video.read()
        frame = cv2.resize(frame,(1020,500))
        zone = frame[100:700, 250 : 850] # Definition of an interest zone around the line
        result = model(zone) # Import of the yolov5 model
        position=[] # Coordonate of the people detected
        
        for _, element in result.pandas().xyxy[0].iterrows(): # For every object detected
            label = int(element['class'])
            if label ==0:  # If the object is a human
                x1, y1, x2, y2 = int(element['xmin']) , int(element['ymin']), int(element['xmax']), int(element['ymax'])
                position.append([x1,y1,x2,y2]) # Add his coordonate
        move = tracker.update(position) # Update the tracker with all person of the new frame
            
        for element in move : 
            x,y,z,h,_= element
            cv2.rectangle(zone,(x,y),(z,h),(0,255,0),2) # Draw the rectangle for every person
            cross=cross_line(coo, element) 
            # Check if the element cross the line
            if (cross!=None):
                if (cross=="up"):
                    up+=1
                else:
                    down+=1
        total = up+down    
             
        cv2.rectangle(frame, (250, 100), (850, 495), (255, 0, 0), 1) # Drawing of the interest zone
        cv2.line(frame, pt1, pt2, (0, 0, 255), 2) # Draw the line
        cv2.putText(frame,str(up), (50,50), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3) # Counter of people who cross the line by the bottom
        cv2.putText(frame,str(down), (50,100), cv2.FONT_HERSHEY_PLAIN,3,(0,255,255),3) # Counter of people who cross the line by the top
        cv2.putText(frame,str(total), (50,150), cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3) # Counter of people who cross the line 
        cv2.imshow("Video", frame)
        
        if cv2.waitKey(1) == ord('q') : 
            break
    
    video.release()
    cv2.destroyAllWindows()
    
#------ Cross Line Detection ------#

def cross_line(line_coo, element_coo):
    global status # status table of the persons, their situationin relation to the line
    x1, y1, x2, y2, i= element_coo
    # Update the coordonate to the entire video
    x1+=250 
    x2+=250
    y1+=100
    y2+=100 
    # Find the center point of the person's rectangle
    centre_x = (x1 + x2) / 2
    centre_y = (y1 + y2) / 2
    check = up_line(line_coo,centre_x,centre_y)
    if (status[i]==None): # If it's the first time we check the person we define it's status
        status[i]=check
    else:
        if (status[i]!=check): # If the status change the person cross the line
            status[i]=check
            if (status[i]==1):
                return "up"
            else:
                return "down"
    return None

#------ Line distance -------#

def up_line (line_coo,x,y):
    x1, y1 = line_coo[0]
    x2, y2 = line_coo[1]
    
    # Calculate the slope and intercept of the line
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    
    # Check if the point is under or upper
    if y > (slope * x + intercept):
        return 0
    elif y < (slope * x + intercept):
        return 1
        

if __name__ == '__main__':
    coo, path = read_json("./config/conf.json")
    status= [None]*10000 # Initialisation of a big table for the status
    play_video(path,coo)
    
    