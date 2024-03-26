#import packages
from exif import Image
import os
import piexif
import pvl
import arcpy

#define function to convert coordinates from decimal degrees to degrees, minutes, seconds
def decdeg2dms(dd):
    mult = -1 if dd < 0 else 1
    mnt,sec = divmod(abs(dd)*3600, 60)
    deg,mnt = divmod(mnt, 60)
    print ("did it")
    return mult*deg, mult*mnt, mult*sec


#define function to pull spacecraft info from pvl files
def pull_xyz(file_name):

    label = pvl.load(file_name)

    x = (label['GroundPoint']['SubSpacecraftLongitude'])
    # print(x)
    x_string = str(x)
    x_split = x_string.split("=")
    # print(x_split)
    x_split_2 = x_split[1].split(",")
    # print(x_split_2)
    x_value = x_split_2[0]
    print(x_value)
    # return(x_value)

    y = (label['GroundPoint']['SubSpacecraftLatitude'])
    # print(y)
    y_string = str(y)
    y_split = y_string.split("=")
    # print(y_split)
    y_split_2 = y_split[1].split(",")
    # print(y_split_2)
    y_value = y_split_2[0]
    print(y_value)
    # return(y_value)

    z = (label['GroundPoint']['SpacecraftAltitude'])
    # print(z)
    z_string = str(z)
    z_split = z_string.split("=")
    # print(z_split)
    z_split_2 = z_split[1].split(",")
    # print(z_split_2)
    z_value = z_split_2[0]
    print(z_value)
    return [x_value, y_value, z_value]


#define function that erases exif data attached to drone image (to get formatting), reproject and rewrite
def erase(my_image, y1):

    exif_dict = piexif.transplant(r'C:\Users\kdp167\Documents\MEta\METASHAPE_TUTORIAL\Five_Mile_Updated\DJI_0691.jpg', my_image)

    with open(my_image, 'rb') as image_file:
        my_image = Image(image_file)


    print(my_image.list_all())

    # my_image.delete_all()
    # my_image["gps_altitude"] = 199.034

    # print(my_image.gps_longitude_ref)
    # print(my_image.gps_version_id)
    #
    # list = my_image.list_all()
    # print(list)
    # for x in list:
    #     print (x)

    del my_image.image_description
    del my_image.make
    del my_image.model
    del my_image.orientation
    del my_image.x_resolution
    del my_image.y_resolution
    del my_image.resolution_unit
    del my_image.software
    del my_image.datetime
    del my_image.y_and_c_positioning
    del my_image._exif_ifd_pointer
    # del my_image._gps_ifd_pointer
    del my_image.xp_comment
    del my_image.xp_keywords
    del my_image.compression
    del my_image.jpeg_interchange_format
    del my_image.jpeg_interchange_format_length
    del my_image.exposure_time
    del my_image.f_number
    del my_image.exposure_program
    del my_image.photographic_sensitivity
    del my_image.exif_version
    del my_image.datetime_original
    del my_image.datetime_digitized
    del my_image.components_configuration
    del my_image.compressed_bits_per_pixel
    del my_image.shutter_speed_value
    del my_image.aperture_value
    del my_image.exposure_bias_value
    del my_image.max_aperture_value
    del my_image.subject_distance
    del my_image.metering_mode
    del my_image.light_source
    del my_image.flash
    del my_image.focal_length
    del my_image.maker_note
    del my_image.flashpix_version
    del my_image.color_space
    del my_image.pixel_x_dimension
    del my_image.pixel_y_dimension
    del my_image._interoperability_ifd_Pointer
    del my_image.exposure_index
    del my_image.file_source
    del my_image.scene_type
    del my_image.custom_rendered
    del my_image.exposure_mode
    del my_image.white_balance
    del my_image.digital_zoom_ratio
    del my_image.focal_length_in_35mm_film
    del my_image.scene_capture_type
    del my_image.gain_control
    del my_image.contrast
    del my_image.saturation
    del my_image.sharpness
    del my_image.device_setting_description
    del my_image.subject_distance_range

    x_rename = y1 + "_mapt.PVL"
    x_rename_filepath = os.path.join(r'E:\final_52_map _no_extract',x_rename)
    coord_list = pull_xyz(x_rename_filepath)
    print(coord_list)

    point_list_moon200 = coord_list  # For example, x=100000, y=200000, z=50000
    print("this is the coorlist for the pull xyz funtion", point_list_moon200)

    # Extract x, y, z values from the list
    x, y, z = point_list_moon200

    # Create a Point object
    point_moon200 = arcpy.Point(x, y, z)
    # Print point properties
    print("Point properties:")
    print(" X:  {0}".format(point_moon200.X))
    print(" Y:  {0}".format(point_moon200.Y))
    print(" Z:  {0}".format(point_moon200.Z))

    print("This is point_moon200, this is pre-projection", point_moon200)

    # Define the input coordinate system (Moon 200) and output coordinate system (WGS 1984)
    input_coordinate_system = arcpy.SpatialReference(103878)
    output_coordinate_system = arcpy.SpatialReference(4326)  # WKID for WGS 1984

    # Project the point from Moon 200 to WGS 1984
    projected_point = arcpy.PointGeometry(point_moon200, input_coordinate_system, "TRUE").projectAs(output_coordinate_system)

    # print("this is after point is projected", projected_point)

    # Extract x, y, z values from the projected point
    x_proj, y_proj, z_proj = projected_point.firstPoint.X, projected_point.firstPoint.Y, projected_point.firstPoint.Z

    # Print the projected point coordinates (optional)
    print("Projected Point coordinates: X={}, Y={}, Z={}".format(x_proj, y_proj, z_proj))

    # Now you can use x_proj, y_proj, z_proj variables in your arcpy operations





    # x_dd = decdeg2dms(float(coord_list[0]))
    proj_x_dd = decdeg2dms(x_proj)
    print("This is x_dd", proj_x_dd)
    # if float(coord_list[1]) < 0:



    y_dd_S = (float(y_proj) * -1)

    print("This is ydds", y_dd_S)

    # y_dd = decdeg2dms(y_dd_S)
    proj_y_dd = decdeg2dms(y_dd_S)
    print("This is ydd", proj_y_dd)

    # z_meter = (float(coord_list[2]) * 1000)
    z_meter = (z_proj * 1000)
    integer_z_meter = int(z_meter)
    print("This is after the z value is converted to integer", integer_z_meter)


    print("This is z_meter value", z_meter)

    # Sample list containing x, y, z values in Moon 200 coordinate system






    my_image.gps_longitude = (proj_x_dd)
    print("x added to jpg")


    my_image.gps_latitude = (proj_y_dd)
    print("y added to jpg")
    my_image.gps_latitude_ref = "S"

    my_image.gps_longitude_ref = "E"


    my_image.gps_altitude = (integer_z_meter)  # in meters
    print("z added to jpg")
    print(my_image.list_all())

    output_name = "C:\\Users\\kdp167\\Documents\\EXIF_Projection\\" + str(y1) + ".jpg"
    print(output_name)
    with open(output_name, 'wb') as new_image_file:
        new_image_file.write(my_image.get_file())


#loop through list
list = os.listdir(r"E:\big_chunk_run\chunk_img\JPG")

for x in list:
    # print(list)
    y = "E:\\big_chunk_run\\chunk_img\\JPG\\" + str(x)
    print (y)
    x_pass = x.split(".")[0]
    print(x_pass)
    # x_pass1 = x_pass[0]
    erase(y, x_pass)




#
# module = pvl.label
#
# print(module)




# variables = ['gps_latitude', 'gps_longitude', 'gps_altitude']
# for pvl_f in os.listdir(r'E:\final_52_map _no_extract'):
#     if pvl_f.endswith('.PVL'):
#         run_file = os.path.join(r'E:\final_52_map _no_extract',pvl_f)
#         pull_xyz(run_file)

