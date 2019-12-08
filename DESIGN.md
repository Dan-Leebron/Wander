Our website, Wander, uses a Python program linked to several HTML pages and a SQL database.
The HTML pages are designed with CSS and they rely on information passed through by the Python
code. The SQL database compiles a list of users, their details and interests, and the people
they have indicated a match with. In order to run this website, all the user needs to do is
enter “flask run” in the specified folder.

When a user registers, they input information such as name, interests, and destination country.
After hitting submit on that form, the information inserted is stored in the SQL database under
the “accounts” table in the Wander database. By doing this, that information can be pulled any
time it is needed. There are certain requirements during registration such as a unique username
and a password with alphabetical and numeric characters. If these conditions are not met during
registration we return an error and invite the user to try registering again while meeting the
conditions. The one distinct field is interests, which has multiple activities which the user
can select some or all from. Because this requires a nuanced SQL query, we created a new table
for interests specifically, called “interests2”. This creates an interests ID for each user.

The next page prompts the user to upload an image. This stores an image in the server in which
the website is running. The naming of the image is an important detail: it stores it as an image
file named as the user’s ID number. This way, even users who have saved their files under the
same name will have unique file names for their image, such as 20.jpg. After the user uploads
their image, the database now has all the information needed for the user along with an image
that corresponds to that information. The  website then redirects the user to their profile
page, which pulls the user’s information from the SQL database. For this, the program uses
session, i.e. the person logged in will get their information as opposed to someone else’s
information.

Next is the matching page. We implement a SQL query that pulls users who have entered a desired
location identical to the logged in user’s desired location. This SQL query randomly selects a
user who you may click “Match” or “Keep Wandering” on. The “Match” button sets the value of
match to “yes”; in the matches table in the Wander database, a new record is inserted where
account id is equal to the logged in user’s ID and match id is equal to the user’s ID whose
“Match” button was selected. For example, if your ID is 10 and you swipe on a user whose ID is
13, the new record in the matches table will have values account id = 10 and match id = 13.
The “Keep Wandering” button sets the value of match to “no”, and nothing is inserted into
the matches table.

Each profile is selected randomly, but when the user selects match or keep wandering, a temporary
table called “swiped” stores the ids of these profiles - so as to not show them to the user again.
Once all profiles have been displayed for a given destination, this function means that there will
be no more to display; the page renders an apology and prompts the user to log out and back in to
see the other profiles again. On logging out, the code clears the swiped table to allow this. To
actually store the information of the selected user to match or not match with, we have a SQL
table called swipee that stores the information of the selected user. This gets changed with each
user that is displayed, and the information displayed on the page is pulled from swipee, which
stores values some of the columns from the accounts table for the swipee.

The next page is the Matches page, where each user gets a table of users they matched with and
their emails. This table requires that both users have indicated “Match” with one another. If
only one user has matched, neither user will see the other in their Matches page. The way we
implement this is through another SQL query, which searches for two records. In the aforementioned
example, ID 10 has indicated “match” with ID 13. If ID 13 did not do the same to ID 10, then
the match is not rendered. If, however, ID 13 matched with user 10, then a new record is generated
in the matches table in the database. This means there are two records: one where account id = 10,
match id = 13 and one where account id = 13 and match id = 10. If this is the case, then the logged
in user, say user 13, will see user 10 in their matches, and vice versa.