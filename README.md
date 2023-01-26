# Maya-Python-Tools
 Simple Python Tools for Maya

 I am making these in an effort to learn how Python is used within Maya.
 I followed [this](https://www.udemy.com/course/python-for-maya/) Udemy course by **Dhruv Govil** which was very helpful.

## Tools

#### 1. Object Rename
Adds a suffix to all visible objects in the scene. If selected=True is provided to the rename function, only the selected objects are renamed.

#### 2. Gear Creator
When an instance of gear class is generated, the user can create a new gear geometry specifying the number of teeth and length of them. Once the geometry is created, the user can modify these values as well. In order to use a UI element to create gears, use the ReusableU's GearUI class, which will create a window for the user to input the necessary values.

#### 3. Animation Tweener
This tool is used to tween keyframes in Maya to create gradual motion. Simply select a frame between two keyframes, run the ReusableUI scripts TweenerUI class, which will open a window where the user can use the slider to input a value from 1 to 100 in order to tween the animation.

#### 4. Controller Library
This tool is a UI component that lets users save selected components or the entire scene, shows the saved components, and lets the users import previously saved components into the scene.

#### 5. Lighting manager
A dockable UI tool that allows users to add any type of light, save and import lights, modify them by changing their color and intensity, and isolate any single light if needed.

#### 6. Command Line Renamer
Command Line tool that renames files found in the directory. User can specify in directory, out directory, whether they want the renamed items duplicated or simply renamed, or if they want to use regex
