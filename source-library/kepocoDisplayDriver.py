import math

class DisplayDriver:
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.max_x = width-1
        self.max_y = height-1
    
    def init_display(self):
        pass
    
    def poweroff(self):
        pass
    
    def poweron(self):
        pass
    
    def contrast(self, contrast):
        pass

    def invert(self, invert):
        pass
    
    def setModeGreyscale(self):
        raise NotImplementedError("Greyscale not supported.")
    
    def setModeMono(self):
        raise NotImplementedError("Mono not supported")
    
    def setModeTinted(self, red, green, blue):
        raise NotImplementedError("Colour tint not supported.")
    
    def setModeRGB(self):
        raise NotImplementedError("RGB not supported.")
    
    def enableVGA(self, transferBuffer):
        return NotImplemented
    
    def show(self):
        raise NotImplementedError("Rendering not supported")

    def brightness(self,setting):
        pass

    @micropython.native
    def fill(self, colour:int):
        self.drawFilledRectangle(0, 0, self.width, self.height, colour)
    
    @micropython.native
    def drawFilledEllispe(self, x:int, y:int, width:int, height:int, colour:int):
        a = (width)/2
        b = (height)/2
        if width < height:
            vline = self.drawVLine
            b+=0.5
            for _x in range(width//2):
                
                m = b**2 * (1-(((a - (_x+0.5))**2) / (a**2)))
                _y = math.sqrt(m) if m>0 else 0
                
                s = int(y+b-_y)
                t = int(y+b+_y)
                
                vline(x+_x, s, t-s, colour)
                vline(x+width-_x-1, s, t-s, colour)
            if width & 1:
                vline(x+(width//2), y, height, 2)
        else:
            hline = self.drawHLine
            a+=0.5
            for _y in range(height//2):
                
                m = a**2 * (1-(((b - (_y+0.5))**2) / (b**2)))
                _x = math.sqrt(m) if m>0 else 0
                
                s = int(x+a-_x)
                t = int(x+a+_x)
                
                hline(s, y+_y, t-s, colour)
                hline(s, y+height-_y-1, t-s, colour)
            if height & 1:
                hline(x, y+(height//2), width, 2)
    
    def drawEllispe(self, x:int, y:int, width:int, height:int, colour:int):
        raise NotImplementedError("Ellipse not supported")
    
    @micropython.native
    def drawFilledRectangle(self, x:int, y:int, width:int, height:int, colour:int):
        hline = self.drawHLine
        for y in range(y, y+height):
            hline(x, y, width, colour)

    @micropython.native
    def drawRectangle(self, x:int, y:int, width:int, height:int, colour:int):
        self.drawHLine(x, y, width, colour)
        self.drawVLine(x, y, height, colour)
        self.drawVLine(x+width-1, y, height, colour)
        self.drawHLine(x, y+height-1, width, colour)

    def setPixel(self, x:int, y:int, colour:int):
        raise NotImplementedError("Not supported")

    def getPixel(self, x:int, y:int):
        pass
    
    @micropython.native
    def drawHLine(self, x:int, y:int, width:int, colour:int):
        sp = self.setPixel
        for x in range(max(0, x), min(x+width, self.width)):
            sp(x, y, colour)
    
    @micropython.native
    def drawVLine(self, x:int, y:int, height:int, colour:int):
        sp = self.setPixel
        for y in range(max(0, y), min(y+height, self.height)):
            sp(x, y, colour)
        

    @micropython.native
    def drawLine(self, x0:int, y0:int, x1:int, y1:int, colour:int):
        sp = self.setPixel
        yr = y1 - y0
        xr = x1 - x0
        if yr == 0:
            self.drawHLine(min(x0, x1), y0, abs(x1-x0), colour)
        elif xr == 0:
            self.drawVLine(x0, min(y0, y1), abs(y1-y0), colour)
        elif abs(xr) > abs(yr):
            if xr < 0:
                x0, x1 = x1, x0
                y0, y1 = y1, x0
                xr = -xr
                yr = -yr
            for x in range(xr+1):
                sp(x+x0, x*yr//xr+y0, colour)
        else:
            if yr < 0:
                x0, x1 = x1, x0
                y0, y1 = y1, x0
                xr = -xr
                yr = -yr
            for y in range(yr+1):
                sp(y*xr//yr+x0, y+y0, colour)

    def blit(self, src, x:int, y:int, width:int, height:int, key:int, mirrorX:int, mirrorY:int):
        raise NotImplementedError("Blit function not implemented.")

    def blitWithMask(self, src, x:int, y:int, width:int, height:int, key:int, mirrorX:int, mirrorY:int, mask):
        raise NotImplementedError("Blit w/ mask not implemented.")

    def calibrate(self):
        pass