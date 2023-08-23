"use client";
import { useState } from "react";
import Link from "next/link";
import Navbar from "../components/navbar";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { redirect } from "next/navigation";

const Login = () => {
    const [userData, setUserData] = useState({
        username: "",
        password: ""
    })
    const loginUser = async () => {
        try {
            const res = await fetch('/login/api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });
            const data = await res.json()
            if (data.status==="Logged in successfully")
                redirect("/")
            toast(data.status);
            setUserData({username: "", password: ""});
        } catch (err) {
            toast("Internal error, try again.");
        }
    }
    return (
        <div className="min-h-screen flex">
            <Navbar />
            <main className="p-4 w-full">
                <h2>Login</h2>
                <div className="space-y-2 flex flex-col m-8">
                    <label>Username</label>
                    <input type="text" id="username" placeholder="Enter Username" className="rounded p-2" onChange={(e) => setUserData({ ...userData, username: e.target.value })} />

                    <label>Password</label>
                    <input type="password" id="password" placeholder="Enter Password" className="rounded p-2" onChange={(e) => setUserData({ ...userData, password: e.target.value })} />

                    <button className="bg-sky-600" onClick={() => loginUser()}>Submit</button>
                </div>
                <p className="text-center">Don&apos;t have an account? <Link href="/register" className="text-sky-600 font-bold hover:underline">Register!</Link></p>
            </main>
            <ToastContainer/>
        </div>
    )
}

export default Login;