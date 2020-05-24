import json
import os
from pathlib import PurePath
from zipfile import ZipFile
import subprocess
import pandas as pd
from pyproj import Proj, transform
from arcgis.features import FeatureSet

# from shapely.geometry import Point
from boxnotes2html import BoxNote
from GitHub.HelperScripts import get_funcs
from GitHub.HelperScripts import edit_funcs


def convert_box_note_to_markdown(boxnote_path):
    filename = os.path.basename(boxnote_path).split(".")[0]
    note = BoxNote.from_file(boxnote_path)
    markdown = note.as_markdown()  # returns a markdown strings

    with open(f"{filename}.md", "w") as writer_obj:
        writer_obj.write(markdown)


def excel_to_csv(xls_path):
    filename = os.path.basename(xls_path).split(".")[0]
    data_xls = pd.read_excel(xls_path)
    data_xls.to_csv(filename + ".csv", encoding="utf-8")


def list_to_string(my_list, seperator=", ") -> str:
    return seperator.join(str(x) for x in my_list)


def zip_shapefiles_in_directory(
    data_folder, delete_originals=False
):  # Keep working on this.

    filenames = get_funcs.get_files_in_directory(
        directory=data_folder, extension=".shp"
    )

    for filename in filenames:
        path_parent = PurePath(filename).parent
        filename = PurePath(filename).stem
        with ZipFile(f"{path_parent}/{filename}.zip", "w") as zippy:
            zippy.write(f"{path_parent}/{filename}.shp", arcname=f"{filename}.shp")
            zippy.write(f"{path_parent}/{filename}.shx", arcname=f"{filename}.shx")
            zippy.write(f"{path_parent}/{filename}.dbf", arcname=f"{filename}.dbf")
            zippy.write(f"{path_parent}/{filename}.prj", arcname=f"{filename}.prj")

    if delete_originals:
        edit_funcs.delete_unzipped_shp_files_from_directory(data_folder)


def json_to_python_dict(json_str) -> dict:
    json_acceptable_string = json_str.replace("'", '"')
    python_dict = json.loads(json_acceptable_string)
    return python_dict


# def get_projection(factory_code):
#     s = osr.SpatialReference()
#     s.ImportFromEPSG(factory_code)
#     print(s.GetAttrValue("PROJCS"))


def pandas_df_to_esri_feature_set(pandas_df):
    return FeatureSet.from_dataframe(pandas_df)


def pandas_df_to_csv(pandas_df, csv_name, save_folder_path=None):
    return pandas_df.to_csv("{}/{}".format(save_folder_path, csv_name))


def dict_to_json(python_dict):
    return json.dumps(python_dict, ensure_ascii=False)


def string_to_json(string) -> json:
    return json.loads(string)


def ogr_convert_file(
    origin_file_path, converted_file_extension, destination_folder=None
):

    filename = PurePath(origin_file_path).stem
    file_types = {"geojson": "GeoJSON"}

    if not destination_folder:
        args = [
            "ogr2ogr",
            "-f",
            f"{file_types[converted_file_extension]}",
            f"{filename}.{converted_file_extension}",
            origin_file_path,
        ]
        print(args)
        subprocess.Popen(args)


# def pandas_df_to_geo_data_frame(df):
#     df["Coordinates"] = list(zip(df.Longitude, df.Latitude))
#     df["Coordinates"] = df["Coordinates"].apply(Point)
#
#     geo_data_frame = geopandas.GeoDataFrame(df, geometry="Coordinates")
#     geo_data_frame.crs = {"init": "epsg:4326"}
#
#     return geopandas.GeoDataFrame(df, geometry="Coordinates")


def geo_data_frame_to_shapefile(geo_data_frame, shapefile_save_path):
    geo_data_frame.to_file(filename=shapefile_save_path, driver="ESRI Shapefile")


def convert_coordinates(coordinates: tuple, inproj_epsg_id: str, out_proj_epsg_id: str):
    in_proj = Proj(init=f"epsg:{inproj_epsg_id}")
    out_proj = Proj(init=f"epsg:{out_proj_epsg_id}")
    projected_coordinates = transform(in_proj, out_proj, *coordinates)
    return projected_coordinates


# def combine_pdfs(pdf_binary_objs):
#     merger = PdfFileMerger()
#
#     for pdf in pdf_binary_objs:
#         merger.append(pdf)
#
#     with open("output/Dashboard_test_areas.pdf", "wb") as fout:
#         merger.write(fout)


if __name__ == "__main__":
    # convert_box_note("~/Downloads/Important_External_Contacts.boxnote")

    ogr_convert_file("~/Downloads/2.5_day.csv", "geojson")
