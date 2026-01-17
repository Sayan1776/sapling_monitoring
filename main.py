import rasterio
import pandas as pd
import cv2
import numpy as np
from utils.vision_tools import detect_pits_op1, is_alive
from utils.spatial_tools import align_orthos

# File Paths
OP1_PATH = 'data/op1_ortho.tif'
OP3_PATH = 'data/op3_ortho.tif'

def run_poc():
    print("Step 1: Aligning Orthomosaics...")
    warp_mat = align_orthos(OP1_PATH, OP3_PATH)
    
    with rasterio.open(OP1_PATH) as op1_src, rasterio.open(OP3_PATH) as op3_src:
        op1_img = op1_src.read([1, 2, 3]).transpose(1, 2, 0)
        op3_img = op3_src.read([1, 2, 3]).transpose(1, 2, 0)
        
        # Warp OP3 to match OP1 exactly
        aligned_op3 = cv2.warpAffine(op3_img, warp_mat, (op1_img.shape[1], op1_img.shape[0]))
        
        print("Step 2: Detecting Pits from OP1...")
        pits = detect_pits_op1(op1_img)
        
        results = []
        
        if pits is not None:
            pits = np.round(pits[0, :]).astype("int")
            for (x, y, r) in pits:
                # Define a window around the pit (approx 60x60cm)
                patch = aligned_op3[y-30:y+30, x-30:x+30]
                
                if patch.size == 0: continue
                
                alive, score = is_alive(patch)
                
                # Get real-world coordinates for the failed saplings
                lon, lat = op1_src.xy(y, x)
                
                results.append({
                    "lat": lat,
                    "lon": lon,
                    "status": "Alive" if alive else "Dead",
                    "confidence": score
                })

        # Save to CSV
        df = pd.DataFrame(results)
        df.to_csv('outputs/survival_report.csv', index=False)
        
        # Calculate survival rate
        survival_rate = (df['status'] == 'Alive').mean() * 100
        print(f"Analysis Complete. Survival Rate: {survival_rate:.2f}%")
        print("Dead sapling coordinates saved to outputs/survival_report.csv")

if __name__ == "__main__":
    run_poc()