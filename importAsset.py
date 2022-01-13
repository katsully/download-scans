import unreal
import argparse

def importMyAsset():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", type=str, help="The file path of the new imported fbx scan")
	args = parser.parse_args()

	static_mesh_task = buildImportTask(args.file, '/Game/Scans', buildStaticMeshImportOptions())
	executeImportTasks([static_mesh_task])

def executeImportTasks(tasks):
	unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

def buildImportTask(filename, destination_path, options=None):
	task = unreal.AssetImportTask()
	task.set_editor_property('automated', True)
	task.set_editor_property('destination_name', '')
	task.set_editor_property('destination_path', destination_path)
	task.set_editor_property('filename', filename)
	task.set_editor_property('replace_existing', True)
	task.set_editor_property('save', True)
	return task

def buildStaticMeshImportOptions():
	options = unreal.FbxImportUI()
	options.set_editor_property('import_mesh', True)
	options.set_editor_property('import_textures', False)
	options.set_editor_property('import_materials', True)
	options.set_editor_property('import_as_skeletal', False)
	options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
	options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
	options.static_mesh_import_data.set_editor_property('import_uniform_scale', 20)
	options.static_mesh_import_data.set_editor_property('combine_meshes', True)
	options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
	options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
	return options

importMyAsset()