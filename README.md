# CBR-AND-RECOMMENDATION-SYSTEM


## Overview

This project utilizes the `UCI Wine Quality Dataset` to leverage case-based reasoning. 

Distinct wine profiles are created and clustered by similarity; in the same way, various user profiles with unique wine preferences are simulated. Based on the user's wine profile, the project aims to recommend new wines.


## Key Features

- **Wine Profile Creation**: Wine profiles are defined using five key sensory descriptors: **Vibrancy**, **Sweetness**, **Body**, **Nuance**, and **Tannicity**. Each descriptor is categorized into three levels: low, medium, and high, with corresponding attributes.
  
  1. **Vibrancy (acidity)**:
     - **Fixed Acidity**: Higher values suggest fresher wines.
     - **Volatile Acidity**: High levels may indicate a vinegary taste.
     - **Citric Acid**: More citric acid indicates livelier wines.
     - **pH**: Low pH indicates freshness; high pH suggests softness.
       - **Low**: Liveliness | **Medium**: Live | **High**: Brilliant
  
  2. **Sweetness (sugars)**:
     - **Residual Sugar**: High values imply sweetness; low values suggest dryness.
       - **Low**: Dry | **Medium**: Semi-Dry | **High**: Sweet
  
  3. **Body (alcohol & density)**:
     - **Alcohol**: Higher content indicates fuller-bodied wines.
     - **Density**: Denser wines suggest richness.
       - **Low**: Light | **Medium**: Medium | **High**: Full-Bodied
  
  4. **Nuance (chlorides)**:
     - **Chlorides**: Traces of salinity influence taste.
       - **Low**: Simple | **Medium**: Complex, Spicy | **High**: Intense
  
  5. **Tannicity (sulphates)**:
     - **Sulphates**: Higher levels increase dryness on the palate.
       - **Low**: Soft | **Medium**: Balanced, Structured | **High**: Robust

- **Clustering**: Use clustering algorithms to group similar wines to facilitate recommendations.

- **User Simulation**: Simulate various users with diverse wine preferences and tastes.

- **Recommendation Engine**: Implement a recommendation system that suggests new wines based on case-based reasoning, analyzing user profiles to identify wines with similar attributes.

## Project Structure

The project is organized into the following directories and files:

- **files/**: Contains CSV files with quality data for red and white wines.
- **modules/**: Contains modules with functions used throughout the project.
- **src/**: Contains Python scripts that implement the core functionality.
- **requirements.txt**: Lists the Python packages required to run the project.
- **Dockerfile**: Used to launch the project in a Docker container.

The project utilizes Docker for containerization, ensuring a consistent development and deployment environment.


## Installation and Run Steps

To get started with this project, please follow these steps:

### Prerequisites

1. **Install Docker**: Ensure Docker is installed on your machine. You can download and install it from the [Docker website](https://www.docker.com/products/docker-desktop).

### Configuration for Matplotlib

To use Matplotlib in a Docker container with GUI support, you'll need to configure X11 forwarding on your Windows machine. Follow these instructions:

1. **Install XLaunch**:
   - Download and install **XLaunch** from the [Xming website](https://sourceforge.net/projects/xming/).
   - Launch XLaunch and choose **"Multiple windows"** when prompted.
   - Set the display number to **0**.
   - Select **"Start No client"**.
   - Choose **"Native OpenGL"**.
   - Check **"No access control"** to allow connections.

2. **Get Your Windows IP Address**:
   - Open Command Prompt and run the following command to find your IP address:
     ```bash
     ipconfig
     ```
   - Note the IPv4 Address (e.g., `192.168.1.100`).

### Building the Docker Image

1. **Navigate to the Project Directory**:
   Open your terminal and navigate to the root directory of the project where the `Dockerfile` is located.

2. **Build the Docker Image**:
   Run the following command to build the Docker image:
   ```bash
   docker build -t wine_app .
   ```
2. **Run the Docker Image**:
    Replace `<ip_address>` with corresponding value:
    ```bash
    docker run --rm -it --env=DISPLAY=<ip_address>:0 -v="$(Get-Location):/app" wine_app
    ```
3. **Navigate to corresponding script and run the script**:
    ```bash
    cd src
    python wine_profiling.py
    ```


