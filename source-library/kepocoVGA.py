# Based on https://github.com/HughMaingauche/PICO-VGA-Micropython/tree/main


from machine import Pin, freq, mem32
from rp2 import PIO, StateMachine, asm_pio
from micropython import const
from array import array
from uctypes import addressof
from math import cos,sin,pi,log
from kepocoDisplayDriver import DisplayDriver

GREY_PINS = const(10) # LSB = 10, MSB = 11
HSYNC_PIN = const(9)
VSYNC_PIN = const(29) # const(8)

# VGA parameters for 80x480 using 3b per pixel
H_res=const(80)              # Horizontal resolution in pixels
V_res=const(480)             # Vertical resolution in pixels
bit_per_pix=const(2)         # Bits per pixel
pixel_bitmask=const(0b11)    # Corresponding bitmask (used for replacing one n-bit pixel in a 32b word)
usable_bits=const(32)        # Numbers of bits that will be used in each 32b word
pix_per_word=const(16)       # Number of n-bit pixels per 32b word
words_per_line=const(5)


DMA_CHAN_ABORT = const(0x50000444)
DMA_MULTI_CHAN_TRIGGER = const(0x50000430)
# DMA0_Addr = const(0x50000000) # used by SPI
DMA1_Addr = const(0x50000040)
DMA2_Addr = const(0x50000080)
DMA3_Addr = const(0x500000C0)
DMA_Read  = const(0x00)
DMA_Write = const(0x04)
DMA_Len   = const(0x08)
DMA_Ctrl  = const(0x10)
DMA_Read_Trigger  = const(0x3c)
DMA_Write_Trigger = const(0x2c)
DMA_Len_Trigger   = const(0x1c)
DMA_Ctrl_Trigger  = const(0x0c)

# 2 bit colour names
WHITE     = const(0b11)
LIGHT     = const(0b10)
DARK      = const(0b01)
BLACK     = const(0b00)

# 640*480 resolution
# Scanline part    Pixels    Time [µs]    32bits-Words
# Visible area      640     25.4220          100
# Front porch       16       0.6355          2,5
# Sync pulse        96       3.8133          15
# Back porch        48       1.9066          7,5
# Whole line        800      31.7775         125

#statemachine configuration
#sm0 is used for H sync signal
@asm_pio(set_init=PIO.OUT_HIGH, autopull=True, pull_thresh=32)
def paral_Hsync():
    wrap_target()
    # ACTIVE + FRONTPORCH
    mov(x, osr)               # Copy value from OSR to x scratch register
    label("activeporch")
    jmp(x_dec,"activeporch")  # Remain high in active mode and front porch
    # SYNC PULSE
    set(pins, 0) [31]    # Low for hsync pulse (32 cycles)
    set(pins, 0) [31]    # Low for hsync pulse (32 cycles)
    set(pins, 0) [31]    # Low for hsync pulse (32 cycles)
    # BACKPORCH
    set(pins, 1) [31]    # High for back porch (32 cycles)
    set(pins, 1) [13]    # High for back porch (32 cycles)
    irq(0)               # Set IRQ to signal end of line (47 cycles)
    wrap()
#     

# #
# #sm1 is used for V sync signal
@asm_pio(sideset_init=(PIO.OUT_HIGH,) * 1, autopull=True, pull_thresh=32)
def paral_Vsync():
    pull(block)                         # Pull from FIFO to OSR (only once)
    wrap_target()
    # ACTIVE
    mov(x, osr)                         # Copy value from OSR to x scratch register
    label("active")
    wait(1,irq,0)                       # Wait for hsync to go high
    irq(1)                              # Signal that we're in active mode
    jmp(x_dec,"active")                 # Remain in active mode, decrementing counter
    # FRONTPORCH
    set(y, 9)                           # Use y scratch register as counter
    label("frontporch")
    wait(1,irq,0)                       # Wait for hsync to go high
    jmp(y_dec,"frontporch")             # Remain in frontporch, decrementing counter
    # SYNC PULSE
    wait(1,irq,0)              .side(0) # Wait for hsync to go high and Set pin low
    wait(1,irq,0)                       # Wait for hsync to go high (V sync pulse is 2 lines in 640*480 resolution)
    # BACKPORCH
    set(y, 31)                          # First part of back porch into y scratch register (and delays a cycle)
    label("backporch")
    wait(1,irq,0)              .side(1) # Wait for hsync to go high - SIDESET REPLACEMENT HERE
    jmp(y_dec,"backporch")              # Remain in backporch, decrementing counter
    wait(1,irq,0)
    wrap()
# 


#sm4 is used for RGB signal
@asm_pio(out_init=(PIO.OUT_LOW,) * bit_per_pix, out_shiftdir=PIO.SHIFT_LEFT, sideset_init=(PIO.OUT_LOW,) * bit_per_pix, autopull=True, pull_thresh=usable_bits)
def paral_RGB():
    pull(block)                      # Pull from FIFO to OSR (only once)
    mov(y, osr)                      # Copy value from OSR to y scratch register
    out(null, 32)                    # Tune RGB to HSync
    wrap_target()
    mov(x, y)                  .side(0) # Initialize counter variable + set colour pins to zero
    wait(1,irq,1)                    # Wait for vsync active mode (starts 5 cycles after execution)
    label("colorout")
    out(pins,bit_per_pix)            # Push out to pins (one pixel)
    nop()                      [3]
    nop()                      [2]
    
    jmp(x_dec,"colorout")            # Stay here thru horizontal active mode
    wrap()


class VGADriver(DisplayDriver):
    
    @classmethod
    def detect_vga(cls):
        from thumbyHardware import i2c
        try:
            return i2c.readfrom_mem(0x50, 0, 8) == b'\x00\xff\xff\xff\xff\xff\xff\x00'
        except OSError as e:
            if e.errno == 5:
                return False
            raise e
    
    # Derived from https://gist.github.com/shirriff/dd9e35da12879cf1c5ed9ed92ff704ec
    @classmethod
    def read_edid(cls):
        from thumbyHardware import i2c
        data = i2c.readfrom_mem(0x50, 0, 128)
        
        if data[:8] != b'\x00\xff\xff\xff\xff\xff\xff\x00':
            return None # Not EDID packet
            
        if sum(data) & 0xFF != 0:
            return None # Bad Checksum
            
        # print(data)
        
        manufacturer = (data[8] << 8) | data[9]
        manufacturer = "".join(chr(((manufacturer >> shift) & 0x1f)+64) for shift in [10,5,0])
        # product = data[10] | (data[11] << 8)
        product = int.from_bytes(data[10:12], "little")
        serial = int.from_bytes(data[12:16], "little")
        week = data[16]
        year = data[17] + 1990
        version = tuple(data[18:20])
        features = (data[20], data[24])
        size = tuple(data[21:23])
        rx = ((data[27] << 2) | ((data[25]>>6) & 3)) / 1024.
        ry = ((data[28] << 2) | ((data[25]>>4) & 3)) / 1024.
        gx = ((data[29] << 2) | ((data[25]>>2) & 3)) / 1024.
        gy = ((data[30] << 2) | ((data[25]>>0) & 3)) / 1024.
        bx = ((data[31] << 2) | ((data[26]>>6) & 3)) / 1024.
        by = ((data[32] << 2) | ((data[26]>>4) & 3)) / 1024.
        wx = ((data[33] << 2) | ((data[26]>>2) & 3)) / 1024.
        wy = ((data[34] << 2) | ((data[26]>>0) & 3)) / 1024.
        
        spec_timings = [
            '720x400 @ 70 Hz (VGA)',
            '720x400 @ 88 Hz (XGA)',
            '640x480 @ 60 Hz (VGA)',
            '640x480 @ 67 Hz (Apple Macintosh II)',
            '640x480 @ 72 Hz',
            '640x480 @ 75 Hz',
            '800x600 @ 56 Hz',
            '800x600 @ 60 Hz',
            '800x600 @ 72 Hz',
            '800x600 @ 75 Hz',
            '832x624 @ 75 Hz (Apple Macintosh II)',
            '1024x768 @ 87 Hz, interlaced (1024x768i)',
            '1024x768 @ 60 Hz',
            '1024x768 @ 72 Hz',
            '1024x768 @ 75 Hz',
            '1280x1024 @ 75 Hz',
            '1152x870 @ 75 Hz (Apple Macintosh II)',
            'manufacturer-specific 6',
            'manufacturer-specific 5',
            'manufacturer-specific 4',
            'manufacturer-specific 3',
            'manufacturer-specific 2',
            'manufacturer-specific 1',
            'manufacturer-specific 0',
          ]
        
        timings = int.from_bytes(data[35:38], "little")
        supported = [x for lst in [
            [spec_timings[i] for i in range(24) if timings & (1<<i)],
            [(xres:=(data[i]+31)*8, f"{xres}x{int([10/16,3/4,4/5,9/16][data[i+1]>>6]*xres)} @ {60 + (data[i+1]&63)}Hz")[1] for i in range(38,54,2) if data[i]!=1 or data[i+1]!=1],
            # To Do: detailed and custom monitor descriptors
        ] for x in lst]
        
        return {
            'Manufacturer': manufacturer,
            'Product Code': product,
            'Serial Number': serial,
            'Week': week,
            'Year': year,
            'Version': version,
            'Features': features,
            'Size': size,
            'Chroma': {
                'Red': (rx, ry),
                'Green': (gx, gy),
                'Blue': (bx, by),
                'White': (wx, wy),
            },
            'Supported': supported
        }
    
    @classmethod
    def supported_refresh_rates(cls):
        import re
        return list(sorted(int(m.group(1)) for m in (re.search('@\s*(\d+)\s*Hz', s) for s in VGADriver.read_edid()["Supported"] if s.startswith("640x480")) if m, key=lambda x:abs(60-x)))
    
    # class vars
    shift = array('L', [24,16,8,0])
    
    def __init__(self, wrapped_driver, refreshRate=None):
        super().__init__(wrapped_driver.width, wrapped_driver.height)
        self.wrapped_driver = wrapped_driver
        self.visible_pix=int(H_res*V_res//pix_per_word)
        # Initiate the buffer - an array of consecutive 32bit words containing ALL the visible pixels
        self.H_buffer_line = array('L', [0] * self.visible_pix)
        # We need an array containing the adress of the buffer for the DMA chan0 to read the values
        self.H_buffer_line_address=array('L',[addressof(self.H_buffer_line)])
        self.show_physical_screen = True
        
        if refreshRate is None:
            self.refreshRate = VGADriver.supported_refresh_rates()[0]
        else:
            self.refreshRate = refreshRate
        
        pins = [
            Pin(HSYNC_PIN, Pin.OUT, value=0),
            Pin(VSYNC_PIN, Pin.OUT, value=0),
            Pin(GREY_PINS, Pin.OUT, value=0),
            Pin(GREY_PINS+1, Pin.OUT, value=0)
        ]
        from time import sleep_ms
        sleep_ms(300)
        for p in pins: p.value(1)
        sleep_ms(300)
        for p in pins: p.value(0)
        sleep_ms(300)
    
    def init_display(self):
        # self.wrapped_driver.init_display()
        
        # ------------- #
        # Set up Clocks #
        # ------------- #
        freq(250_000_000)
        mem32[0x4002800c] = (3<<16)|(2<<12)
        mem32[0x40028008] = 125
        # Rough linear approximation of target frame rate (typically 60/70Hz) to needed PIO clock rates.
        # Gets within acceptable tolerance of monitor capabilities.
        # SM0_FREQ = int(2167207.162*0.18*self.refreshRate+2022250.272) # Horizontal sync SM - For use with overclocked 250 MHz system clock
        SM0_FREQ = int(416103.775104*self.refreshRate+388272.052224) # Horizontal sync SM - For use with overclocked 250 MHz system clock
        SM1_FREQ=250_000_000                                     # Vertical sync SM - Max freq (driven by SM0 IRQ)
        SM2_FREQ = int(SM0_FREQ*1.125)                           # RGB signal output - For use with overclocked 250 MHz system clock
        
        print("Base Freq", SM0_FREQ)
    
        # ----------- #
        # Set up PIOs #
        # ----------- #
        
        self.paral_write_Hsync = StateMachine(0, paral_Hsync,freq=SM0_FREQ, set_base=Pin(HSYNC_PIN))
        self.paral_write_Vsync = StateMachine(1, paral_Vsync,freq=SM1_FREQ, sideset_base=Pin(VSYNC_PIN))
        self.paral_write_RGB = StateMachine(2, paral_RGB,freq=SM2_FREQ, out_base=Pin(GREY_PINS),sideset_base=Pin(GREY_PINS))
        
        # ------------------- #
        # Set up DMA Channels #
        # ------------------- #
        
        # RGB DMAs
        # Using chan0 as "configure" DMA and chan1 as "Data transfer" DMA
        # Parameters common to the 2 DMA channels
        IRQ_QUIET = 0  # Do not generate an interrupt
        RING_SEL = 0   # No wrapping
        RING_SIZE = 0  # No wrapping
        HIGH_PRIORITY = 1
        INCR_WRITE = 0  # Non increment while writing
    
        #Setting up the "data" DMA channel 1
        TREQ_SEL = 2    #  num of the RGB statemachine -> at the pace of the PIO
        INCR_READ = 1   # 1 increment while reading
        DATA_SIZE = 2   # 32 bit transfer
        CHAIN_TO = 2    # Chain to configure channel DMA 0 so it starts again
        EN = 1          # Channel is enabled by the configure DMA chan0
        DMA_control_word = ((IRQ_QUIET << 21) | (TREQ_SEL << 15) | (CHAIN_TO  << 11) | (RING_SEL << 10) |
                            (RING_SIZE << 9) | (INCR_WRITE << 5) | (INCR_READ << 4) | (DATA_SIZE << 2) |
                            (HIGH_PRIORITY << 1) | (EN << 0))
        mem32[DMA3_Addr | DMA_Read] = 0                      # DMA Channel 1 Read Address pointer <- not important because reset by DMA0 "configure" channel
        mem32[DMA3_Addr | DMA_Write] = 0x50200018            # DMA Channel 1 Write Address pointer -> PIO TX FIFO 2 (sm2) adress
        mem32[DMA3_Addr | DMA_Len] = len(self.H_buffer_line) # DMA Channel 1 Transfer Count <- length of the Data array buffer
        mem32[DMA3_Addr | DMA_Ctrl] = DMA_control_word       # DMA Channel 1 Control and Status (using alias to not start immediatly - will be started by DMA chanel 0)
    
        #Setting up the "control" DMA channel 0 - to run the Channel 1 - Vertical Visible Area lines 
        TREQ_SEL = 0x3f # Max speed, however synchronization is achieved via the PIO irq 1
        INCR_READ = 0   # No increment while reading
        CHAIN_TO = 2    # chain to itself (no chaining)
        EN = 1          # Start channel upon setting the trigger register
        DMA_control_word = ((IRQ_QUIET << 21) | (TREQ_SEL << 15) | (CHAIN_TO  << 11) | (RING_SEL << 10) |
                            (RING_SIZE << 9) | (INCR_WRITE << 5) | (INCR_READ << 4) | (DATA_SIZE << 2) |
                            (HIGH_PRIORITY << 1) | (EN << 0))
        mem32[DMA2_Addr | DMA_Read] = addressof(self.H_buffer_line_address) # DMA Channel 0 Read Address pointer <- data array to reconfigure DMA1
        mem32[DMA2_Addr | DMA_Write] = DMA3_Addr | DMA_Read_Trigger         # DMA Channel 0 Write Address pointer -> DMA1 read_adress alias register 3 (CH1_AL3_READ_ADDR_TRIG ) - trigger the DMA1 start
        mem32[DMA2_Addr | DMA_Len] = 1                                      # DMA Channel 0 Transfer Count <- Just one data (long) array to transfer continuously
        mem32[DMA2_Addr | DMA_Ctrl] = DMA_control_word                      # DMA Channel 0 Control and Status (using alias to not start immediatly - will be started by DMA trigger register)
        
        # ------------ #
        # Trigger PIOs #
        # ------------ #
        self.pauseVGA()  # reset any residuals
        self.resumeVGA() # actually start

    @micropython.viper
    def resumeVGA(self):
        V=int(ptr16(V_res))
        H=int(ptr16(H_res))
        # pauseVGA leaves all three SMs stopped at instruction zero, with
        # empty FIFOs and synchronised clock dividers.  Queue their initial
        # words before enabling them so no SM can begin a frame early.
        self.paral_write_Hsync.put(655)       # H Visible areas + H Front porch loop
        self.paral_write_Vsync.put(int(V-1))  # V Visible area
        self.paral_write_RGB.put(int(H-1))    # RGB loop
        ptr32(DMA_MULTI_CHAN_TRIGGER)[0] |= 0b00100  #triggers DMA chan0
        ptr32(0x50200000)[0] |= 0b111    # Enable PIO0 SM 0, 1, and 2
    
    @micropython.viper
    def pauseVGA(self):
        # Stop the producers first.  Aborting a DMA channel is asynchronous,
        # so do not reset its PIO consumer until both channels are idle.
        ptr32(0x50200000)[0] &= ~0b111
        ptr32(DMA_CHAN_ABORT)[0] = 0b001100          # Abort DMA channels 2 and 3
        while (ptr32(DMA2_Addr | DMA_Ctrl)[0] & 0x01000000) != 0:
            pass
        while (ptr32(DMA3_Addr | DMA_Ctrl)[0] & 0x01000000) != 0:
            pass

        # SM_RESTART returns execution to each program entry point, and
        # CLKDIV_RESTART makes all three dividers start on the same
        # system-clock edge.  Toggling FJOIN_RX is the RP2040 FIFO-clear
        # sequence; otherwise old pull words survive a software restart and
        # offset RGB from the sync generators.
        ptr32(0x502000d0)[0] |= int(0x80000000)
        ptr32(0x502000d0)[0] &= ~int(0x80000000)
        ptr32(0x502000e8)[0] |= int(0x80000000)
        ptr32(0x502000e8)[0] &= ~int(0x80000000)
        ptr32(0x50200100)[0] |= int(0x80000000)
        ptr32(0x50200100)[0] &= ~int(0x80000000)
        ptr32(0x50200030)[0] = 0xff                  # Clear latched PIO IRQs
        ptr32(0x50200000)[0] = 0x0770                # Restart SMs 0..2 and their dividers
    
    def enablePhysicalScreen(self, enabled):
        self.show_physical_screen = enabled
    
    @micropython.viper
    def show(self):
        if self.show_physical_screen:
            self.wrapped_driver.show()
        
        frame_buffer = ptr32(self.wrapped_driver.buffer)
        grey_buffer = ptr32(self.wrapped_driver.shading)
        src_w = int(self.width)
        src_h = int(self.height)
        dst_w = H_res
        dst_h = V_res
        
        rep = (dst_h // src_h) - 1
        data = ptr32(self.H_buffer_line) # vga buffer
        s = ptr32(VGADriver.shift)
        
        blocks = int((src_w*src_h//8)//4)
        
        
        # 8 bits (pixels) tall
        for o in range(blocks):
             # 4 bytes (pixels) wide
            block_m = frame_buffer[o]
            block_g = grey_buffer[o]
            
            t: int = ((o*4)//src_w)*8   # y coord of top left
            l: int =  (o*4) %src_w      # x coord of top left
            
            for b in range(8):
                m: int = 1<<b
                
                if block_m & (m    ):
                    col  = (LIGHT<<6) if block_g & (m    ) else (WHITE<<6)
                else:
                    col  = (DARK <<6) if block_g & (m    ) else (BLACK<<6)
                        
                if block_m & (m<< 8):
                    col |= (LIGHT<<4) if block_g & (m<< 8) else (WHITE<<4)
                else:
                    col |= (DARK <<4) if block_g & (m<< 8) else (BLACK<<4)
                        
                if block_m & (m<<16):
                    col |= (LIGHT<<2) if block_g & (m<<16) else (WHITE<<2)
                else:
                    col |= (DARK <<2) if block_g & (m<<16) else (BLACK<<2)
                        
                if block_m & (m<<24):
                    col |= (LIGHT   ) if block_g & (m<<24) else (WHITE   )
                else:
                    col |= (DARK    ) if block_g & (m<<24) else (BLACK   )
                
                # data in col is 8 bits wide
                
                idx = l//pix_per_word + ((t+b)*rep)*words_per_line
                if (l//4) & 3 == 0:
                    col <<= s[0]
                    for i in range(rep):
                        data[idx+i*words_per_line]  = col
                else:
                    col <<= s[(l//4) & 3]
                    for i in range(rep):
                        data[idx+i*words_per_line] |= col
    
    @micropython.native
    def poweroff(self):
        self.wrapped_driver.poweroff()
    
    @micropython.native
    def poweron(self):
        self.wrapped_driver.poweron()
    
    @micropython.native
    def contrast(self, contrast):
        self.wrapped_driver.contrast(contrast)

    @micropython.native
    def invert(self, invert):
        self.wrapped_driver.invert(invert)
    
    @micropython.native
    def setModeGreyscale(self):
        self.wrapped_driver.setModeGreyscale()
    
    @micropython.native
    def setModeMono(self):
        self.wrapped_driver.setModeMono()
    
    @micropython.native
    def setModeTinted(self, red, green, blue):
        self.wrapped_driver.setModeTinted(red, green, blue)
    
    @micropython.native
    def setModeRGB(self):
        self.wrapped_driver.setModeRGB()

    def brightness(self,setting):
        self.wrapped_driver.brightness(setting)

    @micropython.native
    def fill(self, colour:int):
        self.wrapped_driver.fill(colour)
    
    @micropython.native
    def drawFilledEllispe(self, x:int, y:int, width:int, height:int, colour:int):
        self.wrapped_driver.drawFilledEllispe(x, y, width, height, colour)
    
    def drawEllispe(self, x:int, y:int, width:int, height:int, colour:int):
        self.wrapped_driver.drawEllispe(x, y, width, height, colour)
    
    @micropython.native
    def drawFilledRectangle(self, x:int, y:int, width:int, height:int, colour:int):
        self.wrapped_driver.drawFilledRectangle(x, y, width, height, colour)

    @micropython.native
    def drawRectangle(self, x:int, y:int, width:int, height:int, colour:int):
        self.wrapped_driver.drawRectangle(x, y, width, height, colour)

    @micropython.native
    def setPixel(self, x:int, y:int, colour:int):
        self.wrapped_driver.setPixel(x, y, colour)

    @micropython.native
    def getPixel(self, x:int, y:int):
        self.wrapped_driver.getPixel(x, y)
    
    @micropython.native
    def drawHLine(self, x:int, y:int, width:int, colour:int):
        self.wrapped_driver.drawHLine(x, y, width, colour)
    
    @micropython.native
    def drawVLine(self, x:int, y:int, height:int, colour:int):
        self.wrapped_driver.drawVLine(x, y, height, colour)

    @micropython.native
    def drawLine(self, x0:int, y0:int, x1:int, y1:int, colour:int):
        self.wrapped_driver.drawLine(x0, y0, x1, y1, colour)

    @micropython.native
    def blit(self, src, x:int, y:int, width:int, height:int, key:int, mirrorX:int, mirrorY:int):
        self.wrapped_driver.blit(src, x, y, width, height, key, mirrorX, mirrorY)

    @micropython.native
    def blitWithMask(self, src, x:int, y:int, width:int, height:int, key:int, mirrorX:int, mirrorY:int, mask):
        self.wrapped_driver.blitWithMask(src, x, y, width, height, key, mirrorX, mirrorY, mask)

    @micropython.native
    def calibrate(self):
        self.wrapped_driver.calibrate()
