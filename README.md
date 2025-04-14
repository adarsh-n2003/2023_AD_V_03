# **JalRakshak - Water-Related Issue Detection System**

**JalRakshak** is a machine learning-based desktop application that identifies whether an uploaded image is related to a water-related issue. It allows users to submit such images along with descriptions and locations, which are then reviewed by admins. The system supports real-time classification and issue tracking through a GUI built with `tkinter`.

---

## **Dataset**

The dataset used in this project was manually created from a variety of sources, as no standard dataset for detecting water-related issues was available.

- Images were collected from the internet, open repositories, and personal captures.
- The dataset was divided into two classes:
    - **Water** – Images showing water-related issues (floods, leakage, waterlogging, etc.).
    - **Non-Water** – Images without visible water-related problems.

The dataset was then used to train a deep learning classification model.

---

## **Project Structure**

This project consists of two main components:

1. **Model Training**
    
    The model was trained using image classification techniques. A `.ipynb` file named `Water_Treatment_ML_model.ipynb` is included for training and saving the model as `water_detection_model.h5`.
    
2. **Graphical User Interface**
    
    A full-featured GUI application using `tkinter` that supports:
    
    - User/Admin registration and login
    - Image upload and automatic classification
    - Problem reporting with location and image
    - Admin dashboard to view and manage submitted issues

---

## **Files and Folders**

- `Water_Treatment_ML_model.ipynb` – Notebook to train and export the image classification model.
- `water_detection_model.h5` – Trained Keras model used by the GUI for inference.
- `water_detection_app.py` – GUI app to upload images, detect water issues, and manage submissions.
- `user_credentials.json` – Automatically created file to store user login info.
- `admin_review.json` – Stores submitted problems for admin review.
- `uploads/` – Folder where uploaded images are saved for tracking.

---

## **Requirements**

Install the required Python packages before running the project:

```bash
pip install numpy keras tensorflow opencv-python pillow
```

---

## **How to Use**

1. **Model Training (optional)**
    
    If you want to retrain or improve the model, run `Water_Treatment_ML_model.ipynb`.
    
2. **Run the Application**
    
    Launch the app using:
    
    ```bash
    python water_detection_app.py
    ```
    
3. **User Flow**
    - Register or log in as a user or admin.
    - Users can upload images with descriptions.
    - The system will classify the image.
    - If it shows a water issue, the problem is submitted to the admin with a unique ticket number.
4. **Admin Flow**
    - Log in as an admin to view and manage all user submissions.
    - View ticket details including image path, location, and status.

---

## **Contributors**

- [Adarsh Nashine](https://github.com/adarsh-n2003)
- [Anuj Tirole](https://github.com/anujtirole)
- [Prabal Singh](https://github.com/Prabalsing)
- [Surendra Singh Koranga](https://github.com/Surendrasingh6289)

---

## **License**

This project is licensed under the MIT License.

Feel free to use, modify, and distribute it for educational or commercial purposes.
