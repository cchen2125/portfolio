Documentation for Down Time

URL to video: https://youtu.be/MLkcVaJaKtQ

Down Time is a web application made using flask. As long as all the relevant packages imported at the beginning of app.py are installed, the application should run by typing "flask run" in the terminal when in the implementation directory. I implemented my project using VS Code on my laptop after downloading SQL, python, and all the other things that were mentioned in the "Developing Your Project Locally with VS Code" seminar. The features of Down Time can be broken down into 7 items: the home page, registering and logging in, activities, goals, analytics, recommendations, and account settings.

The home page provides overall instructions for how to use Down Time. The title says "Welcome to Down Time!" and should include the user's name if they are logged in.

If not logged in, the navigation bar includes links to the login and register pages, where users can log in and register respectively. The log in page requires input of a user name and password in the system and the register page asks the user to provide their name, username, password, confirm password, and color scheme.

Once logged in, the navigation bar includes links to the user's activities, goals, analytics, recommendations, and account settings. On the activities page, the user can input data for sleep (in hours), water (in liters), exercise (in minutes), and "down time" (or relxation time, in minutes). Under each category, there is a graph showing the amounts over the last week and a form to input new data. To input a new data point, the user just needs to select a date and enter an amount. To edit a data point, the user can enter the date they want to edit with the new amount. To delete a data point, the user can enter the date they want to delete with no amount entered.

The goals page allowed users to add new goals, which will automatically be added to the incomplete column. Once goals are completed, they will be moved to the completed column.

The analytics page is broken down into a goals section and an activities section. The goals section should display the total goals the user has ever logged, the total goals the user has ever completed, and a pie chart breaking down the comparative fractions of complete and incomplete goals that the user currently has. If there are no current goals, the pie chart just shows 100% no goals. The activities section shows the overall averages for each activity (sleep, water, exercise, down time) and a table showing the history of all entries.

The recommendations page has 3 buttons representing 3 categories of self-care activities. Clicking one of the button will give a random suggesting from that category. There are approximiately 5-6 hard coded possibilities for each one.

On the account settings page users can change their username (current username is displayed), change their password (which requires entering their current password), and change their color scheme (current color scheme is displayed).
