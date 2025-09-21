# 🚀 Neon PostgreSQL Setup Guide for ShastraBytes

This guide will help you set up Neon PostgreSQL for your Vercel deployment.

## Step 1: Create Neon Database

1. **Go to your Vercel project** → Storage tab
2. **Click "Create Database"**
3. **Select "Neon"** from the marketplace
4. **Click "Continue"**
5. **Follow Neon's setup process:**
   - Choose a database name (e.g., `shastrabytes-db`)
   - Select region (choose closest to your users)
   - Click "Create Database"

## Step 2: Get Your Database URL

After creating the database, you'll get a connection string that looks like:
```
postgresql://username:password@ep-xxx-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

## Step 3: Add Environment Variables in Vercel

1. **Go to your Vercel project** → Settings → Environment Variables
2. **Add these variables:**

```bash
# Database Configuration
DATABASE_URL=postgresql://your_neon_connection_string_here
VERCEL=1

# Security (generate a strong secret key)
SECRET_KEY=ShastraBytes-Production-Secret-Key-2025-$(date +%s)

# Optional: Database Performance Tuning
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
```

## Step 4: Redeploy Your Application

1. **Go to Deployments tab**
2. **Click "Redeploy"** on the latest deployment
3. **Wait for deployment to complete**

## Step 5: Initialize Database Tables

After redeployment, run this command locally to create the database tables:

```bash
# Install psycopg2 if not already installed
pip install psycopg2-binary

# Set your DATABASE_URL and initialize
set DATABASE_URL=your_neon_connection_string_here
python init_prod_db.py
```

Or run it directly:
```bash
python init_prod_db.py "your_neon_connection_string_here"
```

## Step 6: Test Your Application

1. **Visit your Vercel URL**
2. **Try to sign up with test credentials**
3. **Verify no "Database Error" appears**

## 🎯 Neon Benefits for Your App

- ✅ **Serverless**: Auto-scales with your traffic
- ✅ **Auto-pause**: Saves costs when not in use
- ✅ **Fast cold starts**: Optimized for serverless functions
- ✅ **Free tier**: 0.5 GB storage included
- ✅ **Branching**: Database branching for different environments

## 🔧 Troubleshooting

**Connection Issues:**
- Ensure `sslmode=require` is in your connection string
- Check that DATABASE_URL is properly set in Vercel environment variables

**Permission Issues:**
- Neon automatically handles permissions for created databases
- No additional user setup required

**Performance:**
- Neon optimizes connection pooling automatically
- Your app is configured to handle connection limits properly

---

**Need Help?** Check the Neon documentation or Vercel support for additional assistance.