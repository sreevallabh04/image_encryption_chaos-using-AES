import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import sobel
from scipy.stats import pearsonr

def shannon_entropy(image):
    """
    Calculate Shannon entropy of an image.
    
    Args:
        image: Input image (grayscale or color)
        
    Returns:
        Shannon entropy value
    """
    # Ensure image is flattened and in uint8 format
    image_array = np.asarray(image).astype(np.uint8).flatten()
    
    # Calculate histogram
    histogram, _ = np.histogram(image_array, bins=256, range=(0, 256))
    
    # Normalize histogram to get probabilities
    probabilities = histogram / np.sum(histogram)
    
    # Filter out zero probabilities to avoid log(0)
    probabilities = probabilities[probabilities > 0]
    
    # Calculate entropy
    entropy = -np.sum(probabilities * np.log2(probabilities))
    
    return entropy

def plot_histograms_and_images(original_img, decrypted_img, encrypted_bytes, original_filename="histograminput.jpg", encrypted_filename="histogramencrypted.png", comparison_filename="comparison.png"):
    """Generates and saves histograms, side-by-side images, difference image, and additional visualizations."""

    # --- Calculate Entropies ---
    original_entropy = shannon_entropy(original_img)
    # Ensure encrypted_bytes is treated as a flat array of bytes for entropy calculation
    encrypted_entropy = shannon_entropy(encrypted_bytes.astype(np.uint8))

    # --- Create Histograms ---
    fig_hist, axes_hist = plt.subplots(1, 2, figsize=(16, 5))

    # --- Original Image Histogram ---
    ax = axes_hist[0]
    if len(original_img.shape) == 2: # Grayscale
        hist = cv2.calcHist([original_img], [0], None, [256], [0, 256])
        ax.plot(hist, color='black')
        original_color_mode = "gray"
    else: # Color
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            hist = cv2.calcHist([original_img], [i], None, [256], [0, 256])
            ax.plot(hist, color=color)
        original_color_mode = "color"
    ax.set_title(f"Original Image Histogram\nEntropy: {original_entropy:.4f}")
    ax.set_xlabel("Pixel Value")
    ax.set_ylabel("Frequency")
    ax.set_xlim([0, 256])
    ax.grid()

    # --- Encrypted Data Histogram ---
    ax = axes_hist[1]
    # Always plot encrypted data histogram as grayscale byte values
    hist_enc = cv2.calcHist([encrypted_bytes.astype(np.uint8)], [0], None, [256], [0, 256])
    ax.plot(hist_enc, color='black')
    ax.set_title(f"Encrypted Data Histogram\nEntropy: {encrypted_entropy:.4f}")
    ax.set_xlabel("Byte Value")
    ax.set_ylabel("Frequency")
    ax.set_xlim([0, 256])
    ax.grid()

    fig_hist.suptitle("Histogram Analysis")
    fig_hist.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent title overlap
    fig_hist.savefig(original_filename.replace("input", "histograms")) # Save combined histogram plot
    plt.close(fig_hist)
    print(f"[✔] Histograms saved to {original_filename.replace('input', 'histograms')}")

    # --- Correlation Analysis ---
    if len(original_img.shape) > 2:  # Convert to grayscale if color
        original_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    else:
        original_gray = original_img
        
    # Create a visualization showing correlation between adjacent pixels
    correlation_analysis(original_gray, encrypted_bytes.astype(np.uint8).reshape(-1, 1), "correlation_analysis.png")
    
    # Generate bit-plane slicing visualization
    if len(original_img.shape) > 2:
        bit_plane_visualization(cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY), "bit_planes_original.png")
    else:
        bit_plane_visualization(original_img, "bit_planes_original.png")
    
    # Create sample of encrypted bytes as 2D for bit plane visualization
    encrypted_2d = encrypted_bytes.astype(np.uint8)[:10000].reshape(100, 100)
    bit_plane_visualization(encrypted_2d, "bit_planes_encrypted.png")
    
    # Generate edge detection comparison
    edge_detection_comparison(original_gray, encrypted_2d, "edge_detection_comparison.png")
    
    # Create local entropy maps
    generate_entropy_maps(original_gray, encrypted_2d, "entropy_maps.png")

    # --- Side-by-Side and Difference Image ---
    if decrypted_img is not None:
        # Ensure images have the same shape for difference calculation
        if original_img.shape != decrypted_img.shape:
            print(f"[!] Warning: Original ({original_img.shape}) and decrypted ({decrypted_img.shape}) image shapes differ. Resizing decrypted image for comparison.")
            # Resize decrypted to match original, handle color/gray mismatch
            target_shape = original_img.shape
            if len(target_shape) == 3 and len(decrypted_img.shape) == 2: # Original is color, decrypted is gray
                 decrypted_img = cv2.cvtColor(decrypted_img, cv2.COLOR_GRAY2BGR)
            elif len(target_shape) == 2 and len(decrypted_img.shape) == 3: # Original is gray, decrypted is color
                 decrypted_img = cv2.cvtColor(decrypted_img, cv2.COLOR_BGR2GRAY)

            decrypted_img = cv2.resize(decrypted_img, (target_shape[1], target_shape[0])) # (width, height)

        if original_img.shape == decrypted_img.shape:
            fig_comp, axes_comp = plt.subplots(1, 3, figsize=(18, 6))

            # Display Original Image
            ax = axes_comp[0]
            if original_color_mode == "gray":
                ax.imshow(original_img, cmap='gray')
            else:
                ax.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
            ax.set_title("Original Image")
            ax.axis('off')

            # Display Decrypted Image
            ax = axes_comp[1]
            if len(decrypted_img.shape) == 2: # Check decrypted image channels
                ax.imshow(decrypted_img, cmap='gray')
            else:
                ax.imshow(cv2.cvtColor(decrypted_img, cv2.COLOR_BGR2RGB))
            ax.set_title("Decrypted Image")
            ax.axis('off')

            # Display Difference Image
            difference = cv2.absdiff(original_img, decrypted_img)
            ax = axes_comp[2]
            # Check if difference image is all zeros (or very close)
            if np.sum(difference) < 1e-6:
                 # Create a black image of the same size if difference is negligible
                 diff_display = np.zeros_like(original_img)
                 diff_title = "Difference Image (No Difference)"
            else:
                 # If there are differences, display them. Grayscale difference is often clearer.
                 if len(difference.shape) == 3:
                     diff_display = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
                 else:
                     diff_display = difference
                 diff_title = "Difference Image"

            im = ax.imshow(diff_display, cmap='gray', vmin=0, vmax=255)
            ax.set_title(diff_title)
            ax.axis('off')
            # Add a colorbar for the difference image for clarity
            # fig_comp.colorbar(im, ax=ax, fraction=0.046, pad=0.04) # Optional: adds a scale bar

            fig_comp.suptitle("Image Comparison")
            fig_comp.tight_layout(rect=[0, 0.03, 1, 0.95])
            fig_comp.savefig(comparison_filename)
            plt.close(fig_comp)
            print(f"[✔] Image comparison saved to {comparison_filename}")
        else:
             print("[!] Error: Could not make original and decrypted images compatible for comparison.")
    else:
        print("[i] Decrypted image not found or failed to load. Skipping image comparison.")
def correlation_analysis(original_img, encrypted_img, filename):
    """
    Generate correlation scatter plots for original and encrypted images
    
    Args:
        original_img: Original grayscale image
        encrypted_img: Encrypted data (reshaped for visualization)
        filename: Output filename for the visualization
    """
    # Setup figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    directions = ["Horizontal", "Vertical", "Diagonal"]
    
    # Prepare data - ensure both are 2D grayscale
    if len(original_img.shape) > 2:
        original = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    else:
        original = original_img
    
    # If encrypted is 1D, reshape to 2D for correlation
    if encrypted_img.ndim == 1:
        # Make it as close to square as possible
        size = int(np.sqrt(encrypted_img.size))
        encrypted = encrypted_img[:size*size].reshape(size, size)
    elif encrypted_img.ndim == 2 and encrypted_img.shape[1] == 1:
        # 2D but column vector
        size = int(np.sqrt(encrypted_img.size))
        encrypted = encrypted_img.flatten()[:size*size].reshape(size, size)
    else:
        encrypted = encrypted_img
    
    # Sample pixels to keep scatter plot clean (max 5000 points)
    max_points = 5000
    
    # For original image
    h, w = original.shape
    if h*w > max_points:
        # Random sampling
        indices = np.random.choice(h*w, max_points, replace=False)
        original_flat = original.flatten()[indices]
    else:
        original_flat = original.flatten()
    
    # For encrypted image
    h, w = encrypted.shape
    if h*w > max_points:
        # Random sampling
        indices = np.random.choice(h*w, max_points, replace=False)
        encrypted_flat = encrypted.flatten()[indices]
    else:
        encrypted_flat = encrypted.flatten()
    
    correlations = []
    
    # Analyze for each direction
    for i, direction in enumerate(directions):
        # Original image
        ax = axes[0, i]
        if direction == "Horizontal":
            # Get adjacent horizontal pixels
            x = original_flat[:-1]
            y = original_flat[1:]
            corr, _ = pearsonr(x, y) if len(x) > 1 else (0, 0)
        elif direction == "Vertical":
            # Get adjacent vertical pixels (need to handle 2D structure)
            x = original[:-1, :].flatten()
            y = original[1:, :].flatten()
            if len(x) > max_points:
                indices = np.random.choice(len(x), max_points, replace=False)
                x, y = x[indices], y[indices]
            corr, _ = pearsonr(x, y) if len(x) > 1 else (0, 0)
        else:  # Diagonal
            # Get adjacent diagonal pixels
            x = original[:-1, :-1].flatten()
            y = original[1:, 1:].flatten()
            if len(x) > max_points:
                indices = np.random.choice(len(x), max_points, replace=False)
                x, y = x[indices], y[indices]
            corr, _ = pearsonr(x, y) if len(x) > 1 else (0, 0)
        
        # Plot and add title with correlation coefficient
        ax.scatter(x[:max_points], y[:max_points], s=1, alpha=0.5)
        ax.set_title(f"Original - {direction} (r={corr:.4f})")
        ax.set_xlabel("Pixel Value")
        ax.set_ylabel("Adjacent Pixel Value")
        correlations.append(corr)
        
        # Encrypted image
        ax = axes[1, i]
        if direction == "Horizontal":
            # Get adjacent horizontal pixels
            x = encrypted_flat[:-1]
            y = encrypted_flat[1:]
            corr, _ = pearsonr(x, y) if len(x) > 1 else (0, 0)
        elif direction == "Vertical":
            # Get adjacent vertical pixels
            x = encrypted[:-1, :].flatten()
            y = encrypted[1:, :].flatten()
            if len(x) > max_points:
                indices = np.random.choice(len(x), max_points, replace=False)
                x, y = x[indices], y[indices]
            corr, _ = pearsonr(x, y) if len(x) > 1 else (0, 0)
        else:  # Diagonal
            # Get adjacent diagonal pixels
            x = encrypted[:-1, :-1].flatten()
            y = encrypted[1:, 1:].flatten()
            if len(x) > max_points:
                indices = np.random.choice(len(x), max_points, replace=False)
                x, y = x[indices], y[indices]
            corr, _ = pearsonr(x, y) if len(x) > 1 else (0, 0)
        
        # Plot and add title with correlation coefficient
        ax.scatter(x[:max_points], y[:max_points], s=1, alpha=0.5)
        ax.set_title(f"Encrypted - {direction} (r={corr:.4f})")
        ax.set_xlabel("Byte Value")
        ax.set_ylabel("Adjacent Byte Value")
        correlations.append(corr)
    
    fig.suptitle("Pixel Correlation Analysis\nGood encryption should show no correlation in encrypted data", fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(filename)
    plt.close(fig)
    print(f"[✔] Correlation analysis saved to {filename}")
    
    return correlations

def bit_plane_visualization(image, filename):
    """
    Create bit-plane slicing visualization to show how encryption affects each bit level
    
    Args:
        image: Grayscale image
        filename: Output filename
    """
    # Ensure image is grayscale
    if len(image.shape) > 2:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        img = image
    
    # Create figure
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    
    # Extract and visualize each bit plane
    for i in range(8):
        # Extract bit plane
        bit_plane = (img >> i) & 1
        
        # Display
        axes[i].imshow(bit_plane * 255, cmap='gray')
        axes[i].set_title(f"Bit Plane {i}")
        axes[i].axis('off')
    
    fig.suptitle("Bit Plane Analysis\nEach plane shows the distribution of a single bit", fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(filename)
    plt.close(fig)
    print(f"[✔] Bit plane visualization saved to {filename}")

def edge_detection_comparison(original_img, encrypted_img, filename):
    """
    Compare edge detection results between original and encrypted images
    Edge detection should reveal structure in original but not in encrypted
    
    Args:
        original_img: Original grayscale image
        encrypted_img: Encrypted data (reshaped for visualization)
        filename: Output filename
    """
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    
    # Original image
    axes[0, 0].imshow(original_img, cmap='gray')
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis('off')
    
    # Edge detected original
    edges_original = sobel(original_img)
    axes[0, 1].imshow(edges_original, cmap='magma')
    axes[0, 1].set_title("Original Image Edges")
    axes[0, 1].axis('off')
    
    # Encrypted image (or sample)
    axes[1, 0].imshow(encrypted_img, cmap='gray')
    axes[1, 0].set_title("Encrypted Data (Sample)")
    axes[1, 0].axis('off')
    
    # Edge detected encrypted
    edges_encrypted = sobel(encrypted_img)
    axes[1, 1].imshow(edges_encrypted, cmap='magma')
    axes[1, 1].set_title("Encrypted Data Edges")
    axes[1, 1].axis('off')
    
    fig.suptitle("Edge Detection Comparison\nEncrypted data should show no coherent edges", fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(filename)
    plt.close(fig)
    print(f"[✔] Edge detection comparison saved to {filename}")

def generate_entropy_maps(original_img, encrypted_img, filename):
    """
    Generate local entropy maps for original and encrypted images
    
    Args:
        original_img: Original grayscale image
        encrypted_img: Encrypted data (reshaped for visualization)
        filename: Output filename
    """
    def local_entropy(img, win_size=9):
        """Calculate entropy in local windows"""
        from skimage.filters.rank import entropy
        from skimage.morphology import disk
        
        # Ensure uint8 type for entropy calculation
        img_uint8 = img.astype(np.uint8)
        return entropy(img_uint8, disk(win_size//2))
    
    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Calculate and display entropy maps
    entropy_original = local_entropy(original_img)
    im1 = axes[0].imshow(entropy_original, cmap='viridis')
    axes[0].set_title(f"Original Image Local Entropy\nMean: {np.mean(entropy_original):.4f}")
    axes[0].axis('off')
    fig.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)
    
    # Try to resize encrypted to similar size for better visualization
    if encrypted_img.size != original_img.size:
        try:
            # This is only for visualization - might not be perfect size match
            sample_size = min(encrypted_img.size, 10000)  # Limit size
            enc_sample = encrypted_img.flatten()[:sample_size]
            size = int(np.sqrt(sample_size))
            enc_vis = enc_sample.reshape(size, size)
        except:
            enc_vis = encrypted_img  # Use as is
    else:
        enc_vis = encrypted_img
    
    entropy_encrypted = local_entropy(enc_vis)
    im2 = axes[1].imshow(entropy_encrypted, cmap='viridis')
    axes[1].set_title(f"Encrypted Data Local Entropy\nMean: {np.mean(entropy_encrypted):.4f}")
    axes[1].axis('off')
    fig.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)
    
    fig.suptitle("Local Shannon Entropy Maps\nEncrypted data should have high, uniform entropy", fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(filename)
    plt.close(fig)
    print(f"[✔] Entropy maps saved to {filename}")

def save_histogram(image, title, filename, color_mode="gray"): # Keep original function if needed elsewhere, but new function is preferred
    """Compute and save the histogram of an image."""
    plt.figure(figsize=(8, 5))
    if color_mode == "gray":
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        plt.plot(hist, color='black')
    else:
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            plt.plot(hist, color=color)
    
    plt.title(title)
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.xlim([0, 256])
    plt.grid()
    
    # Save histogram as an image instead of displaying it
# --- Main Execution ---
if __name__ == "__main__":
    # Load Original Image
    original_image = cv2.imread("images/input.jpg", cv2.IMREAD_UNCHANGED)
    if original_image is None:
        print("[!] Error: Original image 'images/input.jpg' not found.")
        exit()
    # Load Decrypted Image
    decrypted_image = cv2.imread("images/decrypted.png", cv2.IMREAD_UNCHANGED)
    if decrypted_image is None:
        print("[i] Info: Decrypted image 'images/decrypted.png' not found. Comparison will be limited.")
        # Proceed without decrypted image if necessary, plot_histograms_and_images handles None

    # Load Encrypted Image Data
    try:
        encrypted_data = np.load("images/encrypted.npy", allow_pickle=True)
    except FileNotFoundError:
        print("[!] Error: Encrypted data 'images/encrypted.npy' not found.")
        exit()

    # Convert encrypted data to a flat byte array for histogram/entropy
    if encrypted_data.ndim == 0: # Scalar object (e.g., string)
        encrypted_item = encrypted_data.item()
        if isinstance(encrypted_item, (str, bytes, np.bytes_)):
             encrypted_bytes = np.array([ord(c) for c in str(encrypted_item)], dtype=np.uint8)
        else: # Assume it's a single number, less likely for encryption result
             encrypted_bytes = np.array([encrypted_item]).astype(np.uint8)
    elif isinstance(encrypted_data.item(0) if encrypted_data.size > 0 else None, (str, bytes, np.bytes_)): # Array of strings/bytes
        # Flatten the list of strings/bytes then get ASCII values
        flat_list = encrypted_data.tolist()
        combined_str = ''.join(map(str, flat_list)) # Ensure elements are strings
        encrypted_bytes = np.array([ord(c) for c in combined_str], dtype=np.uint8)
    else: # Assume numerical array
        encrypted_bytes = encrypted_data.flatten().astype(np.uint8)

    # Ensure encrypted_bytes is at least 1D
    if encrypted_bytes.ndim == 0:
        encrypted_bytes = encrypted_bytes.reshape(1) # Make it 1D if it became scalar

    # Generate and save visualizations
    plot_histograms_and_images(
        original_image,
        decrypted_image,
        encrypted_bytes,
        original_filename="histograms_analysis.png", # Combined histogram file
        comparison_filename="image_comparison.png"   # Side-by-side and diff file
    )

    print("\n[✔] Visual analysis completed.")
    print(f"  - Histograms & Entropies saved to 'histograms_analysis.png'")
    if decrypted_image is not None:
        print(f"  - Image Comparison (Original, Decrypted, Difference) saved to 'image_comparison.png'")
    print(f"  - Correlation Analysis saved to 'correlation_analysis.png'")
    print(f"  - Bit Plane Visualizations saved to 'bit_planes_original.png' and 'bit_planes_encrypted.png'")
    print(f"  - Edge Detection Comparison saved to 'edge_detection_comparison.png'")
    print(f"  - Local Entropy Maps saved to 'entropy_maps.png'")
