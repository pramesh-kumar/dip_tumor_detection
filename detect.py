# detect.py

import argparse
import cv2 as cv
from predict_tumor import predict_tumor
from display_tumor import DisplayTumor
import os
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Brain Tumor Detection & Optional Segmentation'
    )
    parser.add_argument('image_path', help='Path to MRI image (jpg/png)')
    parser.add_argument('--view', action='store_true',
                        help='Also segment & save the tumor region overlay')
    parser.add_argument('--out-dir', default='.',
                        help='Directory to write outputs to')
    args = parser.parse_args()

    # 1. Load image
    img = cv.imread(args.image_path, cv.IMREAD_COLOR)
    if img is None:
        print(f"ERROR: Cannot load image {args.image_path}", file=sys.stderr)
        sys.exit(1)

    # 2. Predict
    prob = predict_tumor(img)
    print(f"Tumor probability: {prob:.4f}")

    # write probability to a text file
    os.makedirs(args.out_dir, exist_ok=True)
    prob_file = os.path.join(args.out_dir, 'output_probability.txt')
    with open(prob_file, 'w') as f:
        f.write(f"{prob:.6f}\n")

    # 3. Optional segmentation
    if args.view:
        seg = DisplayTumor()
        seg.read(img)

        # Save initial processed mask (like GUI's noise-removed image)
        mask = seg.get_mask()
        mask_out = os.path.join(args.out_dir, 'processed_mask.png')
        cv.imwrite(mask_out, mask)
        print(f"Initial mask saved to {mask_out}")

        # Now segment and save final output with red boundary
        seg.segment()
        result = seg.get_result()
        out_img = os.path.join(args.out_dir, 'segmented.png')
        cv.imwrite(out_img, result)
        print(f"Segmentation saved to {out_img}")


if __name__ == '__main__':
    main()
