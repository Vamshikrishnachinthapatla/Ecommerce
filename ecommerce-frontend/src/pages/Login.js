import { useState } from "react";
import API from "../api";

function Login({ onLogin, onSwitchToRegister }) {
  const [mobile, setMobile] = useState("");
  const [otp, setOtp] = useState("");

  const sendOtp = async () => {
    try {
      await API.post("auth/send-otp/", { mobile_number: mobile });
      alert("OTP sent");
    } catch (err) {
      console.error(err);
    }
  };

  const verifyOtp = async () => {
    try {
      const res = await API.post("auth/verify-otp/", {
        mobile_number: mobile,
        otp: otp,
      });

      localStorage.setItem("token", res.data.access);
      onLogin(); // 🔥 IMPORTANT
    } catch (err) {
      console.error(err);
      alert("Invalid OTP");
    }
  };

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#f5f5f5",
      }}
    >
      <div
        style={{
          background: "#fff",
          padding: "30px",
          borderRadius: "12px",
          width: "300px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
        }}
      >
        <h2 style={{ textAlign: "center" }}>🔐 Login</h2>

        <input
          placeholder="Mobile"
          value={mobile}
          onChange={(e) => setMobile(e.target.value)}
          style={inputStyle}
        />

        <button onClick={sendOtp} style={btnSecondary}>
          Send OTP
        </button>

        <input
          placeholder="OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          style={inputStyle}
        />

        <button onClick={verifyOtp} style={btnPrimary}>
          Login
        </button>

        {/* 🔥 THIS WAS MISSING */}
        <p style={{ marginTop: "10px", textAlign: "center" }}>
          Don't have an account?{" "}
          <span
            onClick={onSwitchToRegister}
            style={{ color: "blue", cursor: "pointer" }}
          >
            Register
          </span>
        </p>
      </div>
    </div>
  );
}

const inputStyle = {
  width: "100%",
  padding: "10px",
  marginTop: "10px",
  borderRadius: "6px",
  border: "1px solid #ccc",
};

const btnPrimary = {
  width: "100%",
  padding: "10px",
  marginTop: "10px",
  background: "#007bff",
  color: "#fff",
  border: "none",
  borderRadius: "6px",
};

const btnSecondary = {
  width: "100%",
  padding: "10px",
  marginTop: "10px",
  background: "#6c757d",
  color: "#fff",
  border: "none",
  borderRadius: "6px",
};

export default Login;