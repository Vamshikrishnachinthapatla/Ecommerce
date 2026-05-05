import { useState } from "react";
import API from "../api";

function Login({ onLogin }) {
  const [mobile, setMobile] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);

  const sendOtp = async () => {
    try {
      await API.post("auth/send-otp/", { mobile_number: mobile });
      setOtpSent(true);
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
      onLogin(); // 🔥 important
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
          width: "320px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
        }}
      >
        <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
          🔐 Login
        </h2>

        {/* Mobile Input */}
        <input
          type="text"
          placeholder="Enter mobile number"
          value={mobile}
          onChange={(e) => setMobile(e.target.value)}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "10px",
            borderRadius: "6px",
            border: "1px solid #ccc",
          }}
        />

        {/* Send OTP */}
        {!otpSent && (
          <button
            onClick={sendOtp}
            style={{
              width: "100%",
              padding: "10px",
              background: "#007bff",
              color: "#fff",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              marginBottom: "10px",
            }}
          >
            Send OTP
          </button>
        )}

        {/* OTP Input */}
        {otpSent && (
          <>
            <input
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              style={{
                width: "100%",
                padding: "10px",
                marginBottom: "10px",
                borderRadius: "6px",
                border: "1px solid #ccc",
              }}
            />

            <button
              onClick={verifyOtp}
              style={{
                width: "100%",
                padding: "10px",
                background: "#28a745",
                color: "#fff",
                border: "none",
                borderRadius: "6px",
                cursor: "pointer",
              }}
            >
              Verify & Login
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default Login;