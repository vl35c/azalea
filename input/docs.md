# KeyboardHandler

The KeyboardHandler deals with keyboard input, sending it to the required functions

### PROPERTIES
`children` - the objects that the KeyboardHandler is working with

### METHODS
`add_child(self, obj: Any)` - adds an object to the list of children\
\
`obj` - the object to be added to the list of children

---
`key_down_with_child(event: object, child: Any)` - takes a key input and calls the child to handle the event\
\
`child` - the child object to handle the event\
`event` - the event object from pygame when a key is pressed

---

# MouseHandler

The MouseHandler deals with mouse input, currently only the holding of the mouse

### PROPERTIES
`obj` - the object that the mouse clicked on\
`pos` - position of the mouse when it was clicked\
`x` - the x coordinate of the mouse's position\
`y` - the y coordinate of the mouse's position

### METHODS
`click(self, obj: Any)` - store the object and position of the mouse click\
\
`obj` - can be any object that the mouse clicked on

---
`release(self)` - resets the mouse and removes the object and position

---
