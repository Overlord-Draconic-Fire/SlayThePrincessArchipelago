init 800 python:
    class MouseParallax(renpy.Displayable):
        def __init__(self,layer_info):
            import pygame
            super(renpy.Displayable,self).__init__()
            self.xoffset,self.yoffset=0.0,0.0
            self.sort_layer=sorted(layer_info,reverse=True)
            cflayer=[]
            masteryet=False
            for m,n in self.sort_layer:
                if(not masteryet)and(m<41):
                    cflayer.append("master")
                    masteryet=True
                cflayer.append(n)
            if not masteryet:
                cflayer.append("master")
            cflayer.extend(["transient","screens","overlay"])
            config.layers=cflayer
            config.overlay_functions.append(self.overlay)
            if renpy.variant("console"):
                self.controller_gyro_x = 0
                self.controller_gyro_y = 0
                self.gyro_clock = pygame.time.Clock()
            return
        def render(self,width,height,st,at):
            return renpy.Render(width,height)
        def parallax(self,m):
            func = renpy.curry(trans)(disp=self, m=m)
            return Transform(function=func)
        def overlay(self):
            ui.add(self)
            for m,n in self.sort_layer:
                renpy.layer_at_list([self.parallax(m)],n)
            return
        def lerp(self, a, b, t) -> float:
            return (1 - t) * a + t * b
        def event(self,ev,x,y,st):
            import pygame
            if persistent.parallax_on:
                if ev.type==pygame.MOUSEMOTION and not renpy.variant("console_nintendo_switch"):
                    self.xoffset,self.yoffset=((float)(x)/(config.screen_width))-0.5,((float)(y)/(config.screen_height))-0.5
                elif renpy.variant("console") and ev.type==pygame.CONTROLLERSENSORUPDATE:
                    ms = min (100, self.gyro_clock.tick()) / 100
                    if renpy.variant("console_nintendo_switch"):
                        self.controller_gyro_x += ev.data[2] * 2
                        self.controller_gyro_y += -ev.data[0] * 2
                    else:
                        self.controller_gyro_x += ev.data[2] * 0.01
                        self.controller_gyro_y += -ev.data[0] * 0.01
                    self.controller_gyro_x = max(-1, min((float)(self.controller_gyro_x), 1))
                    self.controller_gyro_y = max(-1, min((float)(self.controller_gyro_y), 1))
                    self.xoffset = max(-0.5, min((float)(self.lerp(self.xoffset, self.controller_gyro_x, ms)), 0.5))
                    self.yoffset = max(-0.5, min((float)(self.lerp(self.yoffset, self.controller_gyro_y, ms)), 0.5))
            return

    MouseParallax([(40,"farback"),(20,"back"),(-20,"front"),(-40,"inyourface")])

    def trans(d, st, at, disp=None, m=None):
        d.xoffset, d.yoffset = int(round(m*disp.xoffset)), int(round(m*disp.yoffset))
        return 0

init:
    transform flip:
        xzoom -1.0

    transform yflip:
        yzoom -1.0

    transform doubleflip:
        yzoom -1.0
        xzoom -1.0

    image menu_logo:
        "images/menu/logo menu.png"

    $ Preference("gl framerate", 30)


# commented out code below showing how to apply a shader to written out text.
#image top_text = ParameterizedText(xalign=0.5, yalign=0.0, slow=True, xsize = 500)
#show top_text "You're on a path in the woods. And at the end of that path is a cabin. And in the basement of that cabin is a princess.\n" onlayer front at distortion, truecenter
