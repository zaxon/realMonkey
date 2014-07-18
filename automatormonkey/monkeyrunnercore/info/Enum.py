class UIELEMENT:
    TEXT = 'Text'
    CLASSNAME = 'ClassName'
    INDEX = 'Index'
    DESC = 'Description'
    SID = 'Resource-id'
    ENABLE = 'Enabled'
    
class DIRECTION:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'rsight'
    
class LIST:
    VERTICAL = True #vertical found element or horizontal found element
    
class FLAG:
    SCREENSHOT = True #Whether you need screenshot after each of the steps
    REAMINMATCH = 0
    SCROLLBALE = True
    
    RLVMODE = False
    SEARCH = 'Search'
    DRAG = 'Drag'
    
class INFO:
    STEP=0
    DEVICE = None
    DEVICENAME = None
    DEVICEVERSION = None
    PATH = None
    PICNAME = None
    
    SYSTEM = 'Windows'
    GREP = 'grep'

class PROPERTY:
    DISPLAYWIDTH = 'displayWidth'
    DISPLAYHEIGHT = 'displayHeight'
    CURRENTPACKAGE = 'currentPackageName'


