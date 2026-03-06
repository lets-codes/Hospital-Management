# Secure Login System with MySQL

A fully functional login/signup system with MySQL database integration, password hashing with bcrypt, and form validation.

## Features

✅ **User Registration (Sign Up)**
- Email validation
- Password strength validation (minimum 6 characters)
- Duplicate email detection
- Password hashing with bcrypt for security

✅ **User Login**
- Email and password verification
- Secure password comparison using bcrypt
- User data stored in browser localStorage
- Session management

✅ **User Dashboard (Home Page)**
- Display logged-in user information
- Profile details with name, email, and user ID
- Logout functionality

✅ **Security Features**
- Passwords are hashed using bcrypt (never stored in plaintext)
- SQL injection prevention using prepared statements
- CORS enabled for development
- Input validation on both client and server side

✅ **MySQL Database**
- Automated database and table creation
- Email uniqueness constraint
- Timestamps for user creation and updates
- Performance indexes on email field

## Prerequisites

Before running this application, ensure you have:

1. **Node.js** (v12 or higher) - [Download](https://nodejs.org/)
2. **MySQL Server** (v5.7 or higher) - [Download](https://dev.mysql.com/downloads/mysql/)
3. **npm** (usually comes with Node.js)

## Installation Steps

### Step 1: Set Up MySQL Database

1. Open MySQL Command Line or MySQL Workbench
2. Run the SQL commands from `database.sql`:
   ```sql
   CREATE DATABASE IF NOT EXISTS login_system;
   USE login_system;
   
   CREATE TABLE IF NOT EXISTS information_store (
       id INT AUTO_INCREMENT PRIMARY KEY,
       full_name VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
       INDEX idx_email (email)
   );
   ```

### Step 2: Install Dependencies

Navigate to the project folder and install required packages:

```bash
npm install
```

This will install:
- **express** - Web framework
- **mysql2** - MySQL database driver
- **body-parser** - Parse JSON requests
- **cors** - Enable cross-origin requests
- **bcryptjs** - Password hashing
- **express-session** - Session management
- **dotenv** - Environment variables

### Step 3: Configure Database Connection

Edit `server.js` and update the database configuration:

```javascript
const db = mysql.createConnection({
    host: 'localhost',      // Your MySQL host
    user: 'root',           // Your MySQL username
    password: '',           // Your MySQL password (empty if none)
    database: 'login_system' // Database name
});
```

### Step 4: Start the Server

Run the application:

```bash
npm start
```

Or for development with auto-reload:

```bash
npm run dev
```

You should see:
```
Connected to SQL Database
Server running on port 3000
```

### Step 5: Access the Application

Open your browser and navigate to:
- **Login Page**: `http://localhost:3000/login.html`
- **Sign Up Page**: `http://localhost:3000/signup.html`

## File Structure

```
Login/
├── server.js           # Express server with API endpoints
├── login.html          # Login page
├── signup.html         # Registration page
├── home.html           # Dashboard after login
├── database.sql        # Database schema
├── package.json        # Project dependencies
├── .env.example        # Environment variables example
└── README.md           # This file
```

## API Endpoints

### 1. Sign Up
**POST** `/signup`

Request body:
```json
{
    "fullname": "John Doe",
    "email": "john@example.com",
    "password": "securePassword123"
}
```

Response (Success - 201):
```json
{
    "message": "User registered successfully. Please login."
}
```

Response (Error - 400):
```json
{
    "message": "All fields are required"
}
```

### 2. Login
**POST** `/login`

Request body:
```json
{
    "email": "john@example.com",
    "password": "securePassword123"
}
```

Response (Success - 200):
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    }
}
```

Response (Error - 401):
```json
{
    "message": "Invalid email or password"
}
```

### 3. Get User Profile
**GET** `/profile/:userId`

Response (Success - 200):
```json
{
    "user": {
        "id": 1,
        "full_name": "John Doe",
        "email": "john@example.com",
        "created_at": "2026-02-15 10:30:00"
    }
}
```

### 4. Logout
**POST** `/logout`

Response:
```json
{
    "message": "Logged out successfully"
}
```

## Security Notes

⚠️ **Important Security Practices Implemented:**

1. **Password Hashing**: All passwords are hashed using bcrypt before storage
2. **SQL Injection Prevention**: Parameterized queries used throughout
3. **Input Validation**: Both client-side and server-side validation
4. **Email Uniqueness**: Database constraint prevents duplicate emails
5. **Error Messages**: Generic messages to prevent information leakage

⚠️ **For Production (Additional Steps Needed):**

1. Move sensitive data to `.env` file (not `.env.example`)
2. Use HTTPS instead of HTTP
3. Implement rate limiting to prevent brute force attacks
4. Add CSRF protection
5. Use JWT tokens for better session management
6. Implement password reset functionality
7. Add email verification for new accounts
8. Add two-factor authentication (2FA)

## Troubleshooting

### Error: "Connected to SQL Database" not showing
- Check if MySQL server is running
- Verify database credentials in `server.js`
- Ensure the database exists

### Error: "Cannot GET /login.html"
- Make sure you're accessing `http://localhost:3000/login.html` (not just the file path)
- The server must be running

### Error: "Email already registered"
- The email is already in the database
- Try with a different email address

### Error: "Invalid email or password"
- Check email and password - they are case-sensitive
- Ensure the user was registered successfully first

### npm install fails
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again
- Ensure Node.js and npm are properly installed

## Testing the Application

### Create a Test Account

1. Visit: `http://localhost:3000/signup.html`
2. Fill in the form:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Password: `password123`
3. Click "Sign Up"
4. You should see a success message and redirect to login page

### Login with Test Account

1. Visit: `http://localhost:3000/login.html`
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `password123`
3. Click "Sign In"
4. You should be redirected to the home page with your profile displayed

## Support & Documentation

- [Express.js Documentation](https://expressjs.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [bcryptjs Documentation](https://www.npmjs.com/package/bcryptjs)
- [Node.js Documentation](https://nodejs.org/en/docs/)

## License

MIT License - feel free to use this project for learning and development.

## Author

Created as a secure login system template with MySQL integration.
