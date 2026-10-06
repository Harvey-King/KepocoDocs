import _thread
from machine import Pin, SPI
from kepocoDisplayDriver import DisplayDriver
from utime import sleep_us

from uctypes import addressof

class AbstractST77xxDriver(DisplayDriver):
    # commands
    NOP     = 0x0
    SWRESET = 0x01
    RDDID   = 0x04
    RDDST   = 0x09

    SLPIN  = 0x10
    SLPOUT = 0x11
    PTLON  = 0x12
    NORON  = 0x13

    INVOFF  = 0x20
    INVON   = 0x21
    DISPOFF = 0x28
    DISPON  = 0x29
    CASET   = 0x2A
    RASET   = 0x2B
    RAMWR   = 0x2C
    RAMRD   = 0x2E

    VSCRDEF = 0x33
    VSCSAD  = 0x37
    COLMOD  = 0x3A
    MADCTL  = 0x36
    
    WRDISBV = 0x51

    FRMCTR1 = 0xB1
    FRMCTR2 = 0xB2
    FRMCTR3 = 0xB3
    INVCTR  = 0xB4
    DISSET5 = 0xB6

    PWCTR1 = 0xC0
    PWCTR2 = 0xC1
    PWCTR3 = 0xC2
    PWCTR4 = 0xC3
    PWCTR5 = 0xC4
    VMCTR1 = 0xC5

    RDID1 = 0xDA
    RDID2 = 0xDB
    RDID3 = 0xDC
    RDID4 = 0xDD

    GMCTRP1 = 0xE0
    GMCTRN1 = 0xE1

    PWCTR6 = 0xFC
    
    
    #	rotations (0deg=0x00, 90deg=0x60, 180deg=0xC0, 270deg=0xA0)
    ROT_0DEG      = 0x00
    ROT_90DEG     = 0x60
    ROT_180DEG    = 0xC0
    ROT_270DEG    = 0xA0
    
    _screen_lock = _thread.allocate_lock()
    
    def __init__(self, width: int, height: int, rotation: int, spi: SPI, dc: Pin, res: Pin, cs: Pin):
        super().__init__(width, height)
        self._rot = rotation
        
        #common spi buffers
        self._windowLocData = bytearray(4)
        self._cmdBuffer = bytearray(1)
        
        # based on SSD1306_SPI class
        self.rate = 24 * 1000 * 1000 # MBit, maxes out at around 22-24MBit ??
        dc.init(Pin.OUT, pull=Pin.PULL_DOWN, value=0)
        cs.init(Pin.OUT, pull=Pin.PULL_DOWN, value=1)
        res.init(Pin.OUT, pull=Pin.PULL_DOWN)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
    
    def init_display(self):
        with AbstractST77xxDriver._screen_lock:
            # print("AbstractST77xxDriver.init_display")
            # clear previous state
            self._reset()
            self._writeCommand(AbstractST77xxDriver.SWRESET) #Software reset
            sleep_us(150)
            self._writeCommand(AbstractST77xxDriver.SLPOUT)  #Wake up
            sleep_us(500)
    
            # buffers
            data1 = bytearray(1)
            data2 = bytearray(2)
    
            #Frame rate control.
            data3 = bytearray([0x01, 0x2C, 0x2D])       #fastest refresh, 6 lines front, 3 lines back.
            self._writeCommandAndData(AbstractST77xxDriver.FRMCTR1, data3)
            self._writeCommandAndData(AbstractST77xxDriver.FRMCTR2, data3)
            data6 = bytearray([0x01, 0x2c, 0x2d, 0x01, 0x2c, 0x2d])
            self._writeCommandAndData(AbstractST77xxDriver.FRMCTR3, data6)
            sleep_us(10)
    
            #Display inversion control
            data1[0] = 0x07 #Line inversion.
            self._writeCommandAndData(AbstractST77xxDriver.INVCTR, data1)
    
            #Power control
            data3[0] = 0xA2
            data3[1] = 0x02
            data3[2] = 0x84
            self._writeCommandAndData(AbstractST77xxDriver.PWCTR1, data3)
            data1[0] = 0xC5   #VGH = 14.7V, VGL = -7.35V
            self._writeCommandAndData(AbstractST77xxDriver.PWCTR2, data1)
            data2[0] = 0x0A   #Opamp current small
            data2[1] = 0x00   #Boost frequency
            self._writeCommandAndData(AbstractST77xxDriver.PWCTR3, data2)
            data2[0] = 0x8A   #Opamp current small
            data2[1] = 0x2A   #Boost frequency
            self._writeCommandAndData(AbstractST77xxDriver.PWCTR4, data2)
            data2[0] = 0x8A   #Opamp current small
            data2[1] = 0xEE   #Boost frequency
            self._writeCommandAndData(AbstractST77xxDriver.PWCTR5, data2)
            data1[0] = 0x0E
            self._writeCommandAndData(AbstractST77xxDriver.VMCTR1, data1)
    
            self._writeCommand(AbstractST77xxDriver.INVOFF)
            data1[0] = 0x05 # 12-bit = 0x03; 16-bit = 0x05; 18-bit = 0x06
            self._writeCommandAndData(AbstractST77xxDriver.COLMOD, data1)
    
            self._writeCommandAndData(AbstractST77xxDriver.GMCTRP1, bytearray([0x0f, 0x1a, 0x0f, 0x18, 0x2f, 0x28, 0x20, 0x22, 0x1f,
                                0x1b, 0x23, 0x37, 0x00, 0x07, 0x02, 0x10]))
            self._writeCommandAndData(AbstractST77xxDriver.GMCTRN1, bytearray([0x0f, 0x1b, 0x0f, 0x17, 0x33, 0x2c, 0x29, 0x2e, 0x30,
                                0x30, 0x39, 0x3f, 0x00, 0x07, 0x03, 0x10]))
            sleep_us(10)
    
            # Enable
            self._writeCommand(AbstractST77xxDriver.DISPON)
            sleep_us(100)
            self._writeCommand(AbstractST77xxDriver.NORON)
            sleep_us(10)
    
    def _full_clear(self, width, height, color):
        data1 = bytearray(1)
        data1[0] = 0x00
        self._writeCommandAndData(AbstractST77xxDriver.MADCTL, data1)
        buf = bytes([(color>>8)&0xFF,color&0xFF]*32)
        self._setWindow(0, 0, width, height)
        self._writeCommand(AbstractST77xxDriver.RAMWR)            #Write to RAM.

        self.dc(1)
        self.cs(0)
        for _ in range(width * height // 32):
            self.spi.write(buf)
        rest = (width * height) % 32
        if rest:
            self.spi.write(buf[:rest*2])
        self.cs(1)
        data1[0] = self._rot | 0x00
        self._writeCommandAndData(AbstractST77xxDriver.MADCTL, data1)
    
    def poweroff(self):
        with AbstractST77xxDriver._screen_lock:
            self._writeCommand(AbstractST77xxDriver.DISPOFF)

    def poweron(self):
        with AbstractST77xxDriver._screen_lock:
            self._writeCommand(AbstractST77xxDriver.DISPON)

    def contrast(self, contrast):
        data = bytearray(1)
        data[0] = contrast & 0xFF
        self._writeCommandAndData(AbstractST77xxDriver.WRDISBV, data)

    def invert(self, invert):
        with AbstractST77xxDriver._screen_lock:
            self._writeCommand(AbstractST77xxDriver.INVON if invert else AbstractST77xxDriver.INVOFF)

    @micropython.native
    def _reset(self):
        '''Reset the device.'''
        self.dc(0) # command mode
        self.res(1) # on
        sleep_us(500)
        self.res(0) # off
        sleep_us(500)
        self.res(1) # on
        sleep_us(500)

    @micropython.viper
    def _setWindow(self, left: int, top: int, width: int, height: int):
        '''Set a rectangular area for drawing a color to.'''
        windowLocData_lcl = self._windowLocData
        windowLocData = ptr8(windowLocData_lcl)

        windowLocData[0] = left>>8
        windowLocData[1] = left
        windowLocData[2] = (left + width - 1)>>8
        windowLocData[3] = left + width - 1
        self._writeCommandAndData(AbstractST77xxDriver.CASET, windowLocData_lcl)  # Column address set.

        windowLocData[0] = top>>8
        windowLocData[1] = top
        windowLocData[2] = (top + height - 1)>>8
        windowLocData[3] = top + height - 1
        self._writeCommandAndData(AbstractST77xxDriver.RASET, windowLocData_lcl)  # Row address set.

    @micropython.viper
    def _writeCommand(self, command: int):
        '''Write given command to the device.'''
        buf = self._cmdBuffer
        buf[0] = command
        spi = self.spi
        cs = self.cs
        spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.dc(0)
        cs(0)
        spi.write(buf)
        cs(1)

    @micropython.viper
    def _writeCommandAndData(self, command: int, data):
        '''Write given command to the device.'''
        buf = self._cmdBuffer
        buf[0] = command
        spi = self.spi
        cs = self.cs
        dc = self.dc
        spiwrite = spi.write
        spi.init(baudrate=self.rate, polarity=0, phase=0)
        dc(0)
        cs(0)
        spiwrite(buf)
        dc(1)
        spiwrite(data)
        cs(1)

    # Set display brightness, valid values 0 to 127
    @micropython.native
    def brightness(self,setting):
        if(setting>127):
            setting=127
        if(setting<0):
            setting=0
        self.contrast(setting)
    
    @micropython.native
    def show(self):
        
        with AbstractST77xxDriver._screen_lock: # lock costs ~400us
            # print("D locked")
            
            self._show_inner()
            
            # print("D release")
    

class ST77xxCompatDriver(AbstractST77xxDriver):
    
    # top 2 bits cannot be explicitly set for positive numbers in const() expressions ???
    _bg = const(0x00000000)
    _fg = const(-1)
    _lg = const(0x18C618C6)
    _dg = const(0x0C630C63)
    
    def __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin, rot: int, actualSize: tuple[int, int], alignX="center", alignY="center"):
        super().__init__(width, height, rot, spi, dc, res, cs)
        self._buffSize = self.height * self.width // 8
        self.drawBuffer = bytearray(2 * self._buffSize)
        memv = memoryview(self.drawBuffer)
        self.buffer = memv[:self._buffSize]
        self.shading = memv[self._buffSize:]
        self._bank_offsets = bytearray(height>>1) # banks = height/8, bytes per bank = 4
        # print([((4-i)*width) for i in range(height >> 3)])
        
        # custom for ST7735
        self._pixel_scale = min(actualSize[0]//width, actualSize[1]//height)
        if alignX == "left":
            self._offsetL = 0
        elif alignX == "right":
            self._offsetL = actualSize[0]-(width*self._pixel_scale)
        else:
            self._offsetL = (actualSize[0]-(width*self._pixel_scale))//2
        if alignX == "top":
            self._offsetT = 0
        elif alignX == "bottom":
            self._offsetT = actualSize[1]-(height*self._pixel_scale)
        else:
            self._offsetT = (actualSize[1]-(height*self._pixel_scale))//2
        self._actualSize = actualSize
        self._alignX = alignX
        self._alignY = alignY
    
    @micropython.viper
    def fill(self, colour:int):
        _BUFF_INT_SIZE = int(self._buffSize) // 4
        buffer = ptr32(self.buffer)
        shading = ptr32(self.shading)
        f1 = -1 if colour & 1 else 0
        f2 = -1 if colour & 2 else 0
        i = 0
        while i < _BUFF_INT_SIZE:
            buffer[i] = f1
            shading[i] = f2
            i += 1
    
    @micropython.viper
    def drawFilledRectangle(self, x:int, y:int, width:int, height:int, colour:int):
        _WIDTH = int(self.width)
        _HEIGHT = int(self.height)
        if x + width <= 0 or x >= _WIDTH or y + height <= 0 or y >= _HEIGHT:
            return
        if width <= 0 or height <= 0: return
        if x < 0:
            width += x
            x = 0
        if y < 0:
            height += y
            y = 0
        x2 = x + width
        y2 = y + height
        if x2 > _WIDTH:
            x2 = _WIDTH
            width = _WIDTH - x
        if y2 > _HEIGHT:
            y2 = _HEIGHT
            height = _HEIGHT - y

        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)

        o = (y >> 3) * _WIDTH
        oe = o + x2
        o += x
        strd = _WIDTH - width

        c1 = colour & 1
        c2 = colour & 2
        v1 = 0xff if c1 else 0
        v2 = 0xff if c2 else 0

        yb = y & 7
        ybh = 8 - yb
        if height <= ybh:
            m = ((1 << height) - 1) << yb
        else:
            m = 0xff << yb
        im = 255-m
        while o < oe:
            if c1:
                buffer[o] |= m
            else:
                buffer[o] &= im
            if c2:
                shading[o] |= m
            else:
                shading[o] &= im
            o += 1
        height -= ybh
        while height >= 8:
            o += strd
            oe += _WIDTH
            while o < oe:
                buffer[o] = v1
                shading[o] = v2
                o += 1
            height -= 8
        if height > 0:
            o += strd
            oe += _WIDTH
            m = (1 << height) - 1
            im = 255-m
            while o < oe:
                if c1:
                    buffer[o] |= m
                else:
                    buffer[o] &= im
                if c2:
                    shading[o] |= m
                else:
                    shading[o] &= im
                o += 1

    @micropython.viper
    def drawRectangle(self, x:int, y:int, width:int, height:int, colour:int):
        dfr = self.drawFilledRectangle
        dfr(x, y, width, 1, colour)
        dfr(x, y, 1, height, colour)
        dfr(x, y+height-1, width, 1, colour)
        dfr(x+width-1, y, 1, height, colour)

    @micropython.viper
    def setPixel(self, x:int, y:int, colour:int):
        _WIDTH = int(self.width)
        _HEIGHT = int(self.height)
        if x < 0 or x >= _WIDTH or y < 0 or y >= _HEIGHT:
            return
        o = (y >> 3) * _WIDTH + x
        m = 1 << (y & 7)
        im = 255-m
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)
        if colour & 1:
            buffer[o] |= m
        else:
            buffer[o] &= im
        if colour & 2:
            shading[o] |= m
        else:
            shading[o] &= im

    @micropython.viper
    def getPixel(self, x:int, y:int) -> int:
        _WIDTH = int(self.width)
        _HEIGHT = int(self.height)
        if x < 0 or x >= _WIDTH or y < 0 or y >= _HEIGHT:
            return 0
        o = (y >> 3) * _WIDTH + x
        m = 1 << (y & 7)
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)
        colour = 0
        if buffer[o] & m:
            colour = 1
        if shading[o] & m:
            colour |= 2
        return colour
    
    @micropython.native
    def drawHLine(self, x:int, y:int, width:int, colour:int):
        self.drawFilledRectangle(x, y, width, 1, colour)
    
    @micropython.native
    def drawVLine(self, x:int, y:int, height:int, colour:int):
        self.drawFilledRectangle(x, y, 1, height, colour)

    @micropython.viper
    def drawLine(self, x0:int, y0:int, x1:int, y1:int, colour:int):
        if x0 == x1:
            self.drawFilledRectangle(x0, y0, 1, y1 - y0, colour)
            return
        if y0 == y1:
            self.drawFilledRectangle(x0, y0, x1 - x0, 1, colour)
            return
        _WIDTH = int(self.width)
        _HEIGHT = int(self.height)
        dx = x1 - x0
        dy = y1 - y0
        sx = 1
        # y increment is always 1
        if dy < 0:
            x0,x1 = x1,x0
            y0,y1 = y1,y0
            dy = 0 - dy
            dx = 0 - dx
        if dx < 0:
            dx = 0 - dx
            sx = -1
        x = x0
        y = y0
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)

        o = (y >> 3) * _WIDTH + x
        m = 1 << (y & 7)
        im = 255-m
        c1 = colour & 1
        c2 = colour & 2

        if dx > dy:
            err = dx >> 1
            x1 += 1
            while x != x1:
                if 0 <= x < _WIDTH and 0 <= y < _HEIGHT:
                    if c1:
                        buffer[o] |= m
                    else:
                        buffer[o] &= im
                    if c2:
                        shading[o] |= m
                    else:
                        shading[o] &= im
                err -= dy
                if err < 0:
                    y += 1
                    m <<= 1
                    if m & 0x100:
                        o += _WIDTH
                        m = 1
                        im = 0xfe
                    else:
                        im = 255-m
                    err += dx
                x += sx
                o += sx
        else:
            err = dy >> 1
            y1 += 1
            while y != y1:
                if 0 <= x < _WIDTH and 0 <= y < _HEIGHT:
                    if c1:
                        buffer[o] |= m
                    else:
                        buffer[o] &= im
                    if c2:
                        shading[o] |= m
                    else:
                        shading[o] &= im
                err -= dx
                if err < 0:
                    x += sx
                    o += sx
                    err += dy
                y += 1
                m <<= 1
                if m & 0x100:
                    o += _WIDTH
                    m = 1
                    im = 0xfe
                else:
                    im = 255-m
    
    @micropython.viper
    def blit(self, src, x:int, y:int, width:int, height:int, key:int, mirrorX:int, mirrorY:int):
        _WIDTH = int(self.width)
        _HEIGHT = int(self.height)
        if x+width < 0 or x >= _WIDTH:
            return
        if y+height < 0 or y >= _HEIGHT:
            return
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)

        if isinstance(src, (tuple, list)):
            shd = 1
            src1 = ptr8(src[0])
            src2 = ptr8(src[1])
        else:
            shd = 0
            src1 = ptr8(src)
            src2 = ptr8(0)

        stride = width

        srcx = 0 ; srcy = 0
        dstx = x ; dsty = y
        sdx = 1
        if mirrorX:
            sdx = -1
            srcx += width - 1
            if dstx < 0:
                srcx += dstx
                width += dstx
                dstx = 0
        else:
            if dstx < 0:
                srcx = 0 - dstx
                width += dstx
                dstx = 0
        if dstx+width > _WIDTH:
            width = _WIDTH - dstx
        if mirrorY:
            srcy = height - 1
            if dsty < 0:
                srcy += dsty
                height += dsty
                dsty = 0
        else:
            if dsty < 0:
                srcy = 0 - dsty
                height += dsty
                dsty = 0
        if dsty+height > _HEIGHT:
            height = _HEIGHT - dsty

        srco = (srcy >> 3) * stride + srcx
        srcm = 1 << (srcy & 7)

        dsto = (dsty >> 3) * _WIDTH + dstx
        dstm = 1 << (dsty & 7)
        dstim = 255 - dstm

        while height != 0:
            srcco = srco
            dstco = dsto
            i = width
            while i != 0:
                v = 0
                if src1[srcco] & srcm:
                    v = 1
                if shd and (src2[srcco] & srcm):
                    v |= 2
                if (key == -1) or (v != key):
                    if v & 1:
                        buffer[dstco] |= dstm
                    else:
                        buffer[dstco] &= dstim
                    if v & 2:
                        shading[dstco] |= dstm
                    else:
                        shading[dstco] &= dstim
                srcco += sdx
                dstco += 1
                i -= 1
            dstm <<= 1
            if dstm & 0x100:
                dsto += _WIDTH
                dstm = 1
                dstim = 0xfe
            else:
                dstim = 255 - dstm
            if mirrorY:
                srcm >>= 1
                if srcm == 0:
                    srco -= stride
                    srcm = 0x80
            else:
                srcm <<= 1
                if srcm & 0x100:
                    srco += stride
                    srcm = 1
            height -= 1

    @micropython.viper
    def blitWithMask(self, src, x:int, y:int, width:int, height:int, key:int, mirrorX:int, mirrorY:int, mask):
        _WIDTH = int(self.width)
        _HEIGHT = int(self.height)
        if x+width < 0 or x >= _WIDTH:
            return
        if y+height < 0 or y >= _HEIGHT:
            return
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)

        if isinstance(src, (tuple, list)):
            shd = 1
            src1 = ptr8(src[0])
            src2 = ptr8(src[1])
        else:
            shd = 0
            src1 = ptr8(src)
            src2 = ptr8(0)

        if isinstance(mask, (tuple, list)):
            maskp = ptr8(mask[0])
        else:
            maskp = ptr8(mask)

        stride = width

        srcx = 0 ; srcy = 0
        dstx = x ; dsty = y
        sdx = 1
        if mirrorX:
            sdx = -1
            srcx += width - 1
            if dstx < 0:
                srcx += dstx
                width += dstx
                dstx = 0
        else:
            if dstx < 0:
                srcx = 0 - dstx
                width += dstx
                dstx = 0
        if dstx+width > _WIDTH:
            width = _WIDTH - dstx
        if mirrorY:
            srcy = height - 1
            if dsty < 0:
                srcy += dsty
                height += dsty
                dsty = 0
        else:
            if dsty < 0:
                srcy = 0 - dsty
                height += dsty
                dsty = 0
        if dsty+height > _HEIGHT:
            height = _HEIGHT - dsty

        srco = (srcy >> 3) * stride + srcx
        srcm = 1 << (srcy & 7)

        dsto = (dsty >> 3) * _WIDTH + dstx
        dstm = 1 << (dsty & 7)
        dstim = 255 - dstm

        while height != 0:
            srcco = srco
            dstco = dsto
            i = width
            while i != 0:
                if maskp[srcco] & srcm:
                    if src1[srcco] & srcm:
                        buffer[dstco] |= dstm
                    else:
                        buffer[dstco] &= dstim
                    if shd and (src2[srcco] & srcm):
                        shading[dstco] |= dstm
                    else:
                        shading[dstco] &= dstim
                srcco += sdx
                dstco += 1
                i -= 1
            dstm <<= 1
            if dstm & 0x100:
                dsto += _WIDTH
                dstm = 1
                dstim = 0xfe
            else:
                dstim = 255 - dstm
            if mirrorY:
                srcm >>= 1
                if srcm == 0:
                    srco -= stride
                    srcm = 0x80
            else:
                srcm <<= 1
                if srcm & 0x100:
                    srco += stride
                    srcm = 1
            height -= 1


class ST7735CompatDriver(ST77xxCompatDriver):
    def __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin):
        super().__init__(width, height, spi, dc, res, cs, AbstractST77xxDriver.ROT_180DEG, (161,130), alignX="right", alignY="center")
        assert self._pixel_scale == 2
        self._show_inner = self._show_mono
        self._tint = None
        self._rowBuffer = bytearray(int(self.height * 2 * 2 * 2)) # 2 bytes per pixel in 16bit (565) colour, 2x2 real pixels per pixel
    
    def init_display(self):
        super().init_display()
        self._full_clear(130, 161, 0x0000)
        self._setWindow(self._offsetT, self._offsetL, self.height*self._pixel_scale, self.width*self._pixel_scale)
    
    def setModeMono(self):
        self._show_inner = self._show_mono
        self._tint = None
    
    def setModeGreyscale(self):
        self._show_inner = self._show_grey
        self._tint = None
    
    def setModeTinted(self, red, green, blue):
        fg = ((red << 8) & 0xF800) | ((green << 3) & 0x07E0) | ((blue >> 3) & 0x001F)
        red = (red*2)//3
        green = (green*2)//3
        blue = (blue*2)//3
        lg = ((red << 8) & 0xF800) | ((green << 3) & 0x07E0) | ((blue >> 3) & 0x001F)
        dg = ((red << 7) & 0x7800) | ((green << 2) & 0x03E0) | ((blue >> 4) & 0x000F)
        self._tint = b"".join([
            b"\x00\x00\x00\x00",
            fg.to_bytes(2), fg.to_bytes(2),
            dg.to_bytes(2), dg.to_bytes(2),
            lg.to_bytes(2), lg.to_bytes(2),
        ])
        self.show = self._show_tinted
    
    @micropython.viper
    def _show_mono(self):
        self._writeCommand(AbstractST77xxDriver.RAMWR) # memory write mode
        self.dc(1) # data mode
        self.cs(0) # start data
        
        frame_buffer = ptr8(self.buffer)
        rowBuffer = self._rowBuffer
        rowBuffer32 = ptr32(rowBuffer)
        spi_write = self.spi.write
        pixel_scale = int(self._pixel_scale)
        w = int(self.width)
        h = int(self.height)
        
        for x in range(w):
            p: int = rowBuffer32
            bank = h>>3
            while bank:
                bank -= 1
                index: int = bank * w + x
                mono: int = frame_buffer[index]
                
                if mono & 128:
                    p[0] = _fg
                else:
                    p[0] = _bg
                
                if mono & 64:
                    p[1] = _fg
                else:
                    p[1] = _bg
                
                if mono & 32:
                    p[2] = _fg
                else:
                    p[2] = _bg
                
                if mono & 16:
                    p[3] = _fg
                else:
                    p[3] = _bg
                
                if mono & 8:
                    p[4] = _fg
                else:
                    p[4] = _bg
                
                if mono & 4:
                    p[5] = _fg
                else:
                    p[5] = _bg
                
                if mono & 2:
                    p[6] = _fg
                else:
                    p[6] = _bg
                
                if mono & 1:
                    p[7] = _fg
                else:
                    p[7] = _bg
                
                p[40] = p[0]
                p[41] = p[1]
                p[42] = p[2]
                p[43] = p[3]
                p[44] = p[4]
                p[45] = p[5]
                p[46] = p[6]
                p[47] = p[7]
                
                p = ptr32(int(p) + 32) # 32 = 8 pixels * 4 bytes/pixel
                
            spi_write(rowBuffer)

        self.cs(1) # end data
        
        self._writeCommand(AbstractST77xxDriver.NOP) # nop mode, stops any noise on the data line being rendered

    @micropython.viper
    def _show_grey(self):
        self._writeCommand(AbstractST77xxDriver.RAMWR) # memory write mode
        self.dc(1) # data mode
        self.cs(0) # start data
        
        frame_buffer = ptr8(self.buffer)
        grey_buffer = ptr8(self.shading)
        rowBuffer = self._rowBuffer
        rowBuffer32 = ptr32(rowBuffer)
        spi_write = self.spi.write
        pixel_scale = int(self._pixel_scale)
        w = int(self.width)
        h = int(self.height)
            
        for x in range(w):
            p: ptr32 = rowBuffer32
            bank = h>>3
            while bank:
                bank -= 1
                index: int = bank * w + x
                mono: int = frame_buffer[index]
                grey: int = grey_buffer[index]
                
                if mono & 128:
                    if grey & 128: p[0] = _lg
                    else:  p[0] = _fg
                else:
                    if grey & 128: p[0] = _dg
                    else:  p[0] = _bg
                
                if mono & 64:
                    if grey & 64: p[1] = _lg
                    else:  p[1] = _fg
                else:
                    if grey & 64: p[1] = _dg
                    else:  p[1] = _bg
                
                if mono & 32:
                    if grey & 32: p[2] = _lg
                    else:  p[2] = _fg
                else:
                    if grey & 32: p[2] = _dg
                    else:  p[2] = _bg
                
                if mono & 16:
                    if grey & 16: p[3] = _lg
                    else:  p[3] = _fg
                else:
                    if grey & 16: p[3] = _dg
                    else:  p[3] = _bg
                
                if mono & 8:
                    if grey & 8: p[4] = _lg
                    else:  p[4] = _fg
                else:
                    if grey & 8: p[4] = _dg
                    else:  p[4] = _bg
                
                if mono & 4:
                    if grey & 4: p[5] = _lg
                    else:  p[5] = _fg
                else:
                    if grey & 4: p[5] = _dg
                    else:  p[5] = _bg
                
                if mono & 2:
                    if grey & 2: p[6] = _lg
                    else:  p[6] = _fg
                else:
                    if grey & 2: p[6] = _dg
                    else:  p[6] = _bg
                
                if mono & 1:
                    if grey & 1: p[7] = _lg
                    else:  p[7] = _fg
                else:
                    if grey & 1: p[7] = _dg
                    else:  p[7] = _bg
                
                p[40] = p[0]
                p[41] = p[1]
                p[42] = p[2]
                p[43] = p[3]
                p[44] = p[4]
                p[45] = p[5]
                p[46] = p[6]
                p[47] = p[7]
                
                p = ptr32(int(p) + 32) # 32 = 8 pixels * 4 bytes/pixel
                
            spi_write(rowBuffer)

        self.cs(1) # end data
        
        self._writeCommand(AbstractST77xxDriver.NOP) # nop mode, stops any noise on the data line being rendered

    @micropython.viper
    def _show_tinted(self):
        self._writeCommand(AbstractST77xxDriver.RAMWR) # memory write mode
        self.dc(1) # data mode
        self.cs(0) # start data
        
        frame_buffer = ptr8(self.buffer)
        grey_buffer = ptr8(self.shading)
        rowBuffer = self._rowBuffer
        rowBuffer32 = ptr32(rowBuffer)
        spi_write = self.spi.write
        pixel_scale = int(self._pixel_scale)
        w = int(self.width)
        h = int(self.height)
        lut = ptr32(self._tint)
            
        for x in range(w):
            p: ptr32 = rowBuffer32
            bank = h>>3
            while bank:
                bank -= 1
                index: int = bank * w + x
                mono: int = frame_buffer[index]
                grey: int = grey_buffer[index]
                
                if mono & 128:
                    if grey & 128: p[0] = lut[3]
                    else:  p[0] = lut[1]
                else:
                    if grey & 128: p[0] = lut[2]
                    else:  p[0] = lut[0]
                
                if mono & 64:
                    if grey & 64: p[1] = lut[3]
                    else:  p[1] = lut[1]
                else:
                    if grey & 64: p[1] = lut[2]
                    else:  p[1] = lut[0]
                
                if mono & 32:
                    if grey & 32: p[2] = lut[3]
                    else:  p[2] = lut[1]
                else:
                    if grey & 32: p[2] = lut[2]
                    else:  p[2] = lut[0]
                
                if mono & 16:
                    if grey & 16: p[3] = lut[3]
                    else:  p[3] = lut[1]
                else:
                    if grey & 16: p[3] = lut[2]
                    else:  p[3] = lut[0]
                
                if mono & 8:
                    if grey & 8: p[4] = lut[3]
                    else:  p[4] = lut[1]
                else:
                    if grey & 8: p[4] = lut[2]
                    else:  p[4] = lut[0]
                
                if mono & 4:
                    if grey & 4: p[5] = lut[3]
                    else:  p[5] = lut[1]
                else:
                    if grey & 4: p[5] = lut[2]
                    else:  p[5] = lut[0]
                
                if mono & 2:
                    if grey & 2: p[6] = lut[3]
                    else:  p[6] = lut[1]
                else:
                    if grey & 2: p[6] = lut[2]
                    else:  p[6] = lut[0]
                
                if mono & 1:
                    if grey & 1: p[7] = lut[3]
                    else:  p[7] = lut[1]
                else:
                    if grey & 1: p[7] = lut[2]
                    else:  p[7] = lut[0]
                
                p[40] = p[0]
                p[41] = p[1]
                p[42] = p[2]
                p[43] = p[3]
                p[44] = p[4]
                p[45] = p[5]
                p[46] = p[6]
                p[47] = p[7]
                
                p = ptr32(int(p) + 32) # 32 = 8 pixels * 4 bytes/pixel
            
            spi_write(rowBuffer)

        self.cs(1) # end data
        
        self._writeCommand(AbstractST77xxDriver.NOP) # nop mode, stops any noise on the data line being rendered


class ST7789CompatDriver(ST77xxCompatDriver):
    def __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin):
        super().__init__(width, height, spi, dc, res, cs, 0b01100010, (320,240), alignX="center", alignY="center")
        assert self._pixel_scale == 4, f"pixel scale 4 expected, got: {self._pixel_scale}"
        # super().__init__(width, height, spi, dc, res, cs, 0b01100010, (160,240), alignX="center", alignY="center")
        self._show_inner = self._show_mono
        self._tint = None
        self._rowBuffer = bytearray(int(self.height) * 2 * 4 - 4) # 2 bytes per pixel in 16bit (565) colour, pixel scale (4) pixels per pixel,  2 pixels (4 bytes) not needed
    
    def init_display(self):
        super().init_display()
        self._full_clear(320, 240, 0x0000)
    
    def setModeMono(self):
        self._show_inner = self._show_mono
        self._tint = None
    
    def setModeGreyscale(self):
        self._show_inner = self._show_grey
        self._tint = None
    
    def setModeTinted(self, red, green, blue):
        fg = ((red << 8) & 0xF800) | ((green << 3) & 0x07E0) | ((blue >> 3) & 0x001F)
        red = (red*2)//3
        green = (green*2)//3
        blue = (blue*2)//3
        lg = ((red << 8) & 0xF800) | ((green << 3) & 0x07E0) | ((blue >> 3) & 0x001F)
        dg = ((red << 7) & 0x7800) | ((green << 2) & 0x03E0) | ((blue >> 4) & 0x000F)
        self._tint = b"".join([
            b"\x00\x00\x00\x00",
            fg.to_bytes(2), fg.to_bytes(2),
            dg.to_bytes(2), dg.to_bytes(2),
            lg.to_bytes(2), lg.to_bytes(2),
        ])
        self.show = self._show_tinted
    
    @micropython.viper
    def _show_mono(self):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        frame_buffer = ptr8(self.buffer)
        grey_buffer = ptr8(self.shading)
        rowBuffer = self._rowBuffer
        rowBuffer32 = ptr32(rowBuffer)
        spi_write = self.spi.write
        cs = self.cs
        dc = self.dc
        pixel_scale = int(self._pixel_scale)
        w = int(self.width)
        h = int(self.height)
        
        offsetT = int(self._offsetT) + 1 # +1 to centralise the 2x2 pixels
        offsetL = int(self._offsetL) + 1 #    within the 4x4 space
        
        CASET = AbstractST77xxDriver.CASET
        RASET = AbstractST77xxDriver.RASET
        RAMWR = AbstractST77xxDriver.RAMWR
        windowLocData_lcl = self._windowLocData
        windowLocData = ptr8(windowLocData_lcl)
        cmd_buf = self._cmdBuffer
    
        cmd_buf[0] = CASET
        windowLocData[0] = offsetT>>8
        windowLocData[1] = offsetT
        windowLocData[2] = (offsetT + (h*4) - 3)>>8
        windowLocData[3] = offsetT + (h*4) - 3
        dc(0)
        cs(0)
        spi_write(cmd_buf)
        dc(1)
        spi_write(windowLocData_lcl)
        cs(1)
            
        for x in range(w):
            p: ptr32 = rowBuffer32
            bank = h>>3
            while bank:
                bank -= 1
                index: int = bank * w + x
                mono: int = frame_buffer[index]
                grey: int = grey_buffer[index]
                
                p[ 0] = _fg if mono & 128 else _bg
                p[ 2] = _fg if mono & 64  else _bg
                p[ 4] = _fg if mono & 32  else _bg
                p[ 6] = _fg if mono & 16  else _bg
                p[ 8] = _fg if mono & 8   else _bg
                p[10] = _fg if mono & 4   else _bg
                p[12] = _fg if mono & 2   else _bg
                p[14] = _fg if mono & 1   else _bg
                
                p = ptr32(int(p) + 64) # 32 = 16 pixels * 4 bytes/pixel
                
                
            '''Set a rectangular area for drawing a color to.'''
    
            cmd_buf[0] = RASET
            windowLocData[0] = offsetL>>8
            windowLocData[1] = offsetL
            windowLocData[2] = (offsetL + 1)>>8 # index of last row, 1 = 2 rows - 1
            windowLocData[3] = offsetL + 1
            dc(0)
            cs(0)
            spi_write(cmd_buf)
            dc(1)
            spi_write(windowLocData_lcl)
            cs(1)
            
            cmd_buf[0] = RAMWR
            dc(0)
            cs(0)
            spi_write(cmd_buf)
            dc(1)
            spi_write(rowBuffer)
            spi_write(rowBuffer)
            cs(1)
            
            offsetL += 4
            
        cmd_buf[0] = AbstractST77xxDriver.NOP
        dc(0)
        cs(0)
        spi_write(cmd_buf)
        dc(1)
        cs(1)

    @micropython.viper
    def _show_grey(self):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        frame_buffer = ptr8(self.buffer)
        grey_buffer = ptr8(self.shading)
        rowBuffer = self._rowBuffer
        rowBuffer32 = ptr32(rowBuffer)
        spi_write = self.spi.write
        cs = self.cs
        dc = self.dc
        pixel_scale = int(self._pixel_scale)
        w = int(self.width)
        h = int(self.height)
        
        offsetT = int(self._offsetT) + 1 # +1 to centralise the 2x2 pixels
        offsetL = int(self._offsetL) + 1 #    within the 4x4 space
        
        CASET = AbstractST77xxDriver.CASET
        RASET = AbstractST77xxDriver.RASET
        RAMWR = AbstractST77xxDriver.RAMWR
        windowLocData_lcl = self._windowLocData
        windowLocData = ptr8(windowLocData_lcl)
        cmd_buf = self._cmdBuffer
    
        cmd_buf[0] = CASET
        windowLocData[0] = offsetT>>8
        windowLocData[1] = offsetT
        windowLocData[2] = (offsetT + (h*4) - 3)>>8
        windowLocData[3] = offsetT + (h*4) - 3
        dc(0)
        cs(0)
        spi_write(cmd_buf)
        dc(1)
        spi_write(windowLocData_lcl)
        cs(1)
            
        for x in range(w):
            p: ptr32 = rowBuffer32
            bank = h>>3
            while bank:
                bank -= 1
                index: int = bank * w + x
                mono: int = frame_buffer[index]
                grey: int = grey_buffer[index]
                
                if mono & 128:  p[ 0] = _lg if grey & 128 else _fg
                else:           p[ 0] = _dg if grey & 128 else _bg
                
                if mono & 64:   p[ 2] = _lg if grey & 64  else _fg
                else:           p[ 2] = _dg if grey & 64  else _bg
                
                if mono & 32:   p[ 4] = _lg if grey & 32  else _fg
                else:           p[ 4] = _dg if grey & 32  else _bg
                
                if mono & 16:   p[ 6] = _lg if grey & 16  else _fg
                else:           p[ 6] = _dg if grey & 16  else _bg
                
                if mono & 8:    p[ 8] = _lg if grey & 8   else _fg
                else:           p[ 8] = _dg if grey & 8   else _bg
                
                if mono & 4:    p[10] = _lg if grey & 4   else _fg
                else:           p[10] = _dg if grey & 4   else _bg
                
                if mono & 2:    p[12] = _lg if grey & 2   else _fg
                else:           p[12] = _dg if grey & 2   else _bg
                
                if mono & 1:    p[14] = _lg if grey & 1   else _fg
                else:           p[14] = _dg if grey & 1   else _bg
                
                p = ptr32(int(p) + 64) # 32 = 16 pixels * 4 bytes/pixel
                
                
            '''Set a rectangular area for drawing a color to.'''
    
            cmd_buf[0] = RASET
            windowLocData[0] = offsetL>>8
            windowLocData[1] = offsetL
            windowLocData[2] = (offsetL + 1)>>8 # index of last row, 1 = 2 rows - 1
            windowLocData[3] = offsetL + 1
            dc(0)
            cs(0)
            spi_write(cmd_buf)
            dc(1)
            spi_write(windowLocData_lcl)
            cs(1)
            
            cmd_buf[0] = RAMWR
            dc(0)
            cs(0)
            spi_write(cmd_buf)
            dc(1)
            spi_write(rowBuffer)
            spi_write(rowBuffer)
            cs(1)
            
            offsetL += 4
            
        cmd_buf[0] = AbstractST77xxDriver.NOP
        dc(0)
        cs(0)
        spi_write(cmd_buf)
        dc(1)
        cs(1)

    @micropython.viper
    def _show_tinted(self):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        frame_buffer = ptr8(self.buffer)
        grey_buffer = ptr8(self.shading)
        rowBuffer = self._rowBuffer
        rowBuffer32 = ptr32(rowBuffer)
        spi_write = self.spi.write
        cs = self.cs
        dc = self.dc
        pixel_scale = int(self._pixel_scale)
        w = int(self.width)
        h = int(self.height)
        lut = ptr32(self._tint)
        
        offsetT = int(self._offsetT) + 1 # +1 to centralise the 2x2 pixels
        offsetL = int(self._offsetL) + 1 #    within the 4x4 space
        
        CASET = AbstractST77xxDriver.CASET
        RASET = AbstractST77xxDriver.RASET
        RAMWR = AbstractST77xxDriver.RAMWR
        windowLocData_lcl = self._windowLocData
        windowLocData = ptr8(windowLocData_lcl)
        cmd_buf = self._cmdBuffer
    
        cmd_buf[0] = CASET
        windowLocData[0] = offsetT>>8
        windowLocData[1] = offsetT
        windowLocData[2] = (offsetT + (h*4) - 3)>>8
        windowLocData[3] = offsetT + (h*4) - 3
        dc(0)
        cs(0)
        spi_write(cmd_buf)
        dc(1)
        spi_write(windowLocData_lcl)
        cs(1)
            
        for x in range(w):
            p: ptr32 = rowBuffer32
            bank = h>>3
            while bank:
                bank -= 1
                index: int = bank * w + x
                mono: int = frame_buffer[index]
                grey: int = grey_buffer[index]
                
                if mono & 128:  p[ 0] = lut[3] if grey & 128 else lut[1]
                else:           p[ 0] = lut[2] if grey & 128 else lut[0]
                
                if mono & 64:   p[ 2] = lut[3] if grey & 64  else lut[1]
                else:           p[ 2] = lut[2] if grey & 64  else lut[0]
                
                if mono & 32:   p[ 4] = lut[3] if grey & 32  else lut[1]
                else:           p[ 4] = lut[2] if grey & 32  else lut[0]
                
                if mono & 16:   p[ 6] = lut[3] if grey & 16  else lut[1]
                else:           p[ 6] = lut[2] if grey & 16  else lut[0]
                
                if mono & 8:    p[ 8] = lut[3] if grey & 8   else lut[1]
                else:           p[ 8] = lut[2] if grey & 8   else lut[0]
                
                if mono & 4:    p[10] = lut[3] if grey & 4   else lut[1]
                else:           p[10] = lut[2] if grey & 4   else lut[0]
                
                if mono & 2:    p[12] = lut[3] if grey & 2   else lut[1]
                else:           p[12] = lut[2] if grey & 2   else lut[0]
                
                if mono & 1:    p[14] = lut[3] if grey & 1   else lut[1]
                else:           p[14] = lut[2] if grey & 1   else lut[0]
                
                p = ptr32(int(p) + 64) # 32 = 16 pixels * 4 bytes/pixel
                
                
            '''Set a rectangular area for drawing a color to.'''
    
            cmd_buf[0] = RASET
            windowLocData[0] = offsetL>>8
            windowLocData[1] = offsetL
            windowLocData[2] = (offsetL + 1)>>8 # index of last row, 1 = 2 rows - 1
            windowLocData[3] = offsetL + 1
            dc(0)
            cs(0)
            spi_write(cmd_buf)
            dc(1)
            spi_write(windowLocData_lcl)
            cs(1)
            
            cmd_buf[0] = RAMWR
            dc(0)
            cs(0)
            spi_write(cmd_buf)
            dc(1)
            spi_write(rowBuffer)
            spi_write(rowBuffer)
            cs(1)
            
            offsetL += 4
            
        cmd_buf[0] = AbstractST77xxDriver.NOP
        dc(0)
        cs(0)
        spi_write(cmd_buf)
        dc(1)
        cs(1)
