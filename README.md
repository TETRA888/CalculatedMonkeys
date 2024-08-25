# This is a simple script that randomly assigns colors to the faces of "Suzzane" the monkey from Blender
## The way it works is quite simple, here are the steps:
### 1. We initially, generate the monkey mesh using primitive Blender-Python operations
### 2. Next, we select the individual mesh and iterate through the faces using a library called BMesh, this essentially provides easier mesh handling
### 3. We then randomly assign the color to that face and thats it!

## Now as for the VR headset, well...
### 1. The same primitive mesh generation principles are used to create an overall mesh that looks like a VR headset

## To position the monkeys, its pretty simple highschool math
### 1. you calculate the x and y coordinates using sines and cosines
![trig2_2](https://github.com/user-attachments/assets/a0d3fe68-8b7a-4156-9b19-0bc6bc4cdb2c)
### 2. Additionally, you can tweak a few parameters such as the radius and the number of steps or "jumps" on the unit circle
### 3. to calculate these steps its pretty simple you just use the formula: angle_increment = 𝜏/steps which essentially just means you divide a 360 degree circle into n steps 
### and increment the angle based on the angle_increment
### 4. Finally, once the x and y coordinates are calculated, you simple position the monkey in that position.

## However, you also need to make sure that the monkey faces away from the center otherwise your generated mesh would just look like this:
![image](https://github.com/user-attachments/assets/6ae70226-b119-48b9-84de-040456d2b77a)
### 1. To correct for this, I found that you can assign the Z-axis rotation of the monkey mesh to the (current angle + π/2), after doing so you get this:
![image](https://github.com/user-attachments/assets/fe0becde-1a84-4119-8bcc-1e49d53aaef9)



