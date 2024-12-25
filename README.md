
# Traffic Monitoring and BOLA Testing with MongoDB and Mitmproxy

## Overview

This project provides a framework to intercept and monitor HTTP/HTTPS traffic using **Mitmproxy** and store the data in a **MongoDB** database. Additionally, it includes functionality to perform **Broken Object Level Authorization (BOLA)** testing based on YAML configurations.

---

## Features

- **Intercept HTTP and HTTPS traffic:** Capture all incoming and outgoing traffic for analysis.
- **Store traffic data in MongoDB:** Save key information, including request/response headers and bodies, for future reference.
- **Run BOLA tests:** Execute tests based on configurable rules to detect potential BOLA vulnerabilities.
- **Analyze captured data:** Easily query and analyze the stored traffic data to identify patterns or vulnerabilities.

---

## Prerequisites

1. **Python 3.11+** installed on your system.
2. **MongoDB** installed and running locally or accessible through a cloud service like MongoDB Atlas.
3. **Mitmproxy** installed for traffic interception.

---

## Installation and Setup

### Step 1: Install Python Packages

Install the required Python packages using `pip`:
```bash
pip install mitmproxy pymongo pyyaml
```

### Step 2: Install Mitmproxy

You need to install **Mitmproxy**, a powerful tool for intercepting and modifying HTTP/HTTPS traffic.

To install Mitmproxy, run the following command:
```bash
brew install mitmproxy
```
For Windows users, download the installer from the [Mitmproxy website](https://mitmproxy.org/) and follow the installation instructions.

---

## Configuration

### MongoDB Configuration

Ensure that MongoDB is set up and running. You can either run MongoDB locally or use a cloud service like [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

If you're running MongoDB locally, it will be accessible at `mongodb://localhost:27017` by default.

### Mitmproxy Configuration

Mitmproxy needs to be configured to capture traffic. You will need to set up your system or browser to trust the **Mitmproxy** certificate. This allows **Mitmproxy** to intercept HTTPS traffic.

To generate the SSL certificate:
1. Run the following command to start Mitmproxy:
   ```bash
   mitmproxy
   ```
2. Navigate to `http://mitm.it` in your browser and install the certificate.

---

## Usage

### Step 1: Start the Mitmproxy

Start the Mitmproxy proxy server using the following command:
```bash
mitmproxy --mode http --listen-port 8080
```

This will start **Mitmproxy** on port `8080` and capture all HTTP/HTTPS traffic passing through it.

### Step 2: Run the Traffic Monitoring and BOLA Testing Script

Run the Python script to start intercepting traffic and perform BOLA testing. The script will listen for intercepted traffic and save the data to MongoDB. You can also provide YAML configuration files to define the rules for BOLA testing.

```bash
python traffic_monitoring.py
```

### Step 3: Monitor the Traffic in MongoDB

Captured HTTP/HTTPS traffic will be stored in your MongoDB database. You can query the data from the `traffic_data` collection in MongoDB to analyze the captured traffic. Use MongoDB commands or MongoDB clients like [MongoDB Compass](https://www.mongodb.com/products/compass) for this.

### Step 4: Perform BOLA Testing

BOLA testing is based on YAML configuration files. Each YAML file defines rules for testing object-level authorization vulnerabilities. These rules will be applied to the captured traffic to detect potential vulnerabilities.

To run BOLA tests, use the following command:
```bash
python bola_testing.py --config config.yaml
```

Make sure to replace `config.yaml` with your actual YAML configuration file.

---

## File Structure

```plaintext
/
|-- traffic_monitoring.py        # Main script for traffic monitoring and BOLA testing
|-- bola_testing.py              # Script for BOLA testing
|-- config.yaml                 # YAML configuration for BOLA testing
|-- requirements.txt            # List of Python dependencies
|-- README.md                   # Project documentation
```

---

## Example YAML Configuration for BOLA Testing

Here's an example of how a YAML configuration file for BOLA testing (`config.yaml`) could look:

```yaml
tests:
  - name: "Test User A Access to User B's Object"
    description: "Ensure that User A cannot access User B's data"
    url: "/api/user/{user_id}/data"
    method: "GET"
    rules:
      - parameter: "user_id"
        condition: "not_equal"
        value: "{user_a_id}"
        message: "User A should not access User B's data"
  - name: "Test Admin Access to All Objects"
    description: "Ensure that Admin can access all user data"
    url: "/api/user/{user_id}/data"
    method: "GET"
    rules:
      - parameter: "user_id"
        condition: "equal"
        value: "{admin_id}"
        message: "Admin should access all user data"
```

---

## Troubleshooting

- **Mitmproxy SSL Issues:** If you encounter SSL certificate errors while intercepting HTTPS traffic, ensure that you have installed Mitmproxy's SSL certificate in your browser or device.
- **MongoDB Connection Issues:** Make sure MongoDB is running and accessible. If you're using a cloud instance, verify that your MongoDB Atlas cluster is accessible and the correct connection string is used.
- **BOLA Tests Not Running:** Verify that your YAML configuration is correctly formatted. You can test individual rules with simpler cases to isolate issues.

---

## Contributing

Feel free to fork this repository, submit issues, and create pull requests for enhancements or bug fixes. Contributions are always welcome!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Mitmproxy** - For traffic interception and manipulation.
- **MongoDB** - For the database storage.
- **PyYAML** - For parsing YAML files used in BOLA testing.
