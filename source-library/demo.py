

def demo(button_src: str|list[str], duration: int|None = None, run: str|None = None, rseed = 0xC0DEBEEF, return_module: bool = False):
    import sys
    loaded_modules = set(sys.modules.keys())  # record loaded modules to unload additional ones later
    
    from machine import freq
    freq(250_000_000)
    from thumbyButton import buttonA, buttonB, buttonC, buttonU, buttonD, buttonL, buttonR, updateButtons
    from thumbyGraphics import display
    from thumbyAudio import audio
    import random, gc
    
    realFuncs = {
        "A": buttonA.pressed,
        "B": buttonB.pressed,
        "C": buttonC.pressed if buttonC else None,
        "U": buttonU.pressed,
        "D": buttonD.pressed,
        "L": buttonL.pressed,
        "R": buttonR.pressed,
        "update": display.update
    }
    
    dispstate = {
        "fps": display.frameRate,
        "bmap": display.font_bmap,
        "width": display.font_width,
        "height": display.font_height,
        "space": display.font_space,
        "glyphcnt": display.font_glyphcnt
    }
    
    endButtons = [realFuncs[x] for x in ("ABCUDLR" if buttonC else "ABUDLR")]
    
    global activeButtons
    activeButtons = set()
    
    buttonA.pressed = lambda: "A" in activeButtons
    buttonB.pressed = lambda: "B" in activeButtons
    buttonC.pressed = lambda: "C" in activeButtons
    buttonU.pressed = lambda: "U" in activeButtons
    buttonD.pressed = lambda: "D" in activeButtons
    buttonL.pressed = lambda: "L" in activeButtons
    buttonR.pressed = lambda: "R" in activeButtons
    
    updateButtons() # clears any residual 'just pressed' button state
    
    _seed = random.getrandbits(32)
    random.seed(rseed)
    mod = None
    
    try:
        if type(button_src) is str:
            try:
                with open(button_src, "r") as file:
                    seq = file.readlines()
            except OSError:
                seq = button_src.split("\n")
        else:
            seq = iter(button_src)
        
        def processLine(line): # processess a line in the demo file, returning a list of button sequences
            try:
                if line.startswith("$"): # special command
                    if line.startswith("$S"):
                        random.seed(int(line.split("=", 2)[1].strip()))
                    elif line.startswith("$F"):
                        display.setFPS(int(line.split("=", 2)[1].strip()))
                    return [] # no buttons to be pressed
                parts = line.split("X")
                return [set(parts[0])] if len(parts) == 1 else [set(parts[0].rstrip())]*int(parts[1].lstrip())
            except Exception as e:
                print("Error parsing line:", line)
                raise e
        
        it = iter(chars for line in seq for chars in processLine(line.split("#")[0].strip().upper()))
        
        def updateAndStep():
            global activeButtons
            realFuncs["update"]()
            if any(map(lambda x:x(), endButtons)):
                raise StopIteration("manual demo end")
            activeButtons.clear()
            activeButtons |= next(it)
        
        display.update = updateAndStep
            
        if run is not None:
            if run in sys.modules:
                # module already loaded, delete first
                del sys.modules[run]
            gc.collect()
            mod = __import__(run)
    
    except StopIteration as stp: # normal end of demo or a button was pressed
        pass
    except MemoryError as me: # menu + demo + import use too much RAM
        print(me)
        pass
    except ImportError as ie: # import error, typically typo
        print(ie)
        pass
    except Exception as ex: # some odd error from the demo
        print(ex)
        pass
    finally:
        #restore RNG somewhat
        random.seed(_seed)
        #restore functions
        buttonA.pressed = realFuncs["A"]
        buttonB.pressed = realFuncs["B"]
        if buttonC:
            buttonC.pressed = realFuncs["C"]
        buttonU.pressed = realFuncs["U"]
        buttonD.pressed = realFuncs["D"]
        buttonL.pressed = realFuncs["L"]
        buttonR.pressed = realFuncs["R"]
        display.update = realFuncs["update"]
        #stop any broken audio
        audio.stop(0)
        # clear screen
        if not (run and return_module):
            display.fill(0)
            display.show()
        # restore display
        display.framerate = dispstate["fps"]
        display.font_bmap = dispstate["bmap"]
        display.font_width = dispstate["width"]
        display.font_height = dispstate["height"]
        display.font_space = dispstate["space"]
        display.font_glyphcnt = dispstate["glyphcnt"]
        # unload additional modules
        curr_modules = set(sys.modules.keys())
        for module in curr_modules:
            if module not in loaded_modules:
                del sys.modules[module]
        if not return_module:
            del mod
        
        import gc
        gc.collect()
        if "gc" not in loaded_modules:
            del gc
        
        # restore clock freq
        freq(250_000_000)
    
    if return_module:
        return mod
    else:
        return None

def record(run: str):
    from thumby import display, buttonA, buttonB, buttonC, buttonU, buttonD, buttonL, buttonR
    import random
    
    realFuncs = {"update": display.update}
    activeButtons = set()
    
    def capture(button, name):
        func = button.pressed
        realFuncs[name] = func
        def on_press():
            pressed_state = func()
            if pressed_state:
                activeButtons.add(name)
            return pressed_state
        button.pressed = on_press
    
    record_file = open(f"{run[:run.rfind('/')]}/demo.txt", "wt")
    random.seed(0xC0DEBEEF)
    # _seed = random.getrandbits(32)
    # record_file.write(f"$S={_seed}\n")
    # random.seed(_seed)
    
    global flush_counter
    flush_counter = 5
    
    def update():
        global flush_counter
        realFuncs["update"]()
        print("update")
        record_file.write("".join(activeButtons))
        record_file.write("\n")
        if flush_counter == 0:
            record_file.flush()
            flush_counter = 20
        else:
            flush_counter -= 1
        activeButtons.clear()
        
    
    display.update = update
    
    capture(buttonA, "A")
    capture(buttonB, "B")
    if buttonC:
        capture(buttonC, "C")
    capture(buttonD, "D")
    capture(buttonL, "L")
    capture(buttonR, "R")
    capture(buttonU, "U")
    
    print("recording begins")
    
    __import__(run)
    
    record_file.close()
    
    #restore
    buttonA.pressed = realFuncs["A"]
    buttonB.pressed = realFuncs["B"]
    if buttonC:
        buttonC.pressed = realFuncs["C"]
    buttonD.pressed = realFuncs["D"]
    buttonL.pressed = realFuncs["L"]
    buttonR.pressed = realFuncs["R"]
    buttonU.pressed = realFuncs["U"]
    display.update = realFuncs["update"]
    

if __name__ == "__main__":
    try:
        demo("/Games/RocketCup/demo.txt", 5, run = "/Games/RocketCup/RocketCup")
    except Exception as e:
        from io import StringIO
        import sys
        s=StringIO();
        sys.print_exception(err, s)
        s.seek(0)
        err_str = s.read()
        
        with open("err.log", "wt") as errf:
            errf.write(f"Error importing {gamePath}")
            errf.write("")
            errf.write(err_str)
        
        print(err_str)
        
        sleep_ms(500)
        