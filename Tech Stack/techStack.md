# Pünktlich Tech Stack

## Overview
Pünktlich. is an app designed to optimize morning routines and manage the user’s day. It sets personalized alarms based on calendar entries and commute preferences. Pünktlich. also prioritizes user privacy, which is why we try to store sensitive information locally.

## Frontend
- **Framework:** Flutter
- **Language:** Dart
- **Build Tool:** Gradle

## Backend
- **Framework:** FastAPI
- **Language:** Python
- **API Style:** RESTful
- **Authentication:** TBD

## Database
- TBD

## Infrastructure
- **Hosting (Dev):** Vercel
- **Hosting (Production):** TBD
- **Storefront:** Google Play Store / Apple App Store (planned)

## Development
- **Version Control:** GitHub
- **Package Manager:** npm
- **Code Quality:** Prettier

## Decision Rationale
We chose Flutter for its simple deployment to different platforms, which will enable us to access a bigger market early in development.

The API has been implemented using FastAPI due to its high performance and compatibility with Python, which is essential because early versions of the app will depend on a Python-based GitHub repository that functions as a wrapper for the VVS API. We also plan to make use of the Google Maps and Calendar APIs.

Due to privacy concerns we initially decided not to implement a database; however, a database that periodically calls the VVS API and stores the route data is currently being debated. This would have the advantage of reducing the number of user-driven API calls, thus increasing scalability and decreasing API costs.

As of right now our API is being hosted on Vercel as stateless functions, but a migration is planned before a production release.

GitHub, npm, and Prettier have been chosen for being state of the art.
