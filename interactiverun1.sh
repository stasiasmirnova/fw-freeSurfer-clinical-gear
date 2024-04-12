#!/usr/bin/env bash 

GEAR=fw-freeSurfer-clinical-gear
IMAGE=flywheel/recon-all-clinical:0.1.9
LOG=recon-all-clinical-0.1.9-66166b9e3771258f3fcb69ab


# Command:
docker run -it --rm --entrypoint bash\
	-v /Users/flywheel/Downloads/fw-clinical/${GEAR}/app/:/flywheel/v0/app\
	-v /Users/flywheel/Downloads/fw-clinical/${GEAR}/utils:/flywheel/v0/utils\
	-v /Users/flywheel/Downloads/fw-clinical/${GEAR}/run.py:/flywheel/v0/run.py\
	-v /Users/flywheel/Downloads/fw-clinical/${GEAR}/${LOG}/input:/flywheel/v0/input\
	-v /Users/flywheel/Downloads/fw-clinical/${GEAR}/${LOG}/output:/flywheel/v0/output\
	-v /Users/flywheel/Downloads/fw-clinical/${GEAR}/${LOG}/work:/flywheel/v0/work\
	-v /Users/flywheel/Downloads/fw-clinical/${GEAR}/${LOG}/config.json:/flywheel/v0/config.json\
	-v /Users/flywheel/Downloads/fw-clinical/${GEAR}/${LOG}/manifest.json:/flywheel/v0/manifest.json\
	$IMAGE