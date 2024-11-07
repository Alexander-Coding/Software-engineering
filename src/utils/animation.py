class Animation:
    def __init__(self, frames, frame_duration=0.1, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.current_time = 0
        self.finished = False
        
    def update(self, dt):
        if self.finished:
            return self.frames[-1]
            
        self.current_time += dt
        
        if self.current_time >= self.frame_duration:
            self.current_time = 0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    
        return self.frames[self.current_frame]
        
    def reset(self):
        self.current_frame = 0
        self.current_time = 0
        self.finished = False

class AnimationController:
    def __init__(self):
        self.animations = {}
        self.current_animation = None
        
    def add_animation(self, name, frames, frame_duration=0.1, loop=True):
        self.animations[name] = Animation(frames, frame_duration, loop)
        
    def play(self, name):
        if self.current_animation != name:
            self.current_animation = name
            self.animations[name].reset()
            
    def update(self, dt):
        if self.current_animation:
            return self.animations[self.current_animation].update(dt)
        return None