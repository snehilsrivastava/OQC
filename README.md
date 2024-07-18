# **QMS**

**QMS**, or Quality Management System is a web application designed to streamline the creation, update, and approval process for test records across various products and testing stages. The application is designed for centralized test record management and efficient approval workflow through collaboration between different teams.

## Framework and Services Used for Development

- **Django** is the project's main codebase
- **HTML, CSS and JavaScript** for the project's UI
- **AWS EC2** as a VM for the server
- **SQLite** as the database for the server

# **Documentation for Future Developers**

## Introduction and Architecture Overview

- QMS is a django project which maintains mainly the employee, test details, model details and test record  models. The web-app is hosted on the domain **http://protrackindkal.in/** through an AWS EC2 instance. All changes made to this repository can be pulled to the VM on AWS and it reflects on the website hosted.

- To work on the VM, the AWS EC2 interface offers a linux terminal to pull changes from the repository or stop the server.

## Setup and Configuration

- Clone the repository to your local machine using HTTPS or SSL or the github CLI.
- Ensure you have python installed. Version 3.12.3 was used and recommended. For more details visit **https://www.python.org/downloads/**.
- Ensure you have **pip** installed. For Python versions above 3.4, it is automatically installed. For more details visit **https://pypi.org/project/pip/**.
- You are recommended to install virtual environment and install the requirements on it so as to not disturb your other projects. You can choose to forgo this step if this is the only project you intend to run or are not worried about other package versions.

    -Install virtual environment using the command:

    ```python
    pip install virtualenv
    ```

    -Create a new virtual environment with the name (for eg. myenv):

    ```python
    virtualenv myenv
    ```

    -Now activate the virtual environment with the command:

    On Windows:

    ```python
    myenv\Scripts\activate
    ```

    On Mac or Linux:

    ```python
    source venv/bin/activate
    ```

    Note: You can deactivate the virtual environment using the command:

    ```python
    deactivate
    ```

- Install all the requirements of the project with the following command:

  ```python
  pip install -r oqc_model\req.txt
  ```

- You can run a local server after installing the necessary package using the following commands:

  On Windows:

  ```python
  python manage.py runserver
  ```

  On Linux or Mac:

  ```python
  python3 manage.py runserver
  ```
## Project Structure and Codebase

- The project is structured like a standard django project with apps **authapp**, **employee**, **product** and **oqc**. These apps are placed inside the oqc folder which holds other folders like **media**, which contains files relating to the images uploaded. The innermost **oqc** folder contains the main settings.py code which dictates all major operations of the django project.
- The database, which is stored as `db.sqlite3` contains all models responsible for the backend of the website.
- The **.gitignore** files are written to ignore all pycache and information like the .venv and the database.
- The static and the templates folder in **oqc_model/oqc/authapp/**  holds the html pages, their css stylings and js files to make them more interactive. Other main files of interest for development in this path will be **forms.py**, **models.py** and more importantly, **views.py** in the apps mentioned above.

## Customizing the Application

- To customize the application itself, clone the repository and perform changes and push them to a separate repository. This repository is intended to hold this base code and future versions of this same vision. Ensure you have the proper authorisations to copy the repository from the company and then proceed with the customization.


## Troubleshooting and Debugging
- In case of bugs and errors, the django app provides the source code line and an appropriate message. This is displayed both on the website itself and the command line visible for the VM set up on the EC2 instance in AWS.

- The debugging process for front-end errors mostly deal with the workaround to perform operations unsupported by django templates. Mathematical operations, loops and conditionals should be carefully dealt with. The back-end errors require logical reasoning and proper python syntax.

- When the repository is set-up to run on a local server, if you are using wsl(Windows subsystem for linux), leaving the wsl idle may cause a time difference between the windows and ubuntu and cause many errors. In such a scenario, it is recommended to shutdown wsl using the command: ```wsl --shutdown```, and restart it by typing the command: ```wsl```.

# **Administration Documentation**

Admin Page Features and Usage

The admin section of the code provides a user-friendly interface for managing the application's data and configurations. It is built using Django's built-in admin site, which allows authorized users to perform CRUD operations on the Employee models.

## Key Features

- User Authentication: The admin site supports user authentication, ensuring that only authorized users can access and modify the admin functionalities.
- Model Registration: The relevant models are registered with the admin site, allowing administrators to view, create, update, and delete records through the admin interface.
- Customization: The admin section can be customized to suit specific requirements by modifying the admin.py file.

## Usage

1. Accessing the Admin Interface: To access the admin section, navigate to the designated URL endpoint (i.e., '/admin') in a web browser and log in using valid credentials.
2. Navigating the Admin Interface: Once logged in, the admin interface provides a dashboard listing the registered models. Click on a model to view, create, update, or delete records.
3. Modifying Model Behavior: The behavior of models in the admin interface can be customized by modifying the respective ModelAdmin classes in the admin.py file.

## Security Considerations

- User Access Control: Ensure that only authorized users have access to the admin interface
- Limited Database Exposure: Avoid displaying sensitive information or personally identifiable data in the admin interface to minimize the risk of unauthorized access.

For more information on Django's admin site and its customization options, refer to the official Django documentation: https://docs.djangoproject.com/en/3.2/ref/contrib/admin/


## Content Management

- To maintain the security of data and ensure proper functioning of the platform, frequent checks and tests are recommended.
- Checking for dead links on the platform will ensure the functionality of cloud storage. Ensuring no files are named with special characters(other than underscore('_')) is an important precausionality.
- Maintenance of a user manual and updation of this documentation are further content management steps to take by future developers to facilitate a seamless onboaring for future work on this project.

## Analytics and Reporting

- Usage data of the EC2 instance, AWS RDS and the S3 cloud storage is readily available as generated on AWS. General trends can be extracted from this data along with the generated logs.

## Troubleshooting and Support

- The EC2 instance's VM holds logs of every access made to the website. The error message displayed in case of any bugs provides meaningful insight into troubleshooting. Restarting the server may fix minor bugs. Shutdown the server with ```Ctrl + c``` and rerun it with:
  ```python
  python3 manage.py runserver
  ```

- For further support, contact the developers:

  Snehil Srivastava, @snehilsr, snehil.s@inkdaltechno.onmicrosoft.com

  Akshay Verma, @unhappyTWO, akshay.v@indkaltechno.onmicrosoft.com