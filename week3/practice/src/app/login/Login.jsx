"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    if (!username || !password) {
      alert("Please enter both username and password");
      return;
    }

    const user = {
      username
    };

    localStorage.setItem("currentUser", JSON.stringify(user));

    router.push("/");
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <section className="bg-white shadow-lg rounded-xl p-8 w-full max-w-md">

        <h1 className="text-center text-2xl font-semibold mb-8">Login</h1>

        <form onSubmit={handleLogin}>
          <label htmlFor="username" className="block text-sm mb-2">
            Username
          </label>
          <div className="mb-4">
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 border rounded-md focus:outline-none bg-gray-50"
              placeholder="Username"
            />
          </div>

          <label htmlFor="password" className="block text-sm mb-2">
            Password
          </label>
          <div className="mb-4">
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border rounded-md focus:outline-none bg-gray-50"
              placeholder="Password"
            />
          </div>

          <div className="flex items-center justify-between mb-6">
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
              />
              Remember me
            </label>

            <a href="#" className="text-sm text-gray-500 hover:underline">
              Forgot Password?
            </a>
          </div>

          <button
            type="submit"
            className="w-full py-3 bg-green-500 text-white font-semibold rounded-md hover:bg-green-600 transition"
          >
            LOGIN
          </button>
        </form>
      </section>
    </main>
  );
}
