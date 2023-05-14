import bpy
import mathutils
from math import radians
from enum import IntEnum, auto
  
class poses(IntEnum):
    EXT   = 1
    FIST  = 2
    FLEX  = 3
    NEY   = 4
    PEACE = 5
    REP   = 6
    ROCK  = 8
    SEÑ   = 9

class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"
    state = ''
    angle_rep = 0
    bone10_angle_rep = 0
     
    _timer = None

    def get_pose_index(self, obj, pose_name ):
        idx = 0
        for pm in obj.pose_library.pose_markers:
            if pose_name == pm.name:
                return idx
            idx += 1
        return None


    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            skeleton = bpy.context.object
            f = open("/Users/aleir97/Documents/eHand/python/3D/com.txt", "r")            
            line = f.readline()
        
            if (line == 'REP\n' and self.state != 'REP'):
                self.state = 'REP'
                bpy.data.objects['Esqueleto'].animation_data.action = bpy.data.actions[poses.REP] 
            
            elif (line == 'EXT\n' and self.state != 'EXT') :
                self.state = 'EXT'
                bpy.data.objects['Esqueleto'].animation_data.action = bpy.data.actions[poses.EXT] 
                
            elif (line == 'FLEX\n'  and self.state != 'FLEX'):
                self.state = 'FLEX'
                bpy.data.objects['Esqueleto'].animation_data.action = bpy.data.actions[poses.FLEX] 

            elif (line == 'FIST\n'  and self.state != 'FIST'):
                self.state = 'FIST'           
                bpy.data.objects['Esqueleto'].animation_data.action = bpy.data.actions[poses.FIST] 

            elif (line == 'NEY\n'  and self.state != 'NEY'):
                self.state = 'NEY'           
                bpy.data.objects['Esqueleto'].animation_data.action = bpy.data.actions[poses.NEY] 

            elif (line == 'PEACE\n'  and self.state != 'PEACE'):
                self.state = 'PEACE'           
                bpy.data.objects['Esqueleto'].animation_data.action = bpy.data.actions[poses.PEACE] 

            elif (line == 'ROCK\n'  and self.state != 'ROCK'):
                self.state = 'ROCK'           
                bpy.data.objects['Esqueleto'].animation_data.action = bpy.data.actions[poses.ROCK] 

            elif (line == 'SEÑ\n'  and self.state != 'SEÑ'):
                self.state = 'SEÑ'           
                bpy.data.objects['Esqueleto'].animation_data.action = bpy.data.actions[poses.SEÑ] 
            
                                                            
        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(ModalTimerOperator)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()
