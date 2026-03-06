# QUICK START GUIDE - Hospital Management System

## 🚀 GETTING STARTED IN 2 MINUTES

### Step 1: Start the Server
```bash
cd Login
./START_SERVER_CLEAN.bat
```
**You should see**: Flask running on http://localhost:5000

### Step 2: Open in Browser
Go to: **http://localhost:5000/**

### Step 3: Login
Use one of these demo accounts:
| Role | Username | Password |
|------|----------|----------|
| **Admin** | admin | admin123 |
| **Pharmacist** | pharmacist | pharmacist123 |
| **Doctor** | doctor | doctor123 |
| **Patient** | patient | patient123 |

---

## 📊 WHAT'S NEW

### 💊 Pharmacist Dashboard
**URL**: http://localhost:5000/pharmacist_dashboard.html

Features:
- View all medicines in inventory
- Add new medicine with details
- Edit medicine information
- Delete medicine from stock
- Export inventory as CSV
- See low-stock alerts (≤10 units)

**Login as**: pharmacist

---

### 👨‍💼 Admin Dashboard  
**URL**: http://localhost:5000/admin_dashboard.html

Features:
- **User Management**: View all users, change roles, delete accounts
- **Hospital Settings**: Configure system settings

**Login as**: admin

---

## 🔌 API ENDPOINTS (All Running)

### Medicines API
```
GET    /api/medicines              → List all medicines
POST   /api/medicines              → Add new medicine (needs pharmacist/admin)
PUT    /api/medicines/<id>         → Edit medicine (needs pharmacist/admin)
DELETE /api/medicines/<id>         → Delete medicine (needs pharmacist/admin)
```

### Admin API
```
GET    /api/admin/users?actor_id=X → List users (needs admin)
PUT    /api/admin/user/<id>/role   → Change user role (needs admin)
DELETE /api/admin/user/<id>        → Delete user (needs admin)
GET    /api/admin/settings         → Get settings
PUT    /api/admin/settings         → Update settings (needs admin)
```

---

## 🧪 TEST THE SYSTEM

### Option 1: Run Test Suite
```bash
python test_all_new_endpoints.py
```

### Option 2: Quick Health Check
```bash
python validate_deployment.py
```

### Option 3: Manual Browser Test
1. Open http://localhost:5000/health
   - Should return: `{"service": "Hospital and community Pharmacy management", "status": "ok"}`

---

## ✅ VERIFICATION CHECKLIST

- [x] Server running on port 5000
- [x] All endpoints responding (tested)
- [x] Pharmacist dashboard working
- [x] Admin dashboard working
- [x] Role-based access control enforced
- [x] Database connected
- [x] API authentication working

---

## 🆘 QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Server won't start | Kill python.exe: `taskkill /F /IM python.exe` and restart |
| 404 errors | Check if server is running: http://localhost:5000/health |
| 403 errors on endpoints | Make sure you're logged in as correct role (admin/pharmacist) |
| Can't add medicines | Must be logged in as Pharmacist or Admin |
| Can't manage users | Must be logged in as Admin |

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `server_patient_doctor.py` | Flask backend (all APIs) |
| `pharmacist_dashboard.html` | Medicine management UI |
| `admin_dashboard.html` | User & settings management UI |
| `START_SERVER_CLEAN.bat` | Easy server startup |
| `DEPLOYMENT_COMPLETE.md` | Full feature documentation |

---

## 🎯 TRY THIS

1. **Start server** with `START_SERVER_CLEAN.bat`
2. **Login as pharmacist**: http://localhost:5000 → pharmacist/pharmacist123
3. **Go to pharmacist dashboard**: http://localhost:5000/pharmacist_dashboard.html
4. **Add a medicine**:
   - Name: "Aspirin"
   - Generic: "Acetylsalicylic Acid"
   - Dosage: "500mg"
   - Quantity: "150"
   - Price: "5.50"
   - Manufacturer: "Generic Corp"
   - Click "Add Medicine"
5. **See it in the list!**

---

## 📞 SYSTEM STATUS

Everything is **READY TO USE**. All features have been tested and are operational.

**Happy managing!** 🏥
