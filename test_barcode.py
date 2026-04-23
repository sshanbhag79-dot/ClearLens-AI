try:
    from pyzbar.pyzbar import decode
    from PIL import Image
    print("✅ pyzbar imported successfully.")
except ImportError as e:
    print(f"❌ ImportError: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
