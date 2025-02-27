# Tweeter Auto Account Automation

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Setup and Configuration](#setup-and-configuration)
6. [Usage](#usage)
7. [Code Structure](#code-structure)
8. [Educational Purpose & Disclaimer](#educational-purpose--disclaimer)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)
12. [Acknowledgements](#acknowledgements)
12. [License](#license)    

---

## Introduction
This project is an educational automation tool designed to test and showcase the integration of Selenium WebDriver with the OpenAI API. The primary goal is to demonstrate how to automate browser interactions (including account creation, image generation, and tweeting) on social media platforms—in this case, Twitter (or X)—while using temporary email services and dynamic data generation libraries.

The project serves as a pretext to experiment with:
- **Selenium** for browser automation,
- **GuerrillaMail API** for temporary email generation and verification,
- **Faker** for generating realistic random user data,
- **OpenAI API** (DALL-E 3) for creating images dynamically.

Despite its experimental nature, the code is fully functional and can be adapted for various automation use cases.

---

## Features
- **Automated Account Creation**: Uses Selenium to navigate through the Twitter sign-up process.
- **Temporary Email Integration**: Leverages GuerrillaMail API to generate temporary email addresses and retrieve verification codes.
- **Dynamic Data Generation**: Utilizes Faker to generate random names and details for a more natural sign-up flow.
- **OpenAI API Integration**: Demonstrates image generation using the OpenAI API (DALL-E 3), integrating the generated images into the automated workflow.
- **Tweet Posting Automation**: Automates tweet posting, complete with randomized content to simulate human-like behavior.
- **Account Data Logging**: Stores created account credentials (email, password, username) into a file (`accounts.txt`) for future reference.
- **Resilient Automation Flow**: Incorporates error handling and reinitialization routines to manage pop-ups and dynamic changes on the target website.

---

## Prerequisites
Before running the scripts, ensure you have the following:

- **Python 3.x** installed on your machine.
- The following Python libraries (which you can install via pip):
  - `selenium`
  - `requests`
  - `Faker`
  - `openai`
- **Google Chrome** browser installed.
- **ChromeDriver** corresponding to your version of Chrome. Download from the [ChromeDriver official site](https://sites.google.com/chromium.org/driver/).

---

## Installation
1. **Clone or Download the Repository:**
    ```bash
    git clone https://github.com/your-username/tweeter-auto-acc.git
    ```
2. **Navigate to the Project Directory:**
    ```bash
    cd tweeter-auto-acc
    ```
3. **Install the Dependencies:**
    If a `requirements.txt` file is available, run:
    ```bash
    pip install -r requirements.txt
    ```
    Otherwise, install the dependencies manually:
    ```bash
    pip install selenium requests Faker openai
    ```

---

## Setup and Configuration
1. **ChromeDriver:**
   - Ensure `chromedriver` (or `chromedriver.exe` on Windows) is located in your project directory or in a directory included in your system's PATH.
   
2. **OpenAI API Key:**
   - Sign up for an API key at [OpenAI](https://openai.com/).
   - Set your API key as an environment variable:
     ```bash
     export OPENAI_API_KEY="your_openai_api_key"
     ```
     
3. **GuerrillaMail API:**
   - No additional configuration is required. The project directly calls the GuerrillaMail API endpoints to generate temporary emails and fetch verification messages.

---

## Usage
There are two main scripts in this project:

### autosubscribe.py
- **Purpose:** Automates account sign-up on Twitter/X, including generating a temporary email, filling out the registration form, verifying the account via a code fetched from GuerrillaMail, and uploading a dynamically generated profile picture.
- **How to Run:**
    ```bash
    python autosubscribe.py
    ```

### main.py
- **Purpose:** Builds upon the account creation process and continuously posts tweets with randomized content. It handles pop-up verifications and rotates accounts after a certain number of posts.
- **How to Run:**
    ```bash
    python main.py
    ```

---

## Code Structure
- **accounts.txt:**  
  Stores account credentials (email, password, username) generated during automation.

- **autosubscribe.py:**  
  Contains the logic for:
  - Generating temporary email addresses via GuerrillaMail.
  - Automating the Twitter sign-up flow using Selenium.
  - Fetching and submitting verification codes.
  - Generating random names and details using Faker.
  - Integrating the OpenAI API to generate profile images.

- **main.py:**  
  Extends the functionality to:
  - Automate tweet posting.
  - Handle potential pop-ups and errors during interactions.
  - Cycle through accounts by creating new ones after a defined number of posts.

- **README.md:**  
  This file – providing detailed information about the project, its educational purpose, setup, and usage instructions.

---

## Educational Purpose & Disclaimer
This project is **purely educational**. It was developed as a pretext to test and demonstrate the following:
- **Selenium WebDriver:** Automating browser actions and interacting with dynamic web pages.
- **OpenAI API:** Integrating cutting-edge AI services for generating media (images) on the fly.
- **API Integration & Automation:** Combining multiple services (GuerrillaMail, OpenAI, Twitter/X) into one cohesive automation pipeline.

**Disclaimer:**
- **Educational Use Only:** The code is intended solely for learning, testing, and experimentation.
- **Compliance:** Users are responsible for ensuring that any automation complies with the terms of service of any websites or platforms involved. Automating account creation or posting content may be against the policies of those platforms.
- **No Liability:** The project is provided "as-is" without any warranty. The developer is not responsible for any misuse of this code or any legal repercussions arising from its use.

---

## Troubleshooting
- **ChromeDriver Mismatch:**  
  Ensure that the version of ChromeDriver matches your installed version of Google Chrome.
  
- **Element Locators:**  
  Social media platforms often update their UI. If Selenium fails to find an element, inspect the current web page and update the XPaths or CSS selectors accordingly.
  
- **API Issues:**  
  - For GuerrillaMail, verify your internet connection and check that the API endpoints are accessible.
  - For OpenAI API, ensure your API key is valid and that you have sufficient quota.
  
- **Timeouts and Delays:**  
  You may need to adjust the `time.sleep()` intervals or Selenium's wait conditions if the website responds slower than expected.

---

## Contributing
Contributions and feedback are welcome! If you have suggestions, feature requests, or bug reports, please open an issue on the [GitHub repository](https://github.com/your-username/tweeter-auto-acc/issues).

---

## Acknowledgements
- **Selenium:** For providing a robust framework for browser automation.
- **OpenAI:** For the innovative API that powers AI-driven image generation.
- **GuerrillaMail:** For offering a simple and effective temporary email solution.
- **Faker:** For making random data generation straightforward.
- **Community Contributions:** Thanks to the open-source community for continuous support and ideas.

---

## License
Please just don't steal my code..
