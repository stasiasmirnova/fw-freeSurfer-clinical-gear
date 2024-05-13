# Recon-all-clinical

This gear runs the recon-all-clinical tool ( https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all-clinical ) available in Freesurfer > 7.4.0. This is the out-of-the-box version that runs cortical surface reconstruction and analysis of brain MRI scans of any modality, contrast and resolution without retraining and fine-tuning. This gear has been developed with the processing of Hyperfine data in mind. 

Hyperfine - Construction of isotropic image from tri-plane othogonal aquisitions

## Overview

[Usage](#usage)

[FAQ](#faq)

### Summary
Takes three orthogonally acquired images (axial, coronal, sagittal) collected on Hyperfine Swoop and combines into a single 1mm isotropic image. 

### Cite

**license:**


**url:** <https://gitlab.com/flywheel-io/flywheel-apps/>


Cortical analysis of heterogeneous clinical brain MRI scans for large-scale neuroimaging studies. K Gopinath, DN Greeve, S Das, S Arnold, C Magdamo, JE Iglesias
SynthSeg: Segmentation of brain MRI scans of any contrast and resolution without retraining. B Billot, DN Greve, O Puonti, A Thielscher, K Van Leemput, B Fischl, AV Dalca, JE Iglesias. Medical Image Analysis, 83, 102789 (2023).
Robust machine learning segmentation for large-scale analysis of heterogeneous clinical brain MRI datasets. B Billot, C Magdamo, SE Arnold, S Das, JE Iglesias. PNAS, 120(9), e2216399120 (2023).
SynthSR: a public AI tool to turn heterogeneous clinical brain scans into high-resolution T1-weighted images for 3D morphometry. JE Iglesias, B Billot, Y Balbastre, C Magdamo, S Arnold, S Das, B Edlow, D Alexander, P Golland, B Fischl. Science Advances, 9(5), eadd3607 (2023).

### Classification

*Category:* analysis

*Gear Level:*

* [ ] Project
* [x] Subject
* [x] Session
* [ ] Acquisition
* [ ] Analysis

----

### Inputs

* api-key
  * **Name**: api-key
  * **Type**: object
  * **Optional**: true
  * **Classification**: api-key
  * **Description**: Flywheel API key.

### Config

* debug
  * **Name**: debug
  * **Type**: boolean
  * **Description**: Log debug messages
  * **Default**: false

* input
  * **Base**: file
  * **Description**: input file (usually isotropic reconstruction)
  * **Optional**: false

### Outputs
* output
  * **Base**: file
  * **Description**: segmentated file 
  * **Optional**: false

* parcelation
  * **Base**: file
  * **Description**: parcelation file 
  * **Optional**: true

* vol
  * **Base**: file
  * **Description**: volume estimation file (csv)
  * **Optional**: true

* QC
  * **Base**: file
  * **Description**: QC file (csv)
  * **Optional**: true


#### Metadata

No metadata currently created by this gear

### Pre-requisites

- Three dimensional structural image

#### Prerequisite Gear Runs

This gear runs on BIDS-organized data. To have your data BIDS-ified, it is recommended
that you run, in the following order:

1. ***dcm2niix***
    * Level: Any
2. ***file-metadata-importer***
    * Level: Any
3. ***file-classifier***
    * Level: Any

#### Prerequisite

## Usage

This section provides a more detailed description of the gear, including not just WHAT
it does, but HOW it works in flywheel

### Description

This gear is run at either the `Subject` or the `Session` level. It downloads the data
for that subject/session into the `/flwyhweel/v0/work/bids` folder and then runs the
`synthseg` pipeline on it.

After the pipeline is run, the output folder is zipped and saved into the analysis
container.

#### File Specifications

This section contains specifications on any input files that the gear may need

### Workflow

A picture and description of the workflow

```mermaid
  graph LR;
    A[T1w]:::input --> FW;
    FW[FW] --> FMI;
    FMI((file-metadata-importer)):::gear --> FC;
    FC((file-classifier)):::gear --> D2N;
    D2N((dcm2niix)):::gear --> CB;
    CB((curate-bids)):::gear --> CISO;
    CISO((ciso)):::gear --> SS;
    SS((synthseg)):::gear --> ANA;
    ANA[Analysis]:::container;
    
    classDef container fill:#57d,color:#fff
    classDef input fill:#7a9,color:#fff
    classDef gear fill:#659,color:#fff
```

Description of workflow

1. Upload data to container
2. Prepare data by running the following gears:
   1. file metadata importer
   2. file classifier
   3. dcm2niix
   4. MRIQC (optional)
   5. curate bids
3. Select either a subject or a session.
4. Run the ciso gear (Hyperfine triplane aquisitions)
5. Run the synthseg gear
6. Gear places output in Analysis

### Use Cases

## FAQ

[FAQ.md](FAQ.md)

## Contributing

[For more information about how to get started contributing to that gear,
checkout [CONTRIBUTING.md](CONTRIBUTING.md).]
