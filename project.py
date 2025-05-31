import pydicom
import matplotlib.pyplot as plt

ds = pydicom.dcmread("case1_008.dcm")
plt.imshow(ds.pixel_array, cmap="gray")
plt.title("DICOM Image")
plt.axis("off")
plt.show()

print("Patient Name:", ds.PatientName)
print("Patient ID:", ds.PatientID)
print("Study Date:", ds.StudyDate)
print("Modality:", ds.Modality)
print("Slice Thickness:", ds.SliceThickness)
print("Pixel Spacing:", ds.PixelSpacing)


import cv2
adjusted = cv2.convertScaleAbs(ds.pixel_array, alpha=1.2, beta=50)  
plt.imshow(adjusted, cmap="gray")
plt.title("Adjusted Image")
plt.show()


blurred = cv2.GaussianBlur(ds.pixel_array, (5, 5), 0)
edges = cv2.Canny(ds.pixel_array, 100, 200)


zoomed = ds.pixel_array[100:300, 100:300]
plt.imshow(zoomed, cmap="gray")


import glob
slices = [pydicom.dcmread(f) for f in glob.glob("*.dcm")]
slices.sort(key=lambda x: int(x.InstanceNumber))
