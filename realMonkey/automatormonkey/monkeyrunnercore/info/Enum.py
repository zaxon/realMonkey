class UIELEMENT:
    TEXT = 'Text'
    CLASSNAME = 'ClassName'
    INDEX = 'Index'
    DESC = 'Description'
    
class DIRECTION:
    UP = 'Up'
    DOWN = 'Down'
    LEFT = 'Left'
    RIGHT = 'Right'
    
class LIST:
    VERTICAL = True #vertical found element or horizontal found element
    
class FLAG:
    SCREENSHOT = True #Whether you need screenshot after each of the steps
    PASSMATCH = 0
    REAMINMATCH = 0
    
class INFO:
    STEP=0
    DEVICE = None
    DEVICENAME = None
    PATH = None
    PICNAME = None
    

class PROPERTY:
    DISPLAYWIDTH = 'displayWidth'
    DISPLAYHEIGHT = 'displayHeight'
    CURRENTPACKAGE = 'currentPackageName'


