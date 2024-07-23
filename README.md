
## **Our Architecture of HealthCare System**

![](Aspose.Words.793a7681-2d5d-4288-9865-a9563762bf48.001.jpeg)


We created 3 Virtual machines running ubuntu server. We set it up with disk encryption.

### Website VM:

On the website VM we were using apache2.4 for hosting the django site. It was configured to rely on kerberos hosted in a different virtual machine for authentication. It was set up to allow access to the site on port 8001.

We self signed a certificate for the website and set up apache to use that for enabling the TLS connection.

Django Script handled the database operations and the site’s role based access controls. By default the django process uses sqlite for database management. However to improve the security we modified that to MySQL and the database files are in a different VM.

The website can connect to kerberos and mySQL through different subnets therefore they are not accessible to the outside users interacting through the firewall. Thus the kerberos and website share subnet A and MySQL and website share subnet B which are private subnets only accessible to the network administrator. This design decision was taken considering if the attacker is able to gain access to one of the subnets they are not able to easily get information about other services running.

\*\***The admin account on the website can only be accessed on a different port which is not exposed to outside networks thus only administrator can locally sign in.**

### Firewall VM:

In this virtual machine we configured a basic firewall using the iptables framework.

We configured the firewall to allow incoming requests for the website (basically https requests on port 8001) and dropped all other requests.

### Kerberos VM:

We created a realm HEALTHERCARE.NET in this virtual machine and added principals corresponding to doctor, patient, labtech, accounts (whose credentials were provided)

The pop up dialog that is seen first when accessing the website is due to this authentication through kerberos.

## **Measures to Deceive Potential Attackers**
![](Aspose.Words.793a7681-2d5d-4288-9865-a9563762bf48.002.jpeg)
https://x.com/nerdynaman/status/1780937227167789188?s=46

An image of the main dashboard of one of the users was uploaded to twitter.com . The image uploaded was modified to show various false fields which are not there in the real architecture of our setup.

1) Field showing “super admin” referring to the fact that an admin account could have these features on the contrary there is no such form for admin in real architecture.
1) Top left shows “made with react” to make the attacker believe in a false tech stack while we don’t use react.
1) Multiple buttons on screen showing “authenticate with AD” indicating that AD is being used for authentication so that attackers might try to spend their bandwidth in discovering/performing AD specific attacks while we are not using AD.

**P.S. We were successfully able to make the other team believe in this false information, as their specified understanding of our architecture showed use of AD while there is none.**

## **Attacks We Tested against our Setup and protected**

1. Outdated package vulnerabilities: Use of old versions of software often leads to lots of vulnerabilities in the system. We took care to use the latest version of most softwares so that such vulnerabilities are not exploitable in our system
   1. The version of apache that we used publicly showed a vulnerability available but we specifically patched for that vulnerability.33
1. Input Validation: In web applications, input mediation is really important as we don’t want any malicious user to be able to run scripts or access the database through input fields in the website. Our django script automatically checks for these issues and the user is not able to run scripts from the website.
1. Validity of Role based access controls: We ensured that no category of user is able to escalate privileges and access data of other users which they are not allowed to. This is ensured by manually creating and setting access permissions in the django website configuration python files.
1. If a user modifies the form field values in burp suite interceptor to retrieve or upload the items which they don’t have access to, our django script ensures proper permission validation.
1. We have implemented TLS so the communication between stakeholders is secure and attacks like phishing would lead to a failed certificate check in TLS.

## **Role Based Access of Various Users**

We have tried to secure the patient data by role based access control as in a hospital, not everyone should have access to all the data as a lot of patients information is confidential. For instance a patient wants to get some test done and the doctor prescribes the test, then the lab technician will require to see prescription to verify the tests to be done. But the lab technician should not be able to see patients other diagnosis or prescription. Similarly, the accountant should only be able to see the payment details of the patient and not the diagnosis or prescription.

We have made an enterprise network for a hospital where we consider entities as Doctors, Patient, Lab technicians, Account Managers and Administrators.

Other than above mentioned entities, there are sessions which are very important as they contain information about the patient and their diagnosis. Sessions are created by Doctors and they contain information about the patient, doctor, lab technician, accountant, tests to be done, prescription and total payment due for the session.

name : name of the session

doctor : who all doctor are part of the session, doctor creating the session is necessarily part of the session.

patient : which patient is part of the session

notes : prescription of the session

totalPayment : total payment due for the session

test : list of tests to be done for the session

labTechnician : who all lab technicians are part of the session

accountant : which accountant is part of the session (randomly any one accountant is assigned to the session)

We have also made groups which are managed by django scripts. These groups are used to assign permissions to the users. We have made 4 groups:

`Doctor`, `Lab Technician`, `Account Manager`, `Patient`

Further various users are added to the required group by the administrator. If a user account is made but not assigned to any of these groups then users access to any data is denied.

We have followed the principle of least privilege and assigned only those permissions to the group which are required by the users in that group.

These all entities have can upload and retrieve data from the webportal but they all have to be shown different data and according to their access rights.

We will be explaining the role of each entity in the network and what all data they can access.

### **Administrator:**

1. They have access to add new users(Doc, Lab Tech, Account Manager, Patient) to the network.
1. They can also add test which can be prescribed by the doctors.
1. They dont have access to any other data including sessions and test results.

### **Doctors:**

1. They can view what all patients they are treating.
1. They can view all the sessions they have created and are associated with(other doctor could have added them to the session).
1. They can view Test results of the patients which they have prescribed.
1. They can create sessions and add patients to the session.
1. They can add other doctors to the session for co-consultation.
1. Doctors can not edit and view following data in a session:
1. totalPayment: In a hospital a doctor should not have any reason to see the payment details of the patient.
1. accountant: In a hospital a doctor should not have any reason to see the payment details of the patient.

### **Patients:**

1. They can view their own data.
1. They can view the sessions they are part of and all the data in that session.
1. They can not edit any data in the session.
1. They can view list of doctors who they are getting treatment from.

### **Lab Technicians:**

1. They can view the sessions they are part of.
1. In a session they can only view the name of tests to be done.
3. They can upload the test results for the tests they have done. Only the lab technician can upload the test results.

They can modify the test results uploaded by them if they have made a mistake although any and every change will be logged and they can never delete the test results. p.s. In a case any compromise is detected, the reports wont be deleted and any intent to change the report will be logged.

### **Account Managers:**

1. They can view the sessions they are part of.
1. They can view the total payment due for the session.
1. They can mark the payment as done for the session.
1. They can not edit or view any other data in the session.

# Installation
```
git clone {repo}
cd {repo}
pip install -r req.txt
cd mysite
python manage.py runserver
```
