'''
    - Python script to modify a 3d object's euler rotation via Blender's API
    
	Copyright (C) 2021 Alejandro Iregui Valcarcel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import bpy
import mathutils
from math import radians

class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"
    state = ''
    angle_rep = 0
     
    _timer = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            C = bpy.context
            bone = C.object.pose.bones['Bone.001']
            bone.rotation_mode = 'XYZ'
            axis = 'X'
            
            f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\PY\\3D\\com.txt", "r")            
            line = f.readline()
            #print(line)
            #print(self.state)
            
           
            if (line == 'EXT\n' and self.state != 'EXT') :
                self.state = 'EXT'
                angle = 100
                self.angle_rep = -100
                bone.rotation_euler.rotate_axis(axis, radians(angle))
                bpy.ops.object.mode_set(mode='OBJECT')
                
                #insert a keyframe
                bone.keyframe_insert(data_path="rotation_euler" ,frame=1)
            
            elif (line == 'REP\n' and self.state != 'REP'):
                self.state = 'REP'
                
                bone.rotation_euler.rotate_axis(axis, radians(self.angle_rep))
                bpy.ops.object.mode_set(mode='OBJECT')

                #insert a keyframe
                bone.keyframe_insert(data_path="rotation_euler" ,frame=1)  
            
            elif (line == 'FLEX\n'  and self.state != 'FLEX'):
                self.state = 'FLEX'
                angle = -100
                self.angle_rep = 100
                
                bone.rotation_euler.rotate_axis(axis, radians(angle))
                bpy.ops.object.mode_set(mode='OBJECT')

                #insert a keyframe
                bone.keyframe_insert(data_path="rotation_euler" ,frame=1)    
                                                    
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
