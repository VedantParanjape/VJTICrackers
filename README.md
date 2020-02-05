# HealthSync

**Why do we need *HealthSync*?**
In the health sector, one of the biggest roadblocks to effective solutions is the unavailability of past diagnosis and their respective remedies. For the most part, the health industry in India still uses conventional methods like paper files that have to be brought to the next visit voluntarily. This makes the margin of error huge and often this is the reason for the failure of the health industry. A few hospital chains do have sophisticated computerised systems but they are internalised which stops the widespread use of such systems.
In cases such as these, a system that integrates all parties seamlessly is the need of the hour.

**What does *HealthSync* do?**
The HealthSync website has all these primary goals:
- To centralise all the records of the patient in one place
- To ensure authenticity of the data input by allowing only the doctor to update the patient's medical records.
- To protect privacy of user by introducing an OTP that allows doctor to make edits.
- Aids the doctor to make diagnosis based on the PM 2.5 data which affects health.
- Minimal and aesthetic design to make it user-friendly for everybody.

Features like these and more help the doctor and patient to exchange data with ease so that time is spent on what matters the most, the remedy.

* The home page:
![Image](http://url/a.png)

* The login/signup page:
![Image](http://url/a.png)

* The profile page:
![Image](http://url/a.png)

**Challenges we ran into**
The main challenge was to find a way to handle two different categories of users: 
- doctors and patients in the backend database.   
- This was solved by making a custom login interface that handled role-based authentication.
- The other challenge was to deploy ML in the website to give accurate results. 
- This was solved by using a UK government database relating deaths and the PM 2.5 pollution in different locations and applying - linear regression to it using the scikit-learn library in Python along with visualisation tools like Matplotlib.
- The timeline UI to show medical history was a challenge in on the front-end side especially as it has to be dynamically updated according to the amount of data added previously.
- This was solved by using a custom CSS package and tweaking it to suit our purposes.

**Technologies we used**
- Flask
- Materialise.css
- SQL
- Scikit-learn
- Matplotlib
- HTTP server
- JSON
- BCrypt for password hashing

**Contributors**
* [Bhavya Sheth](https://github.com/BhavyaSheth22)
* [Akshat Shah](https://github.com/akshatshah21)
* [Saharsh Jain](https://github.com/saharshleo)
* [Vedant Paranjape](https://github.com/VedantParanjape)
