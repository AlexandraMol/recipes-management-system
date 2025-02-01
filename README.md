# Web Application - Recipe Management System

## Content

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [How to use](#how-to-use)

## Overview

A web application that allows users to create, manage, and explore recipes. Includes authentication, recipe storage, and shopping list generation.

## Features

• User Authentication (Register and Login)
• Recipe Management (Create, Edit, Delete)
• Explore Public Recipes
• Shopping List Generation (from multiple selected recipes)
• Generate dummy data with Faker.js

## Tech Stack

Frontend: Vue.js (Vuex, Vuetify)
Backend: Express Api with NoSQL Database
Auth: Firebase Authentication
Data generating: @faker-js/faker
State Management: Vuex

## How to use

• User Authentication
Upon accessing the app, the user will be directed to the landing page and has the possibility to register or login.

- User creation is handled by Firebase Authentication.
- Login with email and password.
  After logging in, the user will be redirected to the home page where his own recipes are displayed.

• Creating and Managing Recipes

- Users can create recipes using the form from the add recipe page.
- User can edit or delete the recipes in the home page.
- User can see his own recipes, they being displayed in a different page.

• Exploring Public Recipes

- On the Explore page, users can view public recipes from other users.

• Shopping List Generation

- The user can select multiple recipes from a dropdown to generate a shopping list.
