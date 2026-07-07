# 🎬 Kixel

> **Lossless image representation for kinematic motion data.**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.0.1-orange.svg)]()
[![License](https://img.shields.io/badge/license-MPL--2.0-green.svg)](LICENSE)

**Kixel** is a Python library for representing kinematic motion as images without losing numerical precision.

The library converts motion data from robots, articulated rigs, or 3D characters into an RGBA image representation that preserves every original bit of information. This allows motion sequences to be processed using image-oriented tools and machine learning pipelines while remaining fully reversible.

Unlike traditional approaches that normalize values into a limited image range, Kixel stores each motion value as a full `int32` and encodes its four bytes directly into the RGBA channels of a pixel.

---

## 📑 Table of Contents
- [Motivation](#-motivation)
- [Architecture](#-architecture)
- [Data Model](#-data-model)
- [Encoding Strategy](#-encoding-strategy)
- [Accumulator Model](#-accumulator-model)
- [Lossless Guarantee](#-lossless-guarantee)
- [Usage Example](#-usage-example)
- [Design Goals](#-design-goals)
- [Status & Future](#-status--future-directions)
- [License](#-license)

---

## 💡 Motivation

Modern computer vision architectures such as Convolutional Neural Networks (CNNs) and Vision Transformers (ViTs) are optimized for image-like inputs.

Kixel explores a simple question:

> *Can kinematic motion be represented as an image while preserving the exact original data?*

To answer this, Kixel treats each motion value as a collection of four bytes and stores those bytes directly in RGBA space. The resulting image can be consumed by image-based pipelines while remaining a **100% lossless** representation of the underlying motion.

---

## 🏗️ Architecture

```text
  ┌────────────┐
  │  Karacter  │
  └─────┬──────┘
        │ create_motion()
        ▼
  ┌────────────┐
  │  Kmatrix   │  (frames × dof)
  └─────┬──────┘
        │ encode_image()
        ▼
  ┌────────────┐
  │   Kimage   │  (frames × dof × 4)
  └─────┬──────┘
        │ decode_image()
        ▼
  ┌────────────┐      ┌────────────┐
  │  Kmatrix   │─────▶│   Kframe   │ (matframe / imgframe)
  └────────────┘      └─────┬──────┘
                            │ update_accumulator()
                            ▼
                      ┌────────────┐
                      │  Karacter  │
                      └────────────┘
```

---

## 🧬 Data Model

### `Karacter`
Represents a kinematic system such as a robot, articulated rig, or animated character.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `model_name` | `str` | Human-readable identifier |
| `dof_count` | `uint16` | Number of degrees of freedom |
| `accumulator` | `uint32[dof]` | Current accumulated state of every DOF |

### `Kmatrix`
Stores motion as a row-major matrix of signed 32-bit integers.
* **Shape:** `(frames, dof)`
* **Rows:** Represent frames.
* **Columns:** Represent degrees of freedom.
* **Values:** Motion deltas encoded as `int32`.

### `Kimage`
Lossless RGBA representation of a `Kmatrix`.
* **Shape:** `(frames, dof, 4)`
* **Final Dimension:** `[R, G, B, A]` corresponding to the four bytes of an `int32` value.

### `Kframe`
Represents a single motion frame.
* **Shape:** `(dof,)`
* **Implementation:** Direct subclass of `numpy.ndarray` for seamless interoperability with NumPy operations.

---

## 🎨 Encoding Strategy

Each motion value is stored as a signed 32-bit integer (`int32`). Kixel converts the value into four bytes using a fixed **big-endian** layout:

```text
       int32 (32 bits)
      ┌────┬────┬────┬────┐
      │ B0 │ B1 │ B2 │ B3 │
      └─┬──┴─┬──┴─┬──┴─┬──┘
        │    │    │    │
        ▼    ▼    ▼    ▼
       [R]  [G]  [B]  [A]   ◀── RGBA Pixel
```

The reverse operation reconstructs the original integer exactly. Because the transformation operates directly on raw bytes:
* ❌ No normalization is performed.
* ❌ No quantization is performed.
* ❌ No rounding occurs.
* ✅ **No precision is lost.**

---

## 🔄 Accumulator Model

Motion frames store **relative changes (deltas)**, while the accumulator stores the **current absolute state**.

For each frame:
```math
accumulator \leftarrow accumulator + delta
```

**Internally:**
* Frame values are represented as `int32`.
* Accumulator values are represented as `uint32`.
* Arithmetic wraps naturally at $2^{32}$.

This provides a compact circular representation suitable for rotational systems.

---

## 🔒 Lossless Guarantee

The following identity **always** holds:

```python
decoded = decode_image(encode_image(kmatrix))

assert np.array_equal(
    kmatrix.kmatrix,
    decoded.kmatrix
) # Returns True
```
*Encoding and decoding preserve every single bit of the original motion data.*

---

## 🚀 Usage Example

```python
from kixel import (
    Karacter,
    create_motion,
    encode_image,
    decode_image,
    matframe,
    update_accumulator,
)

# 1. Initialize a kinematic character (e.g., a 6-DOF robot arm)
robot = Karacter("robot_arm", 6)

# 2. Generate motion data
motion = create_motion(
    karacter=robot,
    frames_number=100
)

# 3. Encode to lossless RGBA image
image = encode_image(motion)

# 4. Decode back to exact original motion data
restored = decode_image(image)

# 5. Extract a specific frame and update the robot's state
frame = matframe(0, motion)
update_accumulator(robot, frame)
```

---

## ⚙️ Byte Order

Kixel uses a **fixed big-endian representation** for all encoding and decoding operations. This ensures identical results across platforms regardless of native machine endianness.

---

## 🎯 Design Goals

- [x] **Lossless** motion representation
- [x] **Deterministic** encoding and decoding
- [x] **NumPy-first** implementation
- [x] **Explicit** memory layout
- [x] **Platform-independent** byte ordering
- [x] **Compatibility** with image-processing workflows

---

## 📊 Status & Future Directions

### Current Status (v0.0.1)
**Implemented features:**
* `Karacter`, `Kmatrix`, `Kimage`, `Kframe` core classes.
* Motion creation & Frame extraction.
* Lossless image encoding & decoding.
* Accumulator updates.

### Future Directions
Potential areas of exploration include:
* 📦 Dataset generation utilities
* 🧠 Research workflows for vision-based motion understanding
* 📐 Spatiotemporal DOF indexing tools

---

## ⚖️ License

This project is licensed under the **Mozilla Public License 2.0 (MPL-2.0)**.  
See the [LICENSE](LICENSE) file for details.
