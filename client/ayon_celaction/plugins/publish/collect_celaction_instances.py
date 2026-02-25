import os
import pyblish.api


class CollectCelactionInstances(pyblish.api.ContextPlugin):
    """ Adds the celaction render instances """

    label = "Collect Celaction Instances"
    order = pyblish.api.CollectorOrder + 0.1

    def process(self, context):
        task = context.data["task"]
        current_file = context.data["currentFile"]
        staging_dir = os.path.dirname(current_file)
        scene_file = os.path.basename(current_file)
        version = context.data["version"]

        folder_entity = context.data["folderEntity"]

        folder_attributes = folder_entity["attrib"]

        shared_instance_data = {
            "folderPath": folder_entity["path"],
            "frameStart": folder_attributes["frameStart"],
            "frameEnd": folder_attributes["frameEnd"],
            "handleStart": folder_attributes["handleStart"],
            "handleEnd": folder_attributes["handleEnd"],
            "fps": folder_attributes["fps"],
            "resolutionWidth": folder_attributes["resolutionWidth"],
            "resolutionHeight": folder_attributes["resolutionHeight"],
            "pixelAspect": 1,
            "step": 1,
            "version": version
        }

        celaction_kwargs = context.data.get(
            "passingKwargs", {})

        if celaction_kwargs:
            shared_instance_data.update(celaction_kwargs)

        # workfile instance
        product_base_type = "workfile"
        product_name = product_base_type + task.capitalize()
        # Create instance
        instance = context.create_instance(product_name)

        # creating instance data
        instance.data.update({
            "label": scene_file,
            "productName": product_name,
            "productType": product_base_type,
            "productBaseType": product_base_type,
            "family": product_base_type,
            "families": [product_base_type],
            "representations": []
        })

        # adding basic script data
        instance.data.update(shared_instance_data)

        # creating representation
        representation = {
            'name': 'scn',
            'ext': 'scn',
            'files': scene_file,
            "stagingDir": staging_dir,
        }

        instance.data["representations"].append(representation)

        self.log.info('Publishing Celaction workfile')

        # render instance
        product_name = f"render{task}Main"
        product_base_type = "render"
        instance = context.create_instance(name=product_name)

        # add folderEntity data into instance
        instance.data.update({
            "publish": True,
            "label": f"{product_name} - farm",
            "productType": product_base_type,
            "productBaseType": product_base_type,
            "family": product_base_type,
            "families": [product_base_type, "render.farm"],
            "productName": product_name,
            "representations": [],
        })

        # adding basic script data
        instance.data.update(shared_instance_data)

        self.log.info('Publishing Celaction render instance')
        self.log.debug(f"Instance data: `{instance.data}`")

        for i in context:
            self.log.debug(f"{i.data['families']}")
