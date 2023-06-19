# Person Video Tracking 📹

This project is a Python algorythm who identify people on a video, track them and detect if they cross a line and in witch direction

## Summary

A Python algorithm allowing to count people crossing a line on a video, with this differents steps : 

- 1 configure a line from a json file which will contain its coordinates as well as a link to a video which will be the support of our algorithm

- 2 Play video

- 3 detect the persons present on the video

- 4 track these people in order to extract their trajectories

- 5 analyze these trajectories in relation to the line defined previously to determine whether the person has crossed it or not

- 6 increment a counter on the image that will display the number of people who have crossed the line as the video progresses

### Details :

There is an interest zone around the line represented by a blue rectangle, the algorithm only detect the people in this zone to save ressources

There are 3 counters : 

- 🟪 The purple : Count people who cross the line from the bottom

- 🟨 The Yellow : Count people who cross the line from the top

- ⬜ The White : Total count of the people crossing the line

## Requirements

The algorythm need Python and many libraries to work, 
If it's not already done :
 
👉[ Install Python ](https://https://www.python.org/downloads/)👈

You also need an Internet Connexion to run the program for the first time and load the model 



## Install ⬇️

 First of all, you have to clone the project :

```bash
> git clone https://github.com/RaphaelGuarim/VideoTracker
```

Then, go to the project folder

```bash
> cd VideoTracker
`````
Now, you are in the project.

### Download the Libraries : 

Run the requirements.txt by this command :

```bash
> pip install -r requirements.txt
```

Now refresh your code editor and we can run the project ! 


## Run the project ⚡

Open the main.py file and run it by clicking play

Or run by the command :

```bash
> python main.py
```


## Now see the result !
