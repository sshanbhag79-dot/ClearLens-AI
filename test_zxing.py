try:
    import zxingcpp
    from PIL import Image
    print("✅ zxing-cpp imported successfully.")
except ImportError as e:
    print(f"FAILED: ImportError: {e}")
except Exception as e:
    print(f"FAILED: Error: {e}")
