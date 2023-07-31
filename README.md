# Hype - Experience college like never before!

Hype is an exhilarating web application designed to ignite the college experience. It serves as the ultimate hub for college clubs and committees, delivering an adrenaline-fueled platform that keeps students in the loop with the latest updates, upcoming events, and epic parties. Get ready to ride the wave of excitement as Hype takes you on a wild adventure, where the energy is contagious, the fun is unstoppable, and the memories are legendary.

## Getting Started


1. Clone the repository:
```
 git clone https://github.com/Soumya-Vaidya/Hype.git
```

2. Navigate into the project directory
3. Install the required dependencies (Flask)

4. To run the application, run the following command:
```
python app.py
```

This will start the Flask development server. You can access the application by navigating to http://localhost:8000/ in your web browser.

### OR Install Using Docker

1. 
```
docker build -t hype https://github.com/Soumya-Vaidya/Hype.git
```

2.
```
docker run -p 8000:8000 hype
```



## Features

1. Live timeline displaying upcoming events with essential details.
2. Students can access information about past events.
3. Clubs and committees can add, delete, and edit event details.
4. Creation of subevents or inclusion of event-related details.
5. Responsive and visually appealing user interface.
6. Newsletter for students to stay up-to-date with the upcoming events


## Usage
1. On the homepage, the live timeline displays upcoming events.
2. Click on an event to view detailed information.
3. Use the navigation menu to access past events or view events by specific clubs/committees.
4. On the day of the event the page greets the user with a confetti animation
5. To add a new event, log in as an committee administrator and navigate to the admin panel.
6. In the admin panel, you can add, delete, or edit event details. 
7. Subevents or additional event-related information can be included when adding or editing an event.
8. Fill in email details to recieve updates via Newsletters

## Technology Stack
Hype is built using the following technologies:

Front-end: HTML, CSS, JavaScript, AngularJS, JQuery, Bootstrap

Back-end: Python Flask

Database: SQLite

## Credits

This project was made by Soumya Vaidya and Anushka Bhatnagar
