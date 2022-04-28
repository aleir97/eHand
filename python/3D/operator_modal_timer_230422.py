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
            
            bone9 = C.object.pose.bones['Bone.009']
            bone9.rotation_mode = 'XYZ'
            
            bone2 = C.object.pose.bones['Bone.002']
            bone2.rotation_mode = 'XYZ'
            
            bone4 = C.object.pose.bones['Bone.004']
            bone4.rotation_mode = 'XYZ'
            
            bone6 = C.object.pose.bones['Bone.006']
            bone6.rotation_mode = 'XYZ'
            
            fist = [bone9, bone2, bone4, bone6]
            
            f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\python\\3D\\com.txt", "r")            
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
                if self.state == 'FIST':
                    self.state = 'REP'
                    
                    for bone in fist:
                        bone.rotation_euler.rotate_axis(axis, radians(self.angle_rep))
                        bpy.ops.object.mode_set(mode='OBJECT')

                        #insert a keyframe
                        bone9.keyframe_insert(data_path="rotation_euler" ,frame=1)
                           
                else:
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
                
            elif (line == 'FIST\n'  and self.state != 'FIST'):
                self.state = 'FIST'
                angle = -100
                self.angle_rep = 100
                
                for bone in fist:
                    bone.rotation_euler.rotate_axis(axis, radians(angle))
                    bpy.ops.object.mode_set(mode='OBJECT')

                    #insert a keyframe
                    bone9.keyframe_insert(data_path="rotation_euler" ,frame=1)
            
              
                            
                                                    
        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(1.5, window=context.window)
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
