# CS50 E-Commerce Auctions

A functional e-commerce auction site built with Django. This project allows users to create auctions, place bids, add items to a watchlist, and comment on listings.

## Features

- **Active Listings:** View all currently available auctions.
- **Categories:** Browse listings by category (e.g., Fashion, Home, Toys, Electronics).
- **Listing Details:** Detailed view for each item, including bidding history and comments.
- **Watchlist:** Authenticated users can add/remove items from their personal watchlist.
- **Bidding System:** Users can place bids on active auctions. The system validates that bids are higher than the current price.
- **Comments:** Users can leave comments on auction listings.
- **Auction Management:** The listing creator can close the auction at any time, marking the highest bidder as the winner.

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd E-Commerce-Site-
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   The site will be available at `http://127.0.0.1:8000/`.

## Technologies Used

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Database:** SQLite (default Django database)
- **Environment:** virtualenv
