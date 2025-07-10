import torch

if torch.backends.mps.is_available():
    allocated = torch.mps.current_allocated_memory() / 1024**3  # Convert bytes to GB
    reserved = torch.mps.driver_allocated_memory() / 1024**3

    print(f"MPS Memory Allocated: {allocated:.2f} GB")
    print(f"MPS Memory Reserved: {reserved:.2f} GB")
else:
    print("MPS is not available.")