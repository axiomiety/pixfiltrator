import argparse
import extract_data
import extract_roi
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--captureDir',
        action='store',
        default='/mnt/c/TEMP',
        type=str,
        help='path to the directory containing the captures',
    )
    parser.add_argument(
        '--outDir',
        action='store',
        default='/mnt/c/TEMP/out',
        help='out path for all the captures',
    )
    parser.add_argument(
        '--coords',
        action='store',
        default='coords.json',
        help='path of the file containing the position of the region of interest',
    )
    args = parser.parse_args()

    rois = []
    for fname in (f for f in os.listdir(path=args.captureDir) if 'capture_' in f):
        basename, ext = fname.rsplit('.', 1)
        out_name = f'{basename}_roi.{ext}'
        out_full_path = os.path.join(args.outDir, out_name)
        extract_roi.extract(
            src=os.path.join(args.captureDir, fname),
            dest=out_full_path,
            coords=args.coords,
        )
        rois.append(os.path.join(args.outDir, out_name))

    for roi in rois:
        # bp = os.path.dirname(roi)
        extract_data.extract(
            image=roi, sqWidth=5, regionOnGuest='1200x800', outFile=None, verify=True
        )
