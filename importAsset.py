import unreal
import argparse
import os
import warnings

def importMyAsset():
	parser = argparse.ArgumentParser()
	# unreal will pass in the file name
	parser.add_argument("-f", "--file", type=str, help="The file path of the new imported fbx scan")
	args = parser.parse_args()

	# files inside the game engine must start with /Game if the game is currently running, otherwise you would use /Content
	static_mesh_task = buildImportTask(args.file, '/Game/Scans', buildStaticMeshImportOptions())
	executeImportTasks([static_mesh_task])

	# rename material files to prevent overwriting with other scans
	dir_name = args.file.replace(".fbx", ".fbm")
	object_name = dir_name.split('.')[0]
	last_char_index = object_name.rfind("/")
	new_string = object_name[last_char_index+1:]
	renames = []
	rename_data1 = unreal.AssetRenameData(unreal.load_asset('/Game/Scans/UnnamedMaterial'), '/Game/Scans', "M_" + new_string)
	renames.append(rename_data1)
	rename_data2 = unreal.AssetRenameData(unreal.load_asset('/Game/Scans/0_2'), '/Game/Scans', "Texture_" + new_string)
	renames.append(rename_data2)
	normal_asset = unreal.load_asset('/Game/Scans/1_2')
	if normal_asset is None:
		normal_asset = unreal.load_asset('/Game/Scans/1_2')
		if normal_asset is None:
			print("no normal")
		else:
			rename_data3 = unreal.AssetRenameData(unreal.load_asset('/Game/Scans/2_2'), '/Game/Scans', 'Normal_' + new_string)
			renames.append(rename_data3)
	else:
		rename_data3 = unreal.AssetRenameData(unreal.load_asset('/Game/Scans/1_2'), '/Game/Scans', 'Normal_' + new_string)
		renames.append(rename_data3)
	unreal.AssetToolsHelpers.get_asset_tools().rename_assets_with_dialog(renames)
	

def executeImportTasks(tasks):
	unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
	for t in tasks:
		print(t.get_editor_property('imported_object_paths'))

def buildImportTask(filename, destination_path, options=None):
	print(filename)
	task = unreal.AssetImportTask()
	task.set_editor_property('automated', True)
	# if destination_name is '' it will use the on-disk filename
	task.set_editor_property('destination_name', '')
	task.set_editor_property('destination_path', destination_path)
	task.set_editor_property('filename', filename)
	task.set_editor_property('replace_existing', True)
	task.set_editor_property('options', options) 
	task.set_editor_property('save', True)
	return task

def buildStaticMeshImportOptions():
	options = unreal.FbxImportUI()
	options.set_editor_property('import_mesh', True)
	options.set_editor_property('import_textures', True)
	options.set_editor_property('import_materials', True)
	options.set_editor_property('import_as_skeletal', False)
	options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
	options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
	# by default this is 1, but then everything is very small
	# feel free to adjust as needed
	options.static_mesh_import_data.set_editor_property('import_uniform_scale', 50)
	options.static_mesh_import_data.set_editor_property('combine_meshes', True)
	options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
	options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
	return options

warnings.filterwarnings("error")
importMyAsset()