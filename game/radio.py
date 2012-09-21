import os
import pygame
import traceback
import numpy 
from numpy.fft import fft 
from math import log10 
import math
import copy


class Oscilloscope:
    
    def __init__(self): 
        # Constants
        self.WIDTH, self.HEIGHT = 210, 200
        self.TRACE, self.AFTER, self.GREY = (80, 255, 100),(20, 155, 40),(20, 110, 30)
    
    def open(self, screen=None):
        # Open window
        pygame.init()
        if screen:
            self.screen = screen
            self.screen.set_mode((self.WIDTH, self.HEIGHT), 0)
        else:
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0)
                
        # Create a blank chart with vertical ticks, etc
        self.blank = numpy.zeros((self.WIDTH, self.HEIGHT, 3))
        # Draw x-axis
        self.xaxis = self.HEIGHT/2
        self.blank[::, self.xaxis] = self.GREY
        self.blank[::, self.HEIGHT - 2] = self.TRACE
        self.blank[::, self.HEIGHT - 1] = self.TRACE
        self.blank[::50, self.HEIGHT - 4] = self.TRACE
        self.blank[::50, self.HEIGHT - 3] = self.TRACE
        self.blank[self.WIDTH - 2, ::] = self.TRACE
        self.blank[self.WIDTH - 1, ::] = self.TRACE
        self.blank[self.WIDTH - 3, ::40] = self.TRACE
        self.blank[self.WIDTH - 4, ::40] = self.TRACE
        
        # Draw vertical ticks
        vticks = [-80, -40, +40, +80]
        for vtick in vticks: self.blank[::5, self.xaxis + vtick] = self.GREY # Horizontals
        for vtick in vticks: self.blank[::50, ::5] = self.GREY               # Verticals
    
        # Draw the 'blank' screen.
        pygame.surfarray.blit_array(self.screen, self.blank)      # Blit the screen buffer
        pygame.display.flip()                                     # Flip the double buffer
        
            
    def update(self,time,frequency,power):
        try:
            pixels = copy.copy(self.blank)
            offset = 1
            for x in range(self.WIDTH):
                offset = offset - 1
                if offset < -1:
                    offset = offset + 1.1         
                try:
                    pow = power[int(x/10)]
                    log = math.log10( pow )
                    offset = ((pow / math.pow(10, math.floor(log))) + log)*1.8
                except:
                    pass
                try: 
                    y = float(self.xaxis) - (math.sin((float(x)+float(time))/5.0)*2.0*offset) 
                    pixels[x][y] = self.TRACE
                    pixels[x][y-1] = self.AFTER
                    pixels[x][y+1] = self.AFTER
                    if abs(y) > 120:
                        pixels[x][y-2] = self.AFTER
                        pixels[x][y+2] = self.AFTER
                except: 
                    pass
            pygame.surfarray.blit_array(self.screen, pixels)     # Blit the screen buffer
            pygame.display.flip()  
        except Exception,e:
            print traceback.format_exc()


class SoundSpectrum: 
    """ 
    Obtain the spectrum in a time interval from a sound file. 
    """ 

    left = None 
    right = None 
    
    def __init__(self, filename, force_mono=False): 
        """ 
        Create a new SoundSpectrum instance given the filename of 
        a sound file pygame can read. If the sound is stereo, two 
        spectra are available. Optionally mono can be forced. 
        """ 
        # Get playback frequency 
        nu_play, format, stereo = pygame.mixer.get_init() 
        self.nu_play = 1./nu_play 
        self.format = format 
        self.stereo = stereo 

        # Load sound and convert to array(s) 
        sound = pygame.mixer.Sound(filename) 
        a = pygame.sndarray.array(sound) 
        a = numpy.array(a) 
        if stereo: 
            if force_mono: 
                self.stereo = 0 
                self.left = (a[:,0] + a[:,1])*0.5 
            else: 
                self.left = a[:,0] 
                self.right = a[:,1] 
        else: 
            self.left = a 

    def get(self, data, start, stop): 
        """ 
        Return spectrum of given data, between start and stop 
        time in seconds. 
        """ 
        duration = stop-start 
        # Filter data 
        start = int(start/self.nu_play) 
        stop = int(stop/self.nu_play) 
        N = stop - start 
        data = data[start:stop] 

        # Get frequencies 
        frequency = numpy.arange(N/2)/duration 

        # Calculate spectrum 
        spectrum = fft(data)[1:1+N/2] 
        power = (spectrum).real 

        return frequency, power 

    def get_left(self, start, stop): 
        """ 
        Return spectrum of the left stereo channel between 
        start and stop times in seconds. 
        """ 
        return self.get(self.left, start, stop) 

    def get_right(self, start, stop): 
        """ 
        Return spectrum of the left stereo channel between 
        start and stop times in seconds. 
        """ 
        return self.get(self.right, start, stop) 

    def get_mono(self, start, stop): 
        """ 
        Return mono spectrum between start and stop times in seconds. 
        Note: this only works if sound was loaded as mono or mono 
        was forced. 
        """ 
        return self.get(self.left, start, stop) 

class LogSpectrum(SoundSpectrum): 
    """ 
    A SoundSpectrum where the spectrum is divided into 
    logarithmic bins and the logarithm of the power is 
    returned. 
    """ 

    def __init__(self, filename, force_mono=False, bins=20, start=1e2, stop=1e4): 
        """ 
        Create a new LogSpectrum instance given the filename of 
        a sound file pygame can read. If the sound is stereo, two 
        spectra are available. Optionally mono can be forced. 
        The number of spectral bins as well as the frequency range 
        can be specified. 
        """ 
        SoundSpectrum.__init__(self, filename, force_mono=force_mono) 
        start = log10(start) 
        stop = log10(stop) 
        step = (stop - start)/bins 
        self.bins = 10**numpy.arange(start, stop+step, step) 

    def get(self, data, start, stop): 
        """ 
        Return spectrum of given data, between start and stop 
        time in seconds. Spectrum is given as the log of the 
        power in logatithmically equally sized bins. 
        """ 
        f, p = SoundSpectrum.get(self, data, start, stop) 
        bins = self.bins 
        length = len(bins) 
        result = numpy.zeros(length) 
        ind = numpy.searchsorted(bins, f) 
        for i,j in zip(ind, p): 
            if i<length: 
                result[i] += j 
        return bins, result 

def load_files():
    files = []
    os.chdir("../radio")
    for file in os.listdir("."):
        if file.endswith(".ogg"):
            files.append(os.path.abspath(file))
    return files

def play_pygame(file):
    
    clock = pygame.time.Clock()
    # set up the mixer
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get right sound)
    pygame.mixer.init(freq, bitsize, channels, buffer)
    
    while not pygame.mixer.get_init():
        clock.tick(50)
    
    pygame.mixer.music.load(file)
    s = LogSpectrum(file,force_mono=True) 
    osc = Oscilloscope() 
    osc.open()
    
    f = None
    p = None
    running = True
    paused = False
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy() and running : 
        if not paused:
            start = pygame.mixer.music.get_pos() / 1000.0
            try:
                f,p = s.get_mono(start-0.001, start+0.001)
            except:
                pass
            osc.update(start*50,f,p)             
        pygame.time.wait(50)
        
        for event in pygame.event.get():
            if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_UP):
                    pygame.mixer.music.pause()
                    paused = True
                elif (event.key == pygame.K_DOWN):
                    pygame.mixer.music.unpause()
                    paused = False
            elif event.type == pygame.QUIT:
                running = False
    pygame.mixer.quit()
            
if __name__ == "__main__":
    try:
        files = load_files()
        if files:
            play_pygame(files[2])
    except Exception, e:
        print traceback.format_exc()
