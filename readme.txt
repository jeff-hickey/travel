Overview
1. Built a Hotel Booking app for web & mobile that includes: Hotel Search, Room Search,
Booking, a Shopping cart, User Registration and Django Admin interface.
2. The things I learned include: Django Testing, Sessions, React Components,
GitHub workflows/aactions, flatpickr integration.
3. Complete GOOD, BETTER and BEST requirements from proposal.


Code Highlights

- views.py - Django Session management (shopping cart) and room_availability
would be the most interesting code. It was new working with dates and date comparison.
- tests.py - Includes a test for Room Availability, perhaps the most complex
code in the app.
- models.py - Representing Hotel and Room data can take many forms. This area evolved over
time and could continue to do so, as the site needs expand.
-forms.py - Used Django UnBound forms for Search and Checkout.
-admin.py - Admin site configurations.

- index.html and search.html have flatpickr integration.
- rooms.html and room.js - React Components to manage Room Availability. The biggest
challenge was state management, fetching data and flatpickr integration.
- django.yml - workflow to run tests on push to github.

URLs
https://travel-hotel.herokuapp.com/ | https://git.heroku.com/travel-hotel.git