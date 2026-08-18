## AnyLearning - Datasets

This repository contains a collection of datasets for different tasks - Used for training and testing models of AnyLearning.

Licences are recorded in [LICENSES.md](LICENSES.md). AnyLearning ships commercially,
so **check that file before using a dataset in anything that leaves your machine** —
two of the datasets below have no recorded licence yet.

### Licence-cleared

| Task | Dataset | Licence |
|---|---|---|
| Image classification | [ZhangLabData: Chest X-Ray](zhanglabdata_chest_xray/) | CC BY 4.0 |
| Object detection | [Safety Helmet and Reflective Jacket Detection](helmet_jacket/) | Apache 2.0 |
| Semantic segmentation | [Electron Microscopy Particle Segmentation](electron_microscopy_particle_segmentation/) | CC BY 4.0 |
| Handpose classification | [American Sign Language Letters](american_sign_language/) | Public Domain |
| Keypoint detection | [Generated Keypoint Stick Figures](keypoint_stick_figures/) | CC0 1.0 |

The first four are the real datasets AnyLearning's test suite loads via `REAL_DATASETS` in
`tests/fixtures/datasets.py`.

The keypoint set is a deterministic, generated starter project: 24 training
images, 8 validation images, two instances per image and five named landmarks.
It is intentionally simple and is suitable for tutorials and mechanical tests,
not model-quality claims.

Small, ready-to-upload keypoint archives are also mirrored on the AnyLearning
CDN:

- [CC0 stick figures: train.zip](https://cdn.anylearning.nrl.ai/datasets/keypoint_stick_figures/train.zip)
  and [valid.zip](https://cdn.anylearning.nrl.ai/datasets/keypoint_stick_figures/valid.zip)
- [CC BY 4.0 vertebral X-ray subset: 64-image train.zip](https://cdn.anylearning.nrl.ai/datasets/vertebral_keypoints/v1/vertebral-keypoints-train-64.zip)
  and [16-image valid.zip](https://cdn.anylearning.nrl.ai/datasets/vertebral_keypoints/v1/vertebral-keypoints-valid-16.zip)

Every vertebral archive embeds its attribution and conversion notes. See the
dataset README before using medical images; this is an engineering example,
not a clinically validated dataset.

### Fetch on demand for engineering validation

| Task | Dataset | Why it is not committed |
|---|---|---|
| Keypoint detection | [Spondylolisthesis Vertebral Landmark v1](vertebral_keypoints/) | The complete source is fetched from its fixed DOI; a small attributed subset is mirrored on the CDN. |

### Licence not yet recorded

| Task | Dataset | Status |
|---|---|---|
| Image classification | [NEU Surface Defect](neu_surface_defect/) | No README, no licence — see [LICENSES.md](LICENSES.md) |
| Instance segmentation | [Dental Segmentation](dental_segment/) | Roboflow export with no licence line |

Local experimentation is fine. Shipped examples, demos, and marketing material are not,
until the upstream terms are confirmed and written down.

## Using these with AnyLearning

Each dataset ships as per-subset zips. Clone this repository next to the
`anylearning` checkout, or point `ANYLEARNING_DATA_DIR` at it, and the test suite
will find it automatically:

```bash
git clone https://github.com/AnyLearning/anylearning-data
pytest tests/e2e/test_real_datasets_e2e.py
```

Archives are extracted into `~/.cache/anylearning-test-data/`, never back into a
repository. See `docs/testing.md` in the main repository.
