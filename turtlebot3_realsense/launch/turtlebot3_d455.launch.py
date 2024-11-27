
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 获取包的路径
    realsense_prefix = get_package_share_directory('realsense2_camera')
    
    # 配置启动参数
    config_params = {
        'device_type': 'd455',
        'enable_color': 'true',
        'enable_depth': 'true',
        'depth_module.profile': '640x480x30',
        'rgb_camera.profile': '640x480x30',
        'align_depth.enable': 'true'
    }
    
    # 包含RealSense相机的启动文件
    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            realsense_prefix, 'launch', 'rs_launch.py')]),
        launch_arguments=config_params.items()
    )
    
    # 创建静态TF发布器
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0.172', '0', '0', '0', 'base_link', 'd455_link']
    )
    
    # 返回启动描述
    return LaunchDescription([
        realsense_launch,
        static_tf
    ])