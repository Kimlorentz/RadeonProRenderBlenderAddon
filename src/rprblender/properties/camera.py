import bpy
import pyrpr
from bpy.props import (
    PointerProperty,
    FloatProperty,
    BoolProperty,
)

from rprblender import utils
from rprblender.utils import logging
from . import RPR_Properties


log = logging.Log(tag='Camera')


class RPR_CameraProperties(RPR_Properties):
    motion_blur: BoolProperty(
        name="Motion Blur",
        description="Enable Motion Blur",
        default=True
    )

    motion_blur_exposure: FloatProperty(
        name="Motion Blur Exposure",
        description="Motion Blur Exposure",
        min=0,
        default=1.0,
    )

    def sync(self, rpr_context, obj):
        camera = self.id_data
        log("Syncing camera: %s" % camera.name)
        
        rpr_camera = rpr_context.create_camera(utils.key(obj))
        rpr_camera.set_name(camera.name)
        rpr_camera.set_transform(utils.get_transform(obj))
        
        rpr_camera.set_clip_plane(camera.clip_start, camera.clip_end)
        rpr_camera.set_lens_shift(camera.shift_x, camera.shift_y)   # TODO: Shift has to be fixed

        mode = {
            'ORTHO': pyrpr.CAMERA_MODE_ORTHOGRAPHIC,
            'PERSP': pyrpr.CAMERA_MODE_PERSPECTIVE,
            'PANO': pyrpr.CAMERA_MODE_LATITUDE_LONGITUDE_360,
            }[camera.type]
        rpr_camera.set_mode(mode)

        # TODO: Currently we set only perspective parameters
        rpr_camera.set_focal_length(camera.lens)
        if camera.sensor_fit != 'VERTICAL':
            ratio = rpr_context.width / rpr_context.height
            rpr_camera.set_sensor_size(camera.sensor_width, camera.sensor_width / ratio)
        else:
            rpr_camera.set_sensor_size(camera.sensor_width, camera.sensor_height)

    @classmethod
    def register(cls):
        log("Register")
        bpy.types.Camera.rpr = PointerProperty(
            name="RPR Camera Settings",
            description="RPR Camera settings",
            type=cls,
        )

    @classmethod
    def unregister(cls):
        log("Unregister")
        del bpy.types.Camera.rpr
