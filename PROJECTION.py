import arcpy

arcpy.env.overwriteOutput = True


# ptList =[[20.000,43.000],[25.500, 45.085],[26.574, 46.025], [28.131, 48.124]]
# pt = arcpy.Point()
# ptGeoms = []
# for p in ptList:
#     pt.X = p[0]
#     pt.Y = p[1]
#     ptGeoms.append(arcpy.PointGeometry(pt))

# input_features = arcpy.CopyFeatures_management(ptGeoms, r"C:\Users\kdp167\Documents\project test\test.shp")

input_features = r"C:\Users\kdp167\Documents\project test\moonpoint.shp"


# input data is in NAD 1983 UTM Zone 11N coordinate system
# input_features = r"C:/data/Redlands.shp"

# output data
output_feature_class = r"C:\Users\kdp167\Documents\project test/moonproj.shp"

# create a spatial reference object for the output coordinate system
out_coordinate_system = arcpy.SpatialReference(3857)

# in_coordinate_system = arcpy.SpatialReference(3857)


# arcpy.management.Project(in_dataset, out_dataset, out_coor_system, {transform_method}, {in_coor_system}, {preserve_shape}, {max_deviation}, {vertical})
arcpy.management.Project(input_features, output_feature_class, out_coordinate_system)