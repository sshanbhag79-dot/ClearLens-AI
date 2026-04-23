try:
    import cv2
    print(f"cv2 imported successfully. Version: {cv2.__version__}")
    if hasattr(cv2, 'barcode'):
        print("cv2.barcode is available.")
    else:
        print("WARNING: cv2.barcode is NOT available (older version?).")
except ImportError as e:
    print(f"FAILED: ImportError: {e}")
except Exception as e:
    print(f"FAILED: Error: {e}")
