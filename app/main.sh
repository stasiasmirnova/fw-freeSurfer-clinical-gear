#! /bin/bash
#
# Run script for flywheel/recon-all-clinical Gear.
#
# Authorship: Anastasia Smirnova
#
##############################################################################
# Define directory names and containers

FLYWHEEL_BASE=/flywheel/v0
INPUT_DIR=$FLYWHEEL_BASE/input/
OUTPUT_DIR=$FLYWHEEL_BASE/output
CONFIG_FILE=$FLYWHEEL_BASE/config.json
CONTAINER='[flywheel/recon-all-clinical]'
threads = 4

source /usr/local/freesurfer/SetUpFreeSurfer.sh
##############################################################################
# Parse configuration
function parse_config {

  CONFIG_FILE=$FLYWHEEL_BASE/config.json
  MANIFEST_FILE=$FLYWHEEL_BASE/manifest.json

  if [[ -f $CONFIG_FILE ]]; then
    echo "$(cat $CONFIG_FILE | jq -r '.config.'$1)"
  else
    CONFIG_FILE=$MANIFEST_FILE
    echo "$(cat $MANIFEST_FILE | jq -r '.config.'$1'.default')"
  fi
}

# define output choise:
config_output_nifti="$(parse_config 'output_nifti')"
config_output_mgh="$(parse_config 'output_mgh')"
# define options:
config_rob="$(parse_config 'robust')"

echo "robust is ${config_rob}"
##############################################################################
# Define brain and face templates

brain_template=$FLYWHEEL_BASE/talairach_mixed_with_skull.gca
face_template=$FLYWHEEL_BASE/face.gca

##############################################################################
# Handle INPUT file

# Find input file In input directory with the extension
# .nii, .nii.gz
input_file=`find $INPUT_DIR -iname '*.nii' -o -iname '*.nii.gz'`

# Check that input file exists
if [[ -e $input_file ]]; then
  echo "${CONTAINER}  Input file found: ${input_file}"

    # Determine the type of the input file
  if [[ "$input_file" == *.nii ]]; then
    type=".nii"
  elif [[ "$input_file" == *.nii.gz ]]; then
    type=".nii.gz"
  fi
  # Get the base filename
  base_filename=`basename "$input_file" $type`
  
else
  echo "${CONTAINER} inputs were found within input directory $INPUT_DIR"
  exit 1
fi

##############################################################################
# Run mri_synthseg algorithm

# Set initial exit status
recon_all_clinical_exit_status=0

# Set base output_file name
output_file=$OUTPUT_DIR/"$base_filename"'_recon_all_clinical'
echo "output_file is $output_file"


if [[ $config_rob == 'true' ]]; then
  robust='--robust'
fi

# Run recon-all-clinical with options
if [[ -e $input_file ]]; then
  echo "Running recon-all-clinical..."
  ls -l
  chmod +x recon_all_clinical.sh 
  recon_all_clinical.sh $input_file $base_filename $threads $output_file
  recon_all_clinical_exit_status=$?
fi

##############################################################################
# Handle Exit status

if [[ $recon_all_clinical_exit_status == 0 ]]; then
  echo -e "${CONTAINER} Success!"
  exit 0
else
  echo "${CONTAINER}  Something went wrong! recon-all-clinical exited non-zero!"
  exit 1
fi
return [recon-all-clinical_exit_status]