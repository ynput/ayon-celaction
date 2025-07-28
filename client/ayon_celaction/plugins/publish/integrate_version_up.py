import shutil

import pyblish.api

from ayon_core.lib import version_up
try:
    from ayon_core.pipeline.workfile import (
        save_workfile_info,
        find_workfile_rootless_path,
    )
except ImportError:
    save_workfile_info = None


class VersionUpScene(pyblish.api.ContextPlugin):
    order = pyblish.api.IntegratorOrder + 0.5
    label = "Version Up Scene"
    families = ["workfile"]
    optional = True
    active = True

    def process(self, context):
        current_file = context.data["currentFile"]
        v_up = version_up(current_file)
        self.log.debug(f"Current file is: {current_file}")
        self.log.debug(f"Version up: {v_up}")

        shutil.copy2(current_file, v_up)

        # Create workfile information in AYON server
        if save_workfile_info is not None:
            host_name = context.data["hostName"]
            anatomy = context.data["anatomy"]
            project_name = context.data["projectName"]
            project_settings = context.data["project_settings"]
            project_entity = context.data["projectEntity"]
            folder_entity = context.data["folderEntity"]
            task_entity = context.data["taskEntity"]
            rootless_path = find_workfile_rootless_path(
                v_up,
                project_name,
                folder_entity,
                task_entity,
                host_name,
                project_entity=project_entity,
                project_settings=project_settings,
                anatomy=anatomy,
            )
            save_workfile_info(
                project_name,
                task_entity["id"],
                rootless_path,
                host_name,
            )

        self.log.info(f"Scene saved into new version: {v_up}")
