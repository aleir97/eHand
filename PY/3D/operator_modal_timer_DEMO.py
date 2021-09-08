import bpy
import mathutils
from math import radians

class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"
    
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
            print(line)
            
            if line == 'EXT\n':
                angle = 100
                bone.rotation_euler.rotate_axis(axis, radians(angle))
                bpy.ops.object.mode_set(mode='OBJECT')

                #insert a keyframe
                bone.keyframe_insert(data_path="rotation_euler" ,frame=1)
            
            elif line == 'STOP\n':
                angle = -100
                bone.rotation_euler.rotate_axis(axis, radians(angle))
                bpy.ops.object.mode_set(mode='OBJECT')

                #insert a keyframe
                bone.keyframe_insert(data_path="rotation_euler" ,frame=1)  
            
            elif line == 'FLEX\n':
                angle = -100
                bone.rotation_euler.rotate_axis(axis, radians(angle))
                bpy.ops.object.mode_set(mode='OBJECT')

                #insert a keyframe
                bone.keyframe_insert(data_path="rotation_euler" ,frame=1)    
                            
            elif line == 'STOP2\n':
                angle = 100
                bone.rotation_euler.rotate_axis(axis, radians(angle))
                bpy.ops.object.mode_set(mode='OBJECT')

                #insert a keyframe
                bone.keyframe_insert(data_path="rotation_euler" ,frame=1)   
                        
        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(30, window=context.window)
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
