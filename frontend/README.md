# AI Trend Radar Frontend

This is the frontend application for the AI Trend Radar project, built with Next.js, React, TypeScript, shadcn/ui, and Tailwind CSS.

## Getting Started

1.  **Install Dependencies**:
    ```bash
    npm install
    # or yarn install
    ```

2.  **Configure shadcn/ui (if not already done)**:
    ```bash
    npx shadcn-ui@latest init
    ```
    Then, add the required components:
    ```bash
    npx shadcn-ui@latest add button card tabs skeleton
    ```

3.  **Set Environment Variables**:
    Create a `.env.local` file in the `frontend` directory:
    ```
    # frontend/.env.local
    NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api"
    # Replace with your backend API's public URL when deployed, e.g., https://your-fastapi-app.railway.app/api
    ```

4.  **Run the Development Server**:
    ```bash
    npm run dev
    # or yarn dev
    ```
    Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

5.  **Build for Production**:
    ```bash
    npm run build
    ```

6.  **Start Production Server**:
    ```bash
    npm run start
    ```

## Deployment

This frontend application is designed to be deployed on Vercel.

1.  Push your `frontend` directory to a Git repository (GitHub, GitLab, Bitbucket).
2.  Log in to Vercel, import your project, and select the `frontend` directory as the root.
3.  Configure the `NEXT_PUBLIC_API_BASE_URL` environment variable in Vercel to point to your deployed FastAPI backend URL.
4.  Vercel will automatically build and deploy your Next.js application.

