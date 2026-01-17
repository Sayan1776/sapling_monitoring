import rasterio
import cv2
import numpy as np

def get_pixel_coords(tif_path, lon, lat):
    with rasterio.open(tif_path) as src:
        row, col = src.index(lon, lat)
        return row, col

def align_orthos(ref_path, target_path):
    """Aligns OP3 to OP1 using ECC to fix the 1m GPS drift."""
    with rasterio.open(ref_path) as ref, rasterio.open(target_path) as tar:
        ref_img = ref.read([1, 2, 3]).transpose(1, 2, 0)
        tar_img = tar.read([1, 2, 3]).transpose(1, 2, 0)

    # Convert to grayscale for alignment
    ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_RGB2GRAY)
    tar_gray = cv2.cvtColor(tar_img, cv2.COLOR_RGB2GRAY)

    # Define motion model
    warp_mode = cv2.MOTION_EUCLIDEAN
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    
    # Find transformation
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 1e-8)
    _, warp_matrix = cv2.findTransformECC(ref_gray, tar_gray, warp_matrix, warp_mode, criteria)
    
    return warp_matrix