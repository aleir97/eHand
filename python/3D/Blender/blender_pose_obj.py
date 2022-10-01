'''
    - Python script to modify a 3d object pose via Blender's API
    
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
            f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\python\\3D\\com.txt", "r")            
            line = f.readline()
        
            if (line == 'REP\n' and self.state != 'REP'):
                self.state = 'REP'
                bpy.ops.poselib.apply_pose(pose_index=self.get_pose_index(skeleton, 'REST'))

            elif (line == 'EXT\n' and self.state != 'EXT') :
                self.state = 'EXT'
                bpy.ops.poselib.apply_pose(pose_index=self.get_pose_index(skeleton, 'EXT'))

            elif (line == 'FLEX\n'  and self.state != 'FLEX'):
                self.state = 'FLEX'
                bpy.ops.poselib.apply_pose(pose_index=self.get_pose_index(skeleton, 'FLEX'))

            elif (line == 'FIST\n'  and self.state != 'FIST'):
                self.state = 'FIST'           
                bpy.ops.poselib.apply_pose(pose_index=self.get_pose_index(skeleton, 'FIST'))
            
                                                            
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
