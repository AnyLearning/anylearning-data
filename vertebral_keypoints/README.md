# Spondylolisthesis Vertebral Landmark v1

- **Task:** Keypoint Detection
- **Dataset page:** https://doi.org/10.17632/5jdfdgp762.1
- **Dataset-level licence:** CC BY 4.0
- **Contents:** 698 sagittal lumbar-spine X-rays, four corner landmarks per
  visible vertebra

The source pixels are intentionally not committed to Git. The publisher assigns
CC BY 4.0 to version 1 while describing a mixture of locally collected and
BUU-LSPINE source images, so preserve the supplied attribution and review the
dataset record for your own use case.

For a quick AnyLearning walkthrough, download the attributed engineering
subset directly:

- [64-image training archive](https://cdn.anylearning.nrl.ai/datasets/vertebral_keypoints/v1/vertebral-keypoints-train-64.zip)
  — 463 vertebrae, SHA-256 `d07a61e1590847977dc5f380f8f8a2fa719504968c37f3f87ceabfac4a6776cd`
- [16-image validation archive](https://cdn.anylearning.nrl.ai/datasets/vertebral_keypoints/v1/vertebral-keypoints-valid-16.zip)
  — 119 vertebrae, SHA-256 `c04c363cffdb6cacd605f83d07fce5f257c3fab2b15d232bd5d7ba43a6f9507a`

Each ZIP includes `ATTRIBUTION.md`, the fixed DOI, the CC BY 4.0 link, and the
format conversion notes. No pixel values were modified.

Prepare import-ready archives from the main AnyLearning repository:

```bash
python prepare_vertebral_keypoints.py \
  --download \
  --output-dir /tmp/vertebral-keypoints
```

The tool downloads the fixed DOI version, checks its SHA-256, normalizes the
archive's mixed JSON and YOLO-pose annotations, retains attribution, and writes
`vertebral-keypoints-train.zip` plus `vertebral-keypoints-valid.zip`.

The complete converted split contains 494 training images / 3,151 vertebrae
and 204 validation images / 1,449 vertebrae. It is an engineering benchmark,
not a clinical validation dataset.
